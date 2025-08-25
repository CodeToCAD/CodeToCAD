"""
V-bit tool presets for CAM operations.

Provides preset configurations for V-bits used in
engraving, chamfering, and decorative operations.
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
class VBitSpecs:
    """Specifications for V-bit tools."""

    tip_angle: float  # degrees (60°, 90°, 120°, etc.)
    cutting_diameter: float  # mm (maximum cutting diameter)
    length: float  # mm
    cutting_length: float  # mm
    shank_diameter: float  # mm
    flute_count: int = 2
    material: ToolMaterial = ToolMaterial.HSS
    coating: str = "uncoated"

    # Cutting parameters for aluminum (engraving operations)
    spindle_speed: float = 18000  # RPM
    feed_rate: float = 600  # mm/min
    plunge_rate: float = 150  # mm/min
    step_over: float = 0.5  # mm (constant step over for engraving)
    step_down: float = 0.1  # mm (light cuts for engraving)


class VBitPresets:
    """Preset V-bit configurations."""

    def __init__(self):
        pass

    def _create_v_bit(
        self, specs: VBitSpecs, name: str, tool_number: int = 1
    ) -> "ToolInterface":
        """Create a V-bit tool from specifications."""
        from codetocad.core.cam.tool import Tool  # Import concrete implementation

        tool = Tool()
        tool.set_name(name)
        tool.set_tool_number(tool_number)
        tool.tool_type = ToolType.V_BIT
        tool.material = specs.material

        # Set geometry
        geometry = ToolGeometry(
            diameter=specs.cutting_diameter,
            length=specs.length,
            cutting_length=specs.cutting_length,
            shank_diameter=specs.shank_diameter,
            tip_angle=specs.tip_angle,
            flute_count=specs.flute_count,
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
        tool.add_custom_property("preset_category", "v_bit")
        tool.add_custom_property("tip_angle", specs.tip_angle)

        return tool

    # Standard Engraving V-bits
    def engraving_60_degree(self, tool_number: int = 91) -> "ToolInterface":
        """60° V-bit for fine engraving."""
        specs = VBitSpecs(
            tip_angle=60.0,
            cutting_diameter=6.0,
            length=50.0,
            cutting_length=15.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=20000,
            feed_rate=500,
            plunge_rate=125,
            step_over=0.2,
            step_down=0.05,
        )
        tool = self._create_v_bit(specs, "60° Engraving V-bit", tool_number)
        tool.add_custom_property("application", "fine_engraving")
        return tool

    def engraving_90_degree(self, tool_number: int = 92) -> "ToolInterface":
        """90° V-bit for general engraving."""
        specs = VBitSpecs(
            tip_angle=90.0,
            cutting_diameter=8.0,
            length=50.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=18000,
            feed_rate=600,
            plunge_rate=150,
            step_over=0.3,
            step_down=0.1,
        )
        tool = self._create_v_bit(specs, "90° Engraving V-bit", tool_number)
        tool.add_custom_property("application", "general_engraving")
        return tool

    def engraving_120_degree(self, tool_number: int = 93) -> "ToolInterface":
        """120° V-bit for wide engraving."""
        specs = VBitSpecs(
            tip_angle=120.0,
            cutting_diameter=10.0,
            length=50.0,
            cutting_length=25.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=15000,
            feed_rate=750,
            plunge_rate=188,
            step_over=0.5,
            step_down=0.15,
        )
        tool = self._create_v_bit(specs, "120° Engraving V-bit", tool_number)
        tool.add_custom_property("application", "wide_engraving")
        return tool

    # Chamfering V-bits
    def chamfer_45_degree(self, tool_number: int = 94) -> "ToolInterface":
        """45° V-bit for chamfering edges."""
        specs = VBitSpecs(
            tip_angle=90.0,  # 45° per side = 90° included angle
            cutting_diameter=12.0,
            length=60.0,
            cutting_length=30.0,
            shank_diameter=8.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=12000,
            feed_rate=1200,
            plunge_rate=300,
            step_over=1.0,
            step_down=0.5,
        )
        tool = self._create_v_bit(specs, "45° Chamfer V-bit", tool_number)
        tool.add_custom_property("application", "chamfering")
        tool.tool_type = ToolType.CHAMFER_MILL
        return tool

    def chamfer_30_degree(self, tool_number: int = 95) -> "ToolInterface":
        """30° V-bit for shallow chamfers."""
        specs = VBitSpecs(
            tip_angle=60.0,  # 30° per side = 60° included angle
            cutting_diameter=10.0,
            length=60.0,
            cutting_length=25.0,
            shank_diameter=8.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=15000,
            feed_rate=1000,
            plunge_rate=250,
            step_over=0.8,
            step_down=0.3,
        )
        tool = self._create_v_bit(specs, "30° Chamfer V-bit", tool_number)
        tool.add_custom_property("application", "shallow_chamfering")
        tool.tool_type = ToolType.CHAMFER_MILL
        return tool

    # Specialty V-bits
    def sign_making_90_degree(self, tool_number: int = 96) -> "ToolInterface":
        """90° V-bit optimized for sign making."""
        specs = VBitSpecs(
            tip_angle=90.0,
            cutting_diameter=12.0,
            length=60.0,
            cutting_length=30.0,
            shank_diameter=6.0,
            flute_count=1,  # Single flute for better chip evacuation
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=16000,
            feed_rate=800,
            plunge_rate=200,
            step_over=0.4,
            step_down=0.2,
        )
        tool = self._create_v_bit(specs, "90° Sign Making V-bit", tool_number)
        tool.add_custom_property("application", "sign_making")
        return tool

    def micro_engraving_30_degree(self, tool_number: int = 97) -> "ToolInterface":
        """30° V-bit for micro engraving."""
        specs = VBitSpecs(
            tip_angle=30.0,
            cutting_diameter=3.0,
            length=50.0,
            cutting_length=10.0,
            shank_diameter=3.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="Diamond",
            spindle_speed=25000,
            feed_rate=300,
            plunge_rate=75,
            step_over=0.1,
            step_down=0.02,
        )
        tool = self._create_v_bit(specs, "30° Micro Engraving V-bit", tool_number)
        tool.add_custom_property("application", "micro_engraving")
        return tool

    def decorative_60_degree_ball_nose(self, tool_number: int = 98) -> "ToolInterface":
        """60° Ball nose V-bit for decorative work."""
        specs = VBitSpecs(
            tip_angle=60.0,
            cutting_diameter=8.0,
            length=50.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.CARBIDE,
            coating="TiAlN",
            spindle_speed=18000,
            feed_rate=540,
            plunge_rate=135,
            step_over=0.3,
            step_down=0.1,
        )
        tool = self._create_v_bit(specs, "60° Ball Nose V-bit", tool_number)
        tool.add_custom_property("application", "decorative_engraving")
        tool.add_custom_property("tip_style", "ball_nose")
        return tool

    # HSS V-bits for softer materials
    def engraving_90_degree_hss(self, tool_number: int = 99) -> "ToolInterface":
        """90° HSS V-bit for wood and plastics."""
        specs = VBitSpecs(
            tip_angle=90.0,
            cutting_diameter=8.0,
            length=50.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
            material=ToolMaterial.HSS,
            spindle_speed=12000,
            feed_rate=800,
            plunge_rate=200,
            step_over=0.4,
            step_down=0.2,
        )
        tool = self._create_v_bit(specs, "90° HSS V-bit", tool_number)
        tool.add_custom_property("application", "wood_plastic_engraving")
        return tool

    def get_all_presets(self) -> list["ToolInterface"]:
        """Get all V-bit presets."""
        return [
            # Standard engraving V-bits
            self.engraving_60_degree(),
            self.engraving_90_degree(),
            self.engraving_120_degree(),
            # Chamfering V-bits
            self.chamfer_45_degree(),
            self.chamfer_30_degree(),
            # Specialty V-bits
            self.sign_making_90_degree(),
            self.micro_engraving_30_degree(),
            self.decorative_60_degree_ball_nose(),
            self.engraving_90_degree_hss(),
        ]
