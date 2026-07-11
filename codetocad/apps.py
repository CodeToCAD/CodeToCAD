"""Quick control-panel apps for talking to a microcontroller.

A ``PythonApp`` (native window) or ``WebApp`` (browser page) declares
controls — sliders/buttons/toggles that command actuators, gauges/plots
that display sensor telemetry — and shares the *same* ``Communication``
instance as the ``Microcontroller`` it talks to. ``run()`` federates the
declaration to NiceGUI (``codetocad_integrations.nicegui``); a
``RerunApp`` streams telemetry to the Rerun viewer instead
(``codetocad_integrations.rerun``).

Example::

    comm = SerialCommunication("/dev/ttyUSB0")
    mcu.set_communication(comm)

    app = WebApp("motor lab").set_communication(comm)
    app.add_slider("speed", target=motor, command="velocity_rpm",
                   minimum=0, maximum=300)
    app.add_gauge("current (A)", source=current_sensor)
    app.add_plot("encoder rpm", source=encoder)
    app.run()
"""

from __future__ import annotations

from codetocad.communication import Communication, CommunicationMixin


class Control:
    """One UI element bound to a wire-protocol channel.

    ``target``/``source`` may be a bound sensor/actuator part (its channel
    name is taken from the microcontroller binding) or a channel name
    string."""

    def __init__(self, kind: str, label: str, *, target=None, source=None, **params):
        self.kind = kind
        self.label = label
        self.target = target
        self.source = source
        self.params = params

    @staticmethod
    def _channel_of(device_or_name) -> str | None:
        if device_or_name is None:
            return None
        if isinstance(device_or_name, str):
            return device_or_name
        binding = getattr(device_or_name, "_binding", None)
        if binding is None:
            raise ValueError(
                f"{device_or_name!r} is not bound to a microcontroller; bind "
                "it first or pass the channel name as a string"
            )
        return binding.name

    @property
    def target_channel(self) -> str | None:
        return self._channel_of(self.target)

    @property
    def source_channel(self) -> str | None:
        return self._channel_of(self.source)

    def __repr__(self):
        return f"Control({self.kind!r}, {self.label!r})"


class AppBase(CommunicationMixin):
    """Declarative control panel. Subclasses choose the federation
    (NiceGUI native window, NiceGUI web page, Rerun viewer)."""

    def __init__(self, title: str = "CodeToCAD", communication: Communication | None = None):
        self.title = title
        self._init_communication(communication)
        self.controls: list[Control] = []

    def _add(self, control: Control) -> Control:
        self.controls.append(control)
        return control

    # -- actuator controls --

    def add_slider(
        self,
        label: str,
        target,
        *,
        minimum: float = 0.0,
        maximum: float = 100.0,
        step: float = 1.0,
        command: str | None = None,
    ) -> Control:
        """A slider that sends its value to ``target``'s channel. With
        ``command=`` the value is wrapped as ``{command: value}`` (e.g.
        ``command="velocity_rpm"`` for motors)."""
        return self._add(
            Control(
                "slider",
                label,
                target=target,
                minimum=minimum,
                maximum=maximum,
                step=step,
                command=command,
            )
        )

    def add_button(self, label: str, target, *, value=1, command: str | None = None) -> Control:
        """A button that sends ``value`` (or ``{command: value}``) when
        clicked."""
        return self._add(Control("button", label, target=target, value=value, command=command))

    def add_toggle(
        self, label: str, target, *, on_value=1, off_value=0, command: str | None = None
    ) -> Control:
        return self._add(
            Control(
                "toggle",
                label,
                target=target,
                on_value=on_value,
                off_value=off_value,
                command=command,
            )
        )

    # -- sensor displays --

    def add_gauge(
        self,
        label: str,
        source,
        *,
        minimum: float = 0.0,
        maximum: float = 100.0,
        units: str | None = None,
    ) -> Control:
        """A live numeric readout of ``source``'s telemetry."""
        return self._add(
            Control("gauge", label, source=source, minimum=minimum, maximum=maximum, units=units)
        )

    def add_plot(self, label: str, source, *, window_seconds: float = 30.0) -> Control:
        """A scrolling time-series plot of ``source``'s telemetry."""
        return self._add(Control("plot", label, source=source, window_seconds=window_seconds))

    def add_label(self, text: str) -> Control:
        return self._add(Control("label", text))

    # -- runtime --

    def send_control(self, control: Control, value):
        """Send a control's command over the shared communication channel
        (integrations call this from UI event handlers)."""
        channel = control.target_channel
        if channel is None:
            raise ValueError(f"{control!r} has no target channel")
        command = control.params.get("command")
        payload = {command: value} if command else value
        self._require_communication().send_command(channel, payload)

    def run(self, **options):
        raise NotImplementedError


class PythonApp(AppBase):
    """A native desktop window (NiceGUI in native mode)."""

    def run(self, **options):
        from codetocad_integrations.nicegui import serve

        return serve(self, native=True, **options)


class WebApp(AppBase):
    """A browser control panel (NiceGUI web server)."""

    def run(self, host: str = "0.0.0.0", port: int = 8080, **options):
        from codetocad_integrations.nicegui import serve

        return serve(self, native=False, host=host, port=port, **options)


class RerunApp(AppBase):
    """Streams telemetry to the Rerun viewer (rerun.io); gauges and plots
    become time series, actuator controls are not supported."""

    def run(self, **options):
        from codetocad_integrations.rerun import serve

        return serve(self, **options)
