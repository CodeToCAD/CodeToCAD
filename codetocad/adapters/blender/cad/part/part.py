import bmesh
from typing import TYPE_CHECKING, List
from uuid import uuid4

from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression
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
        # Initialize parent interface first
        super().__init__()

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

    def extrude_sketch(self, distance: LengthType) -> "Part":
        """Extrude the part's sketch to create a solid."""
        if not self.sketch.wires:
            raise ValueError("No wires in sketch to extrude")

        # Create from sketch first if not already done
        if not self._blender_object:
            self.create_from_sketch()

        # Apply extrusion
        self.extrude(distance)
        return self

    def extrude(self, distance: LengthType):
        """Extrude the part along its normal."""
        if not self._blender_object:
            self.create_from_sketch()

        if self._blender_object and isinstance(
            self._blender_object.data, bpy.types.Mesh
        ):
            # Add solidify modifier for extrusion
            apply_solidify_modifier(self._blender_object, float(distance))

    def union(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean union with another part."""
        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.name}_union_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.sketch.copy()
        result_part.create_from_sketch()

        # Apply boolean union
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.UNION,
                other._blender_object,
            )

        return result_part

    def difference(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean difference with another part."""
        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.name}_difference_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.sketch.copy()
        result_part.create_from_sketch()

        # Apply boolean difference
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.DIFFERENCE,
                other._blender_object,
            )

        return result_part

    def intersection(self, other: "PartInterface") -> "PartInterface":
        """Perform boolean intersection with another part."""
        if not isinstance(other, Part):
            raise TypeError(
                "Can only perform boolean operations with other Blender Parts"
            )

        result_part = Part(f"{self.name}_intersection_{other.name}")

        # Copy this part's data to result
        result_part.sketch = self.sketch.copy()
        result_part.create_from_sketch()

        # Apply boolean intersection
        if result_part._blender_object and other._blender_object:
            apply_boolean_modifier(
                result_part._blender_object,
                BlenderBooleanTypes.INTERSECT,
                other._blender_object,
            )

        return result_part

    def boolean_union(self, other: "Part"):
        """Perform boolean union with another part (legacy method)."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.UNION,
                other._blender_object,
            )

    def boolean_difference(self, other: "Part"):
        """Perform boolean difference with another part (legacy method)."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.DIFFERENCE,
                other._blender_object,
            )

    def boolean_intersection(self, other: "Part"):
        """Perform boolean intersection with another part (legacy method)."""
        if self._blender_object and other._blender_object:
            apply_boolean_modifier(
                self._blender_object,
                BlenderBooleanTypes.INTERSECT,
                other._blender_object,
            )

    def translate(self, dx: LengthType, dy: LengthType, dz: LengthType = 0) -> "Part":
        """Translate the part."""
        if self._blender_object:
            current_loc = self._blender_object.location
            self._blender_object.location = (
                current_loc[0] + float(LengthExpression(dx)),
                current_loc[1] + float(LengthExpression(dy)),
                current_loc[2] + float(LengthExpression(dz)),
            )
        return self

    def rotate(self, axis: tuple[float, float, float], angle: float) -> "Part":
        """Rotate the part around an axis."""
        if self._blender_object:
            # Convert axis-angle to Euler angles (simplified)
            # This is a basic implementation - more complex rotation would require matrix math
            import math

            magnitude = math.sqrt(sum(a * a for a in axis))
            if magnitude > 0:
                # Normalize axis and apply rotation
                normalized_axis = tuple(a / magnitude for a in axis)
                # For simplicity, apply rotation as Euler angles
                # In a full implementation, this would use proper axis-angle to Euler conversion
                self._blender_object.rotation_euler = (
                    normalized_axis[0] * angle,
                    normalized_axis[1] * angle,
                    normalized_axis[2] * angle,
                )
        return self

    def scale(self, scale_x: float, scale_y: float, scale_z: float = 1.0) -> "Part":
        """Scale the part."""
        if self._blender_object:
            current_scale = self._blender_object.scale
            self._blender_object.scale = (
                current_scale[0] * scale_x,
                current_scale[1] * scale_y,
                current_scale[2] * scale_z,
            )
        return self

    def move(self, x: float, y: float, z: float):
        """Move the part to a new location"""
        if self._blender_object:
            self._blender_object.location = (x, y, z)

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

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the part."""
        if self._blender_object:
            # Get bounding box in world coordinates
            import mathutils

            bbox = [
                self._blender_object.matrix_world @ mathutils.Vector(corner)
                for corner in self._blender_object.bound_box
            ]

            # Find min and max coordinates
            min_coords = [min(corner[i] for corner in bbox) for i in range(3)]
            max_coords = [max(corner[i] for corner in bbox) for i in range(3)]

            return (
                (min_coords[0], min_coords[1], min_coords[2]),
                (max_coords[0], max_coords[1], max_coords[2]),
            )

        return ((0, 0, 0), (0, 0, 0))

    def export_step(self, _file_path: str):
        """Export the part to STEP format."""
        # Blender doesn't have native STEP export, would need addon
        raise NotImplementedError("STEP export requires additional Blender addon")

    def export_stl(self, _file_path: str, _tolerance: float = 0.1):
        """Export the part to STL format."""
        if self._blender_object:
            # This would require using Blender's export operators
            # For now, raise NotImplementedError as it requires bpy.ops context
            raise NotImplementedError(
                "STL export requires Blender context and operators"
            )

    def export_brep(self, _file_path: str):
        """Export the part to BREP format."""
        # Blender doesn't have native BREP export
        raise NotImplementedError("BREP export not supported in Blender")

    def copy(self) -> "Part":
        """Create a copy of the part."""
        new_part = Part(f"{self.name}_copy")

        # Copy the sketch
        new_part.sketch = self.sketch.copy()

        # Create Blender representation for the copy
        new_part.create_from_sketch()

        return new_part

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
