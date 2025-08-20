from abc import ABC
from codetocad.interfaces.cad.edge.edge_transform import EdgeTransformInterface
from codetocad.interfaces.cad.edge.edge_geometry_interface import EdgeGeometryInterface
from codetocad.interfaces.cad.edge.edge_operations_interface import (
    EdgeOperationsInterface,
)
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class EdgeInterface(ABC):
    def __init__(self, v1: "VertexInterface", v2: "VertexInterface"):
        self.v1: VertexInterface = v1
        self.v2: VertexInterface = v2
        self.transform = EdgeTransformInterface(self)
        self.name: str | None = None

        # Method group properties
        self.geometry = EdgeGeometryInterface(self)
        self.operations = EdgeOperationsInterface(self)

    def direction(self):
        return self.v2.position - self.v1.position

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
