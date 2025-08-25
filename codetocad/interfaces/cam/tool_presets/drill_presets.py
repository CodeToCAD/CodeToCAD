"""
Drill tool presets for CAM operations.

Provides preset configurations for various drill types including
twist drills, center drills, and spot drills.
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
class DrillSpecs:
    """Specifications for drill tools."""

    diameter: float  # mm
    length: float  # mm
    cutting_length: float  # mm
    shank_diameter: float  # mm
    tip_angle: float = 118.0  # degrees (standard twist drill)
    material: ToolMaterial = ToolMaterial.HSS
    coating: str = "uncoated"

    # Cutting parameters for aluminum
    spindle_speed: float = 3000  # RPM
    feed_rate: float = 150  # mm/min
    plunge_rate: float = 150  # mm/min (same as feed for drilling)
    peck_depth: float = 3.0  # mm (for peck drilling)


class DrillPresets:
    """Preset drill configurations."""

    def __init__(self):
        pass

    def _create_drill(
        self, specs: DrillSpecs, name: str, tool_number: int = 1
    ) -> "ToolInterface":
        """Create a drill tool from specifications."""
        from codetocad.core.cam.tool import Tool  # Import concrete implementation

        tool = Tool()
        tool.set_name(name)
        tool.set_tool_number(tool_number)
        tool.tool_type = ToolType.DRILL
        tool.material = specs.material

        # Set geometry
        geometry = ToolGeometry(
            diameter=specs.diameter,
            length=specs.length,
            cutting_length=specs.cutting_length,
            shank_diameter=specs.shank_diameter,
            tip_angle=specs.tip_angle,
            flute_count=2,  # Standard for twist drills
        )
        tool.set_geometry(geometry)

        # Set cutting data
        cutting_data = CuttingData(
            spindle_speed=specs.spindle_speed,
            feed_rate=specs.feed_rate,
            plunge_rate=specs.plunge_rate,
            step_over=1.0,  # Not applicable for drilling
            step_down=specs.peck_depth,
        )
        tool.set_cutting_data(cutting_data)

        # Add custom properties
        tool.add_custom_property("coating", specs.coating)
        tool.add_custom_property("peck_depth", specs.peck_depth)
        tool.add_custom_property("preset_category", "drill")

        return tool

    # Standard HSS Twist Drills
    def twist_drill_hss_3mm(self, tool_number: int = 41) -> "ToolInterface":
        """3mm HSS twist drill."""
        specs = DrillSpecs(
            diameter=3.0,
            length=61.0,
            cutting_length=33.0,
            shank_diameter=3.0,
            tip_angle=118.0,
            material=ToolMaterial.HSS,
            spindle_speed=4000,
            feed_rate=120,
            plunge_rate=120,
            peck_depth=2.0,
        )
        return self._create_drill(specs, "3mm HSS Twist Drill", tool_number)

    def twist_drill_hss_5mm(self, tool_number: int = 42) -> "ToolInterface":
        """5mm HSS twist drill."""
        specs = DrillSpecs(
            diameter=5.0,
            length=86.0,
            cutting_length=52.0,
            shank_diameter=5.0,
            tip_angle=118.0,
            material=ToolMaterial.HSS,
            spindle_speed=3000,
            feed_rate=200,
            plunge_rate=200,
            peck_depth=3.0,
        )
        return self._create_drill(specs, "5mm HSS Twist Drill", tool_number)

    def twist_drill_hss_8mm(self, tool_number: int = 43) -> "ToolInterface":
        """8mm HSS twist drill."""
        specs = DrillSpecs(
            diameter=8.0,
            length=117.0,
            cutting_length=75.0,
            shank_diameter=8.0,
            tip_angle=118.0,
            material=ToolMaterial.HSS,
            spindle_speed=2000,
            feed_rate=320,
            plunge_rate=320,
            peck_depth=4.0,
        )
        return self._create_drill(specs, "8mm HSS Twist Drill", tool_number)

    def twist_drill_hss_10mm(self, tool_number: int = 44) -> "ToolInterface":
        """10mm HSS twist drill."""
        specs = DrillSpecs(
            diameter=10.0,
            length=133.0,
            cutting_length=87.0,
            shank_diameter=10.0,
            tip_angle=118.0,
            material=ToolMaterial.HSS,
            spindle_speed=1500,
            feed_rate=375,
            plunge_rate=375,
            peck_depth=5.0,
        )
        return self._create_drill(specs, "10mm HSS Twist Drill", tool_number)

    # Carbide Drills
    def twist_drill_carbide_3mm(self, tool_number: int = 51) -> "ToolInterface":
        """3mm Carbide twist drill."""
        specs = DrillSpecs(
            diameter=3.0,
            length=61.0,
            cutting_length=33.0,
            shank_diameter=3.0,
            tip_angle=140.0,  # Sharper angle for carbide
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=6000,
            feed_rate=180,
            plunge_rate=180,
            peck_depth=2.0,
        )
        return self._create_drill(specs, "3mm Carbide Twist Drill", tool_number)

    def twist_drill_carbide_5mm(self, tool_number: int = 52) -> "ToolInterface":
        """5mm Carbide twist drill."""
        specs = DrillSpecs(
            diameter=5.0,
            length=86.0,
            cutting_length=52.0,
            shank_diameter=5.0,
            tip_angle=140.0,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=4500,
            feed_rate=300,
            plunge_rate=300,
            peck_depth=3.0,
        )
        return self._create_drill(specs, "5mm Carbide Twist Drill", tool_number)

    def twist_drill_carbide_8mm(self, tool_number: int = 53) -> "ToolInterface":
        """8mm Carbide twist drill."""
        specs = DrillSpecs(
            diameter=8.0,
            length=117.0,
            cutting_length=75.0,
            shank_diameter=8.0,
            tip_angle=140.0,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=3000,
            feed_rate=480,
            plunge_rate=480,
            peck_depth=4.0,
        )
        return self._create_drill(specs, "8mm Carbide Twist Drill", tool_number)

    # Center Drills
    def center_drill_60_degree(self, tool_number: int = 61) -> "ToolInterface":
        """60° Center drill."""
        specs = DrillSpecs(
            diameter=2.5,  # Body diameter
            length=50.0,
            cutting_length=8.0,
            shank_diameter=6.0,
            tip_angle=60.0,
            material=ToolMaterial.HSS,
            spindle_speed=5000,
            feed_rate=100,
            plunge_rate=100,
            peck_depth=1.0,
        )
        tool = self._create_drill(specs, "60° Center Drill", tool_number)
        tool.add_custom_property("drill_type", "center")
        tool.add_custom_property("application", "center_drilling")
        return tool

    def center_drill_90_degree(self, tool_number: int = 62) -> "ToolInterface":
        """90° Center drill."""
        specs = DrillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=10.0,
            shank_diameter=6.0,
            tip_angle=90.0,
            material=ToolMaterial.HSS,
            spindle_speed=4000,
            feed_rate=120,
            plunge_rate=120,
            peck_depth=1.5,
        )
        tool = self._create_drill(specs, "90° Center Drill", tool_number)
        tool.add_custom_property("drill_type", "center")
        tool.add_custom_property("application", "center_drilling")
        return tool

    # Spot Drills
    def spot_drill_90_degree_6mm(self, tool_number: int = 71) -> "ToolInterface":
        """6mm 90° Spot drill."""
        specs = DrillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=15.0,
            shank_diameter=6.0,
            tip_angle=90.0,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=8000,
            feed_rate=240,
            plunge_rate=240,
            peck_depth=1.0,
        )
        tool = self._create_drill(specs, "6mm 90° Spot Drill", tool_number)
        tool.add_custom_property("drill_type", "spot")
        tool.add_custom_property("application", "spot_drilling")
        return tool

    def spot_drill_120_degree_8mm(self, tool_number: int = 72) -> "ToolInterface":
        """8mm 120° Spot drill."""
        specs = DrillSpecs(
            diameter=8.0,
            length=70.0,
            cutting_length=20.0,
            shank_diameter=8.0,
            tip_angle=120.0,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=6000,
            feed_rate=320,
            plunge_rate=320,
            peck_depth=1.5,
        )
        tool = self._create_drill(specs, "8mm 120° Spot Drill", tool_number)
        tool.add_custom_property("drill_type", "spot")
        tool.add_custom_property("application", "spot_drilling")
        return tool

    def get_all_presets(self) -> list["ToolInterface"]:
        """Get all drill presets."""
        return [
            # HSS Twist Drills
            self.twist_drill_hss_3mm(),
            self.twist_drill_hss_5mm(),
            self.twist_drill_hss_8mm(),
            self.twist_drill_hss_10mm(),
            # Carbide Twist Drills
            self.twist_drill_carbide_3mm(),
            self.twist_drill_carbide_5mm(),
            self.twist_drill_carbide_8mm(),
            # Center Drills
            self.center_drill_60_degree(),
            self.center_drill_90_degree(),
            # Spot Drills
            self.spot_drill_90_degree_6mm(),
            self.spot_drill_120_degree_8mm(),
        ]
