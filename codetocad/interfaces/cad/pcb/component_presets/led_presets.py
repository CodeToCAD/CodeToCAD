"""
LED component presets for PCB design.

This module provides preset definitions for common LED types
including standard LEDs, high-power LEDs, and RGB LEDs.
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
class LEDSpecs:
    """Specifications for LED components."""

    color: str = "red"  # "red", "green", "blue", "white", "yellow", "rgb"
    forward_voltage: str = "2.0V"  # Typical forward voltage
    forward_current: str = "20mA"  # Typical forward current
    luminous_intensity: str = "100mcd"  # Luminous intensity
    viewing_angle: str = "120°"  # Viewing angle
    package: str = "0603"  # Package type
    wavelength: str = "630nm"  # Peak wavelength (for colored LEDs)
    power_rating: str = "0.1W"  # Power rating
    led_type: str = "standard"  # "standard", "high_power", "rgb"


class LEDPresets:
    """
    Preset definitions for LED components.

    Provides common LED types including standard indicator LEDs,
    high-power LEDs, and RGB LEDs in various packages.
    """

    def __init__(self):
        pass

    def _create_smd_led_footprint(self, package: str) -> FootprintDefinition:
        """Create SMD LED footprint based on package size."""
        # LED-specific dimensions (may differ from standard resistor/capacitor)
        dimensions = {
            "0603": (1.6, 0.8, 0.8),
            "0805": (2.0, 1.25, 1.1),
            "1206": (3.2, 1.6, 1.1),
            "3528": (3.5, 2.8, 1.9),  # Common LED package
            "5050": (5.0, 5.0, 1.6),  # RGB LED package
        }

        if package not in dimensions:
            raise ValueError(f"Unknown SMD LED package: {package}")

        length, width, height = dimensions[package]

        # LED pads are often larger than standard components
        pad_length = length * 0.7
        pad_width = width * 0.9
        pad_spacing = length + 0.1

        pins = [
            PinDefinition(
                number="1",
                name="A",  # Anode
                x=-pad_spacing / 2,
                y=0,
                drill_diameter=0.0,
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
            PinDefinition(
                number="2",
                name="K",  # Cathode
                x=pad_spacing / 2,
                y=0,
                drill_diameter=0.0,
                pad_width=pad_length,
                pad_height=pad_width,
                shape="rectangle",
            ),
        ]

        return FootprintDefinition(
            name=f"LED_{package}",
            description=f"SMD LED {package}",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=length,
            body_height=width,
            body_thickness=height,
            courtyard_margin=0.25,
            silkscreen_width=0.12,
        )

    def _create_rgb_led_footprint(self, package: str = "5050") -> FootprintDefinition:
        """Create RGB LED footprint."""
        if package == "5050":
            length, width, height = 5.0, 5.0, 1.6
            pad_size = 1.6

            pins = [
                PinDefinition(
                    number="1",
                    name="R",
                    x=-1.75,
                    y=1.75,
                    drill_diameter=0.0,
                    pad_width=pad_size,
                    pad_height=pad_size,
                    shape="rectangle",
                ),
                PinDefinition(
                    number="2",
                    name="G",
                    x=-1.75,
                    y=-1.75,
                    drill_diameter=0.0,
                    pad_width=pad_size,
                    pad_height=pad_size,
                    shape="rectangle",
                ),
                PinDefinition(
                    number="3",
                    name="B",
                    x=1.75,
                    y=-1.75,
                    drill_diameter=0.0,
                    pad_width=pad_size,
                    pad_height=pad_size,
                    shape="rectangle",
                ),
                PinDefinition(
                    number="4",
                    name="VCC",
                    x=1.75,
                    y=1.75,
                    drill_diameter=0.0,
                    pad_width=pad_size,
                    pad_height=pad_size,
                    shape="rectangle",
                ),
            ]
        else:
            raise ValueError(f"Unknown RGB LED package: {package}")

        return FootprintDefinition(
            name=f"LED_RGB_{package}",
            description=f"RGB LED {package}",
            mount_type=MountType.SMD,
            pins=pins,
            body_width=length,
            body_height=width,
            body_thickness=height,
            courtyard_margin=0.5,
            silkscreen_width=0.12,
        )

    def _create_tht_led_footprint(
        self, diameter: float = 5.0, spacing: float = 2.54
    ) -> FootprintDefinition:
        """Create through-hole LED footprint."""
        drill_diameter = 0.8
        pad_diameter = 1.6

        pins = [
            PinDefinition(
                number="1",
                name="A",  # Anode (longer lead)
                x=-spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
            PinDefinition(
                number="2",
                name="K",  # Cathode (shorter lead)
                x=spacing / 2,
                y=0,
                drill_diameter=drill_diameter,
                pad_width=pad_diameter,
                pad_height=pad_diameter,
                shape="circle",
            ),
        ]

        return FootprintDefinition(
            name=f"LED_THT_D{diameter}mm",
            description=f"Through-hole LED D={diameter}mm",
            mount_type=MountType.THT,
            pins=pins,
            body_width=diameter,
            body_height=diameter,
            body_thickness=diameter * 0.6,
            courtyard_margin=0.5,
            silkscreen_width=0.15,
        )

    def red_0603(
        self, forward_voltage: str = "2.0V", forward_current: str = "20mA"
    ) -> "PCBComponentInterface":
        """Create 0603 red LED."""
        specs = LEDSpecs(
            color="red",
            forward_voltage=forward_voltage,
            forward_current=forward_current,
            wavelength="630nm",
            package="0603",
            luminous_intensity="100mcd",
        )
        return self._create_led(specs)

    def green_0805(
        self, forward_voltage: str = "2.2V", forward_current: str = "20mA"
    ) -> "PCBComponentInterface":
        """Create 0805 green LED."""
        specs = LEDSpecs(
            color="green",
            forward_voltage=forward_voltage,
            forward_current=forward_current,
            wavelength="525nm",
            package="0805",
            luminous_intensity="150mcd",
        )
        return self._create_led(specs)

    def white_1206(
        self, forward_voltage: str = "3.2V", forward_current: str = "20mA"
    ) -> "PCBComponentInterface":
        """Create 1206 white LED."""
        specs = LEDSpecs(
            color="white",
            forward_voltage=forward_voltage,
            forward_current=forward_current,
            wavelength="",  # White LEDs don't have a single wavelength
            package="1206",
            luminous_intensity="300mcd",
        )
        return self._create_led(specs)

    def rgb_5050(
        self,
        forward_voltage_r: str = "2.0V",
        forward_voltage_g: str = "3.2V",
        forward_voltage_b: str = "3.2V",
    ) -> "PCBComponentInterface":
        """Create 5050 RGB LED."""
        specs = LEDSpecs(
            color="rgb",
            forward_voltage=f"R:{forward_voltage_r}, G:{forward_voltage_g}, B:{forward_voltage_b}",
            forward_current="20mA",
            package="5050",
            led_type="rgb",
            luminous_intensity="1000mcd",
        )
        return self._create_led(specs)

    def through_hole_5mm(
        self, color: str = "red", forward_voltage: str = "2.0V"
    ) -> "PCBComponentInterface":
        """Create 5mm through-hole LED."""
        wavelengths = {
            "red": "630nm",
            "green": "525nm",
            "blue": "470nm",
            "yellow": "590nm",
            "white": "",
        }

        specs = LEDSpecs(
            color=color,
            forward_voltage=forward_voltage,
            forward_current="20mA",
            wavelength=wavelengths.get(color, ""),
            package="THT",
            luminous_intensity="200mcd",
        )
        return self._create_led(specs, diameter=5.0)

    def _create_led(
        self, specs: LEDSpecs, diameter: float = None
    ) -> "PCBComponentInterface":
        """Create LED component from specifications."""
        # Create footprint based on type
        if specs.led_type == "rgb":
            footprint = self._create_rgb_led_footprint(specs.package)
        elif specs.package == "THT":
            footprint = self._create_tht_led_footprint(diameter or 5.0)
        else:
            footprint = self._create_smd_led_footprint(specs.package)

        # Create electrical properties
        electrical_props = ElectricalProperties(
            value=specs.color,
            voltage_rating=specs.forward_voltage,
            power_rating=specs.power_rating,
            package=specs.package,
            custom_properties={
                "component_type": "led",
                "led_type": specs.led_type,
                "color": specs.color,
                "forward_voltage": specs.forward_voltage,
                "forward_current": specs.forward_current,
                "luminous_intensity": specs.luminous_intensity,
                "viewing_angle": specs.viewing_angle,
                "wavelength": specs.wavelength,
                "specifications": specs,
            },
        )

        # This would create the actual component in a concrete implementation
        raise NotImplementedError("_create_led must be implemented by concrete adapter")
