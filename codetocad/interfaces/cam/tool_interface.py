"""
Tool interface for CAM operations.

Defines the abstract interface for cutting tools including geometry,
material properties, and cutting parameters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
from codetocad.core.dimensions.length_expression import LengthType


class ToolType(Enum):
    """Types of cutting tools."""

    FLAT_END_MILL = "flat_end_mill"
    BALL_END_MILL = "ball_end_mill"
    BULL_NOSE_MILL = "bull_nose_mill"
    V_BIT = "v_bit"
    DRILL = "drill"
    CHAMFER_MILL = "chamfer_mill"
    THREAD_MILL = "thread_mill"
    SLOT_DRILL = "slot_drill"
    ROUGHING_MILL = "roughing_mill"
    FINISHING_MILL = "finishing_mill"


class ToolMaterial(Enum):
    """Tool material types."""

    HSS = "high_speed_steel"
    CARBIDE = "carbide"
    CERAMIC = "ceramic"
    DIAMOND = "diamond"
    CBN = "cubic_boron_nitride"


@dataclass
class ToolGeometry:
    """Tool geometry specifications."""

    diameter: float  # Tool diameter in mm
    length: float  # Overall tool length in mm
    cutting_length: float  # Length of cutting edges in mm
    shank_diameter: float  # Shank diameter in mm
    corner_radius: float | None = None  # Corner radius for bull nose tools
    tip_angle: float | None = None  # Tip angle for V-bits and drills
    helix_angle: float | None = None  # Helix angle in degrees
    flute_count: int = 2  # Number of cutting flutes

    def __post_init__(self):
        """Validate geometry parameters."""
        if self.diameter <= 0:
            raise ValueError("Tool diameter must be positive")
        if self.length <= 0:
            raise ValueError("Tool length must be positive")
        if self.cutting_length <= 0:
            raise ValueError("Cutting length must be positive")
        if self.cutting_length > self.length:
            raise ValueError("Cutting length cannot exceed overall length")


@dataclass
class CuttingData:
    """Cutting parameters and feeds/speeds."""

    spindle_speed: float  # RPM
    feed_rate: float  # mm/min
    plunge_rate: float  # mm/min for Z-axis moves
    step_over: float  # Percentage of tool diameter (0.0-1.0)
    step_down: float  # Maximum depth per pass in mm

    # Optional advanced parameters
    climb_milling: bool = True  # True for climb, False for conventional
    coolant: bool = False  # Coolant usage
    chip_load: float | None = None  # mm per tooth
    surface_speed: float | None = None  # m/min

    def __post_init__(self):
        """Validate cutting parameters."""
        if self.spindle_speed <= 0:
            raise ValueError("Spindle speed must be positive")
        if self.feed_rate <= 0:
            raise ValueError("Feed rate must be positive")
        if self.plunge_rate <= 0:
            raise ValueError("Plunge rate must be positive")
        if not 0.0 < self.step_over <= 1.0:
            raise ValueError("Step over must be between 0.0 and 1.0")
        if self.step_down <= 0:
            raise ValueError("Step down must be positive")


class ToolInterface(ABC):
    """Abstract interface for cutting tools."""

    def __init__(self):
        self.name: str = "default_tool"
        self.tool_number: int = 1
        self.tool_type: ToolType = ToolType.FLAT_END_MILL
        self.material: ToolMaterial = ToolMaterial.HSS
        self.geometry: ToolGeometry | None = None
        self.cutting_data: CuttingData | None = None
        self.description: str = ""
        self.manufacturer: str = ""
        self.part_number: str = ""
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "ToolInterface":
        """Set the tool name."""
        self.name = name
        return self

    def set_tool_number(self, number: int) -> "ToolInterface":
        """Set the tool number for machine tool changer."""
        if number <= 0:
            raise ValueError("Tool number must be positive")
        self.tool_number = number
        return self

    def set_geometry(self, geometry: ToolGeometry) -> "ToolInterface":
        """Set the tool geometry."""
        self.geometry = geometry
        return self

    def set_cutting_data(self, cutting_data: CuttingData) -> "ToolInterface":
        """Set the cutting parameters."""
        self.cutting_data = cutting_data
        return self

    def set_description(self, description: str) -> "ToolInterface":
        """Set the tool description."""
        self.description = description
        return self

    def set_manufacturer(self, manufacturer: str) -> "ToolInterface":
        """Set the tool manufacturer."""
        self.manufacturer = manufacturer
        return self

    def set_part_number(self, part_number: str) -> "ToolInterface":
        """Set the manufacturer part number."""
        self.part_number = part_number
        return self

    def add_custom_property(self, key: str, value: Any) -> "ToolInterface":
        """Add a custom property to the tool."""
        self.custom_properties[key] = value
        return self

    def get_custom_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property value."""
        return self.custom_properties.get(key, default)

    def calculate_chip_load(self) -> float | None:
        """Calculate chip load based on feed rate and spindle speed."""
        if not self.cutting_data or not self.geometry:
            return None

        if self.cutting_data.chip_load is not None:
            return self.cutting_data.chip_load

        # Chip load = Feed rate / (Spindle speed * Flute count)
        return self.cutting_data.feed_rate / (
            self.cutting_data.spindle_speed * self.geometry.flute_count
        )

    def calculate_surface_speed(self) -> float | None:
        """Calculate surface speed based on diameter and spindle speed."""
        if not self.cutting_data or not self.geometry:
            return None

        if self.cutting_data.surface_speed is not None:
            return self.cutting_data.surface_speed

        # Surface speed = π * diameter * RPM / 1000 (m/min)
        import math

        return (
            math.pi * self.geometry.diameter * self.cutting_data.spindle_speed / 1000.0
        )

    def validate(self) -> list[str]:
        """Validate tool configuration and return list of issues."""
        issues = []

        if not self.name:
            issues.append("Tool name is required")

        if self.tool_number <= 0:
            issues.append("Tool number must be positive")

        if not self.geometry:
            issues.append("Tool geometry is required")

        if not self.cutting_data:
            issues.append("Cutting data is required")

        # Validate geometry and cutting data if present
        try:
            if self.geometry:
                # Geometry validation happens in __post_init__
                pass
        except ValueError as e:
            issues.append(f"Geometry error: {e}")

        try:
            if self.cutting_data:
                # Cutting data validation happens in __post_init__
                pass
        except ValueError as e:
            issues.append(f"Cutting data error: {e}")

        return issues

    @abstractmethod
    def copy(self) -> "ToolInterface":
        """Create a copy of the tool."""
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert tool to dictionary representation."""
        pass

    @abstractmethod
    def from_dict(self, data: dict[str, Any]) -> "ToolInterface":
        """Load tool from dictionary representation."""
        pass

    def __repr__(self) -> str:
        diameter = self.geometry.diameter if self.geometry else "unknown"
        return f"<Tool: {self.name} (#{self.tool_number}), {self.tool_type.value}, ⌀{diameter}mm>"
