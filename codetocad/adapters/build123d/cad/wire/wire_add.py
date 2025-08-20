"""
build123d-specific wire add operations.
"""

from typing import TYPE_CHECKING

from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.cad.edge.edge import Edge
from codetocad.adapters.build123d.cad.vertex.vertex import Vertex

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.wire.wire import Wire


class WireAdd(WireAddInterface):
    """build123d-specific wire add operations."""

    def __init__(self, wire: "Wire"):
        self.wire = wire

    def point(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        """Add a point to the wire."""
        v = Vertex(x, y, z)
        e = Edge(v, v)
        self.wire.edges.append(e)

        # Update the native build123d wire
        self.wire._update_native_wire()

        return e

    def line_to(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        """
        Draws a line from the last vertex of the wire to the specified coordinates.
        If the wire is empty, it starts from the origin (0, 0, 0).
        """
        # Get the starting vertex
        if self.wire.edges:
            v1 = self.wire.edges[-1].v2
        else:
            v1 = Vertex(0, 0, 0)

        # Create the end vertex
        v2 = Vertex(x, y, z)

        # Create the edge
        e = Edge(v1, v2)
        self.wire.edges.append(e)

        # Update the native build123d wire
        self.wire._update_native_wire()

        return e

    def arc_to(
        self,
        x: LengthType,
        y: LengthType,
        z: LengthType = 0,
        radius: LengthType = None,
        center_x: LengthType = None,
        center_y: LengthType = None,
        center_z: LengthType = 0,
    ) -> Edge:
        """
        Draws an arc from the last vertex of the wire to the specified coordinates.
        """
        # Get the starting vertex
        if self.wire.edges:
            v1 = self.wire.edges[-1].v2
        else:
            v1 = Vertex(0, 0, 0)

        # Create the end vertex
        v2 = Vertex(x, y, z)

        # For now, create a simple line edge
        # TODO: Implement proper arc creation with build123d
        e = Edge(v1, v2)
        self.wire.edges.append(e)

        # Update the native build123d wire
        self.wire._update_native_wire()

        return e

    def spline_to(
        self, points: list[tuple[LengthType, LengthType, LengthType]]
    ) -> Edge:
        """
        Draws a spline through the specified points.
        """
        if not points:
            raise ValueError("At least one point is required for spline")

        # Get the starting vertex
        if self.wire.edges:
            v1 = self.wire.edges[-1].v2
        else:
            v1 = Vertex(0, 0, 0)

        # For now, create line segments to each point
        # TODO: Implement proper spline creation with build123d
        last_vertex = v1
        last_edge = None

        for point in points:
            v2 = Vertex(point[0], point[1], point[2])
            e = Edge(last_vertex, v2)
            self.wire.edges.append(e)
            last_vertex = v2
            last_edge = e

        # Update the native build123d wire
        self.wire._update_native_wire()

        return last_edge

    def close(self) -> Edge:
        """Close the wire by connecting the last vertex to the first vertex."""
        if len(self.wire.edges) < 2:
            raise ValueError("Wire must have at least 2 edges to close")

        # Get first and last vertices
        first_vertex = self.wire.edges[0].v1
        last_vertex = self.wire.edges[-1].v2

        # Create closing edge
        e = Edge(last_vertex, first_vertex)
        self.wire.edges.append(e)

        # Update the native build123d wire
        self.wire._update_native_wire()

        return e
