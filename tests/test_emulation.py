import pytest

from codetocad import EmulatedMicrocontroller, Microcontroller, WebApp
from codetocad.mixins import DCMotorMixin, EncoderMixin


class Motor(DCMotorMixin):
    pass


def _rig():
    mcu = Microcontroller("rig")
    motor = Motor()
    encoder = EncoderMixin()
    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    mcu.bind_sensor(encoder, name="enc", a=32, b=33, sample_rate_hz=100.0)
    return mcu, motor, encoder


def test_commands_reach_handlers_and_telemetry_flows_back():
    mcu, motor, encoder = _rig()
    emulator = EmulatedMicrocontroller(mcu)
    assert mcu.communication is emulator.communication

    received = []
    emulator.on_command("wheel", received.append)
    state = {"count": 0, "rpm": 0.0}
    emulator.set_sensor("enc", lambda: dict(state))

    emulator.communication.connect()
    motor.set_velocity(120)  # computer side -> wire
    emulator.step(now=0.0)  # device side: dispatch + sample
    assert received == [{"velocity_rpm": 120.0}]

    state.update(count=512, rpm=30.0)
    emulator.step(now=0.5)  # 100 Hz sensor is due again
    mcu.poll()  # computer side: route telemetry to the bound encoder
    assert encoder.read_count() == 512
    assert encoder.read_velocity_rpm() == 30.0


def test_sensor_sampling_respects_rate_and_extra_telemetry():
    mcu, _, _ = _rig()
    emulator = EmulatedMicrocontroller(mcu)
    emulator.set_sensor("enc", lambda: 1, sample_rate_hz=10.0)  # every 100 ms
    emulator.add_telemetry("pose", lambda: {"x": 1.5}, sample_rate_hz=10.0)
    emulator.communication.connect()

    for now in (0.0, 0.01, 0.02, 0.101):  # due at 0.0 and 0.101 only
        emulator.step(now=now)
    messages = emulator.communication.poll()
    names = [m["name"] for m in messages]
    assert names.count("enc") == 2
    assert names.count("pose") == 2
    assert {"type": "telemetry", "name": "pose", "value": {"x": 1.5}, "t": 0.0} in messages


def test_channel_validation():
    mcu, _, _ = _rig()
    emulator = EmulatedMicrocontroller(mcu)
    with pytest.raises(KeyError):
        emulator.on_command("typo", lambda value: None)
    with pytest.raises(ValueError, match="sensor"):
        emulator.on_command("enc", lambda value: None)
    with pytest.raises(ValueError, match="actuator"):
        emulator.set_sensor("wheel", lambda: 0)


def test_app_drives_emulated_device():
    mcu, motor, _ = _rig()
    emulator = EmulatedMicrocontroller(mcu)
    targets = []
    emulator.on_command("wheel", targets.append)
    emulator.communication.connect()

    app = WebApp("panel").set_communication(emulator.communication)
    slider = app.add_slider("speed", target=motor, command="velocity_rpm")
    app.send_control(slider, 42)
    emulator.step(now=0.0)
    assert targets == [{"velocity_rpm": 42}]
