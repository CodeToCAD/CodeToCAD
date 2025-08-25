"""
End mill tool presets for CAM operations.

Provides preset configurations for various end mill types including
flat end mills, roughing mills, and finishing mills.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cam.tool_interface import ToolInterface

from codetocad.interfaces.cam.tool_interface import (
    ToolType,
    ToolMaterial,
    ToolGeometry,
    CuttingData,
)


@dataclass
class EndMillSpecs:
    """Specifications for end mill tools."""

    diameter: float  # mm
    length: float  # mm
    cutting_length: float  # mm
    shank_diameter: float  # mm
    flute_count: int = 2
    helix_angle: float = 30.0  # degrees
    material: ToolMaterial = ToolMaterial.HSS
    coating: str = "uncoated"

    # Cutting parameters for aluminum (can be adjusted for other materials)
    spindle_speed: float = 12000  # RPM
    feed_rate: float = 1200  # mm/min
    plunge_rate: float = 300  # mm/min
    step_over: float = 0.5  # 50% of diameter
    step_down: float = 1.0  # mm


class EndMillPresets:
    """Preset end mill configurations."""

    def __init__(self):
        pass

    def _create_end_mill(
        self, specs: EndMillSpecs, name: str, tool_number: int = 1
    ) -> "ToolInterface":
        """Create an end mill tool from specifications."""
        from codetocad.core.cam.tool import Tool  # Import concrete implementation

        tool = Tool()
        tool.set_name(name)
        tool.set_tool_number(tool_number)
        tool.tool_type = ToolType.FLAT_END_MILL
        tool.material = specs.material

        # Set geometry
        geometry = ToolGeometry(
            diameter=specs.diameter,
            length=specs.length,
            cutting_length=specs.cutting_length,
            shank_diameter=specs.shank_diameter,
            flute_count=specs.flute_count,
            helix_angle=specs.helix_angle,
        )
        tool.set_geometry(geometry)

        # Set cutting data
        cutting_data = CuttingData(
            spindle_speed=specs.spindle_speed,
            feed_rate=specs.feed_rate,
            plunge_rate=specs.plunge_rate,
            step_over=specs.step_over,
            step_down=specs.step_down,
        )
        tool.set_cutting_data(cutting_data)

        # Add custom properties
        tool.add_custom_property("coating", specs.coating)
        tool.add_custom_property("preset_category", "end_mill")

        return tool

    # Standard HSS End Mills
    def flat_hss_3mm(self, tool_number: int = 1) -> "ToolInterface":
        """3mm HSS flat end mill."""
        specs = EndMillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=12.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=15000,
            feed_rate=900,
            plunge_rate=225,
            step_down=0.5,
        )
        return self._create_end_mill(specs, "3mm HSS Flat End Mill", tool_number)

    def flat_hss_6mm(self, tool_number: int = 2) -> "ToolInterface":
        """6mm HSS flat end mill."""
        specs = EndMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=12000,
            feed_rate=1440,
            plunge_rate=360,
            step_down=1.0,
        )
        return self._create_end_mill(specs, "6mm HSS Flat End Mill", tool_number)

    def flat_hss_10mm(self, tool_number: int = 3) -> "ToolInterface":
        """10mm HSS flat end mill."""
        specs = EndMillSpecs(
            diameter=10.0,
            length=75.0,
            cutting_length=30.0,
            shank_diameter=10.0,
            flute_count=3,
            material=ToolMaterial.HSS,
            spindle_speed=8000,
            feed_rate=2000,
            plunge_rate=500,
            step_down=1.5,
        )
        return self._create_end_mill(specs, "10mm HSS Flat End Mill", tool_number)

    # Carbide End Mills
    def flat_carbide_3mm(self, tool_number: int = 11) -> "ToolInterface":
        """3mm Carbide flat end mill."""
        specs = EndMillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=12.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=20000,
            feed_rate=1200,
            plunge_rate=300,
            step_down=0.75,
        )
        return self._create_end_mill(specs, "3mm Carbide Flat End Mill", tool_number)

    def flat_carbide_6mm(self, tool_number: int = 12) -> "ToolInterface":
        """6mm Carbide flat end mill."""
        specs = EndMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=3,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=18000,
            feed_rate=2160,
            plunge_rate=540,
            step_down=1.5,
        )
        return self._create_end_mill(specs, "6mm Carbide Flat End Mill", tool_number)

    def flat_carbide_10mm(self, tool_number: int = 13) -> "ToolInterface":
        """10mm Carbide flat end mill."""
        specs = EndMillSpecs(
            diameter=10.0,
            length=75.0,
            cutting_length=30.0,
            shank_diameter=10.0,
            flute_count=4,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=15000,
            feed_rate=3600,
            plunge_rate=900,
            step_down=2.0,
        )
        return self._create_end_mill(specs, "10mm Carbide Flat End Mill", tool_number)

    # Roughing End Mills
    def roughing_carbide_6mm(self, tool_number: int = 21) -> "ToolInterface":
        """6mm Carbide roughing end mill."""
        specs = EndMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=3,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=16000,
            feed_rate=2400,
            plunge_rate=600,
            step_down=2.0,  # Aggressive for roughing
        )
        tool = self._create_end_mill(
            specs, "6mm Carbide Roughing End Mill", tool_number
        )
        tool.tool_type = ToolType.ROUGHING_MILL
        tool.add_custom_property("application", "roughing")
        return tool

    def roughing_carbide_10mm(self, tool_number: int = 22) -> "ToolInterface":
        """10mm Carbide roughing end mill."""
        specs = EndMillSpecs(
            diameter=10.0,
            length=75.0,
            cutting_length=30.0,
            shank_diameter=10.0,
            flute_count=4,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=12000,
            feed_rate=3600,
            plunge_rate=900,
            step_down=3.0,  # Aggressive for roughing
        )
        tool = self._create_end_mill(
            specs, "10mm Carbide Roughing End Mill", tool_number
        )
        tool.tool_type = ToolType.ROUGHING_MILL
        tool.add_custom_property("application", "roughing")
        return tool

    # Finishing End Mills
    def finishing_carbide_3mm(self, tool_number: int = 31) -> "ToolInterface":
        """3mm Carbide finishing end mill."""
        specs = EndMillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=12.0,
            shank_diameter=3.0,
            flute_count=4,  # More flutes for better finish
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=22000,
            feed_rate=1320,
            plunge_rate=330,
            step_over=0.2,  # Fine step over for finishing
            step_down=0.3,  # Light cuts for finishing
        )
        tool = self._create_end_mill(
            specs, "3mm Carbide Finishing End Mill", tool_number
        )
        tool.tool_type = ToolType.FINISHING_MILL
        tool.add_custom_property("application", "finishing")
        return tool

    def finishing_carbide_6mm(self, tool_number: int = 32) -> "ToolInterface":
        """6mm Carbide finishing end mill."""
        specs = EndMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=4,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=20000,
            feed_rate=2400,
            plunge_rate=600,
            step_over=0.3,
            step_down=0.5,
        )
        tool = self._create_end_mill(
            specs, "6mm Carbide Finishing End Mill", tool_number
        )
        tool.tool_type = ToolType.FINISHING_MILL
        tool.add_custom_property("application", "finishing")
        return tool

    def get_all_presets(self) -> list["ToolInterface"]:
        """Get all end mill presets."""
        return [
            self.flat_hss_3mm(),
            self.flat_hss_6mm(),
            self.flat_hss_10mm(),
            self.flat_carbide_3mm(),
            self.flat_carbide_6mm(),
            self.flat_carbide_10mm(),
            self.roughing_carbide_6mm(),
            self.roughing_carbide_10mm(),
            self.finishing_carbide_3mm(),
            self.finishing_carbide_6mm(),
        ]
