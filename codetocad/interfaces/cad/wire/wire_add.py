from typing import TYPE_CHECKING
from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface
from codetocad.core.dimensions.length import Length, LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class WireAddInterface:
    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    def point(self, x: LengthType, y: LengthType, z: LengthType = 0) -> EdgeInterface:
        v = VertexInterface(x, y, z)
        e = EdgeInterface(v, v)
        self.wire.edges.append(e)
        return e

    def line_to(self, x: LengthType, y: LengthType, z: LengthType = 0) -> EdgeInterface:
        """
        Draws a line from the last vertex of the wire to the specified coordinates.
        If the wire is empty, it starts from the origin (0, 0, 0).
        """
        v1 = self.wire.edges[-1].v1 if self.wire.edges else VertexInterface(0, 0, 0)
        v2 = VertexInterface(x, y, z)
        e = EdgeInterface(v1, v2)
        self.wire.edges.append(e)

        x = Length(x)
        y = Length(y)
        z = Length(z)

        return e
