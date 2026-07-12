"""mqtt integration: the computer side of an MqttCommunication (paho-mqtt).

``MqttCommunication.connect()`` resolves this transport automatically once
the extra is installed (``uv sync --extra mqtt``). Commands are published
to ``<topic>/command``; telemetry arrives on ``<topic>/telemetry`` —
matching the topics used by generated microcontroller firmware.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import paho.mqtt.client as _paho

if TYPE_CHECKING:
    from codetocad.communication import MqttCommunication


class MqttTransport:
    """JSON lines mapped onto MQTT publishes."""

    def __init__(self, communication: "MqttCommunication"):
        self.communication = communication
        self.connected = False
        self._incoming: list[str] = []
        self._client = _paho.Client()
        if communication.username:
            self._client.username_pw_set(
                communication.username, communication.password
            )
        self._client.on_message = self._on_message

    def _on_message(self, client, userdata, message):
        self._incoming.append(message.payload.decode(errors="replace"))

    def connect(self):
        self._client.connect(self.communication.broker, self.communication.port)
        self._client.subscribe(self.communication.telemetry_topic)
        self._client.loop_start()
        self.connected = True

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()
        self.connected = False

    def send_line(self, line: str):
        self._client.publish(self.communication.command_topic, line)

    def read_lines(self) -> list[str]:
        lines = self._incoming[:]
        self._incoming.clear()
        return lines


__all__ = ["MqttTransport"]
