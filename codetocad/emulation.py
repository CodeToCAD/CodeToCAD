"""Emulate a microcontroller in-process — no hardware required.

``EmulatedMicrocontroller`` runs the device side of a ``Microcontroller``
definition the way generated firmware would (command dispatch + periodic
telemetry), but with Python handlers instead of GPIO. Wire the handlers to
a physics simulation and the *same* ``PythonApp``/``WebApp`` code that
talks to real hardware drives the simulated robot::

    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    mcu.bind_sensor(encoder, name="enc", a=32, b=33)

    emulator = EmulatedMicrocontroller(mcu)         # also sets mcu.communication
    emulator.on_command("wheel", lambda value: sim.set_wheel(value))
    emulator.set_sensor("enc", lambda: {"count": sim.count, "rpm": sim.rpm})

    app = WebApp("panel").set_communication(emulator.communication)

    emulator.step(now)   # call from your simulation/update loop

Telemetry and commands travel through an in-memory loopback transport as
JSON lines — the exact wire protocol real firmware speaks — so swapping to
a physical board is just replacing ``emulator.communication`` with a
``SerialCommunication``.
"""

from __future__ import annotations

import json
import time
from collections import deque
from typing import TYPE_CHECKING, Callable

from codetocad.communication import Communication

if TYPE_CHECKING:
    from codetocad.microcontroller import Microcontroller


class EmulatedTransport:
    """In-memory loopback: the computer side implements the standard
    transport interface; the device side is used by
    ``EmulatedMicrocontroller``."""

    def __init__(self):
        self.connected = False
        self._to_device: deque[str] = deque()
        self._to_computer: deque[str] = deque()

    # computer side (Communication transport interface)

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def send_line(self, line: str):
        self._to_device.append(line)

    def read_lines(self) -> list[str]:
        lines = list(self._to_computer)
        self._to_computer.clear()
        return lines

    # device side

    def device_send_line(self, line: str):
        self._to_computer.append(line)

    def device_read_lines(self) -> list[str]:
        lines = list(self._to_device)
        self._to_device.clear()
        return lines


class EmulatedCommunication(Communication):
    """A Communication whose transport is an in-memory loopback."""

    kind = "emulated"

    def __init__(self, transport: EmulatedTransport | None = None):
        super().__init__()
        self.attach_transport(transport or EmulatedTransport())


class _TelemetrySource:
    def __init__(self, read_fn, sample_rate_hz):
        self.read_fn = read_fn
        self.period = 1.0 / sample_rate_hz
        self.next_due = 0.0


class EmulatedMicrocontroller:
    """The device side of ``microcontroller``, emulated in-process.

    Commands sent to an actuator channel invoke the handler registered
    with ``on_command``; sensor channels emit whatever ``set_sensor``'s
    read function returns, at the binding's sample rate. Call ``step()``
    regularly (with simulation time, or wall time by default) to pump
    both directions."""

    def __init__(self, microcontroller: "Microcontroller"):
        self.microcontroller = microcontroller
        self.transport = EmulatedTransport()
        self.communication = EmulatedCommunication(self.transport)
        microcontroller.set_communication(self.communication)
        self._command_handlers: dict[str, Callable] = {}
        self._sensors: dict[str, _TelemetrySource] = {}

    def on_command(self, channel: str, handler: Callable) -> "EmulatedMicrocontroller":
        """Handle commands for a bound actuator channel; ``handler`` gets
        the command value (e.g. ``{"velocity_rpm": 120}``)."""
        binding = self.microcontroller.get_binding(channel)  # KeyError on typo
        if binding.role != "actuator":
            raise ValueError(f"Channel {channel!r} is a sensor; use set_sensor()")
        self._command_handlers[channel] = handler
        return self

    def set_sensor(
        self, channel: str, read_fn: Callable, sample_rate_hz: float | None = None
    ) -> "EmulatedMicrocontroller":
        """Emit ``read_fn()`` as the telemetry for a bound sensor channel,
        at ``sample_rate_hz`` (default: the binding's rate)."""
        binding = self.microcontroller.get_binding(channel)
        if binding.role != "sensor":
            raise ValueError(f"Channel {channel!r} is an actuator; use on_command()")
        rate = sample_rate_hz or binding.sample_rate_hz or 10.0
        self._sensors[channel] = _TelemetrySource(read_fn, rate)
        return self

    def add_telemetry(
        self, name: str, read_fn: Callable, sample_rate_hz: float = 10.0
    ) -> "EmulatedMicrocontroller":
        """Emit extra telemetry on a channel with no binding (e.g. a
        simulated robot's pose for the app to display)."""
        self._sensors[name] = _TelemetrySource(read_fn, sample_rate_hz)
        return self

    def step(self, now: float | None = None) -> None:
        """One firmware loop iteration: dispatch queued commands, then
        emit telemetry that is due at ``now`` (seconds; monotonically
        increasing — simulation time or, if omitted, wall time)."""
        if now is None:
            now = time.monotonic()
        for line in self.transport.device_read_lines():
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if message.get("type") != "command":
                continue
            handler = self._command_handlers.get(message.get("name"))
            if handler is not None:
                handler(message.get("value"))
        for name, source in self._sensors.items():
            if now >= source.next_due:
                source.next_due = now + source.period
                self.transport.device_send_line(
                    json.dumps(
                        {
                            "type": "telemetry",
                            "name": name,
                            "value": source.read_fn(),
                            "t": now,
                        }
                    )
                )

    def run(self, duration_seconds: float, rate_hz: float = 100.0) -> None:
        """Convenience wall-clock loop (for emulations not tied to a
        simulation stepper)."""
        end = time.monotonic() + duration_seconds
        while time.monotonic() < end:
            self.step()
            time.sleep(1.0 / rate_hz)
