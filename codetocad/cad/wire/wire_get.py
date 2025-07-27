from typing import TYPE_CHECKING

from codetocad.cad.edge.edge import Edge
from codetocad.cad.vertex.vertex import Vertex


if TYPE_CHECKING:
    from codetocad.cad.wire.wire import Wire


class WireGet:
    def __init__(self, wire: "Wire"):
        self.wire = wire

    def vertex(self, i) -> "Vertex":
        return [vertex for edge in self.wire.edges for vertex in [edge.v1, edge.v2]][i]

    def edge(self, i) -> "Edge":
        return self.wire.edges[i]
