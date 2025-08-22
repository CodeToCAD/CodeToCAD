"""
Resistor component presets for PCB design.

This module provides preset definitions for common resistor types
including SMD and through-hole variants with standard footprints.
"""

from typing import TYPE_CHECKING
from dataclasses import dataclass
from codetocad.interfaces.cad.pcb.pcb_component_interface import (
    ComponentType,
    MountType,
    PinDefinition,
    FootprintDefinition,
    ElectricalProperties,
)

if TYPE_CHECKING:
    from ..pcb_component_interface import PCBComponentInterface


@dataclass
class ResistorSpecs:
    """Specifications for resistor components."""

    value: str  # e.g., "10k", "4.7k", "100"
    tolerance: str = "5%"  # e.g., "1%", "5%", "10%"
    power_rating: str = "0.25W"  # e.g., "0.125W", "0.25W", "0.5W"
    temperature_coefficient: str = "±100ppm/°C"
    package: str = "0603"  # SMD package or "THT" for through-hole
    voltage_rating: str = "50V"


class ResistorPresets:
    """
    Preset definitions for resistor components.

    Provides common resistor values and packages for both SMD and through-hole types.
    """

    def __init__(self):
        pass

    def _create_smd_footprint(self, package: str) -> FootprintDefinition:
        """Create SMD resistor footprint based on package size."""
        # Standard SMD resistor dimensions (length x width in mm)
        dimensions = {
            "0201": (0.6, 0.3, 0.13),  # L x W x H
            "0402": (1.0, 0.5, 0.35),
            "0603": (1.6, 0.8, 0.45),
            "0805": (2.0, 1.25, 0.6),
            "1206": (3.2, 1.6, 0.65),
            "1210": (3.2, 2.5, 0.65),
            "2010": (5.0, 2.5, 0.65),
            "2512": (6.4, 3.2, 0.65),
        }

        if package not in dimensions:
            raise ValueError(f"Unknown SMD resistor package: {package}")

        length, width, height = dimensions[package]

        # Standard pad dimensions (typically 60% of component length)
        pad_length = length * 0.6
        pad_width = width
        pad_spacing = length + 0.2  # Add some spacing

        pins = [
            PinDefinition(
                number="1",
                name="A",
                x=-pad_spacing / 2,
                y=0,
                drill_diameter=0.0,  # SMD
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
            PinDefinition(
                number="2",
                name="B",
                x=pad_spacing / 2,
                y=0,
                drill_diameter=0.0,  # SMD
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
        ]

        return FootprintDefinition(
            name=f"R_{package}",
            description=f"SMD Resistor {package}",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=length,
            body_height=width,
            body_thickness=height,
            courtyard_margin=0.25,
            silkscreen_width=0.12,
        )

    def _create_tht_footprint(self, spacing: float = 10.16) -> FootprintDefinition:
        """Create through-hole resistor footprint."""
        drill_diameter = 0.8  # mm
        pad_diameter = 1.6  # mm

        pins = [
            PinDefinition(
                number="1",
                name="A",
                x=-spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
            PinDefinition(
                number="2",
                name="B",
                x=spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
        ]

        return FootprintDefinition(
            name="R_THT_10.16mm",
            description="Through-hole Resistor 10.16mm spacing",
            mount_type=MountType.THT,
            pins=pins,
            body_width=spacing - 2.0,
            body_height=2.5,
            body_thickness=2.5,
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def smd_0603(self, value: str, tolerance: str = "5%") -> "PCBComponentInterface":
        """Create 0603 SMD resistor."""
        specs = ResistorSpecs(
            value=value,
            tolerance=tolerance,
            power_rating="0.1W",
            package="0603",
            voltage_rating="50V",
        )
        return self._create_resistor(specs)

    def smd_0805(self, value: str, tolerance: str = "5%") -> "PCBComponentInterface":
        """Create 0805 SMD resistor."""
        specs = ResistorSpecs(
            value=value,
            tolerance=tolerance,
            power_rating="0.125W",
            package="0805",
            voltage_rating="150V",
        )
        return self._create_resistor(specs)

    def smd_1206(self, value: str, tolerance: str = "5%") -> "PCBComponentInterface":
        """Create 1206 SMD resistor."""
        specs = ResistorSpecs(
            value=value,
            tolerance=tolerance,
            power_rating="0.25W",
            package="1206",
            voltage_rating="200V",
        )
        return self._create_resistor(specs)

    def through_hole(
        self, value: str, tolerance: str = "5%", power_rating: str = "0.25W"
    ) -> "PCBComponentInterface":
        """Create through-hole resistor."""
        specs = ResistorSpecs(
            value=value,
            tolerance=tolerance,
            power_rating=power_rating,
            package="THT",
            voltage_rating="250V",
        )
        return self._create_resistor(specs)

    def _create_resistor(self, specs: ResistorSpecs) -> "PCBComponentInterface":
        """Create resistor component from specifications."""
        # This would be implemented by concrete adapters
        # For now, we'll create the basic structure

        # Create footprint
        if specs.package == "THT":
            footprint = self._create_tht_footprint()
        else:
            footprint = self._create_smd_footprint(specs.package)

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=specs.value,
            tolerance=specs.tolerance,
            power_rating=specs.power_rating,
            voltage_rating=specs.voltage_rating,
            temperature_coefficient=specs.temperature_coefficient,
            package=specs.package,
            custom_properties={"component_type": "resistor", "specifications": specs},
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError(
            "_create_resistor must be implemented by concrete adapter"
        )
