from typing import TYPE_CHECKING, List
from uuid import uuid4

from codetocad.interfaces.cad.wire.wire_interface import WireInterface
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.blender.cad.edge.edge import Edge
from codetocad.adapters.blender.cad.vertex.vertex import Vertex
from codetocad.adapters.blender.cad.wire.wire_add import WireAdd
from codetocad.adapters.blender.cad.wire.wire_preset_class_property import (
    _WirePresetClassProperty,
)
from codetocad.adapters.blender.blender_actions.objects import create_object
from codetocad.adapters.blender.blender_actions.collections import (
    assign_object_to_collection,
)
from codetocad.adapters.blender.blender_actions.curve import create_curve
from codetocad.adapters.blender.blender_definitions import BlenderCurveTypes

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.part.part import Part
    from codetocad.adapters.blender.cad.sketch.sketch import Sketch
    import bpy


class Wire(WireInterface, metaclass=_WirePresetClassProperty):
    """Blender implementation of WireInterface."""

    def __init__(
        self,
        sketch: "Sketch|None" = None,
        name: str | None = None,
        native_instance: "bpy.types.Spline | bpy.types.MeshPolygon| None" = None,
    ):
        # Initialize the parent interface first
        super().__init__(sketch)

        # Blender-specific properties
        self.name = name or f"wire_{str(uuid4())[:8]}"
        self.native_instance = native_instance
        self._blender_object: bpy.types.Object | None = None
        self._curve_data: bpy.types.Curve | None = None

        self.member_sketches: list["Sketch"] = [sketch] if sketch is not None else []  # type: ignore

        # Override method groups with Blender-specific implementations
        from codetocad.adapters.blender.cad.wire.wire_geometry import WireGeometry
        from codetocad.adapters.blender.cad.wire.wire_operations import WireOperations

        self.geometry = WireGeometry(self)
        self.operations = WireOperations(self)

        self.edges: list[Edge] = []  # type: ignore

        self.add = WireAdd(self)
        self.get = WireGetInterface(self)
        self.constraint = WireConstraintInterface(self)

        # Create Blender representation
        self._create_blender_wire()

    def _create_blender_wire(self):
        """Create a Blender curve to represent this wire."""
        # Create an empty curve initially with basic points
        initial_points = [(0, 0, 0), (0, 0, 0)]  # Start with minimal curve

        spline, curve_data, spline_points = create_curve(
            curve_name=self.name,
            curve_type=BlenderCurveTypes.NURBS,
            points=initial_points,
            is_3d=True,
        )
        self._curve_data = curve_data

        # Create object from curve
        self._blender_object = create_object(self.name, self._curve_data)
        assign_object_to_collection(self._blender_object)

    def _update_blender_curve(self):
        """Update the Blender curve based on current edges."""
        if not self._curve_data or not self.edges:
            return

        # Clear existing splines
        self._curve_data.splines.clear()

        if len(self.edges) == 0:
            return

        # Create a new spline
        spline = self._curve_data.splines.new(type="NURBS")

        # Collect all unique vertices in order
        vertices = []
        if self.edges:
            vertices.append(self.edges[0].v1)
            for edge in self.edges:
                vertices.append(edge.v2)

        # Set spline points
        spline.points.add(len(vertices) - 1)  # -1 because one point already exists
        for i, vertex in enumerate(vertices):
            spline.points[i].co = (*vertex.position, 1.0)

        # Update the curve
        self._curve_data.update_tag()

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this wire."""
        return self._blender_object

    def get_native_instance(self) -> "bpy.types.Spline | bpy.types.MeshPolygon | None":
        """Get the native Blender wire instance."""
        return self.native_instance

    def get_length(self) -> float:
        """Calculate the total length of the wire (legacy method)."""
        return self.geometry.length()

    def extude(self, length: LengthType) -> "Part":
        """Extrude the wire to create a part (legacy method with typo)."""
        return self.operations.extrude(length)

    def __repr__(self):
        return f"Wire(name='{self.name}', edges={len(self.edges)})"
