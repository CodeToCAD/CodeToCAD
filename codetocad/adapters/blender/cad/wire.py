from typing import TYPE_CHECKING
import bpy
import bmesh
from uuid import uuid4

from codetocad.interfaces.cad.wire.wire_interface import (
    _WirePresetClassPropertyInterface,
    WireInterface,
)
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length import LengthType
from codetocad.adapters.blender.cad.edge import Edge
from codetocad.adapters.blender.cad.vertex import Vertex
from codetocad.adapters.blender.blender_actions.objects import create_object
from codetocad.adapters.blender.blender_actions.collections import (
    assign_object_to_collection,
)
from codetocad.adapters.blender.blender_actions.curve import create_curve
from codetocad.adapters.blender.blender_definitions import BlenderCurveTypes

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.part import Part
    from codetocad.adapters.blender.cad.sketch import Sketch


class _WirePresetClassProperty(_WirePresetClassPropertyInterface):
    """Metaclass to provide a preset property for the Wire class."""

    @property
    def preset(self):
        return WirePresetsInterface(Wire, None)


class WireAdd(WireAddInterface):
    """Blender-specific wire add operations."""

    def __init__(self, wire: "Wire"):
        self.wire = wire

    def point(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        v = Vertex(x, y, z)
        e = Edge(v, v)
        self.wire.edges.append(e)
        return e

    def line_to(self, x: LengthType, y: LengthType, z: LengthType = 0) -> Edge:
        """
        Draws a line from the last vertex of the wire to the specified coordinates.
        If the wire is empty, it starts from the origin (0, 0, 0).
        """
        v1 = self.wire.edges[-1].v2 if self.wire.edges else Vertex(0, 0, 0)
        v2 = Vertex(x, y, z)
        e = Edge(v1, v2)
        self.wire.edges.append(e)

        # Update Blender representation
        self.wire._update_blender_curve()

        return e


class Wire(WireInterface, metaclass=_WirePresetClassProperty):
    """Blender implementation of WireInterface."""

    def __init__(
        self,
        sketch: "Sketch|None" = None,
        name: str | None = None,
        native_instance: "bpy.types.Spline | bpy.types.MeshPolygon| None" = None,
    ):
        # Initialize the parent interface
        self.name = name or f"wire_{str(uuid4())[:8]}"
        self.native_instance = native_instance
        self._blender_object: bpy.types.Object | None = None
        self._curve_data: bpy.types.Curve | None = None

        # Initialize parent with sketch
        if sketch is not None:
            self.member_sketches: list["Sketch"] = [sketch]
        else:
            self.member_sketches: list["Sketch"] = []

        self.edges: list[Edge] = []
        self.add = WireAdd(self)
        self.get = WireGetInterface(self)
        self.constraint = WireConstraintInterface(self)

        # Create Blender representation
        self._create_blender_wire()

    def _create_blender_wire(self):
        """Create a Blender curve to represent this wire."""
        # Create an empty curve initially
        self._curve_data = bpy.data.curves.new(self.name, type="CURVE")
        self._curve_data.dimensions = "3D"

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

    def close(self):
        """Close the wire by connecting the last vertex to the first."""
        if len(self.edges) >= 2:
            first_vertex = self.edges[0].v1
            last_vertex = self.edges[-1].v2

            if first_vertex != last_vertex:
                closing_edge = Edge(last_vertex, first_vertex)
                self.edges.append(closing_edge)
                self._update_blender_curve()

    def get_vertices(self) -> list[Vertex]:
        """Get all vertices in the wire."""
        vertices = []
        if self.edges:
            vertices.append(self.edges[0].v1)
            for edge in self.edges:
                vertices.append(edge.v2)
        return vertices

    def get_length(self) -> float:
        """Calculate the total length of the wire."""
        return sum(edge.length() for edge in self.edges)

    def is_closed(self) -> bool:
        """Check if the wire forms a closed loop."""
        if len(self.edges) < 3:
            return False
        return self.edges[0].v1.position.tolist() == self.edges[-1].v2.position.tolist()

    def extude(self, length: LengthType) -> "Part":
        """Extrude the wire to create a part."""
        from codetocad.adapters.blender.cad.part import Part
        from codetocad.adapters.blender.cad.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self)
        self.member_sketches.append(sketch)

        return part

    def __repr__(self):
        return f"Wire(name='{self.name}', edges={len(self.edges)})"
