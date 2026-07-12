"""End-to-end: the diff-drive turtlebot example driven through the full
stack — WebApp-style commands over the emulated wire protocol, into MuJoCo,
and encoder/pose telemetry back out."""

import importlib.util
import math
from pathlib import Path

import pytest

pytest.importorskip("mujoco")

_EXAMPLE = (
    Path(__file__).parent.parent
    / "codetocad_integrations/mujoco/examples/turtlebot_diff_drive.py"
)
_spec = importlib.util.spec_from_file_location("turtlebot_diff_drive", _EXAMPLE)
turtlebot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(turtlebot)

# 57 rpm for ~3 s is ~2.85 revolutions -> ~11700 ticks; allow spin-up.
ENCODER_MIN_TICKS = 8000


@pytest.fixture()
def rig(tmp_path):
    chassis, left_wheel, right_wheel = turtlebot.build_turtlebot()
    sim = turtlebot.make_simulation(chassis, output_dir=tmp_path)
    mcu, left_encoder, right_encoder = turtlebot.make_microcontroller(
        left_wheel, right_wheel
    )
    emulator = turtlebot.wire_emulation(sim, mcu)
    emulator.communication.connect()
    return sim, mcu, emulator, left_wheel, right_wheel, left_encoder, right_encoder


def test_drives_straight_and_reports_encoders(rig):
    sim, mcu, emulator, left_wheel, right_wheel, left_encoder, right_encoder = rig
    left_wheel.set_velocity(57)
    right_wheel.set_velocity(57)
    turtlebot.drive(sim, emulator, duration_seconds=3.0)
    mcu.poll()

    (x, y, _), _ = sim.get_body_pose("chassis")
    assert x > 0.3  # ~0.2 m/s once spun up
    assert abs(y) < 0.1

    assert left_encoder.read_velocity_rpm() == pytest.approx(57, rel=0.15)
    assert right_encoder.read_velocity_rpm() == pytest.approx(57, rel=0.15)
    assert left_encoder.read_count() > ENCODER_MIN_TICKS
    assert right_encoder.read_count() > ENCODER_MIN_TICKS

    pose = emulator.communication.telemetry.last_value
    assert mcu.communication.telemetry.last_value is pose  # shared channel


def test_opposite_wheels_spin_in_place(rig):
    sim, mcu, emulator, left_wheel, right_wheel, _, _ = rig
    left_wheel.set_velocity(57)
    right_wheel.set_velocity(-57)
    turtlebot.drive(sim, emulator, duration_seconds=3.0)

    (x, y, _), quat = sim.get_body_pose("chassis")
    assert math.hypot(x, y) < 0.08  # stays near the start
    w, qx, qy, qz = quat
    yaw = math.atan2(2 * (w * qz + qx * qy), 1 - 2 * (qy * qy + qz * qz))
    assert abs(yaw) > math.radians(30)  # but has rotated


def test_stop_command_halts_wheel(rig):
    sim, mcu, emulator, left_wheel, right_wheel, left_encoder, _ = rig
    left_wheel.set_velocity(57)
    right_wheel.set_velocity(57)
    turtlebot.drive(sim, emulator, duration_seconds=1.0)
    left_wheel.stop()
    right_wheel.stop()
    turtlebot.drive(sim, emulator, duration_seconds=1.5)
    mcu.poll()
    assert abs(left_encoder.read_velocity_rpm()) < 5


def test_app_controls_target_the_wire_channels(rig):
    _, mcu, emulator, left_wheel, right_wheel, left_encoder, right_encoder = rig
    app = turtlebot.make_app(
        emulator.communication, left_wheel, right_wheel, left_encoder, right_encoder
    )
    sliders = [c for c in app.controls if c.kind == "slider"]
    assert [s.target_channel for s in sliders] == ["left_motor", "right_motor"]
    gauges = [c for c in app.controls if c.kind == "gauge"]
    assert {g.source_channel for g in gauges} == {
        "left_encoder",
        "right_encoder",
        "pose",
    }
