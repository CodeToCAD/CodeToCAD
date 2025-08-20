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
        import numpy as np

        direction = self.edge.v2.position - self.edge.v1.position
        return float(np.linalg.norm(direction))

    def midpoint(self) -> "VertexInterface":
        """Get the midpoint of the edge."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific vertex type
        raise NotImplementedError("midpoint must be implemented by concrete classes")

    def direction_vector(self) -> tuple[float, float, float]:
        """Get the direction vector of the edge."""
        direction = self.edge.v2.position - self.edge.v1.position
        return tuple(direction)

    def is_parallel_to(self, other: "EdgeInterface", tolerance: float = 1e-6) -> bool:
        """Check if this edge is parallel to another edge."""
        import numpy as np

        dir1 = self.edge.v2.position - self.edge.v1.position
        dir2 = other.v2.position - other.v1.position

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if cross product is near zero (parallel) or near 1 (anti-parallel)
        cross_product = np.cross(dir1_norm, dir2_norm)
        cross_magnitude = np.linalg.norm(cross_product)

        return cross_magnitude < tolerance

    def is_perpendicular_to(
        self, other: "EdgeInterface", tolerance: float = 1e-6
    ) -> bool:
        """Check if this edge is perpendicular to another edge."""
        import numpy as np

        dir1 = self.edge.v2.position - self.edge.v1.position
        dir2 = other.v2.position - other.v1.position

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if dot product is near zero (perpendicular)
        dot_product = np.dot(dir1_norm, dir2_norm)
        return abs(dot_product) < tolerance
