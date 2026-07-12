"""Shared offscreen rendering helpers for the MuJoCo example renders."""
import mujoco
from PIL import Image

_ASSET_XML = (
    '<asset>\n'
    '    <texture type="skybox" builtin="gradient" rgb1="0.95 0.96 0.98" '
    'rgb2="0.75 0.8 0.88" width="256" height="256" />\n'
    '    <texture name="grid" type="2d" builtin="checker" rgb1="0.82 0.83 0.85" '
    'rgb2="0.9 0.91 0.93" width="300" height="300" />\n'
    '    <material name="grid" texture="grid" texrepeat="6 6" reflectance="0.1" />'
)
_WORLDBODY_XML = (
    '<worldbody>\n'
    '    <geom name="floor" type="plane" size="1.5 1.5 0.1" material="grid" />'
)


def _render_model(sim):
    """``sim``'s MJCF with a checkered floor + skybox injected, compiled
    into a fresh (render-only) model."""
    xml = sim.mjcf_path.read_text()
    xml = xml.replace("<asset>", _ASSET_XML)
    xml = xml.replace("<worldbody>", _WORLDBODY_XML)
    mod_path = sim.mjcf_path.with_name("robot_render.xml")
    mod_path.write_text(xml)
    return mujoco.MjModel.from_xml_path(str(mod_path))


def capture(sim, qpos, out_png, lookat, distance, azimuth, elevation):
    """Rebuild ``sim``'s model at the given ``qpos`` and save an offscreen
    render to ``out_png``."""
    model = _render_model(sim)
    data = mujoco.MjData(model)
    data.qpos[: len(qpos)] = qpos
    mujoco.mj_forward(model, data)

    renderer = mujoco.Renderer(model, height=480, width=640)
    cam = mujoco.MjvCamera()
    cam.lookat[:] = lookat
    cam.distance = distance
    cam.azimuth = azimuth
    cam.elevation = elevation
    renderer.update_scene(data, camera=cam)
    Image.fromarray(renderer.render()).save(out_png)
    print("saved", out_png)


def record_gif(
    sim,
    out_gif,
    *,
    duration_seconds,
    fps,
    lookat,
    distance,
    azimuth,
    elevation,
    width=480,
    height=360,
):
    """Step ``sim`` forward (unactuated joints evolve under gravity/initial
    velocity alone) and record an offscreen render every ``1/fps`` seconds
    into an animated GIF."""
    model = _render_model(sim)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=height, width=width)
    cam = mujoco.MjvCamera()
    cam.lookat[:] = lookat
    cam.distance = distance
    cam.azimuth = azimuth
    cam.elevation = elevation

    steps_per_frame = max(1, round((1.0 / fps) / sim.model.opt.timestep))
    frame_count = round(duration_seconds * fps)

    frames = []
    for i in range(frame_count):
        # Render before stepping, so frame 0 is the release pose rather
        # than one frame interval into the motion.
        data.qpos[:] = sim.data.qpos
        mujoco.mj_forward(model, data)
        renderer.update_scene(data, camera=cam)
        frame = Image.fromarray(renderer.render()).convert("P", palette=Image.ADAPTIVE)
        frames.append(frame)
        if i < frame_count - 1:
            sim.step(steps_per_frame)

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / fps),
        loop=0,
        optimize=True,
    )
    print("saved", out_gif, f"({len(frames)} frames)")
