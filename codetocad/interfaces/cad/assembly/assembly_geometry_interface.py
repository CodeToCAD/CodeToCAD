"""
Geometry operations interface for Assembly objects.
"""

from abc import ABC


class AssemblyGeometryInterface(ABC):
    """Interface for assembly geometry operations."""

    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire assembly."""
        return self.assembly.get_bounding_box()

    def total_volume(self) -> float:
        """Get the total volume of all parts in the assembly."""
        return self.assembly.get_total_volume()
