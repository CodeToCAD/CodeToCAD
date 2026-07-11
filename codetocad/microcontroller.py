"""Microcontroller definition: boards, GPIO bindings and firmware upload.

A ``Microcontroller`` is an ``ElectricalComponent`` (so it has a footprint,
schematic pins and can be placed on a board assembly) that additionally
declares *bindings*: which sensor/actuator parts hang off which GPIO pins,
and a ``Communication`` channel to a computer.

The declaration is federated by runtime:

- MicroPython boards (ESP32, ESP8266, Raspberry Pi Pico):
  ``codetocad_integrations.micropython`` generates a ``main.py`` from the
  bindings and uploads it with mpremote; the board then speaks the
  codetocad wire protocol over the declared communication channel.
- Python boards (Raspberry Pi): run the generated agent script with
  CPython on the device.

Example::

    from codetocad import (
        Microcontroller, MicrocontrollerBoard, SerialCommunication, cube,
    )
    from codetocad.mixins import DCMotorMixin, SensorMixin

    class Motor(DCMotorMixin):
        pass

    motor = Motor()
    mcu = Microcontroller("driver", board=MicrocontrollerBoard.ESP32)
    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    mcu.set_communication(SerialCommunication("/dev/ttyUSB0"))
    mcu.upload()      # generate + flash main.py
    mcu.connect()
    motor.set_velocity(120)
"""

from __future__ import annotations

from enum import Enum

from codetocad.communication import Communication, CommunicationMixin
from codetocad.ecad import ComponentType, ElectricalComponent
from codetocad.mixins import (
    ActuatorMixin,
    CurrentSensorMixin,
    EncoderMixin,
    IMUMixin,
    MotorMixin,
    StepperMotorMixin,
)


class MicrocontrollerRuntime(Enum):
    MICROPYTHON = "micropython"
    PYTHON = "python"


class MicrocontrollerBoard(Enum):
    """Supported boards. ``runtime`` selects how firmware is generated and
    uploaded; ``adc_max`` is the full-scale raw ADC reading used to convert
    analog samples to volts."""

    ESP32 = ("esp32", MicrocontrollerRuntime.MICROPYTHON, 4095, 3.3)
    ESP8266 = ("esp8266", MicrocontrollerRuntime.MICROPYTHON, 1023, 3.3)
    RASPBERRY_PI_PICO = (
        "raspberry_pi_pico",
        MicrocontrollerRuntime.MICROPYTHON,
        65535,
        3.3,
    )
    RASPBERRY_PI = ("raspberry_pi", MicrocontrollerRuntime.PYTHON, None, 3.3)
    GENERIC_MICROPYTHON = ("generic", MicrocontrollerRuntime.MICROPYTHON, 4095, 3.3)

    def __init__(self, board_name, runtime, adc_max, logic_voltage):
        self.board_name = board_name
        self.runtime = runtime
        self.adc_max = adc_max
        self.logic_voltage = logic_voltage


# Drivers name the firmware routine that services a binding. The
# micropython integration documents the wiring each driver expects.
SENSOR_DRIVERS = (
    "analog",
    "digital_in",
    "encoder",
    "current",
    "imu_mpu6050",
    # bus sensors
    "i2c_register",
    "current_ina219",
    "adc_mcp3008",
)
ACTUATOR_DRIVERS = (
    "pwm",
    "digital_out",
    "dc_motor",
    "stepper",
    "servo",
    # bus actuators
    "pwm_pca9685",
    "servo_pca9685",
    "dc_motor_drv8830",
    "vesc_uart",
)


class I2CBus:
    """An I2C bus on the microcontroller. Share one instance between every
    device on the bus; each binding adds its own ``address``."""

    kind = "i2c"

    def __init__(self, sda: int, scl: int, id: int = 0, frequency_hz: int = 400_000):
        self.sda = sda
        self.scl = scl
        self.id = id
        self.frequency_hz = frequency_hz

    def __repr__(self):
        return f"I2CBus(id={self.id}, sda={self.sda}, scl={self.scl})"


class SPIBus:
    """An SPI bus on the microcontroller. Each binding adds its own chip
    select with ``cs=<gpio>``."""

    kind = "spi"

    def __init__(
        self, sck: int, mosi: int, miso: int, id: int = 1, baud_rate: int = 1_000_000
    ):
        self.sck = sck
        self.mosi = mosi
        self.miso = miso
        self.id = id
        self.baud_rate = baud_rate

    def __repr__(self):
        return f"SPIBus(id={self.id}, sck={self.sck})"


class UARTBus:
    """A UART on the microcontroller for serial peripherals (VESC, GPS,
    ...). ``device_path`` is used on Python boards (Raspberry Pi), where
    UARTs are device files rather than pin-mapped ids."""

    kind = "uart"

    def __init__(
        self,
        tx: int | None = None,
        rx: int | None = None,
        id: int = 1,
        baud_rate: int = 115200,
        device_path: str = "/dev/serial0",
    ):
        self.tx = tx
        self.rx = rx
        self.id = id
        self.baud_rate = baud_rate
        self.device_path = device_path

    def __repr__(self):
        return f"UARTBus(id={self.id}, baud_rate={self.baud_rate})"


class PinBinding:
    """A sensor or actuator attached to GPIO pins or a bus.

    ``pins`` maps role names to GPIO numbers, e.g. ``{"pin": 34}`` for an
    analog sensor, ``{"pwm": 5, "dir": 18}`` for a DC motor or
    ``{"cs": 5}`` for an SPI device's chip select. Bus devices carry the
    shared ``bus`` (I2CBus/SPIBus/UARTBus) and, for I2C, their ``address``.
    ``name`` is the wire protocol channel for the device's telemetry and
    commands."""

    def __init__(
        self,
        microcontroller: "Microcontroller",
        device,
        name: str,
        role: str,
        driver: str,
        pins: dict[str, int],
        sample_rate_hz: float | None = None,
        params: dict | None = None,
        bus: "I2CBus | SPIBus | UARTBus | None" = None,
        address: int | None = None,
    ):
        self.microcontroller = microcontroller
        self.device = device
        self.name = name
        self.role = role
        self.driver = driver
        self.pins = pins
        self.sample_rate_hz = sample_rate_hz
        self.params = params or {}
        self.bus = bus
        self.address = address

    def send(self, value):
        """Send a command for this channel over the microcontroller's
        communication (no-op while disconnected; the command is still
        recorded on the device)."""
        communication = self.microcontroller.communication
        if communication is not None and communication.is_connected:
            communication.send_command(self.name, value)

    def __repr__(self):
        attachment = f"bus={self.bus}" if self.bus is not None else f"pins={self.pins}"
        return f"PinBinding({self.name!r}, driver={self.driver!r}, {attachment})"


def _infer_driver(device, role: str, bus=None) -> str:
    if isinstance(bus, I2CBus):
        if role == "sensor":
            if isinstance(device, IMUMixin):
                return "imu_mpu6050"
            if isinstance(device, CurrentSensorMixin):
                return "current_ina219"
            return "i2c_register"
        if isinstance(device, MotorMixin):
            return "dc_motor_drv8830"
        return "pwm_pca9685"
    if isinstance(bus, SPIBus):
        if role == "sensor":
            return "adc_mcp3008"
        raise ValueError(
            "No default SPI actuator driver; pass driver= explicitly"
        )
    if isinstance(bus, UARTBus):
        if isinstance(device, MotorMixin):
            return "vesc_uart"
        raise ValueError("No default UART driver for this device; pass driver=")
    if role == "sensor":
        if isinstance(device, EncoderMixin):
            return "encoder"
        if isinstance(device, CurrentSensorMixin):
            return "current"
        if isinstance(device, IMUMixin):
            return "imu_mpu6050"
        return "analog"
    if isinstance(device, StepperMotorMixin):
        return "stepper"
    if isinstance(device, MotorMixin):
        return "dc_motor"
    return "pwm"


class Microcontroller(ElectricalComponent, CommunicationMixin):
    """A microcontroller board with GPIO bindings and a communication
    channel. See the module docstring for the full workflow."""

    def __init__(
        self,
        name: str | None = None,
        board: MicrocontrollerBoard = MicrocontrollerBoard.ESP32,
        description: str | None = None,
    ):
        super().__init__(name, description)
        self._init_communication()
        self.component_type = ComponentType.IC
        self.board = board
        self.bindings: list[PinBinding] = []
        self.buses: list[I2CBus | SPIBus | UARTBus] = []
        self._unsubscribe_telemetry = None

    # -- bindings --

    def bind_sensor(
        self,
        device,
        *,
        name: str | None = None,
        driver: str | None = None,
        sample_rate_hz: float | None = None,
        params: dict | None = None,
        bus: "I2CBus | SPIBus | UARTBus | None" = None,
        address: int | None = None,
        **pins: int,
    ) -> PinBinding:
        """Attach a sensor to GPIO pins or a bus, e.g.
        ``bind_sensor(pot, pin=34)``, ``bind_sensor(encoder, a=32, b=33)``,
        ``bind_sensor(imu, bus=i2c, address=0x68)`` or
        ``bind_sensor(adc, bus=spi, cs=5, params={"channel": 0})``.
        Telemetry for the channel updates ``device.read()``/``device.events``."""
        driver = driver or _infer_driver(device, "sensor", bus)
        if driver not in SENSOR_DRIVERS:
            raise ValueError(f"Unknown sensor driver {driver!r}; use {SENSOR_DRIVERS}")
        if sample_rate_hz is None:
            sample_rate_hz = getattr(device, "sample_rate_hz", 10.0)
        return self._bind(
            device, name, "sensor", driver, pins, sample_rate_hz, params, bus, address
        )

    def bind_actuator(
        self,
        device,
        *,
        name: str | None = None,
        driver: str | None = None,
        params: dict | None = None,
        bus: "I2CBus | SPIBus | UARTBus | None" = None,
        address: int | None = None,
        **pins: int,
    ) -> PinBinding:
        """Attach an actuator to GPIO pins or a bus, e.g.
        ``bind_actuator(motor, pwm_pin=5, dir_pin=18)``,
        ``bind_actuator(motor, bus=i2c, address=0x60)`` (DRV8830),
        ``bind_actuator(servo, bus=i2c, address=0x40, params={"channel": 0})``
        (PCA9685) or ``bind_actuator(bldc, bus=uart)`` (VESC).
        ``device.write`` (and the motor set_* methods) then command the
        channel."""
        driver = driver or _infer_driver(device, "actuator", bus)
        if driver not in ACTUATOR_DRIVERS:
            raise ValueError(
                f"Unknown actuator driver {driver!r}; use {ACTUATOR_DRIVERS}"
            )
        return self._bind(device, name, "actuator", driver, pins, None, params, bus, address)

    def _bind(
        self, device, name, role, driver, pins, sample_rate_hz, params, bus, address
    ):
        if not pins and bus is None:
            raise ValueError(
                "Give at least one GPIO pin (e.g. pin=34 or pwm_pin=5) or a "
                "bus= (I2CBus/SPIBus/UARTBus)"
            )
        if isinstance(bus, I2CBus) and address is None:
            raise ValueError("I2C devices need address= (e.g. address=0x40)")
        if isinstance(bus, SPIBus) and "cs" not in {
            key.removesuffix("_pin") for key in pins
        }:
            raise ValueError("SPI devices need a chip select, e.g. cs=5")
        pins = {key.removesuffix("_pin"): number for key, number in pins.items()}
        name = name or self._next_channel_name(device)
        if any(binding.name == name for binding in self.bindings):
            raise ValueError(f"Channel {name!r} is already bound")
        binding = PinBinding(
            self, device, name, role, driver, pins, sample_rate_hz, params, bus, address
        )
        if bus is not None and bus not in self.buses:
            self.buses.append(bus)
        self.bindings.append(binding)
        device._binding = binding
        return binding

    def _next_channel_name(self, device) -> str:
        base = getattr(device, "name", None) or type(device).__name__.lower()
        names = {binding.name for binding in self.bindings}
        if base not in names:
            return base
        number = 2
        while f"{base}{number}" in names:
            number += 1
        return f"{base}{number}"

    def get_binding(self, name: str) -> PinBinding:
        for binding in self.bindings:
            if binding.name == name:
                return binding
        raise KeyError(f"No binding {name!r} on microcontroller {self.name!r}")

    @property
    def sensors(self) -> list[PinBinding]:
        return [binding for binding in self.bindings if binding.role == "sensor"]

    @property
    def actuators(self) -> list[PinBinding]:
        return [binding for binding in self.bindings if binding.role == "actuator"]

    # -- communication --

    def set_communication(self, communication: Communication):
        """Set the channel to the computer and route its telemetry to the
        bound sensors."""
        if self._unsubscribe_telemetry is not None:
            self._unsubscribe_telemetry()
        CommunicationMixin.set_communication(self, communication)
        self._unsubscribe_telemetry = communication.telemetry.subscribe(
            self._route_telemetry
        )
        return self

    def _route_telemetry(self, message: dict):
        for binding in self.sensors:
            if binding.name == message.get("name"):
                binding.device._update(message.get("value"), message.get("t"))

    def poll(self) -> list[dict]:
        """Pump the communication channel: reads pending messages and
        routes telemetry to the bound sensors."""
        if self.communication is None:
            return []
        return self.communication.poll()

    # -- firmware --

    def generate_firmware(self) -> str:
        """The device-side agent script (MicroPython ``main.py`` or a
        CPython script for Python boards) generated from the bindings."""
        from codetocad_integrations.micropython import generate_main_py

        return generate_main_py(self)

    def upload(self, port: str | None = None, firmware_path: str | None = None):
        """Generate the firmware and put it on the board.

        MicroPython boards are flashed over ``port`` (defaults to the
        serial communication's port) with mpremote. For Python boards
        (Raspberry Pi), pass ``firmware_path`` to write the agent script,
        then copy it to the device and run it with CPython."""
        if self.board.runtime is MicrocontrollerRuntime.MICROPYTHON:
            from codetocad_integrations.micropython import upload

            return upload(self, port=port)
        firmware = self.generate_firmware()
        if firmware_path is None:
            raise ValueError(
                f"{self.board.name} runs plain Python: pass firmware_path= to "
                "write the agent script, copy it to the device (scp) and run "
                "it with python3"
            )
        from pathlib import Path

        Path(firmware_path).write_text(firmware)
        return firmware_path

    def __repr__(self):
        return (
            f"Microcontroller({self.name!r}, board={self.board.board_name!r}, "
            f"bindings={len(self.bindings)})"
        )
