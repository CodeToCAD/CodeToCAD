from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

from codetocad.cad.edge.edge import Edge
from codetocad.cad.vertex.vertex import Vertex
from codetocad.cad.wire.wire_operations import WireOperationConstraint


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

    def coincident(self, v1: "Vertex", v2: "Vertex"):
        self.wire._add_operation(
            WireOperationConstraint(WireConstraintCoincident(v1=v1, v2=v2))
        )

    def midpoint(self, edge: "Edge", target: "Vertex"):
        self.wire._add_operation(
            WireOperationConstraint(WireConstraintMidpoint(edge=edge, target=target))
        )

    def parallel(self, e1: "Edge", e2: "Edge"):
        self.wire._add_operation(
            WireOperationConstraint(WireConstraintParallel(edge1=e1, edge2=e2))
        )

    def perpendicular(self, e1: "Edge", e2: "Edge"):
        self.wire._add_operation(
            WireOperationConstraint(WireConstraintPerpendicular(edge1=e1, edge2=e2))
        )

    def tangent(self, wire: "Wire", edge: "Edge"):
        self.wire._add_operation(
            WireOperationConstraint(WireConstraintTangent(wire=wire, edge=edge))
        )
