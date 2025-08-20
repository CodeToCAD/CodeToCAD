import numpy as np
from codetocad.core.dimensions.length_expression import LengthExpression, LengthType


class VertexInterface:
    def __init__(self, x: LengthType, y: LengthType, z: LengthType = 0):
        self.position = np.array(
            [
                float(LengthExpression(x)),
                float(LengthExpression(y)),
                float(LengthExpression(z)),
            ]
        )

    def transform(self, matrix):
        pos = np.append(self.position, 1)
        self.position = (matrix @ pos)[:3]

    def __repr__(self):
        return f"Vertex({self.position})"
