from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias


if TYPE_CHECKING:
    from codetocad.cad.wire.wire_constraint import WireOperationConstraintType
from codetocad.core.dimensions.length import Length


@dataclass
class WireOperationLineTo:
    x: Length
    y: Length
    z: Length = Length(0)


@dataclass
class WireOperationExtrude:
    length: "Length"


@dataclass
class WireOperationConstraint:
    constraint: "WireOperationConstraintType"


WireOperationType: TypeAlias = (
    WireOperationExtrude | WireOperationConstraint | WireOperationLineTo
)
