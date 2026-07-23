import math

import pytest

pytest.importorskip("pybullet")

from codetocad import Camera, Location, cube, cylinder, sphere
from codetocad_integrations.pybullet import simulate


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
    with simulate(
        build_pendulum(),
        collision_exclusions=[("mount", "rod")],
        output_dir=tmp_path,
    ) as sim:
        assert sim.joint_names == ["pivot"]
        assert (tmp_path / "robot.urdf").exists()
        assert (tmp_path / "rod.stl").exists()
        initial = math.radians(60)
        sim.set_joint_value("pivot", initial)
        angles = []
        for _ in range(720):  # 3 seconds
            sim.step()
            angles.append(sim.get_joint_value("pivot"))
        assert min(angles) < -math.radians(20)  # swung through bottom
        assert max(angles) <= initial * 1.05  # no energy gained
        assert max(angles[-240:]) > initial * 0.7  # little energy lost


def test_position_control(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi,
    )
    with simulate(
        base, collision_exclusions=[(base, arm)], output_dir=tmp_path
    ) as sim:
        sim.get_joint("shoulder").move_to(1.0)
        sim.step(1200)
        assert sim.get_joint_value("shoulder") == pytest.approx(1.0, abs=0.05)


def test_starting_angle_applied(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi, starting_angle="30deg",
    )
    with simulate(base, output_dir=tmp_path) as sim:
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
    with simulate(base, collision_exclusions=[(base, arm)], output_dir=tmp_path) as sim:
        assert hinge.is_bound
        hinge.move_to("60deg")
        sim.step(1200)
        assert hinge.get_angle().to_degrees() == pytest.approx(60, abs=3)
        # Velocity control spins the joint back the other way.
        hinge.set_velocity("-30rpm")
        sim.step(240)
        assert hinge.get_angle().to_degrees() < 55


def test_capture_image_and_record_gif(tmp_path):
    with simulate(build_pendulum(), output_dir=tmp_path) as sim:
        image = sim.capture_image(width=120, height=90)
        assert image.shape == (90, 120, 3)
        assert image.dtype.name == "uint8"
        gif = sim.record_gif(
            tmp_path / "swing.gif", duration=0.2, fps=10, width=80, height=60
        )
        assert gif[:6] == b"GIF89a"
        assert (tmp_path / "swing.gif").exists()


def test_capture_image_honors_camera(tmp_path):
    # A Location-based camera passed to simulate(), then re-aimed live.
    with simulate(
        build_pendulum(),
        camera=Camera.look_at(eye=(1.5, -1.5, 1.0), target=(0, 0, 0.3)),
        output_dir=tmp_path,
    ) as sim:
        assert sim.camera.location is not None
        assert sim.capture_image(width=80, height=60).shape == (60, 80, 3)
        sim.set_camera(Camera.look_at(eye=(0, -2, 1), target=(0, 0, 0.3), fov=35))
        assert sim.camera.fov == 35
        assert sim.capture_image(width=80, height=60).shape == (60, 80, 3)


def test_keyframe_recording_and_playback(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    hinge = base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi,
    )
    with simulate(base, collision_exclusions=[(base, arm)], output_dir=tmp_path) as sim:
        hinge.move_to("0deg"); sim.set_keyframe(0.0)
        hinge.move_to("45deg"); sim.set_keyframe(1.0)
        assert len(sim._keyframes) == 2
        gif = sim.record_gif(keyframes=True, fps=6, width=80, height=60)
        assert gif[:6] == b"GIF89a"


def test_unknown_joint_raises(tmp_path):
    with simulate(build_pendulum(), output_dir=tmp_path) as sim:
        with pytest.raises(KeyError, match="pivot"):
            sim.get_joint_value("nope")


def test_joint_referenced_by_child_part(tmp_path):
    base = cube("10cm", "10cm", "4cm", start_location=Location(z="2cm"))
    base.name = "base"
    arm = cylinder("1.5cm", "20cm", start_location=Location(z="14cm"))
    arm.name = "arm"
    base.revolute(
        Location(z="4cm", name="shoulder"), arm, Location(z="4cm"),
        min_limits=-math.pi, max_limits=math.pi,
    )
    with simulate(base, output_dir=tmp_path) as sim:
        # The joined part addresses its own joint -- no need to know its name.
        sim.set_joint_value(arm, 0.5)
        assert sim.get_joint_value(arm) == pytest.approx(0.5)
        assert sim.get_joint_value("shoulder") == pytest.approx(0.5)
        with pytest.raises(KeyError, match="movable joint"):
            sim.get_joint_value(base)  # the root is not joined to anything
