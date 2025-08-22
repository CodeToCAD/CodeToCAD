"""
IC (Integrated Circuit) component presets for PCB design.

This module provides preset definitions for common IC packages
including DIP, SOIC, QFP, BGA, and other standard packages.
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
class ICSpecs:
    """Specifications for IC components."""

    ic_type: str = "logic"  # "logic", "analog", "microcontroller", "memory", "power"
    package: str = "DIP-8"  # Package type
    pin_count: int = 8  # Number of pins
    supply_voltage: str = "5V"  # Operating voltage
    power_consumption: str = "10mW"  # Typical power consumption
    operating_temperature: str = "-40°C to +85°C"  # Operating temperature range
    function: str = ""  # Brief description of IC function


class ICPresets:
    """
    Preset definitions for IC components.

    Provides common IC packages including DIP, SOIC, QFP, and BGA
    with standard pin configurations.
    """

    def __init__(self):
        pass

    def _create_dip_footprint(
        self, pin_count: int, pitch: float = 2.54
    ) -> FootprintDefinition:
        """Create DIP (Dual In-line Package) footprint."""
        if pin_count % 2 != 0:
            raise ValueError("DIP packages must have even number of pins")

        pins_per_side = pin_count // 2
        drill_diameter = 0.8
        pad_diameter = 1.6
        row_spacing = 7.62  # Standard DIP row spacing

        pins = []

        # Left side pins (1 to pins_per_side)
        for i in range(pins_per_side):
            pins.append(
                PinDefinition(
                    number=str(i + 1),
                    name=f"Pin{i + 1}",
                    x=-row_spacing / 2,
                    y=(pins_per_side - 1 - i) * pitch - (pins_per_side - 1) * pitch / 2,
                    drill_diameter=drill_diameter,
                    pad_width=pad_diameter,
                    pad_height=pad_diameter,
                    shape="circle",
                )
            )

        # Right side pins (pin_count down to pins_per_side + 1)
        for i in range(pins_per_side):
            pins.append(
                PinDefinition(
                    number=str(pins_per_side + i + 1),
                    name=f"Pin{pins_per_side + i + 1}",
                    x=row_spacing / 2,
                    y=i * pitch - (pins_per_side - 1) * pitch / 2,
                    drill_diameter=drill_diameter,
                    pad_width=pad_diameter,
                    pad_height=pad_diameter,
                    shape="circle",
                )
            )

        body_length = (pins_per_side - 1) * pitch + 2.0

        return FootprintDefinition(
            name=f"DIP-{pin_count}",
            description=f"DIP {pin_count}-pin through-hole package",
            mount_type=MountType.THT,
            pins=pins,
            body_width=row_spacing + 2.0,
            body_height=body_length,
            body_thickness=4.0,
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def _create_soic_footprint(
        self, pin_count: int, pitch: float = 1.27
    ) -> FootprintDefinition:
        """Create SOIC (Small Outline IC) footprint."""
        if pin_count % 2 != 0:
            raise ValueError("SOIC packages must have even number of pins")

        pins_per_side = pin_count // 2
        pad_width = 0.6
        pad_height = 1.5
        row_spacing = 5.3  # Standard SOIC row spacing

        pins = []

        # Left side pins
        for i in range(pins_per_side):
            pins.append(
                PinDefinition(
                    number=str(i + 1),
                    name=f"Pin{i + 1}",
                    x=-row_spacing / 2,
                    y=(pins_per_side - 1 - i) * pitch - (pins_per_side - 1) * pitch / 2,
                    drill_diameter=0.0,
                    pad_width=pad_width,
                    pad_height=pad_height,
                    shape="rectangle",
                )
            )

        # Right side pins
        for i in range(pins_per_side):
            pins.append(
                PinDefinition(
                    number=str(pins_per_side + i + 1),
                    name=f"Pin{pins_per_side + i + 1}",
                    x=row_spacing / 2,
                    y=i * pitch - (pins_per_side - 1) * pitch / 2,
                    drill_diameter=0.0,
                    pad_width=pad_width,
                    pad_height=pad_height,
                    shape="rectangle",
                )
            )

        body_length = (pins_per_side - 1) * pitch + 1.0

        return FootprintDefinition(
            name=f"SOIC-{pin_count}",
            description=f"SOIC {pin_count}-pin SMD package",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=3.9,
            body_height=body_length,
            body_thickness=1.75,
            courtyard_margin=0.25,
            silkscreen_width=0.12,
        )

    def _create_qfp_footprint(
        self, pin_count: int, pitch: float = 0.8, body_size: float = 10.0
    ) -> FootprintDefinition:
        """Create QFP (Quad Flat Package) footprint."""
        if pin_count % 4 != 0:
            raise ValueError("QFP packages must have pin count divisible by 4")

        pins_per_side = pin_count // 4
        pad_width = 0.4
        pad_height = 1.2

        pins = []
        pin_num = 1

        # Bottom side (left to right)
        for i in range(pins_per_side):
            x = (i - (pins_per_side - 1) / 2) * pitch
            y = -body_size / 2 - pad_height / 2
            pins.append(
                PinDefinition(
                    number=str(pin_num),
                    name=f"Pin{pin_num}",
                    x=x,
                    y=y,
                    drill_diameter=0.0,
                    pad_width=pad_width,
                    pad_height=pad_height,
                    shape="rectangle",
                )
            )
            pin_num += 1

        # Right side (bottom to top)
        for i in range(pins_per_side):
            x = body_size / 2 + pad_height / 2
            y = (i - (pins_per_side - 1) / 2) * pitch
            pins.append(
                PinDefinition(
                    number=str(pin_num),
                    name=f"Pin{pin_num}",
                    x=x,
                    y=y,
                    drill_diameter=0.0,
                    pad_width=pad_height,  # Swapped for 90° rotation
                    pad_height=pad_width,
                    shape="rectangle",
                )
            )
            pin_num += 1

        # Top side (right to left)
        for i in range(pins_per_side):
            x = ((pins_per_side - 1) / 2 - i) * pitch
            y = body_size / 2 + pad_height / 2
            pins.append(
                PinDefinition(
                    number=str(pin_num),
                    name=f"Pin{pin_num}",
                    x=x,
                    y=y,
                    drill_diameter=0.0,
                    pad_width=pad_width,
                    pad_height=pad_height,
                    shape="rectangle",
                )
            )
            pin_num += 1

        # Left side (top to bottom)
        for i in range(pins_per_side):
            x = -body_size / 2 - pad_height / 2
            y = ((pins_per_side - 1) / 2 - i) * pitch
            pins.append(
                PinDefinition(
                    number=str(pin_num),
                    name=f"Pin{pin_num}",
                    x=x,
                    y=y,
                    drill_diameter=0.0,
                    pad_width=pad_height,  # Swapped for 90° rotation
                    pad_height=pad_width,
                    shape="rectangle",
                )
            )
            pin_num += 1

        return FootprintDefinition(
            name=f"QFP-{pin_count}",
            description=f"QFP {pin_count}-pin SMD package",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=body_size,
            body_height=body_size,
            body_thickness=1.6,
            courtyard_margin=0.5,
            silkscreen_width=0.12,
        )

    def logic_gate_dip14(
        self, part_number: str = "74HC00", function: str = "Quad NAND"
    ) -> "PCBComponentInterface":
        """Create 14-pin DIP logic gate."""
        specs = ICSpecs(
            ic_type="logic",
            package="DIP-14",
            pin_count=14,
            supply_voltage="5V",
            power_consumption="2mW",
            function=function,
        )
        return self._create_ic(specs, part_number)

    def microcontroller_qfp32(
        self, part_number: str = "STM32F103", function: str = "32-bit MCU"
    ) -> "PCBComponentInterface":
        """Create 32-pin QFP microcontroller."""
        specs = ICSpecs(
            ic_type="microcontroller",
            package="QFP-32",
            pin_count=32,
            supply_voltage="3.3V",
            power_consumption="50mW",
            function=function,
        )
        return self._create_ic(specs, part_number)

    def op_amp_soic8(
        self, part_number: str = "LM358", function: str = "Dual Op-Amp"
    ) -> "PCBComponentInterface":
        """Create 8-pin SOIC operational amplifier."""
        specs = ICSpecs(
            ic_type="analog",
            package="SOIC-8",
            pin_count=8,
            supply_voltage="±15V",
            power_consumption="1mW",
            function=function,
        )
        return self._create_ic(specs, part_number)

    def voltage_regulator_soic8(
        self, part_number: str = "LM7805", output_voltage: str = "5V"
    ) -> "PCBComponentInterface":
        """Create voltage regulator IC."""
        specs = ICSpecs(
            ic_type="power",
            package="SOIC-8",
            pin_count=8,
            supply_voltage="7V-35V",
            power_consumption="5W",
            function=f"Voltage Regulator {output_voltage}",
        )
        return self._create_ic(specs, part_number)

    def _create_ic(self, specs: ICSpecs, part_number: str) -> "PCBComponentInterface":
        """Create IC component from specifications."""
        # Create footprint based on package
        if specs.package.startswith("DIP"):
            footprint = self._create_dip_footprint(specs.pin_count)
        elif specs.package.startswith("SOIC"):
            footprint = self._create_soic_footprint(specs.pin_count)
        elif specs.package.startswith("QFP"):
            footprint = self._create_qfp_footprint(specs.pin_count)
        else:
            raise ValueError(f"Unknown IC package: {specs.package}")

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=part_number,
            voltage_rating=specs.supply_voltage,
            power_rating=specs.power_consumption,
            package=specs.package,
            part_number=part_number,
            custom_properties={
                "component_type": "ic",
                "ic_type": specs.ic_type,
                "pin_count": specs.pin_count,
                "supply_voltage": specs.supply_voltage,
                "power_consumption": specs.power_consumption,
                "operating_temperature": specs.operating_temperature,
                "function": specs.function,
                "specifications": specs,
            },
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError("_create_ic must be implemented by concrete adapter")
