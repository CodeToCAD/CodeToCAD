import bmesh
from typing import TYPE_CHECKING, List
from uuid import uuid4

from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.blender.cad.sketch.sketch import Sketch
from codetocad.adapters.blender.blender_actions.objects import (
    create_object,
    update_object_data_name,
    update_object_name,
    get_object,
    remove_object,
)
from codetocad.adapters.blender.blender_actions.objects_transmute import (
    create_mesh_from_curve,
)
from codetocad.adapters.blender.blender_actions.modifiers import (
    apply_solidify_modifier,
    apply_boolean_modifier,
)
from codetocad.adapters.blender.blender_definitions import BlenderBooleanTypes
from codetocad.adapters.blender.cad.part.part_preset_class_property import (
    _PartPresetClassProperty,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    import bpy


class Part(PartInterface, metaclass=_PartPresetClassProperty):
    """Blender implementation of PartInterface."""

    def __init__(self, name: str | None = None):
        # Blender-specific properties
        self.name = name or f"part_{str(uuid4())[:8]}"
        self._blender_object: bpy.types.Object | None = None

        self.sketch = Sketch(f"{self.name}_sketch")

    def set_name(self, name: str):
        """Set the part name and update Blender object."""
        self.name = name
        if self._blender_object:
            update_object_name(self._blender_object, name)
            update_object_data_name(self._blender_object, name)

    @classmethod
    def get_by_name(cls, name: str) -> "Part| None":
        """Get a part by name from the Blender scene."""
        blender_obj = get_object(name)
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
            apply_solidify_modifier(self._blender_object, float(distance))

    def boolean_union(self, other: "Part"):
        """Perform boolean union with another part."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.UNION,
                other._blender_object,
            )

    def boolean_difference(self, other: "Part"):
        """Perform boolean difference with another part."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.DIFFERENCE,
                other._blender_object,
            )

    def boolean_intersection(self, other: "Part"):
        """Perform boolean intersection with another part."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.INTERSECT,
                other._blender_object,
            )

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location."""
        if self._blender_object:
            self._blender_object.location = (x, y, z)

    def rotate(self, x: float, y: float, z: float):
        """Rotate the part by the given angles (in radians)."""
        if self._blender_object:
            self._blender_object.rotation_euler = (x, y, z)

    def scale(self, x: float, y: float | None = None, z: float | None = None):
        """Scale the part."""
        if self._blender_object:
            y_val = y if y is not None else x
            z_val = z if z is not None else x
            self._blender_object.scale = (x, y_val, z_val)

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
            remove_object(self._blender_object)
            self._blender_object = None

    def __repr__(self):
        return f"<Part(name='{self.name}'): {self.sketch}>"
