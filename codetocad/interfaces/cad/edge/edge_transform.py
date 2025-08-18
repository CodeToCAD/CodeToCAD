import numpy as np

from codetocad.core.dimensions.length import Length


class EdgeTransformInterface:
    def __init__(self, edge):
        self.edge = edge

    def translate(self, dx, dy, dz=0):
        t = np.array(
            [
                [1, 0, 0, float(Length(dx))],
                [0, 1, 0, float(Length(dy))],
                [0, 0, 1, float(Length(dz))],
                [0, 0, 0, 1],
            ]
        )
        self.edge.v1.transform(t)
        self.edge.v2.transform(t)
