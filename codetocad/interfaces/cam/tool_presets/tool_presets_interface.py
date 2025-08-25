"""
Tool presets interface for CAM operations.

Defines the abstract interface for tool preset systems with metaclass pattern
for easy access similar to Part.preset pattern.
"""

from abc import ABC, ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cam.tool_interface import ToolInterface
    from codetocad.interfaces.cam.tool_presets.end_mill_presets import EndMillPresets
    from codetocad.interfaces.cam.tool_presets.drill_presets import DrillPresets
    from codetocad.interfaces.cam.tool_presets.ball_mill_presets import BallMillPresets
    from codetocad.interfaces.cam.tool_presets.v_bit_presets import VBitPresets


class ToolPresetsInterface(ABC):
    """
    Abstract interface for tool presets.

    Provides access to common cutting tool configurations including:
    - End mills (flat, roughing, finishing)
    - Drills (twist, center, spot)
    - Ball mills (various sizes and materials)
    - V-bits (engraving and chamfering)
    """

    def __init__(self):
        self.end_mill: "EndMillPresets" = None  # Set by concrete implementations
        self.drill: "DrillPresets" = None
        self.ball_mill: "BallMillPresets" = None
        self.v_bit: "VBitPresets" = None

    def get_all_presets(self) -> list["ToolInterface"]:
        """Get all available tool presets."""
        presets = []

        if self.end_mill:
            presets.extend(self.end_mill.get_all_presets())
        if self.drill:
            presets.extend(self.drill.get_all_presets())
        if self.ball_mill:
            presets.extend(self.ball_mill.get_all_presets())
        if self.v_bit:
            presets.extend(self.v_bit.get_all_presets())

        return presets

    def find_tool_by_diameter(
        self, diameter: float, tool_type: str = None
    ) -> list["ToolInterface"]:
        """Find tools by diameter, optionally filtered by type."""
        all_presets = self.get_all_presets()
        matching_tools = []

        for tool in all_presets:
            if (
                tool.geometry and abs(tool.geometry.diameter - diameter) < 0.01
            ):  # 0.01mm tolerance
                if tool_type is None or tool.tool_type.value == tool_type:
                    matching_tools.append(tool)

        return matching_tools

    def get_recommended_tool(
        self, operation: str, material: str = "aluminum"
    ) -> "ToolInterface | None":
        """Get recommended tool for specific operation and material."""
        # This would contain logic to recommend appropriate tools
        # based on operation type and material properties

        operation_lower = operation.lower()
        material_lower = material.lower()

        if "rough" in operation_lower:
            if self.end_mill:
                return self.end_mill.roughing_carbide_6mm()
        elif "finish" in operation_lower:
            if self.end_mill:
                return self.end_mill.finishing_carbide_3mm()
        elif "drill" in operation_lower:
            if self.drill:
                return self.drill.twist_drill_hss_5mm()
        elif "engrave" in operation_lower:
            if self.v_bit:
                return self.v_bit.engraving_60_degree()

        return None
