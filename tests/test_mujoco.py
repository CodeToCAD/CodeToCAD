import math

import pytest

pytest.importorskip("mujoco")

from codetocad import Camera, Lighting, Location, cube, cylinder, sphere
from codetocad_integrations.mujoco import simulate


def build_pendulum():
    mount = cube("6cm", "6cm", "4cm", start_location=Location(z="52cm"))
    mount.name = "mount"
    rod = cylinder("1cm", "40cm", start_location=Location(z="30cm"))
    rod.name = "rod"
    bob = sphere("5cm", start_location=Location(z="10cm"))
    bob.name = "bob"
    pivot = Location.from_euler(0, 0, "50cm", x_deg=-90, name="pivot")
    mount.revolute(pivot, rod, pivot)
    rod.fixed(Location(z="10cm"), bob, Location(z="10cm"))
    return mount


def test_pendulum_swings_and_conserves_amplitude(tmp_path):
    # The rod is modeled touching its mount at the pivot, so that pair is
    # excluded from collision or contact friction would damp the swing.
    sim = simulate(
        build_pendulum(),
        actuated=False,
        collision_exclusions=[("mount", "rod")],
        output_dir=tmp_path,
    )
    assert sim.joint_names == ["pivot"]
    assert (tmp_path / "robot.xml").exists()
    # Meshes were converted to binary STL for MuJoCo.
    assert not (tmp_path / "rod.stl").read_bytes().startswith(b"solid")
    initial = math.radians(60)
    sim.set_joint_value("pivot", initial)
    angles = []
    for _ in range(720):  # 3 seconds
        sim.step()
        angles.append(sim.get_joint_value("pivot"))
    assert min(angles) < -math.radians(20)
    assert max(angles) <= initial * 1.05
    assert max(angles[-240:]) > initial * 0.7


def test_position_control(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi,
    )
    sim = simulate(
        base, collision_exclusions=[(base, arm)], output_dir=tmp_path
    )
    sim.get_joint("shoulder").move_to(1.0)
    sim.step(1200)
    assert sim.get_joint_value("shoulder") == pytest.approx(1.0, abs=0.1)


def test_unactuated_rejects_targets(tmp_path):
    sim = simulate(build_pendulum(), actuated=False, output_dir=tmp_path)
    with pytest.raises(RuntimeError, match="actuated"):
        sim.get_joint("pivot").move_to(1.0)


def test_starting_angle_applied(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi, starting_angle="30deg",
    )
    sim = simulate(base, output_dir=tmp_path)
    assert sim.get_joint_value("shoulder") == pytest.approx(math.radians(30))


def test_returned_joint_object_controls_simulation(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    hinge = base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi,
    )
    sim = simulate(base, collision_exclusions=[(base, arm)], output_dir=tmp_path)
    assert hinge.is_bound
    hinge.move_to("1rad")
    sim.step(1200)
    assert hinge.get_angle().value == pytest.approx(1.0, abs=0.1)


def _offscreen_gl_available() -> bool:
    import mujoco

    try:
        renderer = mujoco.Renderer(mujoco.MjModel.from_xml_string("<mujoco/>"), 1, 1)
        renderer.close()
    except Exception:
        return False
    return True


requires_gl = pytest.mark.skipif(
    not _offscreen_gl_available(),
    reason="offscreen OpenGL context unavailable (headless CI)",
)


@requires_gl
def test_capture_image_and_record_gif(tmp_path):
    sim = simulate(build_pendulum(), output_dir=tmp_path)
    image = sim.capture_image(width=120, height=90)
    assert image.shape == (90, 120, 3)
    assert image.dtype.name == "uint8"
    gif = sim.record_gif(
        tmp_path / "swing.gif", duration=0.2, fps=10, width=80, height=60
    )
    assert gif[:6] == b"GIF89a"
    assert (tmp_path / "swing.gif").exists()
    sim.close()


def test_capture_image_honors_camera_and_lighting(tmp_path):
    sim = simulate(
        build_pendulum(),
        camera=Camera.look_at(eye=(1.2, -1.2, 0.8), target=(0, 0, 0.3)),
        output_dir=tmp_path,
    )
    image = sim.capture_image(width=80, height=60)
    assert image.shape == (60, 80, 3)
    # Re-aim the camera live.
    sim.set_camera(Camera.look_at(eye=(0.6, 0.6, 0.6), target=(0, 0, 0.3)))
    assert sim.capture_image(width=80, height=60).shape == (60, 80, 3)
    # Re-lighting the live model keeps rendering.
    sim.set_lighting([Lighting(name="light", position=(2, 2, 3))])
    assert sim.capture_image(width=80, height=60).shape == (60, 80, 3)
    sim.close()
