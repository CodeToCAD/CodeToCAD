"""
Work Coordinate System (WCS) interface for CAM operations.

Manages coordinate system setup, origin management, and transformations
between different coordinate systems used in machining.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Any, List
import math


class WCSOrigin(Enum):
    """Work coordinate system origin positions."""

    BOTTOM_LEFT_FRONT = "bottom_left_front"
    BOTTOM_CENTER_FRONT = "bottom_center_front"
    BOTTOM_RIGHT_FRONT = "bottom_right_front"
    CENTER_LEFT_FRONT = "center_left_front"
    CENTER_CENTER_FRONT = "center_center_front"
    CENTER_RIGHT_FRONT = "center_right_front"
    TOP_LEFT_FRONT = "top_left_front"
    TOP_CENTER_FRONT = "top_center_front"
    TOP_RIGHT_FRONT = "top_right_front"

    # Back positions
    BOTTOM_LEFT_BACK = "bottom_left_back"
    BOTTOM_CENTER_BACK = "bottom_center_back"
    BOTTOM_RIGHT_BACK = "bottom_right_back"
    CENTER_LEFT_BACK = "center_left_back"
    CENTER_CENTER_BACK = "center_center_back"
    CENTER_RIGHT_BACK = "center_right_back"
    TOP_LEFT_BACK = "top_left_back"
    TOP_CENTER_BACK = "top_center_back"
    TOP_RIGHT_BACK = "top_right_back"

    # Center positions
    BOTTOM_LEFT_CENTER = "bottom_left_center"
    BOTTOM_CENTER_CENTER = "bottom_center_center"
    BOTTOM_RIGHT_CENTER = "bottom_right_center"
    CENTER_LEFT_CENTER = "center_left_center"
    CENTER_CENTER_CENTER = "center_center_center"
    CENTER_RIGHT_CENTER = "center_right_center"
    TOP_LEFT_CENTER = "top_left_center"
    TOP_CENTER_CENTER = "top_center_center"
    TOP_RIGHT_CENTER = "top_right_center"


@dataclass
class CoordinateSystem:
    """Coordinate system definition with origin and orientation."""

    origin: tuple[float, float, float]  # X, Y, Z origin position
    rotation: tuple[float, float, float] = (
        0.0,
        0.0,
        0.0,
    )  # Rotation angles in degrees (X, Y, Z)
    name: str = "WCS"
    description: str = ""

    def __post_init__(self):
        """Validate coordinate system parameters."""
        if len(self.origin) != 3:
            raise ValueError("Origin must be a 3-tuple (x, y, z)")
        if len(self.rotation) != 3:
            raise ValueError("Rotation must be a 3-tuple (rx, ry, rz)")


@dataclass
class WorkpieceSetup:
    """Workpiece setup information."""

    length: float  # X dimension
    width: float  # Y dimension
    height: float  # Z dimension
    material_thickness: float | None = None  # For sheet materials
    stock_to_leave: float = 0.0  # Stock allowance for finishing
    fixture_height: float = 0.0  # Height of fixture/vise

    def __post_init__(self):
        """Validate workpiece dimensions."""
        if self.length <= 0:
            raise ValueError("Length must be positive")
        if self.width <= 0:
            raise ValueError("Width must be positive")
        if self.height <= 0:
            raise ValueError("Height must be positive")
        if self.stock_to_leave < 0:
            raise ValueError("Stock to leave cannot be negative")
        if self.fixture_height < 0:
            raise ValueError("Fixture height cannot be negative")


class WorkCoordinateSystemInterface(ABC):
    """Abstract interface for work coordinate system management."""

    def __init__(self):
        self.name: str = "WCS1"
        self.coordinate_system: CoordinateSystem | None = None
        self.workpiece_setup: WorkpieceSetup | None = None
        self.active: bool = True
        self.description: str = ""
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "WorkCoordinateSystemInterface":
        """Set the WCS name."""
        self.name = name
        return self

    def set_description(self, description: str) -> "WorkCoordinateSystemInterface":
        """Set the WCS description."""
        self.description = description
        return self

    def set_coordinate_system(
        self, coordinate_system: CoordinateSystem
    ) -> "WorkCoordinateSystemInterface":
        """Set the coordinate system definition."""
        self.coordinate_system = coordinate_system
        return self

    def set_workpiece_setup(
        self, workpiece_setup: WorkpieceSetup
    ) -> "WorkCoordinateSystemInterface":
        """Set the workpiece setup information."""
        self.workpiece_setup = workpiece_setup
        return self

    def activate(self) -> "WorkCoordinateSystemInterface":
        """Activate this coordinate system."""
        self.active = True
        return self

    def deactivate(self) -> "WorkCoordinateSystemInterface":
        """Deactivate this coordinate system."""
        self.active = False
        return self

    def set_origin_from_preset(
        self, origin_preset: WCSOrigin
    ) -> "WorkCoordinateSystemInterface":
        """Set origin based on preset position relative to workpiece."""
        if not self.workpiece_setup:
            raise ValueError("Workpiece setup must be defined before setting origin")

        # Calculate origin position based on preset
        x, y, z = self._calculate_origin_from_preset(origin_preset)

        if self.coordinate_system:
            self.coordinate_system.origin = (x, y, z)
        else:
            self.coordinate_system = CoordinateSystem(
                origin=(x, y, z), name=f"{self.name}_origin"
            )

        return self

    def _calculate_origin_from_preset(
        self, preset: WCSOrigin
    ) -> tuple[float, float, float]:
        """Calculate origin coordinates from preset position."""
        if not self.workpiece_setup:
            raise ValueError("Workpiece setup required")

        wp = self.workpiece_setup

        # X position mapping
        x_map = {"left": 0.0, "center": wp.length / 2.0, "right": wp.length}

        # Y position mapping
        y_map = {"front": 0.0, "center": wp.width / 2.0, "back": wp.width}

        # Z position mapping
        z_map = {
            "bottom": wp.fixture_height,
            "center": wp.fixture_height + wp.height / 2.0,
            "top": wp.fixture_height + wp.height,
        }

        # Parse preset name
        parts = preset.value.split("_")
        if len(parts) != 3:
            raise ValueError(f"Invalid preset format: {preset.value}")

        z_pos, x_pos, y_pos = parts

        x = x_map.get(x_pos, 0.0)
        y = y_map.get(y_pos, 0.0)
        z = z_map.get(z_pos, 0.0)

        return (x, y, z)

    def set_origin_manual(
        self, x: float, y: float, z: float
    ) -> "WorkCoordinateSystemInterface":
        """Set origin manually with specific coordinates."""
        if self.coordinate_system:
            self.coordinate_system.origin = (x, y, z)
        else:
            self.coordinate_system = CoordinateSystem(
                origin=(x, y, z), name=f"{self.name}_origin"
            )
        return self

    def set_rotation(
        self, rx: float, ry: float, rz: float
    ) -> "WorkCoordinateSystemInterface":
        """Set coordinate system rotation in degrees."""
        if self.coordinate_system:
            self.coordinate_system.rotation = (rx, ry, rz)
        else:
            self.coordinate_system = CoordinateSystem(
                origin=(0.0, 0.0, 0.0),
                rotation=(rx, ry, rz),
                name=f"{self.name}_rotation",
            )
        return self

    def transform_point_to_machine(
        self, point: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """Transform a point from WCS to machine coordinates."""
        if not self.coordinate_system:
            return point

        x, y, z = point
        ox, oy, oz = self.coordinate_system.origin
        rx, ry, rz = self.coordinate_system.rotation

        # Apply rotation (simplified - assumes small angles)
        if any(angle != 0 for angle in (rx, ry, rz)):
            # Convert to radians
            rx_rad = math.radians(rx)
            ry_rad = math.radians(ry)
            rz_rad = math.radians(rz)

            # Apply Z rotation (most common)
            if rz != 0:
                cos_rz = math.cos(rz_rad)
                sin_rz = math.sin(rz_rad)
                x_rot = x * cos_rz - y * sin_rz
                y_rot = x * sin_rz + y * cos_rz
                x, y = x_rot, y_rot

        # Apply translation
        return (x + ox, y + oy, z + oz)

    def transform_point_from_machine(
        self, point: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        """Transform a point from machine coordinates to WCS."""
        if not self.coordinate_system:
            return point

        x, y, z = point
        ox, oy, oz = self.coordinate_system.origin
        rx, ry, rz = self.coordinate_system.rotation

        # Remove translation
        x, y, z = x - ox, y - oy, z - oz

        # Remove rotation (reverse of forward transform)
        if any(angle != 0 for angle in (rx, ry, rz)):
            rx_rad = math.radians(-rx)  # Negative for reverse
            ry_rad = math.radians(-ry)
            rz_rad = math.radians(-rz)

            # Remove Z rotation
            if rz != 0:
                cos_rz = math.cos(rz_rad)
                sin_rz = math.sin(rz_rad)
                x_rot = x * cos_rz - y * sin_rz
                y_rot = x * sin_rz + y * cos_rz
                x, y = x_rot, y_rot

        return (x, y, z)

    def get_workpiece_bounds(
        self,
    ) -> tuple[tuple[float, float, float | None, tuple[float, float, float]]]:
        """Get workpiece bounding box in machine coordinates."""
        if not self.workpiece_setup or not self.coordinate_system:
            return None

        wp = self.workpiece_setup

        # Workpiece corners in WCS
        corners = [
            (0, 0, wp.fixture_height),
            (wp.length, 0, wp.fixture_height),
            (0, wp.width, wp.fixture_height),
            (wp.length, wp.width, wp.fixture_height),
            (0, 0, wp.fixture_height + wp.height),
            (wp.length, 0, wp.fixture_height + wp.height),
            (0, wp.width, wp.fixture_height + wp.height),
            (wp.length, wp.width, wp.fixture_height + wp.height),
        ]

        # Transform to machine coordinates
        machine_corners = [
            self.transform_point_to_machine(corner) for corner in corners
        ]

        # Find bounding box
        min_x = min(corner[0] for corner in machine_corners)
        max_x = max(corner[0] for corner in machine_corners)
        min_y = min(corner[1] for corner in machine_corners)
        max_y = max(corner[1] for corner in machine_corners)
        min_z = min(corner[2] for corner in machine_corners)
        max_z = max(corner[2] for corner in machine_corners)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def validate(self) -> list[str]:
        """Validate WCS configuration."""
        issues = []

        if not self.name:
            issues.append("WCS name is required")

        if not self.coordinate_system:
            issues.append("Coordinate system is required")

        if not self.workpiece_setup:
            issues.append("Workpiece setup is required")

        # Validate coordinate system
        if self.coordinate_system:
            try:
                # Validation happens in __post_init__
                pass
            except ValueError as e:
                issues.append(f"Coordinate system error: {e}")

        # Validate workpiece setup
        if self.workpiece_setup:
            try:
                # Validation happens in __post_init__
                pass
            except ValueError as e:
                issues.append(f"Workpiece setup error: {e}")

        return issues

    @abstractmethod
    def copy(self) -> "WorkCoordinateSystemInterface":
        """Create a copy of the WCS."""
        pass

    def __repr__(self) -> str:
        origin = (
            self.coordinate_system.origin if self.coordinate_system else "undefined"
        )
        active_status = "active" if self.active else "inactive"
        return f"<WCS: {self.name}, origin={origin}, {active_status}>"
