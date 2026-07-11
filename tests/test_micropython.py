"""The micropython integration's codegen is pure Python (mpremote is only
needed to flash), so these tests run without any extras installed."""

import pytest

from codetocad import (
    I2CBus,
    Microcontroller,
    MicrocontrollerBoard,
    MqttCommunication,
    SPIBus,
    UARTBus,
    WifiCommunication,
)
from codetocad.mixins import (
    BLDCMotorMixin,
    CurrentSensorMixin,
    DCMotorMixin,
    EncoderMixin,
    IMUMixin,
    SensorMixin,
    StepperMotorMixin,
)
from codetocad_integrations.micropython import generate_main_py, upload
from codetocad_integrations.micropython.firmware import _VESC_HELPERS


class Motor(DCMotorMixin):
    no_load_speed_rpm = 240


class Potentiometer(SensorMixin):
    sample_rate_hz = 20.0


def _esp32_rig():
    mcu = Microcontroller("rig", board=MicrocontrollerBoard.ESP32)
    mcu.bind_actuator(Motor(), name="wheel", pwm_pin=5, dir_pin=18)
    mcu.bind_sensor(Potentiometer(), name="pot", pin=34)
    encoder = EncoderMixin()
    encoder.counts_per_revolution = 1024
    mcu.bind_sensor(encoder, name="enc", a=32, b=33)
    mcu.bind_actuator(StepperMotorMixin(), name="axis", step_pin=12, dir_pin=13)
    return mcu


def test_micropython_firmware_compiles_and_wires_bindings():
    firmware = generate_main_py(_esp32_rig())
    compile(firmware, "main.py", "exec")  # valid syntax
    assert "from machine import Pin, ADC, PWM" in firmware
    assert "PWM(Pin(5), freq=1000)" in firmware
    assert "ADC(Pin(34))" in firmware
    assert "/ 1024 / dt * 60" in firmware  # encoder cpr from the device
    assert "/ 240" in firmware  # dc motor max_rpm from no_load_speed_rpm
    assert "'wheel': command_wheel" in firmware
    assert "'axis': command_axis" in firmware
    assert "['pot', read_pot, 50, 0]" in firmware  # 20 Hz -> 50 ms
    assert "sys.stdin" in firmware  # default serial communication


def test_micropython_wifi_and_mqtt_comm_sections():
    mcu = _esp32_rig()
    mcu.set_communication(
        WifiCommunication("192.168.4.1", port=9000, ssid="lab", password="pw")
    )
    firmware = generate_main_py(mcu)
    compile(firmware, "main.py", "exec")
    assert "WIFI_SSID = 'lab'" in firmware
    assert "TCP_PORT = 9000" in firmware

    mcu.set_communication(MqttCommunication("broker.local", topic="rig"))
    firmware = generate_main_py(mcu)
    compile(firmware, "main.py", "exec")
    assert "umqtt.simple" in firmware
    assert "'rig/command'" in firmware
    assert "'rig/telemetry'" in firmware


def test_python_board_firmware_uses_gpiozero():
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    mcu.bind_actuator(Motor(), name="wheel", pwm_pin=5, dir_pin=18)
    encoder = EncoderMixin()
    mcu.bind_sensor(encoder, name="enc", a=17, b=27)
    firmware = generate_main_py(mcu)
    compile(firmware, "agent.py", "exec")
    assert "from gpiozero import" in firmware
    assert "RotaryEncoder(17, 27" in firmware


def test_python_board_rejects_analog_bindings():
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    mcu.bind_sensor(Potentiometer(), name="pot", pin=4)
    with pytest.raises(ValueError, match="ADC"):
        generate_main_py(mcu)


def test_micropython_i2c_firmware():
    from codetocad.mixins import ActuatorMixin

    mcu = Microcontroller("bus-rig", board=MicrocontrollerBoard.ESP32)
    i2c = I2CBus(sda=21, scl=22)
    mcu.bind_sensor(IMUMixin(), name="imu", bus=i2c, address=0x69)
    mcu.bind_sensor(CurrentSensorMixin(), name="amps", bus=i2c, address=0x40,
                    params={"shunt_ohms": 0.05})
    mcu.bind_sensor(SensorMixin(), name="temp", bus=i2c, address=0x48,
                    params={"register": 0x00, "scale": 0.0078125, "signed": True})
    mcu.bind_actuator(DCMotorMixin(), name="drv", bus=i2c, address=0x60)
    mcu.bind_actuator(ActuatorMixin(), name="fan", bus=i2c, address=0x41,
                      params={"channel": 3})
    firmware = generate_main_py(mcu)
    compile(firmware, "main.py", "exec")
    assert "_i2c0 = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)" in firmware
    assert "readfrom_mem(105, 0x3B, 14)" in firmware  # IMU at 0x69 on shared bus
    assert "readfrom_mem(64, 0x01, 2)" in firmware  # INA219 shunt register
    assert "1e-05 / 0.05" in firmware
    assert "raw * 0.0078125" in firmware  # generic register sensor
    assert "_pca9685_init(_i2c0, 65, 1000)" in firmware
    assert "writeto_mem(96, 0x00" in firmware  # DRV8830


def test_micropython_spi_and_uart_firmware():
    mcu = Microcontroller("bus-rig", board=MicrocontrollerBoard.ESP32)
    spi = SPIBus(sck=14, mosi=13, miso=12)
    uart = UARTBus(tx=17, rx=16, id=2)
    mcu.bind_sensor(SensorMixin(), name="adc", bus=spi, cs=5, params={"channel": 2})
    bldc = BLDCMotorMixin()
    bldc.pole_pairs = 7
    mcu.bind_actuator(bldc, name="bldc", bus=uart)
    firmware = generate_main_py(mcu)
    compile(firmware, "main.py", "exec")
    assert "_spi1 = SPI(1, baudrate=1000000, sck=Pin(14)" in firmware
    assert "_uart2 = UART(2, baudrate=115200, tx=Pin(17), rx=Pin(16))" in firmware
    assert "_vesc_crc16" in firmware
    assert "* 7))" in firmware  # rpm -> erpm via pole_pairs


def test_vesc_framing_is_valid():
    """Exec the generated VESC helpers and check the frame against the
    known CRC16-XMODEM check value."""
    namespace = {}
    exec(_VESC_HELPERS, namespace)
    assert namespace["_vesc_crc16"](b"123456789") == 0x31C3
    packet = namespace["_vesc_command"](8, -7000)
    payload = bytes([8]) + ((-7000) & 0xFFFFFFFF).to_bytes(4, "big")
    assert packet[0] == 2 and packet[1] == len(payload) and packet[-1] == 3
    assert packet[2:7] == payload
    assert packet[7:9] == namespace["_vesc_crc16"](payload).to_bytes(2, "big")


def test_i2c_register_requires_register_param():
    mcu = Microcontroller("mcu", board=MicrocontrollerBoard.ESP32)
    mcu.bind_sensor(SensorMixin(), name="raw", bus=I2CBus(sda=21, scl=22),
                    address=0x48)
    with pytest.raises(ValueError, match="register"):
        generate_main_py(mcu)


def test_python_board_i2c_spi_uart_firmware():
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    i2c = I2CBus(sda=2, scl=3, id=1)
    mcu.bind_sensor(IMUMixin(), name="imu", bus=i2c, address=0x68)
    mcu.bind_sensor(SensorMixin(), name="adc",
                    bus=SPIBus(sck=11, mosi=10, miso=9), cs=7,
                    params={"channel": 1})
    mcu.bind_actuator(BLDCMotorMixin(), name="bldc",
                      bus=UARTBus(device_path="/dev/ttyACM0"))
    firmware = generate_main_py(mcu)
    compile(firmware, "agent.py", "exec")
    assert "from smbus2 import SMBus" in firmware
    assert "_i2c1 = _I2CAdapter(1)" in firmware
    assert "MCP3008(channel=1, device=1)" in firmware  # cs=7 -> CE1
    assert "serial.Serial('/dev/ttyACM0', 115200)" in firmware


def test_python_board_i2c_needs_a_bus():
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    mcu.bind_sensor(IMUMixin(), name="imu", sda=2, scl=3)  # pins, no bus
    with pytest.raises(ValueError, match="bus=I2CBus"):
        generate_main_py(mcu)


def test_upload_requires_a_port_and_micropython_board():
    with pytest.raises(ValueError, match="port"):
        upload(_esp32_rig())
    with pytest.raises(ValueError, match="MicroPython"):
        upload(Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI))


def test_python_board_upload_writes_agent_script(tmp_path):
    mcu = Microcontroller("pi", board=MicrocontrollerBoard.RASPBERRY_PI)
    mcu.bind_actuator(Motor(), name="wheel", pwm_pin=5, dir_pin=18)
    path = mcu.upload(firmware_path=str(tmp_path / "agent.py"))
    assert (tmp_path / "agent.py").read_text().startswith('"""CodeToCAD agent')
    assert path == str(tmp_path / "agent.py")
