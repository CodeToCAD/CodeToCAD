"""
Capacitor component presets for PCB design.

This module provides preset definitions for common capacitor types
including ceramic, electrolytic, and tantalum variants.
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
    from codetocad.interfaces.cad.pcb.pcb_component_interface import (
        PCBComponentInterface,
    )


@dataclass
class CapacitorSpecs:
    """Specifications for capacitor components."""

    value: str  # e.g., "100nF", "10uF", "1000pF"
    tolerance: str = "10%"  # e.g., "5%", "10%", "20%"
    voltage_rating: str = "50V"  # e.g., "16V", "25V", "50V"
    dielectric: str = "X7R"  # e.g., "C0G", "X7R", "Y5V" for ceramic
    package: str = "0603"  # SMD package or "THT" for through-hole
    capacitor_type: str = "ceramic"  # "ceramic", "electrolytic", "tantalum"
    temperature_coefficient: str = "±15%"
    esr: str = ""  # Equivalent Series Resistance


class CapacitorPresets:
    """
    Preset definitions for capacitor components.

    Provides common capacitor values and packages for ceramic, electrolytic, and tantalum types.
    """

    def __init__(self):
        pass

    def _create_smd_footprint(self, package: str) -> FootprintDefinition:
        """Create SMD capacitor footprint based on package size."""
        # Standard SMD capacitor dimensions (same as resistors for most packages)
        dimensions = {
            "0201": (0.6, 0.3, 0.33),
            "0402": (1.0, 0.5, 0.5),
            "0603": (1.6, 0.8, 0.8),
            "0805": (2.0, 1.25, 1.25),
            "1206": (3.2, 1.6, 1.6),
            "1210": (3.2, 2.5, 2.5),
            "1812": (4.5, 3.2, 2.5),
            "2220": (5.7, 5.0, 2.5),
        }

        if package not in dimensions:
            raise ValueError(f"Unknown SMD capacitor package: {package}")

        length, width, height = dimensions[package]

        # Pad dimensions
        pad_length = length * 0.6
        pad_width = width
        pad_spacing = length + 0.2

        pins = [
            PinDefinition(
                number="1",
                name="+",
                x=-pad_spacing / 2,
                y=0,
                drill_diameter=0.0,
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
            PinDefinition(
                number="2",
                name="-",
                x=pad_spacing / 2,
                y=0,
                drill_diameter=0.0,
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
        ]

        return FootprintDefinition(
            name=f"C_{package}",
            description=f"SMD Capacitor {package}",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=length,
            body_height=width,
            body_thickness=height,
            courtyard_margin=0.25,
            silkscreen_width=0.12,
        )

    def _create_electrolytic_footprint(
        self, diameter: float, spacing: float = 2.5
    ) -> FootprintDefinition:
        """Create electrolytic capacitor footprint."""
        drill_diameter = 0.8
        pad_diameter = 1.6

        pins = [
            PinDefinition(
                number="1",
                name="+",
                x=-spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
            PinDefinition(
                number="2",
                name="-",
                x=spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
        ]

        return FootprintDefinition(
            name=f"C_Electrolytic_D{diameter}mm",
            description=f"Electrolytic Capacitor D={diameter}mm",
            mount_type=MountType.THT,
            pins=pins,
            body_width=diameter,
            body_height=diameter,
            body_thickness=diameter * 1.2,  # Height is typically larger
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def ceramic_0603(
        self, value: str, voltage: str = "50V", dielectric: str = "X7R"
    ) -> "PCBComponentInterface":
        """Create 0603 ceramic capacitor."""
        specs = CapacitorSpecs(
            value=value,
            voltage_rating=voltage,
            dielectric=dielectric,
            package="0603",
            capacitor_type="ceramic",
            tolerance="10%",
        )
        return self._create_capacitor(specs)

    def ceramic_0805(
        self, value: str, voltage: str = "50V", dielectric: str = "X7R"
    ) -> "PCBComponentInterface":
        """Create 0805 ceramic capacitor."""
        specs = CapacitorSpecs(
            value=value,
            voltage_rating=voltage,
            dielectric=dielectric,
            package="0805",
            capacitor_type="ceramic",
            tolerance="10%",
        )
        return self._create_capacitor(specs)

    def ceramic_1206(
        self, value: str, voltage: str = "50V", dielectric: str = "X7R"
    ) -> "PCBComponentInterface":
        """Create 1206 ceramic capacitor."""
        specs = CapacitorSpecs(
            value=value,
            voltage_rating=voltage,
            dielectric=dielectric,
            package="1206",
            capacitor_type="ceramic",
            tolerance="10%",
        )
        return self._create_capacitor(specs)

    def electrolytic_tht(
        self, value: str, voltage: str, diameter: float = 6.3
    ) -> "PCBComponentInterface":
        """Create through-hole electrolytic capacitor."""
        specs = CapacitorSpecs(
            value=value,
            voltage_rating=voltage,
            package="THT",
            capacitor_type="electrolytic",
            tolerance="20%",
            dielectric="electrolytic",
        )
        return self._create_capacitor(specs, diameter)

    def tantalum_smd(
        self, value: str, voltage: str, package: str = "1206"
    ) -> "PCBComponentInterface":
        """Create SMD tantalum capacitor."""
        specs = CapacitorSpecs(
            value=value,
            voltage_rating=voltage,
            package=package,
            capacitor_type="tantalum",
            tolerance="10%",
            dielectric="tantalum",
        )
        return self._create_capacitor(specs)

    def _create_capacitor(
        self, specs: CapacitorSpecs, diameter: float | None = None
    ) -> "PCBComponentInterface":
        """Create capacitor component from specifications."""
        # Create footprint based on type
        if specs.capacitor_type == "electrolytic" and specs.package == "THT":
            footprint = self._create_electrolytic_footprint(diameter or 6.3)
        else:
            footprint = self._create_smd_footprint(specs.package)

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=specs.value,
            tolerance=specs.tolerance,
            voltage_rating=specs.voltage_rating,
            package=specs.package,
            temperature_coefficient=specs.temperature_coefficient,
            custom_properties={
                "component_type": "capacitor",
                "capacitor_type": specs.capacitor_type,
                "dielectric": specs.dielectric,
                "esr": specs.esr,
                "specifications": specs,
            },
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError(
            "_create_capacitor must be implemented by concrete adapter"
        )
