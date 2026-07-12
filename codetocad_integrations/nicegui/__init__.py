"""nicegui integration: serve PythonApp/WebApp control panels.

``app.run()`` calls ``serve(app)`` under the hood, so usually you only
need the extra installed (``uv sync --extra nicegui``; native windows also
need ``pywebview``). Sliders/buttons/toggles send commands over the app's
communication channel; gauges and plots update from telemetry, polled on a
UI timer.
"""

from __future__ import annotations

import time
from collections import deque

from nicegui import ui

from codetocad.apps import AppBase, Control


def _numeric(value):
    """Best-effort scalar from a telemetry value (dicts pick the first
    numeric entry, preferring 'rpm' for encoders)."""
    if isinstance(value, dict):
        if isinstance(value.get("rpm"), (int, float)):
            return value["rpm"]
        for entry in value.values():
            if isinstance(entry, (int, float)):
                return entry
        return None
    return value if isinstance(value, (int, float)) else None


def _control_value(control: Control, latest: dict):
    """The scalar a gauge/plot should show: the control's `key` entry of
    dict telemetry when given, else the best-effort scalar."""
    value = latest.get(control.source_channel)
    key = control.params.get("key")
    if key is not None and isinstance(value, dict):
        value = value.get(key)
    return _numeric(value)


def serve(
    app: AppBase,
    *,
    native: bool = False,
    host: str = "0.0.0.0",
    port: int = 8080,
    poll_interval_seconds: float = 0.05,
    show: bool = True,
):
    """Build a NiceGUI page from ``app.controls`` and run it (blocks).

    The page is passed to NiceGUI as a root function (rebuilt per client),
    so this also works from a background thread — e.g. while a physics
    viewer owns the main thread."""
    latest: dict[str, object] = {}
    communication = app.communication
    if communication is not None:
        communication.telemetry.subscribe(
            lambda message: latest.__setitem__(message.get("name"), message.get("value"))
        )

    def root():
        updaters = []
        with ui.column().classes("w-full max-w-xl mx-auto gap-4"):
            ui.label(app.title).classes("text-2xl")
            for control in app.controls:
                _build_control(app, control, latest, updaters)

        def on_tick():
            if communication is not None:
                communication.poll()
            for update in updaters:
                update()

        ui.timer(poll_interval_seconds, on_tick)

    if communication is not None:

        def on_startup():
            try:
                if not communication.is_connected:
                    communication.connect()
            except Exception as error:  # device offline: keep UI usable
                print(f"codetocad: could not connect: {error}")

        from nicegui import app as nicegui_app

        nicegui_app.on_startup(on_startup)

    ui.run(
        root=root,
        title=app.title,
        native=native,
        host=host,
        port=port,
        reload=False,
        show=show,
    )


def _build_control(app: AppBase, control: Control, latest: dict, updaters: list):
    params = control.params
    if control.kind == "label":
        ui.label(control.label)
    elif control.kind == "slider":
        ui.label(control.label)
        ui.slider(
            min=params["minimum"],
            max=params["maximum"],
            step=params["step"],
            on_change=lambda event, c=control: app.send_control(c, event.value),
        ).props("label-always")
    elif control.kind == "button":
        ui.button(
            control.label,
            on_click=lambda c=control: app.send_control(c, c.params["value"]),
        )
    elif control.kind == "toggle":
        ui.switch(
            control.label,
            on_change=lambda event, c=control: app.send_control(
                c, c.params["on_value"] if event.value else c.params["off_value"]
            ),
        )
    elif control.kind == "gauge":
        label = ui.label(f"{control.label}: —")

        def update_gauge(label=label, control=control):
            value = _control_value(control, latest)
            if value is not None:
                units = control.params.get("units") or ""
                label.text = f"{control.label}: {value:.4g} {units}".rstrip()

        updaters.append(update_gauge)
    elif control.kind == "plot":
        chart = ui.echart(
            {
                "title": {"text": control.label},
                "xAxis": {"type": "value", "name": "s"},
                "yAxis": {"type": "value"},
                "series": [{"type": "line", "showSymbol": False, "data": []}],
                "animation": False,
            }
        ).classes("w-full h-64")
        window = params["window_seconds"]
        points: deque = deque()
        start = time.monotonic()

        def update_plot(chart=chart, points=points, control=control):
            value = _control_value(control, latest)
            now = time.monotonic() - start
            if value is not None:
                points.append((now, value))
            while points and now - points[0][0] > window:
                points.popleft()
            chart.options["series"][0]["data"] = [list(p) for p in points]
            chart.update()

        updaters.append(update_plot)
    else:
        raise ValueError(f"Unknown control kind {control.kind!r}")


__all__ = ["serve"]
