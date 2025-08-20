"""
Transform operations interface for Part objects.
"""

from abc import ABC, abstractmethod
from codetocad.core.dimensions.length_expression import LengthType


class PartTransformInterface(ABC):
    """Interface for part transformation operations."""

    def __init__(self, part: "PartInterface"):
        self.part = part

    def translate(
        self, dx: LengthType, dy: LengthType, dz: LengthType = 0
    ) -> "PartInterface":
        """Translate the part."""
        return self.part.translate(dx, dy, dz)

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "PartInterface":
        """Rotate the part around an axis."""
        return self.part.rotate(axis, angle)

    def scale(
        self, scale_x: float, scale_y: float, scale_z: float = 1.0
    ) -> "PartInterface":
        """Scale the part."""
        return self.part.scale(scale_x, scale_y, scale_z)

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        return self.part.move(x, y, z)
