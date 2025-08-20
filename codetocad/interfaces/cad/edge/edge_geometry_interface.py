"""
Geometry operations interface for Edge objects.
"""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class EdgeGeometryInterface(ABC):
    """Interface for edge geometry operations."""

    def __init__(self, edge: "EdgeInterface"):
        self.edge = edge

    def length(self) -> float:
        """Get the length of the edge."""
        return self.edge.length()

    def midpoint(self) -> "VertexInterface":
        """Get the midpoint of the edge."""
        return self.edge.midpoint()

    def direction_vector(self) -> tuple[float, float, float]:
        """Get the direction vector of the edge."""
        return self.edge.direction_vector()

    def is_parallel_to(self, other: "EdgeInterface", tolerance: float = 1e-6) -> bool:
        """Check if this edge is parallel to another edge."""
        return self.edge.is_parallel_to(other, tolerance)

    def is_perpendicular_to(
        self, other: "EdgeInterface", tolerance: float = 1e-6
    ) -> bool:
        """Check if this edge is perpendicular to another edge."""
        return self.edge.is_perpendicular_to(other, tolerance)
