"""
Transistor component presets for PCB design.

This module provides preset definitions for common transistor types
including BJTs, MOSFETs, and various packages.
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
class TransistorSpecs:
    """Specifications for transistor components."""

    transistor_type: str = "npn"  # "npn", "pnp", "n-channel", "p-channel"
    technology: str = "bjt"  # "bjt", "mosfet", "jfet"
    package: str = "SOT-23"  # Package type
    max_voltage: str = "30V"  # Maximum voltage rating
    max_current: str = "100mA"  # Maximum current rating
    power_rating: str = "0.2W"  # Power dissipation
    gain: str = "100"  # Current gain (hFE for BJT, not applicable for MOSFET)
    threshold_voltage: str = ""  # Gate threshold voltage (MOSFET only)
    on_resistance: str = ""  # On-state resistance (MOSFET only)


class TransistorPresets:
    """
    Preset definitions for transistor components.

    Provides common transistor types including BJTs and MOSFETs
    in various packages like SOT-23, TO-220, etc.
    """

    def __init__(self):
        pass

    def _create_sot23_footprint(self) -> FootprintDefinition:
        """Create SOT-23 footprint (3-pin SMD package)."""
        # SOT-23 standard dimensions
        pad_width = 0.6
        pad_height = 1.0

        pins = [
            PinDefinition(
                number="1",
                name="B",  # Base (BJT) or Gate (MOSFET)
                x=-0.95,
                y=-1.0,
                drill_diameter=0.0,
                pad_width=pad_width,
                pad_height=pad_height,
                shape="rectangle",
            ),
            PinDefinition(
                number="2",
                name="E",  # Emitter (BJT) or Source (MOSFET)
                x=0.95,
                y=-1.0,
                drill_diameter=0.0,
                pad_width=pad_width,
                pad_height=pad_height,
                shape="rectangle",
            ),
            PinDefinition(
                number="3",
                name="C",  # Collector (BJT) or Drain (MOSFET)
                x=0,
                y=1.0,
                drill_diameter=0.0,
                pad_width=pad_width,
                pad_height=pad_height,
                shape="rectangle",
            ),
        ]

        return FootprintDefinition(
            name="SOT-23",
            description="SOT-23 3-pin SMD package",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=2.9,
            body_height=1.3,
            body_thickness=1.1,
            courtyard_margin=0.25,
            silkscreen_width=0.12,
        )

    def _create_to220_footprint(self) -> FootprintDefinition:
        """Create TO-220 footprint (3-pin through-hole package)."""
        drill_diameter = 1.0
        pad_diameter = 1.8
        spacing = 2.54

        pins = [
            PinDefinition(
                number="1",
                name="B",  # Base (BJT) or Gate (MOSFET)
                x=-spacing,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
            PinDefinition(
                number="2",
                name="C",  # Collector (BJT) or Drain (MOSFET)
                x=0,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
            PinDefinition(
                number="3",
                name="E",  # Emitter (BJT) or Source (MOSFET)
                x=spacing,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
        ]

        return FootprintDefinition(
            name="TO-220",
            description="TO-220 3-pin through-hole package",
            mount_type=MountType.THT,
            pins=pins,
            body_width=10.16,
            body_height=4.57,
            body_thickness=15.24,  # Including heat sink tab
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def _create_sot223_footprint(self) -> FootprintDefinition:
        """Create SOT-223 footprint (4-pin SMD package with heat sink)."""
        # SOT-223 dimensions
        small_pad_width = 0.7
        small_pad_height = 2.0
        large_pad_width = 3.0
        large_pad_height = 2.0

        pins = [
            PinDefinition(
                number="1",
                name="B",  # Base (BJT) or Gate (MOSFET)
                x=-2.3,
                y=-3.15,
                drill_diameter=0.0,
                pad_width=small_pad_width,
                pad_height=small_pad_height,
                shape="rectangle",
            ),
            PinDefinition(
                number="2",
                name="C",  # Collector (BJT) or Drain (MOSFET)
                x=0,
                y=-3.15,
                drill_diameter=0.0,
                pad_width=small_pad_width,
                pad_height=small_pad_height,
                shape="rectangle",
            ),
            PinDefinition(
                number="3",
                name="E",  # Emitter (BJT) or Source (MOSFET)
                x=2.3,
                y=-3.15,
                drill_diameter=0.0,
                pad_width=small_pad_width,
                pad_height=small_pad_height,
                shape="rectangle",
            ),
            PinDefinition(
                number="4",
                name="C",  # Heat sink pad (connected to collector/drain)
                x=0,
                y=3.15,
                drill_diameter=0.0,
                pad_width=large_pad_width,
                pad_height=large_pad_height,
                shape="rectangle",
            ),
        ]

        return FootprintDefinition(
            name="SOT-223",
            description="SOT-223 4-pin SMD package with heat sink",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=6.5,
            body_height=3.5,
            body_thickness=1.8,
            courtyard_margin=0.5,
            silkscreen_width=0.12,
        )

    def npn_bjt_sot23(
        self,
        part_number: str = "2N3904",
        max_voltage: str = "40V",
        max_current: str = "200mA",
    ) -> "PCBComponentInterface":
        """Create NPN BJT in SOT-23 package."""
        specs = TransistorSpecs(
            transistor_type="npn",
            technology="bjt",
            package="SOT-23",
            max_voltage=max_voltage,
            max_current=max_current,
            power_rating="0.2W",
            gain="100",
        )
        return self._create_transistor(specs, part_number)

    def pnp_bjt_sot23(
        self,
        part_number: str = "2N3906",
        max_voltage: str = "40V",
        max_current: str = "200mA",
    ) -> "PCBComponentInterface":
        """Create PNP BJT in SOT-23 package."""
        specs = TransistorSpecs(
            transistor_type="pnp",
            technology="bjt",
            package="SOT-23",
            max_voltage=max_voltage,
            max_current=max_current,
            power_rating="0.2W",
            gain="100",
        )
        return self._create_transistor(specs, part_number)

    def n_channel_mosfet_sot23(
        self,
        part_number: str = "2N7002",
        max_voltage: str = "60V",
        max_current: str = "300mA",
        threshold_voltage: str = "2.5V",
    ) -> "PCBComponentInterface":
        """Create N-channel MOSFET in SOT-23 package."""
        specs = TransistorSpecs(
            transistor_type="n-channel",
            technology="mosfet",
            package="SOT-23",
            max_voltage=max_voltage,
            max_current=max_current,
            power_rating="0.2W",
            threshold_voltage=threshold_voltage,
            on_resistance="5Ω",
        )
        return self._create_transistor(specs, part_number)

    def power_mosfet_to220(
        self,
        part_number: str = "IRF540N",
        max_voltage: str = "100V",
        max_current: str = "33A",
        threshold_voltage: str = "4V",
    ) -> "PCBComponentInterface":
        """Create power MOSFET in TO-220 package."""
        specs = TransistorSpecs(
            transistor_type="n-channel",
            technology="mosfet",
            package="TO-220",
            max_voltage=max_voltage,
            max_current=max_current,
            power_rating="130W",
            threshold_voltage=threshold_voltage,
            on_resistance="0.044Ω",
        )
        return self._create_transistor(specs, part_number)

    def power_transistor_sot223(
        self,
        part_number: str = "TIP122",
        transistor_type: str = "npn",
        max_voltage: str = "100V",
        max_current: str = "5A",
    ) -> "PCBComponentInterface":
        """Create power transistor in SOT-223 package."""
        specs = TransistorSpecs(
            transistor_type=transistor_type,
            technology="bjt",
            package="SOT-223",
            max_voltage=max_voltage,
            max_current=max_current,
            power_rating="2W",
            gain="1000",
        )
        return self._create_transistor(specs, part_number)

    def _create_transistor(
        self, specs: TransistorSpecs, part_number: str
    ) -> "PCBComponentInterface":
        """Create transistor component from specifications."""
        # Create footprint based on package
        if specs.package == "SOT-23":
            footprint = self._create_sot23_footprint()
        elif specs.package == "TO-220":
            footprint = self._create_to220_footprint()
        elif specs.package == "SOT-223":
            footprint = self._create_sot223_footprint()
        else:
            raise ValueError(f"Unknown transistor package: {specs.package}")

        # Update pin names based on technology
        if specs.technology == "mosfet":
            for pin in footprint.pins:
                if pin.name == "B":
                    pin.name = "G"  # Gate
                elif pin.name == "E":
                    pin.name = "S"  # Source
                elif pin.name == "C":
                    pin.name = "D"  # Drain

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=part_number,
            voltage_rating=specs.max_voltage,
            power_rating=specs.power_rating,
            package=specs.package,
            part_number=part_number,
            custom_properties={
                "component_type": "transistor",
                "transistor_type": specs.transistor_type,
                "technology": specs.technology,
                "max_voltage": specs.max_voltage,
                "max_current": specs.max_current,
                "gain": specs.gain,
                "threshold_voltage": specs.threshold_voltage,
                "on_resistance": specs.on_resistance,
                "specifications": specs,
            },
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError(
            "_create_transistor must be implemented by concrete adapter"
        )
