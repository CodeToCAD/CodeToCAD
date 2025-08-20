"""
Geometry operations interface for Wire objects.
"""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


class WireGeometryInterface(ABC):
    """Interface for wire geometry operations."""

    def __init__(self, wire: "WireInterface"):
        self.wire = wire

    def is_closed(self) -> bool:
        """Check if the wire is closed."""
        return self.wire.is_closed()

    def length(self) -> float:
        """Get the total length of the wire."""
        return self.wire.length()

    def vertices(self) -> list["VertexInterface"]:
        """Get all unique vertices in the wire."""
        return self.wire.get_vertices()

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the wire."""
        return self.wire.get_bounding_box()
