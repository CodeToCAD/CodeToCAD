"""
Blender implementation of WireGeometryInterface.
"""

from codetocad.interfaces.cad.wire.wire_geometry_interface import WireGeometryInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class WireGeometry(WireGeometryInterface):
    """Blender implementation of wire geometry operations."""

    def is_closed(self) -> bool:
        """Check if the wire forms a closed loop."""
        if len(self.wire.edges) < 3:
            return False

        # Use a small tolerance for comparison
        tolerance = 1e-6
        first_vertex = self.wire.edges[0].v1
        last_vertex = self.wire.edges[-1].v2
        distance = first_vertex.geometry.distance_to(last_vertex)
        return distance < tolerance

    def length(self) -> float:
        """Calculate the total length of the wire."""
        return sum(edge.geometry.length() for edge in self.wire.edges)

    def vertices(self) -> list["VertexInterface"]:
        """Get all vertices in the wire."""
        vertices = []
        if self.wire.edges:
            vertices.append(self.wire.edges[0].v1)
            for edge in self.wire.edges:
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
