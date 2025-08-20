"""
Operations interface for Wire objects.
"""

from abc import ABC
from codetocad.core.dimensions.length_expression import LengthType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class WireOperationsInterface(ABC):
    """Interface for wire operations."""

    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    def reverse(self) -> "WireInterface":
        """Create a new wire with reversed direction."""
        return self.wire.reverse()

    def close(self):
        """Close the wire by connecting the last vertex to the first."""
        return self.wire.close()

    def extrude(self, length: LengthType) -> "PartInterface":
        """Extrude the wire to create a part."""
        return self.wire.extrude(length)
