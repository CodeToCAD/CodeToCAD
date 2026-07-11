"""Schematic-level ECAD built on the ECAD mixin.

``ElectricalComponent`` is a Part3D with electrical properties, schematic
``Pin``s and a ``Footprint``, so one definition drives the schematic (via
``codetocad_integrations.skidl``), circuit simulation (via
``codetocad_integrations.spice``) and the physical board assembly (the
component's 3D body comes from its footprint). A ``Circuit`` collects
components and the ``Net``s connecting their pins.
"""

from __future__ import annotations

import re
from enum import Enum

from codetocad.location import Location
from codetocad.materials import MaterialBase, red_material
from codetocad.mixins import ECADMixin
from codetocad.parts import Part2D, Part3D
from codetocad.primitives import _make_part2d, _make_part3d
from codetocad.units import LengthMeters, LengthWithUnit
from codetocad.vectors import Vec4


# -- SPICE-style SI values --

_SI_MULTIPLIERS = {
    "t": 1e12,
    "g": 1e9,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "µ": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
}

_SI_FORMAT = {12: "t", 9: "g", 6: "meg", 3: "k", 0: "", -3: "m", -6: "u", -9: "n", -12: "p", -15: "f"}


def parse_si(value: float | str) -> float:
    """Parse a number with a SPICE-style SI suffix: ``"10k"``, ``"100n"``,
    ``"2.2meg"``. Following SPICE, suffixes are case-insensitive, ``m`` is
    milli and ``meg`` is mega; letters after the suffix (units such as
    ``"10kohm"`` or ``"100nF"``) are ignored."""
    if isinstance(value, (int, float)):
        return float(value)
    match = re.fullmatch(r"\s*([-+]?[0-9.]+(?:[eE][-+]?[0-9]+)?)\s*([a-zA-Zµ]*)\s*", value)
    if not match:
        raise ValueError(f"Cannot parse {value!r} as a number with an SI suffix")
    number, suffix = float(match.group(1)), match.group(2).lower()
    if suffix.startswith("meg"):
        return number * 1e6
    if suffix and suffix[0] in _SI_MULTIPLIERS:
        return number * _SI_MULTIPLIERS[suffix[0]]
    return number


def format_si(value: float) -> str:
    """Format a number with a SPICE-style SI suffix (10000 -> ``"10k"``)."""
    if value == 0:
        return "0"
    magnitude = abs(value)
    for exponent in (12, 9, 6, 3, 0, -3, -6, -9, -12, -15):
        if magnitude >= 10.0**exponent:
            scaled = value / 10.0**exponent
            return f"{scaled:.4g}{_SI_FORMAT[exponent]}"
    return f"{value:.4g}"


# -- enums --


class PinType(Enum):
    """Electrical role of a pin, used for ERC and schematic rendering."""

    PASSIVE = "passive"
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    POWER_IN = "power_in"
    POWER_OUT = "power_out"
    NO_CONNECT = "no_connect"


class ComponentType(Enum):
    """Schematic component categories.

    ``ref_prefix`` seeds reference designators (R1, C2, ...);
    ``spice_prefix`` is the SPICE element letter (None for components with
    no SPICE primitive)."""

    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    DIODE = "diode"
    LED = "led"
    TRANSISTOR_NPN = "transistor_npn"
    TRANSISTOR_PNP = "transistor_pnp"
    VOLTAGE_SOURCE = "voltage_source"
    CURRENT_SOURCE = "current_source"
    IC = "ic"
    CONNECTOR = "connector"
    GENERIC = "generic"

    @property
    def ref_prefix(self) -> str:
        return _REF_PREFIXES[self]

    @property
    def spice_prefix(self) -> str | None:
        return _SPICE_PREFIXES.get(self)


_REF_PREFIXES = {
    ComponentType.RESISTOR: "R",
    ComponentType.CAPACITOR: "C",
    ComponentType.INDUCTOR: "L",
    ComponentType.DIODE: "D",
    ComponentType.LED: "D",
    ComponentType.TRANSISTOR_NPN: "Q",
    ComponentType.TRANSISTOR_PNP: "Q",
    ComponentType.VOLTAGE_SOURCE: "V",
    ComponentType.CURRENT_SOURCE: "I",
    ComponentType.IC: "U",
    ComponentType.CONNECTOR: "J",
    ComponentType.GENERIC: "U",
}

_SPICE_PREFIXES = {
    ComponentType.RESISTOR: "R",
    ComponentType.CAPACITOR: "C",
    ComponentType.INDUCTOR: "L",
    ComponentType.DIODE: "D",
    ComponentType.LED: "D",
    ComponentType.TRANSISTOR_NPN: "Q",
    ComponentType.TRANSISTOR_PNP: "Q",
    ComponentType.VOLTAGE_SOURCE: "V",
    ComponentType.CURRENT_SOURCE: "I",
    ComponentType.IC: "X",
}


# -- connectivity --


class Pin:
    """A component terminal. Join pins into Nets with ``Circuit.connect``."""

    def __init__(
        self,
        name: str,
        number: str | int,
        component: "ElectricalComponent | None" = None,
        pin_type: PinType = PinType.PASSIVE,
    ):
        self.name = str(name)
        self.number = str(number)
        self.component = component
        self.pin_type = pin_type
        self.net: Net | None = None

    def __repr__(self):
        owner = "?"
        if self.component is not None:
            owner = self.component.reference or self.component.name or "?"
        return f"Pin({owner}.{self.name})"


_GROUND_NAMES = {"GND", "AGND", "DGND", "VSS", "0"}


class Net:
    """An electrical connection between pins. Create and join nets through
    a ``Circuit`` (``circuit.net()``, ``circuit.gnd``, ``circuit.connect``)."""

    def __init__(self, name: str | None = None):
        self.name = name
        self.pins: list[Pin] = []
        self._auto_named = name is None

    @property
    def is_ground(self) -> bool:
        return (self.name or "").upper() in _GROUND_NAMES

    @property
    def is_power(self) -> bool:
        name = (self.name or "").upper()
        return name in ("VCC", "VDD") or bool(re.fullmatch(r"\+\d+V\d*", name))

    def __repr__(self):
        return f"Net({self.name!r}, pins={self.pins})"


class Circuit:
    """A schematic: components plus the nets connecting their pins.

    Federate it with ``codetocad_integrations.skidl`` (ERC, KiCad netlists,
    schematic SVGs) or ``codetocad_integrations.spice`` (ngspice
    simulation). Components are Part3Ds, so the same circuit's parts can be
    placed into a board assembly."""

    def __init__(self, name: str = "circuit", description: str | None = None):
        self.name = name
        self.description = description
        self.components: list[ElectricalComponent] = []
        self.nets: list[Net] = []

    # -- components --

    def add(self, *components: "ElectricalComponent"):
        """Add components, assigning reference designators (R1, C1, ...)
        from their ``component_type``. Returns the single component, or a
        tuple when several are given."""
        for component in components:
            if component in self.components:
                continue
            if not component.reference:
                component.reference = self._next_reference(
                    component.component_type.ref_prefix
                )
            self.components.append(component)
        return components[0] if len(components) == 1 else components

    def _next_reference(self, prefix: str) -> str:
        existing = {c.reference for c in self.components}
        number = 1
        while f"{prefix}{number}" in existing:
            number += 1
        return f"{prefix}{number}"

    def get_component(self, reference: str) -> "ElectricalComponent":
        for component in self.components:
            if component.reference == reference:
                return component
        raise KeyError(f"No component {reference!r} in circuit {self.name!r}")

    # -- nets --

    def net(self, name: str | None = None) -> Net:
        """Get or create a named net; with no name, create a new
        auto-named net (N1, N2, ...)."""
        if name is not None:
            for net in self.nets:
                if net.name == name:
                    return net
        net = Net(name)
        if name is None:
            names = {n.name for n in self.nets}
            number = 1
            while f"N{number}" in names:
                number += 1
            net.name = f"N{number}"
        self.nets.append(net)
        return net

    @property
    def gnd(self) -> Net:
        """The ground net (named ``GND``; SPICE node 0)."""
        return self.net("GND")

    def get_net(self, name: str) -> Net:
        for net in self.nets:
            if net.name == name:
                return net
        raise KeyError(f"No net {name!r} in circuit {self.name!r}")

    def connect(self, *terminals: "Pin | Net", name: str | None = None) -> Net:
        """Connect pins (and/or existing nets) together into one net.

        Components involved are added to the circuit automatically. Give
        ``name=`` to label the resulting net (e.g. "VOUT")."""
        if not terminals:
            raise ValueError("connect() needs at least one Pin or Net")
        target = self.net(name) if name is not None else None
        for terminal in terminals:
            if isinstance(terminal, Net):
                if terminal not in self.nets:
                    self.nets.append(terminal)
                target = self._merge(target, terminal) if target else terminal
            elif isinstance(terminal, Pin):
                if terminal.component is not None:
                    self.add(terminal.component)
                if terminal.net is not None:
                    target = (
                        self._merge(target, terminal.net) if target else terminal.net
                    )
            else:
                raise TypeError(
                    f"connect() accepts Pin or Net, got {type(terminal).__name__}"
                    " (use component.get_pin(...) / component[...])"
                )
        if target is None:
            target = self.net(None)
        for terminal in terminals:
            if isinstance(terminal, Pin) and terminal.net is None:
                terminal.net = target
                target.pins.append(terminal)
        return target

    def _merge(self, keep: Net, other: Net) -> Net:
        if other is keep:
            return keep
        if keep._auto_named and not other._auto_named:
            keep, other = other, keep
        for pin in other.pins:
            pin.net = keep
            keep.pins.append(pin)
        other.pins = []
        if other in self.nets:
            self.nets.remove(other)
        return keep

    # -- checks --

    def unconnected_pins(self) -> list[Pin]:
        return [
            pin
            for component in self.components
            for pin in component.pins
            if pin.net is None and pin.pin_type is not PinType.NO_CONNECT
        ]

    def validate(self) -> list[str]:
        """Basic electrical checks; returns a list of warning messages."""
        warnings = [f"{pin!r} is not connected" for pin in self.unconnected_pins()]
        for net in self.nets:
            if len(net.pins) == 1:
                warnings.append(f"Net {net.name!r} has only one pin")
        if self.components and not any(net.is_ground for net in self.nets):
            warnings.append("Circuit has no ground net (circuit.gnd)")
        return warnings

    def __repr__(self):
        return (
            f"Circuit({self.name!r}, components={len(self.components)}, "
            f"nets={len(self.nets)})"
        )


# -- footprints --


class Footprint:
    """A component's physical package. ``library_id`` names the ECAD
    library footprint (KiCad ``Library:Footprint`` convention, exported in
    netlists) and the body dimensions define a placeholder 3D body so the
    component can be placed in Part3D assemblies."""

    def __init__(
        self,
        library_id: str,
        *,
        body: str = "box",
        length: LengthWithUnit | None = None,
        width: LengthWithUnit | None = None,
        height: LengthWithUnit | None = None,
        radius: LengthWithUnit | None = None,
    ):
        if body not in ("box", "cylinder"):
            raise ValueError(f"Unknown footprint body {body!r}")
        self.library_id = library_id
        self.body = body
        as_meters = lambda v: LengthMeters(v).value if v is not None else None
        self.length = as_meters(length)
        self.width = as_meters(width)
        self.height = as_meters(height)
        self.radius = as_meters(radius)

    def make_component(
        self,
        start_location: Location | None = None,
        part_class: type["ElectricalComponent"] | None = None,
    ) -> "ElectricalComponent":
        """Create an ElectricalComponent whose 3D body is this footprint."""
        part_class = part_class or ElectricalComponent
        part = self._make_body(_make_part3d, part_class, start_location)
        part.footprint = self
        return part

    def to_part3d(self, start_location: Location | None = None) -> Part3D:
        """The footprint's placeholder body as a plain Part3D."""
        return self._make_body(_make_part3d, Part3D, start_location)

    def to_part2d(self, start_location: Location | None = None) -> Part2D:
        """The footprint's outline (courtyard) as a Part2D sketch."""
        if self.body == "cylinder":
            return _make_part2d("circle", start_location, radius=self.radius)
        return _make_part2d(
            "rectangle", start_location, width=self.length, height=self.width
        )

    def _make_body(self, maker, part_class, start_location):
        if self.body == "cylinder":
            return maker(
                "cylinder",
                start_location,
                part_class=part_class,
                radius=self.radius,
                height=self.height,
            )
        return maker(
            "cube",
            start_location,
            part_class=part_class,
            length=self.length,
            width=self.width,
            height=self.height,
        )

    def __repr__(self):
        return f"Footprint({self.library_id!r})"


class CommonFootprints(Enum):
    """Common footprints with placeholder body sizes. Call ``.footprint()``
    to get a fresh ``Footprint`` instance."""

    axial_resistor = (
        "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
        "cylinder",
        {"radius": 0.00125, "height": 0.0063},
    )
    radial_capacitor = (
        "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
        "cylinder",
        {"radius": 0.0025, "height": 0.007},
    )
    led_5mm = ("LED_THT:LED_D5.0mm", "cylinder", {"radius": 0.0025, "height": 0.0086})
    axial_inductor = (
        "Inductor_THT:L_Axial_L5.3mm_D2.2mm_P10.16mm_Horizontal",
        "cylinder",
        {"radius": 0.0011, "height": 0.0053},
    )
    diode_do41 = (
        "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",
        "cylinder",
        {"radius": 0.00135, "height": 0.0052},
    )
    battery_aa = (
        "Battery:BatteryHolder_Keystone_2466_1xAA",
        "box",
        {"length": 0.0577, "width": 0.0167, "height": 0.0155},
    )
    chip_0805 = (
        "Resistor_SMD:R_0805_2012Metric",
        "box",
        {"length": 0.002, "width": 0.00125, "height": 0.0006},
    )

    def footprint(self) -> Footprint:
        library_id, body, dimensions = self.value
        return Footprint(library_id, body=body, **dimensions)


# -- components --


class ElectricalComponent(Part3D, ECADMixin):
    """A Part3D with electrical properties, schematic pins and a footprint.

    Look pins up by name or number with ``component["A"]`` /
    ``component[1]``."""

    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._init_ecad()
        self.component_type = ComponentType.GENERIC
        self.value: str | None = None
        """Display/netlist value, e.g. ``"10k"``."""
        self.reference: str | None = None
        """Reference designator (R1, C2, ...), assigned by ``Circuit.add``."""
        self.footprint: Footprint | None = None
        self.spice_model: str | None = None
        """A full SPICE ``.model``/``.subckt`` card for this component, used
        verbatim by the spice integration instead of a generated model."""
        self.dc: float | None = None
        """DC value for sources (volts or amps)."""
        self.ac: float | None = None
        """AC small-signal magnitude for sources."""
        self.waveform: str | None = None
        """SPICE transient waveform for sources, e.g.
        ``"PULSE(0 5 0 1u 1u 1m 2m)"`` or ``"SIN(0 1 1k)"``."""
        self.pins: list[Pin] = []

    def add_pin(
        self,
        name: str,
        number: str | int | None = None,
        pin_type: PinType = PinType.PASSIVE,
    ) -> Pin:
        pin = Pin(
            name,
            number if number is not None else len(self.pins) + 1,
            component=self,
            pin_type=pin_type,
        )
        self.pins.append(pin)
        return pin

    def get_pin(self, key: str | int) -> Pin:
        """Look a pin up by number or (case-insensitive) name."""
        wanted = str(key)
        for pin in self.pins:
            if pin.number == wanted or pin.name.upper() == wanted.upper():
                return pin
        raise KeyError(
            f"{self.reference or self.name or 'component'} has no pin {key!r}; "
            f"pins are {[p.name for p in self.pins]}"
        )

    def __getitem__(self, key: str | int) -> Pin:
        return self.get_pin(key)


def _setup(
    part: ElectricalComponent,
    name: str,
    component_type: ComponentType,
    value: str | None,
    material: MaterialBase | None,
    pin_specs: list[tuple[str, PinType]],
) -> ElectricalComponent:
    part.name = name
    part.component_type = component_type
    part.value = value
    if material is not None:
        part.set_material(material)
    for pin_name, pin_type in pin_specs:
        part.add_pin(pin_name, pin_type=pin_type)
    return part


_PASSIVE_PINS = [("1", PinType.PASSIVE), ("2", PinType.PASSIVE)]
_DIODE_PINS = [("A", PinType.PASSIVE), ("K", PinType.PASSIVE)]
_SOURCE_PINS = [("+", PinType.POWER_OUT), ("-", PinType.POWER_OUT)]


def led(
    color: MaterialBase | None = None,
    forward_voltage: float = 2.0,
    current_limit: float = 0.02,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """A 5mm through-hole LED. Pins: ``A`` (anode), ``K`` (cathode)."""
    footprint = footprint or CommonFootprints.led_5mm.footprint()
    part = footprint.make_component(start_location)
    _setup(
        part,
        "led",
        ComponentType.LED,
        f"{forward_voltage:g}V",
        color or red_material(),
        _DIODE_PINS,
    )
    part.set_electrical_properties(
        forward_voltage=forward_voltage, current_limit=current_limit
    )
    return part


def diode(
    forward_voltage: float = 0.7,
    current_limit: float = 1.0,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """A rectifier diode (DO-41). Pins: ``A`` (anode), ``K`` (cathode)."""
    footprint = footprint or CommonFootprints.diode_do41.footprint()
    part = footprint.make_component(start_location)
    _setup(
        part,
        "diode",
        ComponentType.DIODE,
        f"{forward_voltage:g}V",
        MaterialBase("diode_body", color_rgba=Vec4(0.1, 0.1, 0.1, 1.0)),
        _DIODE_PINS,
    )
    part.set_electrical_properties(
        forward_voltage=forward_voltage, current_limit=current_limit
    )
    return part


def resistor(
    resistance: float | str,
    power_rating: float = 0.25,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """An axial through-hole resistor. ``resistance`` is in ohms (or a
    SPICE-style value such as ``"10k"``)."""
    resistance = parse_si(resistance)
    footprint = footprint or CommonFootprints.axial_resistor.footprint()
    part = footprint.make_component(start_location)
    _setup(
        part,
        "resistor",
        ComponentType.RESISTOR,
        format_si(resistance),
        MaterialBase("resistor_body", color_rgba=Vec4(0.82, 0.71, 0.55, 1.0)),
        _PASSIVE_PINS,
    )
    part.set_electrical_properties(resistance=resistance, power_rating=power_rating)
    return part


def capacitor(
    capacitance: float | str,
    voltage_rating: float = 16.0,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """A radial electrolytic capacitor. ``capacitance`` is in farads (or a
    SPICE-style value such as ``"100n"``)."""
    capacitance = parse_si(capacitance)
    footprint = footprint or CommonFootprints.radial_capacitor.footprint()
    part = footprint.make_component(start_location)
    _setup(
        part,
        "capacitor",
        ComponentType.CAPACITOR,
        format_si(capacitance),
        MaterialBase("capacitor_body", color_rgba=Vec4(0.1, 0.1, 0.35, 1.0)),
        _PASSIVE_PINS,
    )
    part.set_electrical_properties(
        capacitance=capacitance, voltage_rating=voltage_rating
    )
    return part


def inductor(
    inductance: float | str,
    current_limit: float | None = None,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """An axial inductor. ``inductance`` is in henries (or a SPICE-style
    value such as ``"10m"``)."""
    inductance = parse_si(inductance)
    footprint = footprint or CommonFootprints.axial_inductor.footprint()
    part = footprint.make_component(start_location)
    _setup(
        part,
        "inductor",
        ComponentType.INDUCTOR,
        format_si(inductance),
        MaterialBase("inductor_body", color_rgba=Vec4(0.25, 0.35, 0.2, 1.0)),
        _PASSIVE_PINS,
    )
    part.set_electrical_properties(inductance=inductance, current_limit=current_limit)
    return part


def voltage_source(
    dc: float | None = None,
    ac: float | None = None,
    waveform: str | None = None,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """An ideal voltage source (modeled physically as a battery holder).
    Pins: ``+``, ``-``. ``waveform`` is a SPICE transient spec such as
    ``"PULSE(0 5 0 1u 1u 1m 2m)"`` or ``"SIN(0 1 1k)"``."""
    footprint = footprint or CommonFootprints.battery_aa.footprint()
    part = footprint.make_component(start_location)
    if dc is not None:
        value = f"{format_si(dc)}V"
    elif waveform is not None:
        value = waveform.split("(")[0].strip() or "V"
    else:
        value = "V"
    _setup(
        part,
        "voltage_source",
        ComponentType.VOLTAGE_SOURCE,
        value,
        MaterialBase("source_body", color_rgba=Vec4(0.2, 0.2, 0.2, 1.0)),
        _SOURCE_PINS,
    )
    part.dc, part.ac, part.waveform = dc, ac, waveform
    if dc is not None:
        part.set_electrical_properties(voltage_rating=abs(dc))
    return part


def current_source(
    dc: float | None = None,
    ac: float | None = None,
    waveform: str | None = None,
    start_location: Location | None = None,
    footprint: Footprint | None = None,
) -> ElectricalComponent:
    """An ideal current source. Pins: ``+``, ``-`` (current flows from
    ``+`` to ``-`` through the source, per SPICE convention)."""
    footprint = footprint or CommonFootprints.battery_aa.footprint()
    part = footprint.make_component(start_location)
    value = f"{format_si(dc)}A" if dc is not None else "I"
    _setup(
        part,
        "current_source",
        ComponentType.CURRENT_SOURCE,
        value,
        MaterialBase("source_body", color_rgba=Vec4(0.2, 0.2, 0.2, 1.0)),
        _SOURCE_PINS,
    )
    part.dc, part.ac, part.waveform = dc, ac, waveform
    if dc is not None:
        part.set_electrical_properties(current_limit=abs(dc))
    return part
