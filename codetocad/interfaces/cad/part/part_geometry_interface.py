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
        return self.part.get_volume()

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        return self.part.get_bounding_box()
