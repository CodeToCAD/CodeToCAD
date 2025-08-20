"""
build123d implementation of VertexInterface.
"""

from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.build123d_actions.geometry import create_vertex
from codetocad.adapters.build123d.build123d_actions.transformations import (
    translate_object,
)

if TYPE_CHECKING:
    import build123d as bd


class Vertex(VertexInterface):
    """build123d implementation of VertexInterface."""

    def __init__(
        self,
        x: LengthType,
        y: LengthType,
        z: LengthType = 0,
        name: str | None = None,
        native_instance: "bd.Vertex | None" = None,
    ):
        # Initialize the parent interface
        super().__init__(x, y, z)

        # build123d-specific properties
        self.name = name or f"vertex_{str(uuid4())[:8]}"

        # Create or use provided build123d vertex
        if native_instance is not None:
            self.native_instance = native_instance
        else:
            self.native_instance = create_vertex(x, y, z)

    def transform(self, matrix):
        """Transform the vertex using a transformation matrix."""
        # Apply transformation to the position array (parent class behavior)
        super().transform(matrix)

        # Update the native build123d vertex
        # Extract translation from the transformation matrix
        dx = matrix[0, 3] if matrix.shape == (4, 4) else 0
        dy = matrix[1, 3] if matrix.shape == (4, 4) else 0
        dz = matrix[2, 3] if matrix.shape == (4, 4) else 0

        # Apply translation to the native instance
        self.native_instance = translate_object(self.native_instance, dx, dy, dz)

    def __repr__(self):
        return f"Vertex({self.position[0]}, {self.position[1]}, {self.position[2]})"
