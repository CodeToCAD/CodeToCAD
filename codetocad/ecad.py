"""Common electrical components built on the ECAD mixin."""

from __future__ import annotations

from .location import Location
from .materials import MaterialBase, red_material
from .mixins import ECADMixin
from .parts import Part3D
from .primitives import _make_part3d
from .vectors import Vec4


class ElectricalComponent(Part3D, ECADMixin):
    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._init_ecad()


def led(
    color: MaterialBase | None = None,
    forward_voltage: float = 2.0,
    current_limit: float = 0.02,
    start_location: Location | None = None,
) -> ElectricalComponent:
    """A 5mm through-hole LED."""
    part = _make_part3d(
        "cylinder",
        start_location,
        part_class=ElectricalComponent,
        radius=0.0025,
        height=0.0086,
    )
    part.name = "led"
    part.set_material(color or red_material())
    part.set_electrical_properties(
        forward_voltage=forward_voltage, current_limit=current_limit
    )
    return part


def resistor(
    resistance: float,
    power_rating: float = 0.25,
    start_location: Location | None = None,
) -> ElectricalComponent:
    """An axial through-hole resistor. ``resistance`` is in ohms."""
    part = _make_part3d(
        "cylinder",
        start_location,
        part_class=ElectricalComponent,
        radius=0.00125,
        height=0.0063,
    )
    part.name = "resistor"
    part.set_material(
        MaterialBase("resistor_body", color_rgba=Vec4(0.82, 0.71, 0.55, 1.0))
    )
    part.set_electrical_properties(
        resistance=resistance, power_rating=power_rating
    )
    return part


def capacitor(
    capacitance: float,
    voltage_rating: float = 16.0,
    start_location: Location | None = None,
) -> ElectricalComponent:
    """A radial electrolytic capacitor. ``capacitance`` is in farads."""
    part = _make_part3d(
        "cylinder",
        start_location,
        part_class=ElectricalComponent,
        radius=0.0025,
        height=0.007,
    )
    part.name = "capacitor"
    part.set_material(
        MaterialBase("capacitor_body", color_rgba=Vec4(0.1, 0.1, 0.35, 1.0))
    )
    part.set_electrical_properties(
        capacitance=capacitance, voltage_rating=voltage_rating
    )
    return part
