"""
Transform operations interface for Part objects.
"""

from abc import ABC
from codetocad.core.dimensions.length_expression import LengthType


class PartTransformInterface(ABC):
    """Interface for part transformation operations."""

    def __init__(self, part: "PartInterface"):
        self.part = part

    def translate(
        self, dx: LengthType, dy: LengthType, dz: LengthType = 0
    ) -> "PartInterface":
        """Translate the part."""
        # Default implementation - adapters should override this
        return self.part

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "PartInterface":
        """Rotate the part around an axis."""
        # Default implementation - adapters should override this
        return self.part

    def scale(
        self, scale_x: float, scale_y: float, scale_z: float = 1.0
    ) -> "PartInterface":
        """Scale the part."""
        # Default implementation - adapters should override this
        return self.part

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        # Default implementation - adapters should override this
        pass
