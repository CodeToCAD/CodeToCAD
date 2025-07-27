from dataclasses import dataclass
from typing import TypeAlias

from codetocad.core.dimensions.length import LengthType


@dataclass
class WireOperationExtrude:
    length: LengthType


WireOperation: TypeAlias = WireOperationExtrude
