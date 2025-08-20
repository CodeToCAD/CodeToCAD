from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


if TYPE_CHECKING:
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


@dataclass
class WireConstraintCoincidentInterface:
    v1: VertexInterface
    v2: VertexInterface


@dataclass
class WireConstraintMidpointInterface:
    edge: EdgeInterface
    target: VertexInterface


@dataclass
class WireConstraintParallelInterface:
    edge1: EdgeInterface
    edge2: EdgeInterface


@dataclass
class WireConstraintPerpendicularInterface:
    edge1: EdgeInterface
    edge2: EdgeInterface


@dataclass
class WireConstraintTangentInterface:
    edge: EdgeInterface
    wire: "WireInterface"


WireOperationConstraintType: TypeAlias = (
    WireConstraintCoincidentInterface
    | WireConstraintMidpointInterface
    | WireConstraintParallelInterface
    | WireConstraintPerpendicularInterface
    | WireConstraintTangentInterface
)


class WireConstraintInterface:
    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    def coincident(self, v1: "VertexInterface", v2: "VertexInterface"): ...

    def midpoint(self, edge: "EdgeInterface", target: "VertexInterface"): ...

    def parallel(self, e1: "EdgeInterface", e2: "EdgeInterface"): ...

    def perpendicular(self, e1: "EdgeInterface", e2: "EdgeInterface"): ...

    def tangent(self, wire: "WireInterface", edge: "EdgeInterface"): ...
