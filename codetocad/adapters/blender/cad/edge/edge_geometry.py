"""
Blender implementation of EdgeGeometryInterface.
"""

from codetocad.interfaces.cad.edge.edge_geometry_interface import EdgeGeometryInterface
import numpy as np


class EdgeGeometry(EdgeGeometryInterface):
    """Blender implementation of edge geometry operations."""

    def length(self) -> float:
        """Calculate the length of the edge."""
        return float(np.linalg.norm(self.edge.direction()))

    def midpoint(self) -> "VertexInterface":
        """Get the midpoint of the edge as a new Vertex."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.vertex.vertex import Vertex

        mid_pos = (self.edge.v1.position + self.edge.v2.position) / 2
        return Vertex(mid_pos[0], mid_pos[1], mid_pos[2])

    def direction_vector(self) -> tuple[float, float, float]:
        """Get the direction vector of the edge."""
        direction = self.edge.direction()
        return tuple(direction)

    def is_parallel_to(self, other: "EdgeInterface", tolerance: float = 1e-6) -> bool:
        """Check if this edge is parallel to another edge."""
        dir1 = self.edge.direction()
        dir2 = other.direction()

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
        dir1 = self.edge.direction()
        dir2 = other.direction()

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if dot product is near zero
        dot_product = np.dot(dir1_norm, dir2_norm)

        return abs(dot_product) < tolerance
