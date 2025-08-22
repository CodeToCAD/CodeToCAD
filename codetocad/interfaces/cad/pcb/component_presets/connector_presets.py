"""
Connector component presets for PCB design.

This module provides preset definitions for common connector types
including headers, JST connectors, USB connectors, and other standard connectors.
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
class ConnectorSpecs:
    """Specifications for connector components."""

    connector_type: str = "header"  # "header", "jst", "usb", "barrel", "terminal"
    pin_count: int = 2  # Number of pins/contacts
    pitch: float = 2.54  # Pin spacing in mm
    current_rating: str = "1A"  # Current rating per pin
    voltage_rating: str = "250V"  # Voltage rating
    mounting: str = "tht"  # "tht", "smd", "panel"
    orientation: str = "vertical"  # "vertical", "horizontal", "right_angle"
    gender: str = "male"  # "male", "female", "n/a"


class ConnectorPresets:
    """
    Preset definitions for connector components.

    Provides common connector types including pin headers, JST connectors,
    USB connectors, and terminal blocks.
    """

    def __init__(self):
        pass

    def _create_header_footprint(
        self, pin_count: int, rows: int = 1, pitch: float = 2.54
    ) -> FootprintDefinition:
        """Create pin header footprint."""
        drill_diameter = 1.0
        pad_diameter = 1.7

        pins = []
        pins_per_row = pin_count // rows
        row_spacing = pitch if rows > 1 else 0

        pin_num = 1
        for row in range(rows):
            for col in range(pins_per_row):
                x = col * pitch - (pins_per_row - 1) * pitch / 2
                y = row * row_spacing - (rows - 1) * row_spacing / 2

                pins.append(
                    PinDefinition(
                        number=str(pin_num),
                        name=f"Pin{pin_num}",
                        x=x,
                        y=y,
                        drill_diameter=drill_diameter,
                        pad_width=pad_diameter,
                        pad_height=pad_diameter,
                        shape="circle",
                    )
                )
                pin_num += 1

        body_width = (pins_per_row - 1) * pitch + 2.0
        body_height = (rows - 1) * pitch + 2.0 if rows > 1 else 2.5

        return FootprintDefinition(
            name=f"Header_{pin_count}x{rows}",
            description=f"Pin header {pin_count} pins, {rows} rows",
            mount_type=MountType.THT,
            pins=pins,
            body_width=body_width,
            body_height=body_height,
            body_thickness=8.5,
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def _create_jst_footprint(
        self, pin_count: int, series: str = "XH"
    ) -> FootprintDefinition:
        """Create JST connector footprint."""
        # JST XH series specifications
        if series == "XH":
            pitch = 2.5
            drill_diameter = 0.9
            pad_diameter = 1.5
        elif series == "PH":
            pitch = 2.0
            drill_diameter = 0.8
            pad_diameter = 1.4
        else:
            raise ValueError(f"Unknown JST series: {series}")

        pins = []
        for i in range(pin_count):
            x = i * pitch - (pin_count - 1) * pitch / 2
            pins.append(
                PinDefinition(
                    number=str(i + 1),
                    name=f"Pin{i + 1}",
                    x=x,
                    y=0,
                    drill_diameter=drill_diameter,
                    pad_width=pad_diameter,
                    pad_height=pad_diameter,
                    shape="circle",
                )
            )

        body_width = (pin_count - 1) * pitch + 4.0

        return FootprintDefinition(
            name=f"JST_{series}_{pin_count}",
            description=f"JST {series} {pin_count}-pin connector",
            mount_type=MountType.THT,
            pins=pins,
            body_width=body_width,
            body_height=5.5,
            body_thickness=6.0,
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def _create_usb_footprint(self, usb_type: str = "USB-A") -> FootprintDefinition:
        """Create USB connector footprint."""
        if usb_type == "USB-A":
            # USB-A connector (female, through-hole)
            pins = [
                PinDefinition(
                    number="1",
                    name="VBUS",
                    x=-1.5,
                    y=0,
                    drill_diameter=0.9,
                    pad_width=1.5,
                    pad_height=1.5,
                    shape="circle",
                ),
                PinDefinition(
                    number="2",
                    name="D-",
                    x=-0.5,
                    y=0,
                    drill_diameter=0.9,
                    pad_width=1.5,
                    pad_height=1.5,
                    shape="circle",
                ),
                PinDefinition(
                    number="3",
                    name="D+",
                    x=0.5,
                    y=0,
                    drill_diameter=0.9,
                    pad_width=1.5,
                    pad_height=1.5,
                    shape="circle",
                ),
                PinDefinition(
                    number="4",
                    name="GND",
                    x=1.5,
                    y=0,
                    drill_diameter=0.9,
                    pad_width=1.5,
                    pad_height=1.5,
                    shape="circle",
                ),
                # Shield pins
                PinDefinition(
                    number="5",
                    name="Shield",
                    x=-6.57,
                    y=2.71,
                    drill_diameter=2.3,
                    pad_width=3.0,
                    pad_height=3.0,
                    shape="circle",
                ),
                PinDefinition(
                    number="6",
                    name="Shield",
                    x=6.57,
                    y=2.71,
                    drill_diameter=2.3,
                    pad_width=3.0,
                    pad_height=3.0,
                    shape="circle",
                ),
            ]

            return FootprintDefinition(
                name="USB-A_Female_THT",
                description="USB-A female connector through-hole",
                mount_type=MountType.THT,
                pins=pins,
                body_width=13.14,
                body_height=14.0,
                body_thickness=6.5,
                courtyard_margin=0.5,
                silkscreen_width=0.15,
            )

        elif usb_type == "USB-C":
            # Simplified USB-C footprint (would need full 24-pin implementation)
            pins = []
            for i in range(12):  # Simplified to 12 pins for example
                x = (i - 5.5) * 0.5
                pins.append(
                    PinDefinition(
                        number=str(i + 1),
                        name=f"Pin{i + 1}",
                        x=x,
                        y=-2.6,
                        drill_diameter=0.0,
                        pad_width=0.3,
                        pad_height=0.8,
                        shape="rectangle",
                    )
                )

            return FootprintDefinition(
                name="USB-C_SMD",
                description="USB-C connector SMD",
                mount_type=MountType.SMD,
                pins=pins,
                body_width=8.94,
                body_height=7.35,
                body_thickness=3.2,
                courtyard_margin=0.5,
                silkscreen_width=0.12,
            )

        else:
            raise ValueError(f"Unknown USB type: {usb_type}")

    def pin_header_1x2(self) -> "PCBComponentInterface":
        """Create 1x2 pin header."""
        specs = ConnectorSpecs(
            connector_type="header",
            pin_count=2,
            pitch=2.54,
            current_rating="3A",
            voltage_rating="250V",
        )
        return self._create_connector(specs, "Header_1x2")

    def pin_header_2x5(self) -> "PCBComponentInterface":
        """Create 2x5 pin header."""
        specs = ConnectorSpecs(
            connector_type="header",
            pin_count=10,
            pitch=2.54,
            current_rating="3A",
            voltage_rating="250V",
        )
        return self._create_connector(specs, "Header_2x5", rows=2)

    def jst_xh_2pin(self) -> "PCBComponentInterface":
        """Create JST XH 2-pin connector."""
        specs = ConnectorSpecs(
            connector_type="jst",
            pin_count=2,
            pitch=2.5,
            current_rating="3A",
            voltage_rating="250V",
        )
        return self._create_connector(specs, "JST_XH_2")

    def jst_ph_4pin(self) -> "PCBComponentInterface":
        """Create JST PH 4-pin connector."""
        specs = ConnectorSpecs(
            connector_type="jst",
            pin_count=4,
            pitch=2.0,
            current_rating="2A",
            voltage_rating="250V",
        )
        return self._create_connector(specs, "JST_PH_4")

    def usb_a_female(self) -> "PCBComponentInterface":
        """Create USB-A female connector."""
        specs = ConnectorSpecs(
            connector_type="usb",
            pin_count=4,
            current_rating="500mA",
            voltage_rating="30V",
            gender="female",
        )
        return self._create_connector(specs, "USB_A_Female")

    def usb_c_smd(self) -> "PCBComponentInterface":
        """Create USB-C SMD connector."""
        specs = ConnectorSpecs(
            connector_type="usb",
            pin_count=24,
            current_rating="3A",
            voltage_rating="20V",
            mounting="smd",
        )
        return self._create_connector(specs, "USB_C_SMD")

    def _create_connector(
        self, specs: ConnectorSpecs, part_number: str, rows: int = 1
    ) -> "PCBComponentInterface":
        """Create connector component from specifications."""
        # Create footprint based on connector type
        if specs.connector_type == "header":
            footprint = self._create_header_footprint(
                specs.pin_count, rows, specs.pitch
            )
        elif specs.connector_type == "jst":
            series = "XH" if specs.pitch == 2.5 else "PH"
            footprint = self._create_jst_footprint(specs.pin_count, series)
        elif specs.connector_type == "usb":
            usb_type = "USB-C" if specs.mounting == "smd" else "USB-A"
            footprint = self._create_usb_footprint(usb_type)
        else:
            raise ValueError(f"Unknown connector type: {specs.connector_type}")

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=part_number,
            voltage_rating=specs.voltage_rating,
            package=footprint.name,
            part_number=part_number,
            custom_properties={
                "component_type": "connector",
                "connector_type": specs.connector_type,
                "pin_count": specs.pin_count,
                "pitch": specs.pitch,
                "current_rating": specs.current_rating,
                "mounting": specs.mounting,
                "orientation": specs.orientation,
                "gender": specs.gender,
                "specifications": specs,
            },
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError(
            "_create_connector must be implemented by concrete adapter"
        )
