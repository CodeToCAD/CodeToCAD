from codetocad.interfaces.cad.edge.edge_transform import EdgeTransformInterface
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class EdgeInterface:
    def __init__(self, v1: "VertexInterface", v2: "VertexInterface"):
        self.v1: VertexInterface = v1
        self.v2: VertexInterface = v2
        self.transform = EdgeTransformInterface(self)

    def direction(self):
        return self.v2.position - self.v1.position

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
