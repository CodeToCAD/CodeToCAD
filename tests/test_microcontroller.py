import json

import pytest

from codetocad import (
    EventStream,
    I2CBus,
    LowPassFilter,
    MedianFilter,
    Microcontroller,
    MicrocontrollerBoard,
    MovingAverageFilter,
    MqttCommunication,
    SerialCommunication,
    SPIBus,
    UARTBus,
    WebApp,
    WifiCommunication,
    apply_filter,
)
from codetocad.apps import Control
from codetocad.mixins import (
    ActuatorMixin,
    BLDCMotorMixin,
    CurrentSensorMixin,
    DCMotorMixin,
    EncoderMixin,
    IMUMixin,
    SensorMixin,
    StepperMotorMixin,
)


class FakeTransport:
    def __init__(self):
        self.sent = []
        self.incoming = []
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def send_line(self, line):
        self.sent.append(line)

    def read_lines(self):
        lines = self.incoming[:]
        self.incoming.clear()
        return lines


class Potentiometer(SensorMixin):
    pass


class Motor(DCMotorMixin):
    pass


def _connected_serial():
    communication = SerialCommunication("/dev/fake")
    transport = FakeTransport()
    communication.attach_transport(transport)
    communication.connect()
    return communication, transport


# -- EventStream / signals --


def test_event_stream_map_filter_and_unsubscribe():
    stream = EventStream()
    seen = []
    doubled = stream.map(lambda v: v * 2).filter(lambda v: v > 2)
    doubled.subscribe(seen.append)
    unsubscribe = stream.subscribe(seen.append)
    stream.emit(1)  # doubled=2 filtered out; raw 1 recorded
    stream.emit(5)  # doubled=10 recorded; raw 5 recorded
    unsubscribe()
    stream.emit(7)  # raw no longer recorded; doubled=14 recorded
    assert seen == [1, 10, 5, 14]
    assert stream.last_value == 7


def test_signal_filters():
    low_pass = LowPassFilter(alpha=0.5)
    assert low_pass(1.0) == 1.0
    assert low_pass(3.0) == 2.0
    assert list(apply_filter(MovingAverageFilter(2), [1, 3, 5])) == [1.0, 2.0, 4.0]
    median = MedianFilter(3)
    assert [median(v) for v in (1, 100, 2)] == [1.0, 50.5, 2.0]


# -- communication --


def test_send_command_and_poll_routes_telemetry_stream():
    communication, transport = _connected_serial()
    communication.send_command("wheel", {"velocity_rpm": 10})
    assert json.loads(transport.sent[0]) == {
        "type": "command",
        "name": "wheel",
        "value": {"velocity_rpm": 10},
    }

    telemetry = []
    communication.telemetry.subscribe(telemetry.append)
    transport.incoming.append(
        json.dumps({"type": "telemetry", "name": "pot", "value": 1.65, "t": 1.0})
    )
    transport.incoming.append("not json")
    messages = communication.poll()
    assert len(messages) == 2
    assert telemetry == [{"type": "telemetry", "name": "pot", "value": 1.65, "t": 1.0}]
    assert messages[1]["type"] == "raw"


def test_wifi_tcp_transport_round_trip():
    """End-to-end over a real socket: a fake device echoes telemetry."""
    import socket
    import threading

    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]
    received = []

    def device():
        client, _ = server.accept()
        received.append(client.makefile().readline())
        client.sendall(
            json.dumps({"type": "telemetry", "name": "pot", "value": 3.1, "t": 0})
            .encode() + b"\n"
        )
        client.close()

    thread = threading.Thread(target=device)
    thread.start()
    communication = WifiCommunication("127.0.0.1", port=port)
    communication.connect()
    communication.send_command("wheel", 1)
    thread.join(timeout=5)
    message = communication.receive(timeout_seconds=5)
    communication.disconnect()
    server.close()
    assert json.loads(received[0]) == {"type": "command", "name": "wheel", "value": 1}
    assert message == {"type": "telemetry", "name": "pot", "value": 3.1, "t": 0}


def test_communication_specs():
    wifi = WifiCommunication("192.168.4.1", ssid="lab", password="pw")
    assert (wifi.host, wifi.port) == ("192.168.4.1", 8266)
    mqtt = MqttCommunication("broker.local", topic="robot")
    assert mqtt.command_topic == "robot/command"
    assert mqtt.telemetry_topic == "robot/telemetry"


# -- microcontroller bindings --


def test_bind_infers_drivers_and_rejects_duplicates():
    mcu = Microcontroller("mcu", board=MicrocontrollerBoard.ESP32)
    encoder_binding = mcu.bind_sensor(EncoderMixin(), name="enc", a=32, b=33)
    current_binding = mcu.bind_sensor(CurrentSensorMixin(), name="amps", pin=35)
    stepper_binding = mcu.bind_actuator(StepperMotorMixin(), name="axis", step_pin=12, dir_pin=13)
    motor_binding = mcu.bind_actuator(Motor(), name="wheel", pwm_pin=5, dir_pin=18)
    assert encoder_binding.driver == "encoder"
    assert current_binding.driver == "current"
    assert stepper_binding.driver == "stepper"
    assert motor_binding.driver == "dc_motor"
    assert motor_binding.pins == {"pwm": 5, "dir": 18}
    assert [b.name for b in mcu.sensors] == ["enc", "amps"]
    with pytest.raises(ValueError):
        mcu.bind_actuator(Motor(), name="wheel", pwm_pin=19, dir_pin=21)
    with pytest.raises(ValueError):
        mcu.bind_sensor(Potentiometer())  # no pins


def test_bus_bindings_infer_drivers_and_collect_buses():
    mcu = Microcontroller("mcu")
    i2c = I2CBus(sda=21, scl=22)
    spi = SPIBus(sck=14, mosi=13, miso=12)
    uart = UARTBus(tx=17, rx=16)
    imu = mcu.bind_sensor(IMUMixin(), name="imu", bus=i2c, address=0x68)
    amps = mcu.bind_sensor(CurrentSensorMixin(), name="amps", bus=i2c, address=0x40)
    reg = mcu.bind_sensor(SensorMixin(), name="reg", bus=i2c, address=0x48,
                          params={"register": 0x00})
    adc = mcu.bind_sensor(SensorMixin(), name="adc", bus=spi, cs=5,
                          params={"channel": 2})
    drv = mcu.bind_actuator(DCMotorMixin(), name="drv", bus=i2c, address=0x60)
    servo = mcu.bind_actuator(ActuatorMixin(), name="servo", bus=i2c, address=0x41,
                              params={"channel": 3})
    bldc = mcu.bind_actuator(BLDCMotorMixin(), name="bldc", bus=uart)
    assert imu.driver == "imu_mpu6050"
    assert amps.driver == "current_ina219"
    assert reg.driver == "i2c_register"
    assert adc.driver == "adc_mcp3008"
    assert drv.driver == "dc_motor_drv8830"
    assert servo.driver == "pwm_pca9685"
    assert bldc.driver == "vesc_uart"
    assert mcu.buses == [i2c, spi, uart]  # each shared bus collected once


def test_bus_binding_validation():
    mcu = Microcontroller("mcu")
    i2c = I2CBus(sda=21, scl=22)
    with pytest.raises(ValueError, match="address"):
        mcu.bind_sensor(IMUMixin(), name="imu", bus=i2c)
    with pytest.raises(ValueError, match="chip select"):
        mcu.bind_sensor(
            SensorMixin(), name="adc", bus=SPIBus(sck=14, mosi=13, miso=12)
        )
    with pytest.raises(ValueError, match="No default UART driver"):
        mcu.bind_sensor(SensorMixin(), name="gps", bus=UARTBus())


def test_actuator_commands_flow_over_communication():
    mcu = Microcontroller("mcu")
    motor = Motor()
    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    motor.set_velocity(50)  # not connected yet: recorded, not sent
    assert motor.get_velocity() == 50.0

    communication, transport = _connected_serial()
    mcu.set_communication(communication)
    motor.set_speed(120)
    motor.stop()
    payloads = [json.loads(line) for line in transport.sent]
    assert payloads[0] == {
        "type": "command",
        "name": "wheel",
        "value": {"velocity_rpm": 120.0},
    }
    assert payloads[1]["value"] == {"stop": True}


def test_telemetry_routes_to_bound_sensors():
    mcu = Microcontroller("mcu")
    pot = Potentiometer()
    encoder = EncoderMixin()
    encoder.counts_per_revolution = 1000
    mcu.bind_sensor(pot, name="pot", pin=34)
    mcu.bind_sensor(encoder, name="enc", a=32, b=33)
    communication, transport = _connected_serial()
    mcu.set_communication(communication)

    samples = []
    pot.events.subscribe(samples.append)
    transport.incoming = [
        json.dumps({"type": "telemetry", "name": "pot", "value": 1.65, "t": 2.0}),
        json.dumps(
            {
                "type": "telemetry",
                "name": "enc",
                "value": {"count": 500, "rpm": 60.0},
                "t": 2.0,
            }
        ),
    ]
    mcu.poll()
    assert pot.read() == 1.65
    assert samples == [1.65]
    assert encoder.read_count() == 500
    assert encoder.read_position_degrees() == 180.0
    assert encoder.read_velocity_rpm() == 60.0


def test_current_sensor_conversion():
    sensor = CurrentSensorMixin()
    sensor.amps_per_volt = 1 / 0.185
    sensor.zero_offset_volts = 2.5
    sensor._update(2.685)
    assert sensor.read_current() == pytest.approx(1.0)


def test_python_board_upload_needs_firmware_path():
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    with pytest.raises(ValueError, match="firmware_path"):
        mcu.upload()


# -- apps --


def test_app_controls_and_send_control():
    mcu = Microcontroller("mcu")
    motor = Motor()
    pot = Potentiometer()
    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    mcu.bind_sensor(pot, name="pot", pin=34)
    communication, transport = _connected_serial()
    mcu.set_communication(communication)

    app = WebApp("panel").set_communication(communication)
    slider = app.add_slider(
        "speed", target=motor, command="velocity_rpm", maximum=300
    )
    gauge = app.add_gauge("pot (V)", source=pot, units="V")
    app.add_button("stop", target="wheel", value={"stop": True})
    assert slider.target_channel == "wheel"
    assert gauge.source_channel == "pot"

    app.send_control(slider, 150)
    assert json.loads(transport.sent[-1]) == {
        "type": "command",
        "name": "wheel",
        "value": {"velocity_rpm": 150},
    }
    app.send_control(app.controls[2], app.controls[2].params["value"])
    assert json.loads(transport.sent[-1])["value"] == {"stop": True}


def test_unbound_control_target_raises():
    control = Control("slider", "speed", target=Motor())
    with pytest.raises(ValueError, match="not bound"):
        control.target_channel
