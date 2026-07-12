"""Communication channels between a computer and a microcontroller.

A ``Communication`` describes *how* to reach a device (serial port, wifi
host, MQTT broker, ...). The same instance is shared by the
``Microcontroller`` definition and the ``PythonApp``/``WebApp``/``RerunApp``
that talks to it, so both ends agree on the medium.

Messages are dicts spoken as JSON lines (the "codetocad wire protocol"):

- telemetry, device -> computer: ``{"type": "telemetry", "name": <channel>,
  "value": <number|list>, "t": <seconds>}``
- commands, computer -> device: ``{"type": "command", "name": <channel>,
  "value": <number|str|dict>}``

The classes here are declarative; actual I/O is done by a *transport*
attached by an integration (``codetocad_integrations.pyserial``,
``codetocad_integrations.mqtt``, or the built-in TCP transport for wifi).
``connect()`` resolves the default transport for the channel kind.
"""

from __future__ import annotations

import json
import socket
import time
from typing import Callable


class EventStream:
    """A minimal reactive (Rx-style) event stream.

    ``subscribe`` registers an observer and returns an unsubscribe
    callable; ``map``/``filter``/``throttle`` derive new streams. Streaming
    filters from ``codetocad.signals`` are callables, so
    ``stream.map(LowPassFilter(alpha=0.2))`` smooths a sensor stream."""

    def __init__(self):
        self._observers: list[Callable] = []
        self.last_value = None

    def subscribe(self, on_next: Callable) -> Callable[[], None]:
        self._observers.append(on_next)

        def unsubscribe():
            if on_next in self._observers:
                self._observers.remove(on_next)

        return unsubscribe

    def emit(self, value):
        self.last_value = value
        for observer in list(self._observers):
            observer(value)

    def map(self, fn: Callable) -> "EventStream":
        derived = EventStream()
        self.subscribe(lambda value: derived.emit(fn(value)))
        return derived

    def filter(self, predicate: Callable) -> "EventStream":
        derived = EventStream()
        self.subscribe(lambda value: derived.emit(value) if predicate(value) else None)
        return derived

    def throttle(self, min_interval_seconds: float) -> "EventStream":
        derived = EventStream()
        last_emit = [0.0]

        def on_next(value):
            now = time.monotonic()
            if now - last_emit[0] >= min_interval_seconds:
                last_emit[0] = now
                derived.emit(value)

        self.subscribe(on_next)
        return derived


class Communication:
    """Base communication channel. Subclasses declare the medium; a
    transport (attached by an integration or resolved by ``connect``)
    performs the I/O."""

    kind = "base"

    def __init__(self):
        self._transport = None
        self.events = EventStream()
        """Stream of every message received (dicts)."""
        self.telemetry = self.events.filter(
            lambda message: message.get("type") == "telemetry"
        )
        """Stream of telemetry messages only."""

    # -- transport --

    def attach_transport(self, transport):
        """Attach a transport: any object with ``connect()``,
        ``disconnect()``, ``send_line(str)`` and ``read_lines() -> list[str]``."""
        self._transport = transport
        return self

    def _resolve_transport(self):
        raise NotImplementedError(
            f"No transport is available for {type(self).__name__}; attach one "
            "with attach_transport() or install the matching integration"
        )

    @property
    def is_connected(self) -> bool:
        return self._transport is not None and getattr(
            self._transport, "connected", False
        )

    def connect(self):
        if self._transport is None:
            self._transport = self._resolve_transport()
        self._transport.connect()
        return self

    def disconnect(self):
        if self._transport is not None:
            self._transport.disconnect()
        return self

    # -- messages --

    def send(self, message: dict):
        if self._transport is None:
            raise RuntimeError("Not connected; call connect() first")
        self._transport.send_line(json.dumps(message))

    def send_command(self, name: str, value):
        self.send({"type": "command", "name": name, "value": value})

    def poll(self) -> list[dict]:
        """Read pending messages, emit them on ``events`` and return them.
        Apps and integrations call this in their update loop."""
        if self._transport is None:
            return []
        messages = []
        for line in self._transport.read_lines():
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                message = {"type": "raw", "value": line}
            messages.append(message)
            self.events.emit(message)
        return messages

    def receive(self, timeout_seconds: float = 1.0) -> dict | None:
        """Block until one message arrives (or timeout); returns it."""
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            messages = self.poll()
            if messages:
                return messages[0]
            time.sleep(0.005)
        return None


class SerialCommunication(Communication):
    """USB/UART serial link. Requires the pyserial integration
    (``codetocad_integrations.pyserial``, extra ``pyserial``)."""

    kind = "serial"

    def __init__(self, port: str, baud_rate: int = 115200):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate

    def _resolve_transport(self):
        try:
            from codetocad_integrations.pyserial import SerialTransport
        except ImportError as error:
            raise ImportError(
                "SerialCommunication needs pyserial: uv sync --extra pyserial"
            ) from error
        return SerialTransport(self.port, self.baud_rate)

    def __repr__(self):
        return f"SerialCommunication({self.port!r}, baud_rate={self.baud_rate})"


class WifiCommunication(Communication):
    """TCP socket link over wifi. ``ssid``/``password`` are used when
    generating microcontroller firmware (the device joins the network and
    serves ``port``); the computer side connects with the stdlib socket
    transport, no extra dependency."""

    kind = "wifi"

    def __init__(
        self,
        host: str,
        port: int = 8266,
        ssid: str | None = None,
        password: str | None = None,
    ):
        super().__init__()
        self.host = host
        self.port = port
        self.ssid = ssid
        self.password = password

    def _resolve_transport(self):
        return TcpTransport(self.host, self.port)

    def __repr__(self):
        return f"WifiCommunication({self.host!r}, port={self.port})"


class BluetoothCommunication(SerialCommunication):
    """Bluetooth Classic SPP link. Pairing exposes the device as a serial
    port (``/dev/tty.*`` on macOS, ``COMx`` on Windows, ``/dev/rfcomm*`` on
    Linux), so this behaves as a SerialCommunication on that port."""

    kind = "bluetooth"

    def __repr__(self):
        return f"BluetoothCommunication({self.port!r}, baud_rate={self.baud_rate})"


class MqttCommunication(Communication):
    """MQTT pub/sub link. Commands are published to
    ``<topic>/command`` and telemetry is received from ``<topic>/telemetry``.
    Requires the mqtt integration (extra ``mqtt``); microcontrollers use
    ``umqtt.simple`` in generated firmware."""

    kind = "mqtt"

    def __init__(
        self,
        broker: str,
        port: int = 1883,
        topic: str = "codetocad",
        username: str | None = None,
        password: str | None = None,
    ):
        super().__init__()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password

    @property
    def command_topic(self) -> str:
        return f"{self.topic}/command"

    @property
    def telemetry_topic(self) -> str:
        return f"{self.topic}/telemetry"

    def _resolve_transport(self):
        try:
            from codetocad_integrations.mqtt import MqttTransport
        except ImportError as error:
            raise ImportError(
                "MqttCommunication needs paho-mqtt: uv sync --extra mqtt"
            ) from error
        return MqttTransport(self)

    def __repr__(self):
        return f"MqttCommunication({self.broker!r}, topic={self.topic!r})"


class TcpTransport:
    """JSON-lines over a TCP socket (stdlib; used by WifiCommunication)."""

    def __init__(self, host: str, port: int, timeout_seconds: float = 5.0):
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds
        self.connected = False
        self._socket: socket.socket | None = None
        self._buffer = b""

    def connect(self):
        self._socket = socket.create_connection(
            (self.host, self.port), timeout=self.timeout_seconds
        )
        self._socket.setblocking(False)
        self.connected = True

    def disconnect(self):
        if self._socket is not None:
            self._socket.close()
            self._socket = None
        self.connected = False

    def send_line(self, line: str):
        if self._socket is None:
            raise RuntimeError("TcpTransport is not connected")
        self._socket.sendall(line.encode() + b"\n")

    def read_lines(self) -> list[str]:
        if self._socket is None:
            return []
        try:
            while True:
                chunk = self._socket.recv(4096)
                if not chunk:
                    break
                self._buffer += chunk
        except (BlockingIOError, TimeoutError):
            pass
        lines = self._buffer.split(b"\n")
        self._buffer = lines.pop()
        return [line.decode(errors="replace") for line in lines]


class CommunicationMixin:
    """Adds a shared ``communication`` channel to a class (Microcontroller,
    PythonApp, WebApp, ...)."""

    def _init_communication(self, communication: Communication | None = None):
        self.communication: Communication | None = communication

    def set_communication(self, communication: Communication):
        self.communication = communication
        return self

    def _require_communication(self) -> Communication:
        if self.communication is None:
            raise RuntimeError(
                f"{type(self).__name__} has no communication channel; call "
                "set_communication() with a SerialCommunication, "
                "WifiCommunication, BluetoothCommunication or MqttCommunication"
            )
        return self.communication

    def connect(self):
        self._require_communication().connect()
        return self

    def disconnect(self):
        if self.communication is not None:
            self.communication.disconnect()
        return self

    def send_command(self, name: str, value):
        self._require_communication().send_command(name, value)
        return self

    def on_message(self, on_next: Callable) -> Callable[[], None]:
        """Subscribe to every incoming message; returns an unsubscribe
        callable."""
        return self._require_communication().events.subscribe(on_next)

    def on_telemetry(self, on_next: Callable) -> Callable[[], None]:
        """Subscribe to telemetry messages; returns an unsubscribe callable."""
        return self._require_communication().telemetry.subscribe(on_next)
