"""pyserial integration: the computer side of a SerialCommunication.

``SerialCommunication.connect()`` resolves this transport automatically, so
usually you only need the extra installed (``uv sync --extra pyserial``)::

    comm = SerialCommunication("/dev/ttyUSB0")
    comm.connect()
    comm.send_command("wheel", {"velocity_rpm": 120})
    print(comm.receive())

``list_ports()`` helps find the board's port.
"""

from __future__ import annotations

import serial
import serial.tools.list_ports


class SerialTransport:
    """JSON lines over a pyserial port."""

    def __init__(self, port: str, baud_rate: int = 115200, timeout_seconds: float = 0.0):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout_seconds = timeout_seconds
        self.connected = False
        self._serial: serial.Serial | None = None
        self._buffer = b""

    def connect(self):
        self._serial = serial.Serial(
            self.port, self.baud_rate, timeout=self.timeout_seconds
        )
        self.connected = True

    def disconnect(self):
        if self._serial is not None:
            self._serial.close()
            self._serial = None
        self.connected = False

    def send_line(self, line: str):
        if self._serial is None:
            raise RuntimeError("SerialTransport is not connected")
        self._serial.write(line.encode() + b"\n")

    def read_lines(self) -> list[str]:
        if self._serial is None:
            return []
        waiting = self._serial.in_waiting
        if waiting:
            self._buffer += self._serial.read(waiting)
        lines = self._buffer.split(b"\n")
        self._buffer = lines.pop()
        return [line.decode(errors="replace") for line in lines]


def list_ports() -> list[str]:
    """Names of the serial ports on this computer."""
    return [port.device for port in serial.tools.list_ports.comports()]


__all__ = ["SerialTransport", "list_ports"]
