import math

import pytest

pytest.importorskip("pybullet")

from codetocad import Location, cube, cylinder, sphere
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
    with simulate(build_pendulum(), output_dir=tmp_path) as sim:
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
    with simulate(base, output_dir=tmp_path) as sim:
        sim.set_joint_target("shoulder", 1.0)
        sim.step(1200)
        assert sim.get_joint_value("shoulder") == pytest.approx(1.0, abs=0.05)


def test_unknown_joint_raises(tmp_path):
    with simulate(build_pendulum(), output_dir=tmp_path) as sim:
        with pytest.raises(KeyError, match="pivot"):
            sim.get_joint_value("nope")
