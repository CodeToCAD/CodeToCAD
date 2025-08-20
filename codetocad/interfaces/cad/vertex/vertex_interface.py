import numpy as np
from abc import ABC
from codetocad.core.dimensions.length_expression import LengthExpression, LengthType
from codetocad.core.dimensions.point import Point
from codetocad.interfaces.cad.vertex.vertex_geometry_interface import (
    VertexGeometryInterface,
)


class VertexInterface(ABC):
    def __init__(self, x: LengthType, y: LengthType, z: LengthType = 0):
        self.position = np.array(
            [
                float(LengthExpression(x)),
                float(LengthExpression(y)),
                float(LengthExpression(z)),
            ]
        )
        self.name: str | None = None

        # Method group properties
        self.geometry = VertexGeometryInterface(self)

    def transform(self, matrix):
        pos = np.append(self.position, 1)
        self.position = (matrix @ pos)[:3]

    def __repr__(self):
        return f"Vertex({self.position})"
