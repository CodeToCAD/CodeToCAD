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
        # Default implementation - adapters should override this
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific wire type
        raise NotImplementedError("reverse must be implemented by concrete classes")

    def close(self):
        """Close the wire by connecting the last vertex to the first."""
        # Default implementation - adapters should override this
        pass

    def extrude(self, length: LengthType) -> "PartInterface":
        """Extrude the wire to create a part."""
        # Default implementation - adapters should override this
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific part type
        raise NotImplementedError("extrude must be implemented by concrete classes")
