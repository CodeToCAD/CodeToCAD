"""Shared offscreen rendering helpers for the turtlebot example media."""
import math

import mujoco
from PIL import Image

_ASSET_XML = (
    '<asset>\n'
    '    <texture type="skybox" builtin="gradient" rgb1="0.95 0.96 0.98" '
    'rgb2="0.75 0.8 0.88" width="256" height="256" />\n'
    '    <texture name="grid" type="2d" builtin="checker" rgb1="0.82 0.83 0.85" '
    'rgb2="0.9 0.91 0.93" width="300" height="300" />\n'
    '    <material name="grid" texture="grid" texrepeat="6 6" reflectance="0.1" />\n'
    '    <material name="grid_big" texture="grid" texrepeat="80 80" reflectance="0.1" />'
)
_WORLDBODY_XML = (
    '<worldbody>\n'
    '    <geom name="floor" type="plane" size="3 3 0.1" material="grid" />'
)
_EXISTING_FLOOR_XML = (
    '<geom name="floor" type="plane" size="20 20 0.1" rgba="0.85 0.85 0.85 1" />'
)
_EXISTING_FLOOR_REPLACEMENT = (
    '<geom name="floor" type="plane" size="20 20 0.1" material="grid_big" />'
)


def _render_model(sim):
    """``sim``'s MJCF with a checkered floor + skybox injected, compiled
    into a fresh (render-only) model. If ``sim`` was built with
    ``ground_plane=True`` it already has a "floor" geom, so that one is
    re-skinned with the checkered material instead of adding a duplicate."""
    xml = sim.mjcf_path.read_text()
    xml = xml.replace("<asset>", _ASSET_XML)
    if _EXISTING_FLOOR_XML in xml:
        xml = xml.replace(_EXISTING_FLOOR_XML, _EXISTING_FLOOR_REPLACEMENT)
    else:
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
    distance,
    azimuth,
    elevation,
    lookat=None,
    track_body=None,
    joint_velocities_rpm=None,
    width=480,
    height=360,
):
    """Drive ``sim`` for ``duration_seconds``, holding each joint in
    ``joint_velocities_rpm`` (``{joint_name: rpm}``) at a constant velocity
    target, and record an animated GIF. The camera stays fixed at
    ``lookat`` (world xyz) if given, otherwise it tracks ``track_body``'s
    position every frame."""
    model = _render_model(sim)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=height, width=width)
    cam = mujoco.MjvCamera()
    cam.distance = distance
    cam.azimuth = azimuth
    cam.elevation = elevation
    if lookat is not None:
        cam.lookat[:] = lookat

    for joint_name, rpm in (joint_velocities_rpm or {}).items():
        sim.set_joint_velocity_target(joint_name, rpm * 2 * math.pi / 60)

    steps_per_frame = max(1, round((1.0 / fps) / sim.model.opt.timestep))
    frame_count = round(duration_seconds * fps)

    frames = []
    for _ in range(frame_count):
        sim.step(steps_per_frame)
        data.qpos[:] = sim.data.qpos
        mujoco.mj_forward(model, data)
        if track_body is not None:
            position, _ = sim.get_body_pose(track_body)
            cam.lookat[:] = position
        renderer.update_scene(data, camera=cam)
        frame = Image.fromarray(renderer.render()).convert("P", palette=Image.ADAPTIVE)
        frames.append(frame)

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / fps),
        loop=0,
        optimize=True,
    )
    print("saved", out_gif, f"({len(frames)} frames)")
