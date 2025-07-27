from typing import TYPE_CHECKING
import numpy as np

from codetocad.cad.edge.edge import Edge
from codetocad.cad.vertex.vertex import Vertex


if TYPE_CHECKING:
    from codetocad.cad.wire.wire import Wire


class WireConstraint:
    def __init__(self, wire: "Wire"):
        self.wire = wire

    def coincident(self, v1: Vertex, v2: Vertex):
        v2.position[:] = v1.position

    def midpoint(self, v1: Vertex, v2: Vertex, target: Vertex):
        target.position[:] = (v1.position + v2.position) / 2

    def parallel(self, e1: Edge, e2: Edge):
        d1 = e1.direction()
        d2_len = np.linalg.norm(e2.direction())
        unit_d1 = d1 / np.linalg.norm(d1)
        e2.v2.position[:] = e2.v1.position + unit_d1 * d2_len

    def perpendicular(self, e1: Edge, e2: Edge):
        d1 = e1.direction()
        d2 = e2.direction()
        proj = d2 - np.dot(d2, d1) / np.dot(d1, d1) * d1
        e2.v2.position[:] = e2.v1.position + proj

    def tangent(self, e1: Edge, e2: Edge):
        e2.v1.position[:] = e1.v2.position
