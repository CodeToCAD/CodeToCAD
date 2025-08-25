"""
Concrete implementation of Tool interface with preset support.
"""

import copy
from typing import Dict, Any
from abc import ABCMeta

from codetocad.interfaces.cam.tool_interface import ToolInterface
from codetocad.interfaces.cam.tool_presets.tool_presets_interface import (
    ToolPresetsInterface,
)
from codetocad.interfaces.cam.tool_presets.end_mill_presets import EndMillPresets
from codetocad.interfaces.cam.tool_presets.drill_presets import DrillPresets
from codetocad.interfaces.cam.tool_presets.ball_mill_presets import BallMillPresets
from codetocad.interfaces.cam.tool_presets.v_bit_presets import VBitPresets


class _ToolPresetClassProperty(ABCMeta):
    """Metaclass to provide Tool.preset class property."""

    @property
    def preset(cls):
        """Access to tool presets."""
        return ToolPresets()


class Tool(ToolInterface, metaclass=_ToolPresetClassProperty):
    """Concrete implementation of ToolInterface with preset support."""

    def copy(self) -> "Tool":
        """Create a copy of the tool."""
        new_tool = Tool()

        # Copy basic properties
        new_tool.name = self.name
        new_tool.tool_number = self.tool_number
        new_tool.tool_type = self.tool_type
        new_tool.material = self.material
        new_tool.description = self.description
        new_tool.manufacturer = self.manufacturer
        new_tool.part_number = self.part_number

        # Deep copy geometry and cutting data
        if self.geometry:
            new_tool.geometry = copy.deepcopy(self.geometry)
        if self.cutting_data:
            new_tool.cutting_data = copy.deepcopy(self.cutting_data)

        # Copy custom properties
        new_tool.custom_properties = copy.deepcopy(self.custom_properties)

        return new_tool

    def to_dict(self) -> dict[str, Any]:
        """Convert tool to dictionary representation."""
        data = {
            "name": self.name,
            "tool_number": self.tool_number,
            "tool_type": self.tool_type.value,
            "material": self.material.value,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "part_number": self.part_number,
            "custom_properties": self.custom_properties,
        }

        # Add geometry if present
        if self.geometry:
            data["geometry"] = {
                "diameter": self.geometry.diameter,
                "length": self.geometry.length,
                "cutting_length": self.geometry.cutting_length,
                "shank_diameter": self.geometry.shank_diameter,
                "corner_radius": self.geometry.corner_radius,
                "tip_angle": self.geometry.tip_angle,
                "helix_angle": self.geometry.helix_angle,
                "flute_count": self.geometry.flute_count,
            }

        # Add cutting data if present
        if self.cutting_data:
            data["cutting_data"] = {
                "spindle_speed": self.cutting_data.spindle_speed,
                "feed_rate": self.cutting_data.feed_rate,
                "plunge_rate": self.cutting_data.plunge_rate,
                "step_over": self.cutting_data.step_over,
                "step_down": self.cutting_data.step_down,
                "climb_milling": self.cutting_data.climb_milling,
                "coolant": self.cutting_data.coolant,
                "chip_load": self.cutting_data.chip_load,
                "surface_speed": self.cutting_data.surface_speed,
            }

        return data

    def from_dict(self, data: dict[str, Any]) -> "Tool":
        """Load tool from dictionary representation."""
        from codetocad.interfaces.cam.tool_interface import (
            ToolType,
            ToolMaterial,
            ToolGeometry,
            CuttingData,
        )

        self.name = data.get("name", "default_tool")
        self.tool_number = data.get("tool_number", 1)
        self.tool_type = ToolType(data.get("tool_type", "flat_end_mill"))
        self.material = ToolMaterial(data.get("material", "high_speed_steel"))
        self.description = data.get("description", "")
        self.manufacturer = data.get("manufacturer", "")
        self.part_number = data.get("part_number", "")
        self.custom_properties = data.get("custom_properties", {})

        # Load geometry if present
        geometry_data = data.get("geometry")
        if geometry_data:
            self.geometry = ToolGeometry(
                diameter=geometry_data["diameter"],
                length=geometry_data["length"],
                cutting_length=geometry_data["cutting_length"],
                shank_diameter=geometry_data["shank_diameter"],
                corner_radius=geometry_data.get("corner_radius"),
                tip_angle=geometry_data.get("tip_angle"),
                helix_angle=geometry_data.get("helix_angle"),
                flute_count=geometry_data.get("flute_count", 2),
            )

        # Load cutting data if present
        cutting_data = data.get("cutting_data")
        if cutting_data:
            self.cutting_data = CuttingData(
                spindle_speed=cutting_data["spindle_speed"],
                feed_rate=cutting_data["feed_rate"],
                plunge_rate=cutting_data["plunge_rate"],
                step_over=cutting_data["step_over"],
                step_down=cutting_data["step_down"],
                climb_milling=cutting_data.get("climb_milling", True),
                coolant=cutting_data.get("coolant", False),
                chip_load=cutting_data.get("chip_load"),
                surface_speed=cutting_data.get("surface_speed"),
            )

        return self


class ToolPresets(ToolPresetsInterface):
    """Concrete implementation of tool presets."""

    def __init__(self):
        super().__init__()
        self.end_mill = EndMillPresets()
        self.drill = DrillPresets()
        self.ball_mill = BallMillPresets()
        self.v_bit = VBitPresets()


# Tool.preset is now available via the metaclass
