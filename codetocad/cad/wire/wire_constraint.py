from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

from codetocad.cad.edge.edge import Edge
from codetocad.cad.vertex.vertex import Vertex


if TYPE_CHECKING:
    from codetocad.cad.wire.wire import Wire


@dataclass
class WireConstraintCoincident:
    v1: Vertex
    v2: Vertex


@dataclass
class WireConstraintMidpoint:
    edge: Edge
    target: Vertex


@dataclass
class WireConstraintParallel:
    edge1: Edge
    edge2: Edge


@dataclass
class WireConstraintPerpendicular:
    edge1: Edge
    edge2: Edge


@dataclass
class WireConstraintTangent:
    edge: Edge
    wire: "Wire"


WireOperationConstraintType: TypeAlias = (
    WireConstraintCoincident
    | WireConstraintMidpoint
    | WireConstraintParallel
    | WireConstraintPerpendicular
    | WireConstraintTangent
)


class WireConstraint:
    def __init__(self, wire: "Wire"):
        self.wire = wire

    def coincident(self, v1: "Vertex", v2: "Vertex"): ...

    def midpoint(self, edge: "Edge", target: "Vertex"): ...

    def parallel(self, e1: "Edge", e2: "Edge"): ...

    def perpendicular(self, e1: "Edge", e2: "Edge"): ...

    def tangent(self, wire: "Wire", edge: "Edge"): ...
