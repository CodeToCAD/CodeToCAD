"""
Geometry operations interface for Part objects.
"""

from abc import ABC


class PartGeometryInterface(ABC):
    """Interface for part geometry operations."""

    def __init__(self, part: "PartInterface"):
        self.part = part

    def volume(self) -> float:
        """Get the volume of the part."""
        # Default implementation - adapters should override this
        return 0.0

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        # Default implementation - adapters should override this
        return ((0, 0, 0), (0, 0, 0))
