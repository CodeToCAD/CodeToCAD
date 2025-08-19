from typing import TYPE_CHECKING

from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.core.dimensions.length import LengthType
from codetocad.adapters.blender.cad.edge.edge import Edge
from codetocad.adapters.blender.cad.vertex.vertex import Vertex

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.wire.wire import Wire


class WireAdd(WireAddInterface):
    """Blender-specific wire add operations."""

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
        v1 = self.wire.edges[-1].v2 if self.wire.edges else Vertex(0, 0, 0)
        v2 = Vertex(x, y, z)
        e = Edge(v1, v2)
        self.wire.edges.append(e)

        # Update Blender representation
        self.wire._update_blender_curve()

        return e
