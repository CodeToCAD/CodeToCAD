"""
Ball mill tool presets for CAM operations.

Provides preset configurations for ball end mills used in
3D surface machining and finishing operations.
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
class BallMillSpecs:
    """Specifications for ball mill tools."""

    diameter: float  # mm
    length: float  # mm
    cutting_length: float  # mm
    shank_diameter: float  # mm
    flute_count: int = 2
    helix_angle: float = 30.0  # degrees
    material: ToolMaterial = ToolMaterial.HSS
    coating: str = "uncoated"

    # Cutting parameters for aluminum (3D operations)
    spindle_speed: float = 15000  # RPM
    feed_rate: float = 800  # mm/min (slower for 3D work)
    plunge_rate: float = 200  # mm/min
    step_over: float = 0.1  # 10% of diameter for finishing
    step_down: float = 0.2  # mm (light cuts for ball mills)


class BallMillPresets:
    """Preset ball mill configurations."""

    def __init__(self):
        pass

    def _create_ball_mill(
        self, specs: BallMillSpecs, name: str, tool_number: int = 1
    ) -> "ToolInterface":
        """Create a ball mill tool from specifications."""
        from codetocad.core.cam.tool import Tool  # Import concrete implementation

        tool = Tool()
        tool.set_name(name)
        tool.set_tool_number(tool_number)
        tool.tool_type = ToolType.BALL_END_MILL
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
        tool.add_custom_property("preset_category", "ball_mill")
        tool.add_custom_property("application", "3d_finishing")

        return tool

    # Small Ball Mills for Detail Work
    def ball_mill_hss_1mm(self, tool_number: int = 81) -> "ToolInterface":
        """1mm HSS ball mill for fine detail work."""
        specs = BallMillSpecs(
            diameter=1.0,
            length=50.0,
            cutting_length=3.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=20000,
            feed_rate=200,
            plunge_rate=50,
            step_over=0.05,  # 5% for fine finishing
            step_down=0.05,
        )
        return self._create_ball_mill(specs, "1mm HSS Ball Mill", tool_number)

    def ball_mill_carbide_1mm(self, tool_number: int = 82) -> "ToolInterface":
        """1mm Carbide ball mill for fine detail work."""
        specs = BallMillSpecs(
            diameter=1.0,
            length=50.0,
            cutting_length=3.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=25000,
            feed_rate=300,
            plunge_rate=75,
            step_over=0.05,
            step_down=0.05,
        )
        return self._create_ball_mill(specs, "1mm Carbide Ball Mill", tool_number)

    # Standard Ball Mills
    def ball_mill_hss_3mm(self, tool_number: int = 83) -> "ToolInterface":
        """3mm HSS ball mill."""
        specs = BallMillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=12.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=18000,
            feed_rate=540,
            plunge_rate=135,
            step_over=0.15,
            step_down=0.15,
        )
        return self._create_ball_mill(specs, "3mm HSS Ball Mill", tool_number)

    def ball_mill_carbide_3mm(self, tool_number: int = 84) -> "ToolInterface":
        """3mm Carbide ball mill."""
        specs = BallMillSpecs(
            diameter=3.0,
            length=50.0,
            cutting_length=12.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=22000,
            feed_rate=660,
            plunge_rate=165,
            step_over=0.15,
            step_down=0.15,
        )
        return self._create_ball_mill(specs, "3mm Carbide Ball Mill", tool_number)

    def ball_mill_hss_6mm(self, tool_number: int = 85) -> "ToolInterface":
        """6mm HSS ball mill."""
        specs = BallMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=15000,
            feed_rate=900,
            plunge_rate=225,
            step_over=0.3,
            step_down=0.3,
        )
        return self._create_ball_mill(specs, "6mm HSS Ball Mill", tool_number)

    def ball_mill_carbide_6mm(self, tool_number: int = 86) -> "ToolInterface":
        """6mm Carbide ball mill."""
        specs = BallMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=18000,
            feed_rate=1080,
            plunge_rate=270,
            step_over=0.3,
            step_down=0.3,
        )
        return self._create_ball_mill(specs, "6mm Carbide Ball Mill", tool_number)

    # Large Ball Mills for Roughing
    def ball_mill_carbide_10mm(self, tool_number: int = 87) -> "ToolInterface":
        """10mm Carbide ball mill for roughing."""
        specs = BallMillSpecs(
            diameter=10.0,
            length=75.0,
            cutting_length=30.0,
            shank_diameter=10.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=12000,
            feed_rate=1200,
            plunge_rate=300,
            step_over=0.5,  # Larger step over for roughing
            step_down=0.5,
        )
        tool = self._create_ball_mill(specs, "10mm Carbide Ball Mill", tool_number)
        tool.add_custom_property("application", "3d_roughing")
        return tool

    def ball_mill_carbide_12mm(self, tool_number: int = 88) -> "ToolInterface":
        """12mm Carbide ball mill for heavy roughing."""
        specs = BallMillSpecs(
            diameter=12.0,
            length=80.0,
            cutting_length=35.0,
            shank_diameter=12.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=10000,
            feed_rate=1200,
            plunge_rate=300,
            step_over=0.6,
            step_down=0.6,
        )
        tool = self._create_ball_mill(specs, "12mm Carbide Ball Mill", tool_number)
        tool.add_custom_property("application", "3d_roughing")
        return tool

    # High-Performance Ball Mills
    def ball_mill_carbide_6mm_4_flute(self, tool_number: int = 89) -> "ToolInterface":
        """6mm 4-flute Carbide ball mill for high-quality finishing."""
        specs = BallMillSpecs(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=4,  # More flutes for better finish
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=20000,
            feed_rate=1600,  # Higher feed with more flutes
            plunge_rate=400,
            step_over=0.2,
            step_down=0.2,
        )
        tool = self._create_ball_mill(
            specs, "6mm 4-Flute Carbide Ball Mill", tool_number
        )
        tool.add_custom_property("application", "high_quality_finishing")
        return tool

    def ball_mill_carbide_3mm_long_reach(
        self, tool_number: int = 90
    ) -> "ToolInterface":
        """3mm Long-reach Carbide ball mill for deep cavities."""
        specs = BallMillSpecs(
            diameter=3.0,
            length=75.0,
            cutting_length=25.0,  # Extended cutting length
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=20000,
            feed_rate=480,  # Reduced for stability
            plunge_rate=120,
            step_over=0.1,
            step_down=0.1,
        )
        tool = self._create_ball_mill(
            specs, "3mm Long-Reach Carbide Ball Mill", tool_number
        )
        tool.add_custom_property("application", "deep_cavity_finishing")
        return tool

    def get_all_presets(self) -> list["ToolInterface"]:
        """Get all ball mill presets."""
        return [
            # Small detail mills
            self.ball_mill_hss_1mm(),
            self.ball_mill_carbide_1mm(),
            # Standard ball mills
            self.ball_mill_hss_3mm(),
            self.ball_mill_carbide_3mm(),
            self.ball_mill_hss_6mm(),
            self.ball_mill_carbide_6mm(),
            # Large roughing mills
            self.ball_mill_carbide_10mm(),
            self.ball_mill_carbide_12mm(),
            # High-performance mills
            self.ball_mill_carbide_6mm_4_flute(),
            self.ball_mill_carbide_3mm_long_reach(),
        ]
