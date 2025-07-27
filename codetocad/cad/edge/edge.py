from codetocad.cad.edge.edge_transform import EdgeTransform
from codetocad.cad.vertex.vertex import Vertex


class Edge:
    def __init__(self, v1: "Vertex", v2: "Vertex"):
        self.v1: Vertex = v1
        self.v2: Vertex = v2
        self.transform = EdgeTransform(self)

    def direction(self):
        return self.v2.position - self.v1.position

    def __repr__(self):
        return f"Edge({self.v1.position}, {self.v2.position})"
