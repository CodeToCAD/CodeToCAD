import math

import numpy as np
import pytest

from codetocad import (
    AngularSpeedRadiansPerSecond,
    FixedJoint,
    LinearSpeedMetersPerSecond,
    Location,
    PrismaticJoint,
    RevoluteJoint,
    cube,
    cylinder,
)
from codetocad.simulation import Simulation, encode_gif, extract_links


# -- speed units --------------------------------------------------------------


def test_angular_speed_units():
    assert AngularSpeedRadiansPerSecond("1rad/s").value == pytest.approx(1.0)
    assert AngularSpeedRadiansPerSecond("60rpm").value == pytest.approx(2 * math.pi)
    assert AngularSpeedRadiansPerSecond("180deg/s").value == pytest.approx(math.pi)
    assert AngularSpeedRadiansPerSecond("60rpm").to_rpm() == pytest.approx(60.0)


def test_linear_speed_units():
    assert LinearSpeedMetersPerSecond("2m/s").value == pytest.approx(2.0)
    assert LinearSpeedMetersPerSecond("36km/h").value == pytest.approx(10.0)
    assert LinearSpeedMetersPerSecond("10mm/s").value == pytest.approx(0.01)
    assert LinearSpeedMetersPerSecond(
        "10m/s"
    ).to_kilometers_per_hour() == pytest.approx(36.0)


# -- joint objects returned by constraint methods -----------------------------


def test_constraint_methods_return_joint_objects():
    base = cube(0.2, 0.2, 0.2)
    base.name = "base"
    arm = cylinder(0.02, 0.4, start_location=Location(z=0.4))
    arm.name = "arm"
    slider = cube(0.05, 0.05, 0.05, start_location=Location(z=0.8))
    slider.name = "slider"

    hinge = base.revolute(Location(z=0.1, name="shoulder"), arm, Location(z=0.1))
    rail = arm.prismatic(Location(z=0.6, name="rail"), slider, Location(z=0.6))
    weld = base.fixed(Location(name="w"), cube(0.01, 0.01, 0.01), Location())

    assert isinstance(hinge, RevoluteJoint)
    assert isinstance(rail, PrismaticJoint)
    assert isinstance(weld, FixedJoint)
    # Metadata is captured on the joint.
    assert hinge.parent_part is base and hinge.child_part is arm
    assert rail.child_part is slider


def test_starting_angle_and_pos_recorded_on_jointspec():
    base = cube(0.2, 0.2, 0.2)
    arm = cylinder(0.02, 0.4)
    slide = cube(0.05, 0.05, 0.05)
    base.revolute(Location(z=0.1, name="j1"), arm, Location(z=0.1), starting_angle="30deg")
    arm.prismatic(Location(z=0.2, name="j2"), slide, Location(z=0.2), starting_pos="2cm")
    links = extract_links(base)
    assert links[1].joint.initial_value == pytest.approx(math.radians(30))
    assert links[2].joint.initial_value == pytest.approx(0.02)


def test_unbound_joint_control_raises():
    base = cube(0.2, 0.2, 0.2)
    arm = cylinder(0.02, 0.4)
    hinge = base.revolute(Location(z=0.1, name="j"), arm, Location(z=0.1))
    assert hinge.is_bound is False
    with pytest.raises(RuntimeError, match="not bound"):
        hinge.move_to("10deg")


class _FakeSim(Simulation):
    """A backend-free Simulation that records commands, for control tests."""

    def __init__(self, root):
        super().__init__(root)
        self.values: dict[str, float] = {}
        self.velocities: dict[str, float] = {}

    def _set_joint_target(self, name, value, **kwargs):
        self.values[name] = value

    def _set_joint_velocity(self, name, value):
        self.velocities[name] = value

    def get_joint_value(self, joint):
        return self.values.get(self._resolve_joint_name(joint), 0.0)


def test_bound_joint_drives_simulation():
    base = cube(0.2, 0.2, 0.2)
    base.name = "base"
    arm = cylinder(0.02, 0.4)
    arm.name = "arm"
    hinge = base.revolute(Location(z=0.1, name="shoulder"), arm, Location(z=0.1))

    sim = _FakeSim(base)
    assert hinge.is_bound
    assert sim.get_joint(arm) is hinge

    hinge.move_to("90deg")
    assert sim.values["shoulder"] == pytest.approx(math.pi / 2)
    hinge.move_by("90deg")
    assert sim.values["shoulder"] == pytest.approx(math.pi)
    hinge.set_velocity("60rpm")
    assert sim.velocities["shoulder"] == pytest.approx(2 * math.pi)


def test_prismatic_joint_drives_in_meters():
    base = cube(0.2, 0.2, 0.2)
    base.name = "base"
    slide = cube(0.05, 0.05, 0.05)
    slide.name = "slide"
    rail = base.prismatic(Location(z=0.1, name="rail"), slide, Location(z=0.1))
    sim = _FakeSim(base)
    rail.move_to("5cm")
    assert sim.values["rail"] == pytest.approx(0.05)
    rail.move_by("5mm")
    assert sim.values["rail"] == pytest.approx(0.055)


# -- keyframes ----------------------------------------------------------------


def test_keyframe_ledger_and_interpolation():
    base = cube(0.2, 0.2, 0.2)
    base.name = "base"
    arm = cylinder(0.02, 0.4)
    arm.name = "arm"
    hinge = base.revolute(Location(z=0.1, name="shoulder"), arm, Location(z=0.1))
    sim = _FakeSim(base)

    hinge.move_to("0rad")
    assert sim.set_keyframe() == 0.0  # first keyframe at t=0
    hinge.move_to("1rad")
    assert sim.set_keyframe() == 1.0  # auto one second later
    hinge.move_to("0rad")
    sim.set_keyframe(2.0)

    frames = list(sim._keyframe_frames(fps=4))
    # 2 seconds at 4 fps -> 8 intervals + 1.
    assert len(frames) == 9
    assert frames[0]["shoulder"] == pytest.approx(0.0)
    assert frames[4]["shoulder"] == pytest.approx(1.0)  # peak at t=1
    assert frames[2]["shoulder"] == pytest.approx(0.5)  # halfway up


# -- GIF encoder --------------------------------------------------------------


def test_encode_gif_roundtrips_through_pillow():
    Image = pytest.importorskip("PIL.Image")
    frames = [np.full((20, 30, 3), value, np.uint8) for value in (0, 102, 204)]
    data = encode_gif(frames, fps=10, loop=0)
    assert data[:6] == b"GIF89a"

    import io

    image = Image.open(io.BytesIO(data))
    assert image.size == (30, 20)
    assert getattr(image, "n_frames", 1) == 3
    image.seek(2)
    assert int(np.array(image.convert("RGB")).mean()) == pytest.approx(204, abs=2)


def test_encode_gif_needs_a_frame():
    with pytest.raises(ValueError, match="at least one frame"):
        encode_gif([])
