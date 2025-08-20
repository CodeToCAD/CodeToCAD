"""
build123d implementation of EdgeInterface.
"""

from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.adapters.build123d.cad.vertex.vertex import Vertex
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_edge_from_vertices,
)
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
    get_length,
)

if TYPE_CHECKING:
    import build123d as bd


class Edge(EdgeInterface):
    """build123d implementation of EdgeInterface."""

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str | None = None,
        native_instance: "bd.Edge | None" = None,
    ):
        # Initialize the parent interface
        super().__init__(v1, v2)

        # build123d-specific properties
        self.name = name or f"edge_{str(uuid4())[:8]}"

        # Create or use provided build123d edge
        if native_instance is not None:
            self.native_instance = native_instance
        else:
            self.native_instance = create_edge_from_vertices(
                v1.native_instance, v2.native_instance
            )

    def length(self) -> float:
        """Get the length of the edge."""
        return get_length(self.native_instance)

    def midpoint(self) -> "Vertex":
        """Get the midpoint of the edge."""
        mid_pos = (self.v1.position + self.v2.position) / 2
        return Vertex(mid_pos[0], mid_pos[1], mid_pos[2])

    def direction_vector(self) -> tuple[float, float, float]:
        """Get the direction vector of the edge."""
        direction = self.direction()
        return tuple(direction)

    def is_parallel_to(self, other: "Edge", tolerance: float = 1e-6) -> bool:
        """Check if this edge is parallel to another edge."""
        import numpy as np

        dir1 = self.direction()
        dir2 = other.direction()

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if cross product is near zero (parallel) or near 1 (anti-parallel)
        cross_product = np.cross(dir1_norm, dir2_norm)
        cross_magnitude = np.linalg.norm(cross_product)

        return cross_magnitude < tolerance

    def is_perpendicular_to(self, other: "Edge", tolerance: float = 1e-6) -> bool:
        """Check if this edge is perpendicular to another edge."""
        import numpy as np

        dir1 = self.direction()
        dir2 = other.direction()

        # Normalize vectors
        dir1_norm = dir1 / np.linalg.norm(dir1)
        dir2_norm = dir2 / np.linalg.norm(dir2)

        # Check if dot product is near zero
        dot_product = np.dot(dir1_norm, dir2_norm)

        return abs(dot_product) < tolerance

    def split_at_parameter(self, parameter: float) -> tuple["Edge", "Edge"]:
        """Split the edge at a given parameter (0.0 to 1.0)."""
        # Calculate the split point
        split_pos = self.v1.position + parameter * self.direction()
        split_vertex = Vertex(split_pos[0], split_pos[1], split_pos[2])

        # Create two new edges
        edge1 = Edge(self.v1, split_vertex)
        edge2 = Edge(split_vertex, self.v2)

        return edge1, edge2

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
