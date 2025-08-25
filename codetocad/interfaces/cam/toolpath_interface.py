"""
Toolpath interface for CAM operations.

Defines the abstract interface for toolpath generation including
2D/3D milling, drilling, contouring, and pocketing operations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Any, TYPE_CHECKING
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cam.tool_interface import ToolInterface
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface


class ToolpathStrategy(Enum):
    """Toolpath generation strategies."""

    # 2D strategies
    PROFILE = "profile"  # Follow contour/outline
    POCKET = "pocket"  # Clear material from enclosed area
    DRILLING = "drilling"  # Point drilling operations
    ENGRAVING = "engraving"  # Surface engraving

    # 2.5D strategies
    ADAPTIVE_CLEARING = "adaptive_clearing"  # Adaptive roughing
    CONVENTIONAL_CLEARING = "conventional_clearing"  # Traditional roughing

    # 3D strategies
    WATERLINE = "waterline"  # Constant Z-level passes
    SPIRAL = "spiral"  # Spiral toolpath
    RAMP = "ramp"  # Ramping entry
    SURFACE_FINISHING = "surface_finishing"  # 3D surface finishing
    PARALLEL_FINISHING = "parallel_finishing"  # Parallel passes
    RADIAL_FINISHING = "radial_finishing"  # Radial passes


class ToolpathOperation(Enum):
    """Types of machining operations."""

    ROUGHING = "roughing"  # Material removal
    SEMI_FINISHING = "semi_finishing"  # Intermediate finishing
    FINISHING = "finishing"  # Final surface quality
    DRILLING = "drilling"  # Hole making
    THREADING = "threading"  # Thread cutting
    CHAMFERING = "chamfering"  # Edge chamfering
    DEBURRING = "deburring"  # Edge cleanup


@dataclass
class CuttingParameters:
    """Parameters for cutting operations."""

    depth_of_cut: float  # Total depth to cut (mm)
    step_down: float  # Maximum depth per pass (mm)
    step_over: float  # Step over as percentage of tool diameter
    feed_rate: float  # Feed rate (mm/min)
    spindle_speed: float  # Spindle speed (RPM)
    plunge_rate: float  # Z-axis feed rate (mm/min)

    # Safety parameters
    safe_height: float = 5.0  # Safe Z height above workpiece (mm)
    clearance_height: float = 2.0  # Clearance height for rapid moves (mm)

    # Advanced parameters
    lead_in_distance: float | None = None  # Lead-in distance (mm)
    lead_out_distance: float | None = None  # Lead-out distance (mm)
    ramp_angle: float | None = None  # Ramp angle for entry (degrees)
    finish_passes: int = 0  # Number of finish passes

    def __post_init__(self):
        """Validate cutting parameters."""
        if self.depth_of_cut <= 0:
            raise ValueError("Depth of cut must be positive")
        if self.step_down <= 0:
            raise ValueError("Step down must be positive")
        if not 0.0 < self.step_over <= 1.0:
            raise ValueError("Step over must be between 0.0 and 1.0")
        if self.feed_rate <= 0:
            raise ValueError("Feed rate must be positive")
        if self.spindle_speed <= 0:
            raise ValueError("Spindle speed must be positive")
        if self.plunge_rate <= 0:
            raise ValueError("Plunge rate must be positive")


@dataclass
class ToolpathPoint:
    """A point in a toolpath with position and motion data."""

    x: float
    y: float
    z: float
    feed_rate: float | None = None  # Override feed rate for this point
    rapid_move: bool = False  # True for rapid positioning
    spindle_on: bool | None = None  # Spindle state override
    coolant_on: bool | None = None  # Coolant state override


class ToolpathInterface(ABC):
    """Abstract interface for toolpath generation."""

    def __init__(self):
        self.name: str = "default_toolpath"
        self.operation: ToolpathOperation = ToolpathOperation.ROUGHING
        self.strategy: ToolpathStrategy = ToolpathStrategy.PROFILE
        self.tool: "ToolInterface" | None = None
        self.cutting_parameters: CuttingParameters | None = None
        self.points: list[ToolpathPoint] = []
        self.description: str = ""
        self.enabled: bool = True
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "ToolpathInterface":
        """Set the toolpath name."""
        self.name = name
        return self

    def set_operation(self, operation: ToolpathOperation) -> "ToolpathInterface":
        """Set the machining operation type."""
        self.operation = operation
        return self

    def set_strategy(self, strategy: ToolpathStrategy) -> "ToolpathInterface":
        """Set the toolpath generation strategy."""
        self.strategy = strategy
        return self

    def set_tool(self, tool: "ToolInterface") -> "ToolpathInterface":
        """Set the cutting tool for this toolpath."""
        self.tool = tool
        return self

    def set_cutting_parameters(
        self, parameters: CuttingParameters
    ) -> "ToolpathInterface":
        """Set the cutting parameters."""
        self.cutting_parameters = parameters
        return self

    def set_description(self, description: str) -> "ToolpathInterface":
        """Set the toolpath description."""
        self.description = description
        return self

    def enable(self) -> "ToolpathInterface":
        """Enable this toolpath for processing."""
        self.enabled = True
        return self

    def disable(self) -> "ToolpathInterface":
        """Disable this toolpath from processing."""
        self.enabled = False
        return self

    def add_custom_property(self, key: str, value: Any) -> "ToolpathInterface":
        """Add a custom property."""
        self.custom_properties[key] = value
        return self

    @abstractmethod
    def generate_from_sketch(self, sketch: "SketchInterface") -> "ToolpathInterface":
        """Generate toolpath from a 2D sketch."""
        pass

    @abstractmethod
    def generate_from_part(self, part: "PartInterface") -> "ToolpathInterface":
        """Generate toolpath from a 3D part."""
        pass

    @abstractmethod
    def generate_drilling_pattern(
        self, points: list[tuple[float, float]], depth: float
    ) -> "ToolpathInterface":
        """Generate drilling toolpath from point coordinates."""
        pass

    @abstractmethod
    def optimize_toolpath(self) -> "ToolpathInterface":
        """Optimize the toolpath for efficiency and quality."""
        pass

    def get_total_length(self) -> float:
        """Calculate total toolpath length."""
        if len(self.points) < 2:
            return 0.0

        total_length = 0.0
        for i in range(1, len(self.points)):
            p1 = self.points[i - 1]
            p2 = self.points[i]

            # Skip rapid moves for cutting length calculation
            if not p2.rapid_move:
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dz = p2.z - p1.z
                length = (dx * dx + dy * dy + dz * dz) ** 0.5
                total_length += length

        return total_length

    def get_machining_time_estimate(self) -> float:
        """Estimate machining time in minutes."""
        if not self.cutting_parameters or len(self.points) < 2:
            return 0.0

        cutting_time = 0.0
        rapid_time = 0.0

        for i in range(1, len(self.points)):
            p1 = self.points[i - 1]
            p2 = self.points[i]

            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dz = p2.z - p1.z
            distance = (dx * dx + dy * dy + dz * dz) ** 0.5

            if p2.rapid_move:
                # Assume rapid rate of 10000 mm/min
                rapid_time += distance / 10000.0
            else:
                feed_rate = p2.feed_rate or self.cutting_parameters.feed_rate
                cutting_time += distance / feed_rate

        return cutting_time + rapid_time

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float | None, tuple[float, float, float]]]:
        """Get bounding box of toolpath (min_point, max_point)."""
        if not self.points:
            return None

        min_x = min_y = min_z = float("inf")
        max_x = max_y = max_z = float("-inf")

        for point in self.points:
            min_x = min(min_x, point.x)
            max_x = max(max_x, point.x)
            min_y = min(min_y, point.y)
            max_y = max(max_y, point.y)
            min_z = min(min_z, point.z)
            max_z = max(max_z, point.z)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def validate(self) -> list[str]:
        """Validate toolpath configuration."""
        issues = []

        if not self.name:
            issues.append("Toolpath name is required")

        if not self.tool:
            issues.append("Tool is required")

        if not self.cutting_parameters:
            issues.append("Cutting parameters are required")

        if not self.points:
            issues.append("Toolpath has no points")

        # Validate cutting parameters if present
        if self.cutting_parameters:
            try:
                # Validation happens in __post_init__
                pass
            except ValueError as e:
                issues.append(f"Cutting parameters error: {e}")

        return issues

    @abstractmethod
    def copy(self) -> "ToolpathInterface":
        """Create a copy of the toolpath."""
        pass

    def __repr__(self) -> str:
        point_count = len(self.points)
        length = self.get_total_length()
        return f"<Toolpath: {self.name}, {self.strategy.value}, {point_count} points, {length:.2f}mm>"
