import numpy as np
from codetocad.core.dimensions.length import Length, LengthType


class Vertex:
    def __init__(self, x: LengthType, y: LengthType, z: LengthType = 0):
        self.position = np.array([float(Length(x)), float(Length(y)), float(Length(z))])

    def transform(self, matrix):
        pos = np.append(self.position, 1)
        self.position = (matrix @ pos)[:3]

    def __repr__(self):
        return f"Vertex({self.position})"
