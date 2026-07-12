"""rerun integration: stream microcontroller telemetry to the Rerun viewer.

``RerunApp.run()`` calls ``serve(app)``: it spawns the viewer
(`rerun.io <https://rerun.io>`_, extra ``rerun``), connects the app's
communication channel and logs every telemetry value as a time series
under ``telemetry/<channel>`` (dict values fan out to one series per
key). Blocks until interrupted.
"""

from __future__ import annotations

import time

import rerun as rr

from codetocad.apps import AppBase


def _log_scalar(path: str, value):
    try:
        rr.log(path, rr.Scalars(float(value)))
    except AttributeError:  # rerun < 0.23
        rr.log(path, rr.Scalar(float(value)))


def _log_value(channel: str, value):
    if isinstance(value, dict):
        for key, entry in value.items():
            if isinstance(entry, (int, float)):
                _log_scalar(f"telemetry/{channel}/{key}", entry)
            elif isinstance(entry, (list, tuple)):
                for axis, component in zip("xyzw", entry):
                    _log_scalar(f"telemetry/{channel}/{key}/{axis}", component)
    elif isinstance(value, (int, float)):
        _log_scalar(f"telemetry/{channel}", value)


def serve(
    app: AppBase,
    *,
    application_id: str | None = None,
    spawn: bool = True,
    poll_interval_seconds: float = 0.01,
):
    """Spawn the Rerun viewer and pump telemetry into it (blocks)."""
    rr.init(application_id or app.title, spawn=spawn)
    communication = app._require_communication()

    def on_telemetry(message: dict):
        _log_value(message.get("name", "unknown"), message.get("value"))

    communication.telemetry.subscribe(on_telemetry)
    communication.connect()
    try:
        while True:
            communication.poll()
            time.sleep(poll_interval_seconds)
    except KeyboardInterrupt:
        pass
    finally:
        communication.disconnect()


__all__ = ["serve"]
