"""
Blender implementation of EdgeOperationsInterface.
"""

from codetocad.interfaces.cad.edge.edge_operations_interface import (
    EdgeOperationsInterface,
)


class EdgeOperations(EdgeOperationsInterface):
    """Blender implementation of edge operations."""

    def split_at_parameter(
        self, parameter: float
    ) -> tuple["EdgeInterface", "EdgeInterface"]:
        """Split the edge at a given parameter (0.0 to 1.0)."""
        # Import here to avoid circular imports
        from codetocad.adapters.blender.cad.edge.edge import Edge
        from codetocad.adapters.blender.cad.vertex.vertex import Vertex

        # Calculate the split point
        split_pos = self.edge.v1.position + parameter * self.edge.direction()
        split_vertex = Vertex(split_pos[0], split_pos[1], split_pos[2])

        # Create two new edges
        edge1 = Edge(self.edge.v1, split_vertex)
        edge2 = Edge(split_vertex, self.edge.v2)

        return edge1, edge2
