"""
Geometry operations interface for Vertex objects.
"""

from abc import ABC
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.dimensions.point import Point


class VertexGeometryInterface(ABC):
    """Interface for vertex geometry operations."""

    def __init__(self, vertex: "VertexInterface"):
        self.vertex = vertex

    def position(self) -> tuple[float, float, float]:
        """Get the current position of the vertex."""
        return self.vertex.get_position()

    def set_position(self, x: LengthType, y: LengthType, z: LengthType = 0):
        """Set the position of the vertex."""
        return self.vertex.set_position(x, y, z)

    def distance_to(self, other: "VertexInterface") -> float:
        """Calculate distance to another vertex."""
        return self.vertex.distance_to(other)

    def point(self) -> Point:
        """Get the vertex position as a Point object."""
        return self.vertex.get_point()
