"""
Tool presets for CAM operations.

This module provides preset definitions for common cutting tools
including geometry, cutting parameters, and material specifications.
"""

from codetocad.interfaces.cam.tool_presets.tool_presets_interface import (
    ToolPresetsInterface,
)
from codetocad.interfaces.cam.tool_presets.end_mill_presets import EndMillPresets
from codetocad.interfaces.cam.tool_presets.drill_presets import DrillPresets
from codetocad.interfaces.cam.tool_presets.ball_mill_presets import BallMillPresets
from codetocad.interfaces.cam.tool_presets.v_bit_presets import VBitPresets

__all__ = [
    "ToolPresetsInterface",
    "EndMillPresets",
    "DrillPresets",
    "BallMillPresets",
    "VBitPresets",
]
