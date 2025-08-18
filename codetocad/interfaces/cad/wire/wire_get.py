from typing import TYPE_CHECKING

from codetocad.interfaces.cad.edge.edge import Edge
from codetocad.interfaces.cad.vertex.vertex import Vertex


if TYPE_CHECKING:
    from codetocad.interfaces.cad.wire.wire import Wire


class WireGet:
    def __init__(self, wire: "Wire"):
        self.wire = wire

    @property
    def edges(self) -> list[Edge]:
        return self.wire.edges

    @property
    def vertices(self) -> list[Vertex]:
        return [vertex for edge in self.wire.edges for vertex in [edge.v1, edge.v2]]

    def vertex(self, i) -> "Vertex":
        return self.vertices[i]

    def edge(self, i) -> "Edge":
        return self.edges[i]
