from typing import TYPE_CHECKING

from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


if TYPE_CHECKING:
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class WireGetInterface:
    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    @property
    def edges(self) -> list[EdgeInterface]:
        return self.wire.edges

    @property
    def vertices(self) -> list[VertexInterface]:
        return [vertex for edge in self.wire.edges for vertex in [edge.v1, edge.v2]]

    def vertex(self, i) -> "VertexInterface":
        return self.vertices[i]

    def edge(self, i) -> "EdgeInterface":
        return self.edges[i]
