import bpy
import bmesh
from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.interfaces.cad.part.part_interface import (
    _PartPresetClassPropertyInterface,
    PartInterface,
)
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface
from codetocad.core.dimensions.length import LengthType
from codetocad.adapters.blender.cad.sketch import Sketch
from codetocad.adapters.blender.blender_actions.objects import (
    create_object,
    add_primitive,
    update_object_data_name,
    update_object_name,
)
from codetocad.adapters.blender.blender_actions.collections import (
    assign_object_to_collection,
)
from codetocad.adapters.blender.blender_actions.objects_transmute import (
    create_mesh_from_curve,
)
from codetocad.adapters.blender.blender_actions.modifiers import apply_modifier
from codetocad.adapters.blender.blender_definitions import BlenderObjectPrimitiveTypes

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly import Assembly


class _PartPresetClassProperty(_PartPresetClassPropertyInterface):
    @property
    def preset(self):
        return PartPresets()


class PartPresets(PartPresetsInterface):
    """Blender-specific part presets."""

    def __init__(self, assembly: "Assembly|None" = None):
        self.assembly = assembly

    def cube(self, x: LengthType, y: LengthType, z: LengthType) -> "Part":
        """Create a cube part using Blender primitives."""
        part = Part()
        part.set_name(f"cube_{str(uuid4())[:8]}")

        # Create cube using Blender primitive
        dimensions = [float(x), float(y), float(z)]
        add_primitive(BlenderObjectPrimitiveTypes.cube, dimensions)

        # Get the created object
        cube_obj = bpy.context.active_object
        if cube_obj:
            update_object_name(cube_obj, part.name)
            update_object_data_name(cube_obj, part.name)
            part._blender_object = cube_obj

        if self.assembly:
            self.assembly.parts.append(part)

        return part

    def cylinder(self, radius: LengthType, height: LengthType) -> "Part":
        """Create a cylinder part using Blender primitives."""
        part = Part()
        part.set_name(f"cylinder_{str(uuid4())[:8]}")

        # Create cylinder using Blender primitive
        dimensions = [float(radius), float(height)]
        add_primitive(BlenderObjectPrimitiveTypes.cylinder, dimensions)

        # Get the created object
        cylinder_obj = bpy.context.active_object
        if cylinder_obj:
            update_object_name(cylinder_obj, part.name)
            update_object_data_name(cylinder_obj, part.name)
            part._blender_object = cylinder_obj

        if self.assembly:
            self.assembly.parts.append(part)

        return part

    def sphere(self, radius: LengthType) -> "Part":
        """Create a sphere part using Blender primitives."""
        part = Part()
        part.set_name(f"sphere_{str(uuid4())[:8]}")

        # Create sphere using Blender primitive
        dimensions = [float(radius)]
        add_primitive(BlenderObjectPrimitiveTypes.uvsphere, dimensions)

        # Get the created object
        sphere_obj = bpy.context.active_object
        if sphere_obj:
            update_object_name(sphere_obj, part.name)
            update_object_data_name(sphere_obj, part.name)
            part._blender_object = sphere_obj

        if self.assembly:
            self.assembly.parts.append(part)

        return part


class Part(PartInterface, metaclass=_PartPresetClassProperty):
    """Blender implementation of PartInterface."""

    def __init__(self, name: str | None = None):
        # Blender-specific properties
        self.name = name or f"part_{str(uuid4())[:8]}"
        self._blender_object: bpy.types.Object | None = None

        # Initialize parent interface properties
        self.member_assemblies: list["Assembly"] = []
        self.sketch: Sketch = Sketch(f"{self.name}_sketch")

    def set_name(self, name: str):
        """Set the part name and update Blender object."""
        self.name = name
        if self._blender_object:
            self._blender_object.name = name

    @classmethod
    def get_by_name(cls, name: str) -> "Part| None":
        """Get a part by name from the Blender scene."""
        blender_obj = bpy.data.objects.get(name)
        if blender_obj:
            part = cls(name)
            part._blender_object = blender_obj
            return part
        return None

    def get_blender_object(self) -> "bpy.types.Object | None":
        """Get the Blender object representing this part."""
        return self._blender_object

    def create_from_sketch(self):
        """Create a 3D part from the sketch by extruding."""
        if not self.sketch.wires:
            return

        # Convert sketch wires to mesh
        for wire in self.sketch.wires:
            wire_obj = wire.get_blender_object()
            if wire_obj and isinstance(wire_obj.data, bpy.types.Curve):
                # Convert curve to mesh
                mesh_obj = create_mesh_from_curve(wire_obj, f"{self.name}_mesh")
                if mesh_obj:
                    self._blender_object = mesh_obj

    def extrude(self, distance: LengthType):
        """Extrude the part along its normal."""
        if not self._blender_object:
            self.create_from_sketch()

        if self._blender_object and isinstance(
            self._blender_object.data, bpy.types.Mesh
        ):
            # Add solidify modifier for extrusion
            modifier = apply_modifier(self._blender_object, "Solidify", "SOLIDIFY")
            if modifier:
                modifier.thickness = float(distance)

    def boolean_union(self, other: "Part"):
        """Perform boolean union with another part."""
        if self._blender_object and other._blender_object:
            modifier = apply_modifier(self._blender_object, "Boolean_Union", "BOOLEAN")
            if modifier:
                modifier.operation = "UNION"
                modifier.object = other._blender_object

    def boolean_difference(self, other: "Part"):
        """Perform boolean difference with another part."""
        if self._blender_object and other._blender_object:
            modifier = apply_modifier(
                self._blender_object, "Boolean_Difference", "BOOLEAN"
            )
            if modifier:
                modifier.operation = "DIFFERENCE"
                modifier.object = other._blender_object

    def boolean_intersection(self, other: "Part"):
        """Perform boolean intersection with another part."""
        if self._blender_object and other._blender_object:
            modifier = apply_modifier(
                self._blender_object, "Boolean_Intersection", "BOOLEAN"
            )
            if modifier:
                modifier.operation = "INTERSECT"
                modifier.object = other._blender_object

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        if self._blender_object:
            self._blender_object.location = (x, y, z)

    def rotate(self, x: float, y: float, z: float):
        """Rotate the part by the given angles (in radians)."""
        if self._blender_object:
            self._blender_object.rotation_euler = (x, y, z)

    def scale(self, x: float, y: float = None, z: float = None):
        """Scale the part."""
        if self._blender_object:
            y = y or x
            z = z or x
            self._blender_object.scale = (x, y, z)

    def get_volume(self) -> float:
        """Calculate the volume of the part."""
        if self._blender_object and isinstance(
            self._blender_object.data, bpy.types.Mesh
        ):
            # Create bmesh instance
            bm = bmesh.new()
            bm.from_mesh(self._blender_object.data)
            bm.transform(self._blender_object.matrix_world)

            # Calculate volume
            volume = bm.calc_volume()
            bm.free()
            return volume
        return 0.0

    def hide(self):
        """Hide the part in Blender."""
        if self._blender_object:
            self._blender_object.hide_viewport = True

    def show(self):
        """Show the part in Blender."""
        if self._blender_object:
            self._blender_object.hide_viewport = False

    def delete(self):
        """Delete the part from Blender."""
        if self._blender_object:
            # Remove from scene
            bpy.data.objects.remove(self._blender_object, do_unlink=True)
            self._blender_object = None

    def __repr__(self):
        return f"<Part(name='{self.name}'): {self.sketch}>"
