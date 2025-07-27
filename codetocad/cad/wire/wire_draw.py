from typing import TYPE_CHECKING
from codetocad.cad.edge.edge import Edge
from codetocad.cad.vertex.vertex import Vertex
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.cad.wire.wire import Wire


class WireDraw:
    def __init__(self, wire: "Wire"):
        self.wire = wire

    def point(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        v = Vertex(x, y, z)
        e = Edge(v, v)
        self.wire.edges.append(e)
        return e

    def line_to(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        """
        Draws a line from the last vertex of the wire to the specified coordinates.
        If the wire is empty, it starts from the origin (0, 0, 0).
        """
        v1 = self.wire.edges[-1].v1 if self.wire.edges else Vertex(0, 0, 0)
        v2 = Vertex(x, y, z)
        e = Edge(v1, v2)
        self.wire.edges.append(e)
        return e
