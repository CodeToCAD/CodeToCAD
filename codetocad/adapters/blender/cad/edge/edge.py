import bpy
import bmesh
import numpy as np
from uuid import uuid4

from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.edge.edge_transform import EdgeTransformInterface
from codetocad.adapters.blender.cad.vertex.vertex import Vertex
from codetocad.adapters.blender.blender_actions.objects import create_object
from codetocad.adapters.blender.blender_actions.collections import (
    assign_object_to_collection,
)
from codetocad.adapters.blender.blender_actions.curve import create_curve
from codetocad.adapters.blender.blender_actions.mesh import create_mesh
from codetocad.adapters.blender.blender_definitions import BlenderCurveTypes


class Edge(EdgeInterface):
    """Blender implementation of EdgeInterface."""

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str | None = None,
        native_instance: "bpy.types.MeshEdge| bpy.types.Spline | None" = None,
    ):
        # Initialize the parent interface
        super().__init__(v1, v2)

        # Override method groups with Blender-specific implementations
        from codetocad.adapters.blender.cad.edge.edge_geometry import EdgeGeometry
        from codetocad.adapters.blender.cad.edge.edge_operations import EdgeOperations

        self.geometry = EdgeGeometry(self)
        self.operations = EdgeOperations(self)

        # Blender-specific properties
        self.name = name or f"edge_{str(uuid4())[:8]}"
        self.native_instance = native_instance
        self._blender_object: bpy.types.Object | None = None
        self._curve_data: bpy.types.Curve | None = None

        # Create Blender representation if not provided
        if native_instance is None:
            self._create_blender_edge()

    def _create_blender_edge(self):
        """Create a Blender curve to represent this edge."""
        # Create points for the curve
        points = [self.v1.position.tolist(), self.v2.position.tolist()]

        # Create a curve using the blender_actions utility
        try:
            spline, curve_data, spline_points = create_curve(
                curve_name=self.name,
                curve_type=BlenderCurveTypes.NURBS,
                points=points,
                is_3d=True,
            )

            self._curve_data = curve_data
            self.native_instance = spline

            # Create object from curve
            self._blender_object = create_object(self.name, curve_data)
            assign_object_to_collection(self._blender_object)

        except Exception as e:
            # Fallback: create a simple mesh edge
            self._create_mesh_edge()

    def _create_mesh_edge(self):
        """Fallback method to create a mesh-based edge."""
        # Create a mesh with two vertices and one edge
        vertices = [self.v1.position.tolist(), self.v2.position.tolist()]
        edges = [(0, 1)]
        faces = []

        # Use utility function to create mesh
        mesh = create_mesh(self.name, vertices, edges, faces)

        # Create object and assign to scene
        self._blender_object = create_object(self.name, mesh)
        assign_object_to_collection(self._blender_object)

    def direction(self):
        """Get the direction vector of the edge."""
        return self.v2.position - self.v1.position

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this edge."""
        return self._blender_object

    def get_native_instance(self) -> "bpy.types.MeshEdge | bpy.types.Spline | None":
        """Get the native Blender edge instance."""
        return self.native_instance

    def update_endpoints(self, v1: "Vertex", v2: "Vertex"):
        """Update the edge endpoints and refresh Blender representation."""
        self.v1 = v1
        self.v2 = v2

        # Update Blender representation
        if self._blender_object and self._blender_object.data:
            if isinstance(self._blender_object.data, bpy.types.Mesh):
                # Update mesh vertices
                mesh = self._blender_object.data
                mesh.vertices[0].co = self.v1.position
                mesh.vertices[1].co = self.v2.position
                mesh.update()
            elif isinstance(self._blender_object.data, bpy.types.Curve):
                # Update curve points
                if self.native_instance and hasattr(self.native_instance, "points"):
                    points = self.native_instance.points
                    if len(points) >= 2:
                        points[0].co = (*self.v1.position, 1.0)
                        points[1].co = (*self.v2.position, 1.0)

    def subdivide(self, segments: int = 2) -> list["Vertex"]:
        """Subdivide the edge into multiple segments and return intermediate vertices."""
        vertices = []
        for i in range(1, segments):
            t = i / segments
            pos = self.v1.position + t * self.direction()
            vertices.append(Vertex(pos[0], pos[1], pos[2]))
        return vertices

    def __repr__(self):
        return f"Edge(name='{self.name}', v1={self.v1.position}, v2={self.v2.position})"
