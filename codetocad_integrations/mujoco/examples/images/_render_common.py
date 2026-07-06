"""Shared offscreen screenshot helper for the MuJoCo example renders."""
import mujoco
from PIL import Image


def capture(sim, qpos, out_png, lookat, distance, azimuth, elevation):
    """Inject a checkered floor + skybox into ``sim``'s MJCF, rebuild the
    model at the given ``qpos``, and save an offscreen render to
    ``out_png``."""
    xml = sim.mjcf_path.read_text()
    xml = xml.replace(
        "<asset>",
        '<asset>\n'
        '    <texture type="skybox" builtin="gradient" rgb1="0.95 0.96 0.98" '
        'rgb2="0.75 0.8 0.88" width="256" height="256" />\n'
        '    <texture name="grid" type="2d" builtin="checker" rgb1="0.82 0.83 0.85" '
        'rgb2="0.9 0.91 0.93" width="300" height="300" />\n'
        '    <material name="grid" texture="grid" texrepeat="6 6" reflectance="0.1" />',
    )
    xml = xml.replace(
        "<worldbody>",
        '<worldbody>\n'
        '    <geom name="floor" type="plane" size="1.5 1.5 0.1" material="grid" />',
    )
    mod_path = sim.mjcf_path.with_name("robot_render.xml")
    mod_path.write_text(xml)

    model = mujoco.MjModel.from_xml_path(str(mod_path))
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
    pixels = renderer.render()
    Image.fromarray(pixels).save(out_png)
    print("saved", out_png)
