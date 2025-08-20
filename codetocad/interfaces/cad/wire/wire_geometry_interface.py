"""
Geometry operations interface for Wire objects.
"""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class WireGeometryInterface(ABC):
    """Interface for wire geometry operations."""

    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    def is_closed(self) -> bool:
        """Check if the wire is closed."""
        if not self.wire.edges:
            return False

        # Get first and last vertices
        first_vertex = self.wire.edges[0].v1
        last_vertex = self.wire.edges[-1].v2

        # Check if they are at the same position (within tolerance)
        tolerance = 1e-6
        distance = first_vertex.geometry.distance_to(last_vertex)
        return distance < tolerance

    def length(self) -> float:
        """Get the total length of the wire."""
        return sum(edge.geometry.length() for edge in self.wire.edges)

    def vertices(self) -> list["VertexInterface"]:
        """Get all unique vertices in the wire."""
        vertices = []
        for edge in self.wire.edges:
            if edge.v1 not in vertices:
                vertices.append(edge.v1)
            if edge.v2 not in vertices:
                vertices.append(edge.v2)
        return vertices

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the wire as (min_point, max_point)."""
        if not self.wire.edges:
            return ((0, 0, 0), (0, 0, 0))

        vertices = self.vertices()
        positions = [v.position for v in vertices]

        min_x = min(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        min_z = min(pos[2] for pos in positions)

        max_x = max(pos[0] for pos in positions)
        max_y = max(pos[1] for pos in positions)
        max_z = max(pos[2] for pos in positions)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))
