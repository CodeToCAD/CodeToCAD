import numpy as np
import bpy
from uuid import uuid4

from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface
from codetocad.core.dimensions.length import Length, LengthType
from codetocad.core.dimensions.point import Point
from codetocad.adapters.blender.blender_actions.objects import create_object
from codetocad.adapters.blender.blender_actions.collections import (
    assign_object_to_collection,
)


class Vertex(VertexInterface):
    """Blender implementation of VertexInterface."""

    def __init__(
        self,
        x: LengthType,
        y: LengthType,
        z: LengthType = 0,
        name: str | None = None,
        native_instance: "bpy.types.MeshVertex | None" = None,
    ):
        # Initialize the parent interface
        super().__init__(x, y, z)

        # Blender-specific properties
        self.name = name or f"vertex_{str(uuid4())[:8]}"
        self.native_instance = native_instance
        self._blender_object: bpy.types.Object | None = None

        # Create Blender representation if not provided
        if native_instance is None:
            self._create_blender_vertex()

    def _create_blender_vertex(self):
        """Create a Blender object to represent this vertex."""
        # Create a small sphere to represent the vertex
        mesh = bpy.data.meshes.new(self.name)

        # Create a simple vertex mesh (single point)
        vertices = [self.position.tolist()]
        edges = []
        faces = []

        mesh.from_pydata(vertices, edges, faces)
        mesh.update()

        # Create object and assign to scene
        self._blender_object = create_object(self.name, mesh)
        assign_object_to_collection(self._blender_object)

        # Set object location
        self._blender_object.location = self.position

    def transform(self, matrix):
        """Transform the vertex position and update Blender object."""
        super().transform(matrix)

        # Update Blender object location if it exists
        if self._blender_object:
            self._blender_object.location = self.position

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this vertex."""
        return self._blender_object

    def get_native_instance(self) -> "bpy.types.MeshVertex | None":
        """Get the native Blender vertex instance."""
        return self.native_instance

    def set_location(self, x: LengthType, y: LengthType, z: LengthType):
        """Set the vertex location and update Blender representation."""
        self.position = np.array([float(Length(x)), float(Length(y)), float(Length(z))])

        if self._blender_object:
            self._blender_object.location = self.position

    def get_point(self) -> Point:
        """Get the vertex position as a Point object."""
        return Point.from_list(self.position.tolist())

    def distance_to(self, other: "Vertex") -> float:
        """Calculate distance to another vertex."""
        return np.linalg.norm(self.position - other.position)

    def __repr__(self):
        return f"Vertex(name='{self.name}', position={self.position})"
