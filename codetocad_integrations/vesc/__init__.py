"""vesc integration: drive a VESC motor controller over serial (pyvesc).

A `VESC <https://vesc-project.com>`_ speaks its own binary protocol over
UART/USB, so it connects directly to the computer (or to a
microcontroller's UART) rather than through the codetocad wire protocol.
``VESCMotor`` implements the ``BLDCMotorMixin`` API on top of pyvesc
(``uv sync --extra vesc``)::

    from codetocad_integrations.vesc import VESCMotor

    motor = VESCMotor("/dev/ttyACM0", pole_pairs=7)
    motor.connect()
    motor.set_velocity(1500)         # mechanical rpm
    motor.set_current(4.0)           # amps
    print(motor.get_measurements())  # rpm, currents, voltage, temperature
    motor.stop()
"""

from __future__ import annotations

import time

import pyvesc
import serial
from pyvesc.VESC.messages import (
    GetValues,
    SetCurrent,
    SetDutyCycle,
    SetPosition,
    SetRPM,
)

from codetocad.mixins import BLDCMotorMixin


class VESCMotor(BLDCMotorMixin):
    """A BLDC motor on a VESC. ``set_velocity`` takes mechanical rpm and
    converts to electrical rpm via ``pole_pairs``."""

    def __init__(self, port: str, baud_rate: int = 115200, pole_pairs: int = 1):
        self.port = port
        self.baud_rate = baud_rate
        self.pole_pairs = pole_pairs
        self._serial: serial.Serial | None = None

    def connect(self):
        self._serial = serial.Serial(self.port, self.baud_rate, timeout=0.1)
        return self

    def disconnect(self):
        if self._serial is not None:
            self._serial.close()
            self._serial = None
        return self

    def _send(self, message):
        if self._serial is None:
            raise RuntimeError("Not connected; call connect() first")
        self._serial.write(pyvesc.encode(message))

    # MotorMixin API, executed on the VESC instead of a bound channel.

    def set_velocity(self, rpm: float):
        self._target_velocity_rpm = float(rpm)
        self._send(SetRPM(int(rpm * self.pole_pairs)))
        return self

    def set_current(self, amps: float):
        self._target_current_amps = float(amps)
        self._send(SetCurrent(float(amps)))
        return self

    def set_duty(self, duty: float):
        self._send(SetDutyCycle(float(duty)))
        return self

    def set_position(self, degrees: float):
        self._target_position_degrees = float(degrees)
        self._send(SetPosition(float(degrees)))
        return self

    def stop(self):
        self._target_velocity_rpm = 0.0
        self._send(SetCurrent(0))
        return self

    def get_measurements(self, timeout_seconds: float = 1.0):
        """Request and decode a GetValues frame (rpm, motor/input current,
        input voltage, FET temperature, ...)."""
        if self._serial is None:
            raise RuntimeError("Not connected; call connect() first")
        self._serial.write(pyvesc.encode_request(GetValues))
        buffer = b""
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            buffer += self._serial.read(64)
            if buffer:
                response, consumed = pyvesc.decode(buffer)
                if response is not None:
                    return response
        return None


__all__ = ["VESCMotor"]
