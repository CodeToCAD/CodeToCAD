from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from codetocad.cad.wire.wire_constraint import WireOperationConstraintType
    from codetocad.core.dimensions.length import LengthType


@dataclass
class WireOperationExtrude:
    length: "LengthType"


@dataclass
class WireOperationConstraint:
    constraint: "WireOperationConstraintType"


WireOperationType: TypeAlias = WireOperationExtrude | WireOperationConstraint
