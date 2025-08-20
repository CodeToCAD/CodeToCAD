"""
Blender implementation of VertexGeometryInterface.
"""

from codetocad.interfaces.cad.vertex.vertex_geometry_interface import (
    VertexGeometryInterface,
)
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression
from codetocad.core.dimensions.point import Point
import numpy as np


class VertexGeometry(VertexGeometryInterface):
    """Blender implementation of vertex geometry operations."""

    def position(self) -> tuple[float, float, float]:
        """Get the current position of the vertex."""
        return tuple(self.vertex.position)

    def set_position(self, x: LengthType, y: LengthType, z: LengthType = 0):
        """Set the position of the vertex."""
        self.vertex.position = np.array(
            [
                float(LengthExpression(x)),
                float(LengthExpression(y)),
                float(LengthExpression(z)),
            ]
        )

        # Update Blender object location if it exists
        if self.vertex._blender_object:
            self.vertex._blender_object.location = self.vertex.position

    def distance_to(self, other: "VertexInterface") -> float:
        """Calculate distance to another vertex."""
        return float(np.linalg.norm(self.vertex.position - other.position))

    def point(self) -> Point:
        """Get the vertex position as a Point object."""
        return Point.from_list(self.vertex.position.tolist())
