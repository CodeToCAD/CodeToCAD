import mathutils
from typing import TYPE_CHECKING
from uuid import uuid4

from codetocad.adapters.blender.blender_actions.objects import remove_object
from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
from codetocad.adapters.blender.cad.assembly.assembly_add import AssemblyAdd
from codetocad.adapters.blender.cad.assembly.assembly_get import AssemblyGet
from codetocad.adapters.blender.blender_actions.collections import (
    create_collection,
    get_collection,
    get_collection_or_none,
    remove_collection,
)
from codetocad.adapters.blender.blender_actions.context import select_object
from codetocad.adapters.blender.blender_actions.import_export import (
    export_object,
    export_objects,
)

if TYPE_CHECKING:
    import bpy
    from codetocad.adapters.blender.cad.part.part import Part


class Assembly(AssemblyInterface):
    """Blender implementation of AssemblyInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # Blender-specific properties
        self.name = name or f"assembly_{str(uuid4())[:8]}"
        self._blender_collection: bpy.types.Collection | None = None

        # Initialize parent interface properties
        self.parts: list["Part"] = []  # type: ignore
        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

        # Create Blender representation
        self._create_blender_assembly()

    def set_name(self, name: str):
        """Set the assembly name."""
        self.name = name

    def add_part(self, part: "Part"):
        """Add a part to the assembly."""
        if part not in self.parts:
            self.parts.append(part)
            if self not in part.member_assemblies:
                part.member_assemblies.append(self)

    def remove_part(self, part: "Part"):
        """Remove a part from the assembly."""
        if part in self.parts:
            self.parts.remove(part)
            if self in part.member_assemblies:
                part.member_assemblies.remove(self)

    def get_part_by_name(self, name: str) -> "Part | None":
        """Get a part by name."""
        for part in self.parts:
            if part.name == name:
                return part
        return None

    def get_part_by_index(self, index: int) -> "Part":
        """Get a part by index."""
        return self.parts[index]

    def _create_blender_assembly(self):
        """Create a Blender collection to represent this assembly."""
        try:
            create_collection(self.name)
            self._blender_collection = get_collection(self.name)
        except Exception:
            # Collection might already exist
            self._blender_collection = get_collection_or_none(self.name)

    def _get_collection(self) -> "bpy.types.Collection | None":
        """Get the Blender collection representing this assembly."""
        return self._blender_collection

    def _get_all_blender_objects(self) -> "list[bpy.types.Object]":
        """Get all Blender objects in the assembly."""
        return [
            obj
            for obj in [part.get_blender_object() for part in self.parts]
            if obj is not None
        ]

    def move(self, x: float, y: float, z: float):
        """Move all parts in the assembly."""
        for part in self.parts:
            blender_object = part.get_blender_object()
            if blender_object:
                current_loc = blender_object.location
                blender_object.location = (
                    current_loc[0] + x,
                    current_loc[1] + y,
                    current_loc[2] + z,
                )

    def rotate(self, x: float, y: float, z: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            blender_object = part.get_blender_object()
            if blender_object:
                current_rot = blender_object.rotation_euler
                blender_object.rotation_euler = (
                    current_rot[0] + x,
                    current_rot[1] + y,
                    current_rot[2] + z,
                )

    def scale(self, x: float, y: float | None = None, z: float | None = None):
        """Scale all parts in the assembly."""
        y_val = y if y is not None else x
        z_val = z if z is not None else x

        for part in self.parts:
            blender_object = part.get_blender_object()
            if blender_object:
                current_scale = blender_object.scale
                blender_object.scale = (
                    current_scale[0] * x,
                    current_scale[1] * y_val,
                    current_scale[2] * z_val,
                )

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of all parts in the assembly."""
        if not self.parts:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all parts
        part_boxes = [part.get_bounding_box() for part in self.parts]

        if not part_boxes:
            return ((0, 0, 0), (0, 0, 0))

        # Find overall min and max
        min_x = min(box[0][0] for box in part_boxes)
        min_y = min(box[0][1] for box in part_boxes)
        min_z = min(box[0][2] for box in part_boxes)

        max_x = max(box[1][0] for box in part_boxes)
        max_y = max(box[1][1] for box in part_boxes)
        max_z = max(box[1][2] for box in part_boxes)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def get_total_volume(self) -> float:
        """Get the total volume of all parts in the assembly."""
        return sum(part.get_volume() for part in self.parts)

    def translate_all(self, dx: float, dy: float, dz: float = 0):
        """Translate all parts in the assembly."""
        for part in self.parts:
            part.translate(dx, dy, dz)

    def rotate_all(self, axis: tuple[float, float, float], angle: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            part.rotate(axis, angle)

    def scale_all(self, scale_x: float, scale_y: float, scale_z: float = 1.0):
        """Scale all parts in the assembly."""
        for part in self.parts:
            part.scale(scale_x, scale_y, scale_z)

    def hide(self):
        """Hide the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = True

    def show(self):
        """Show the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = False

    def export_step(self, file_path: str):
        """Export the assembly to STEP format."""
        # Blender doesn't have native STEP export, would need addon
        raise NotImplementedError("STEP export requires additional Blender addon")

    def export_brep(self, file_path: str):
        """Export the assembly to BREP format."""
        # Blender doesn't have native BREP export
        raise NotImplementedError("BREP export not supported in Blender")

    def copy(self) -> "Assembly":
        """Create a copy of the assembly."""
        new_assembly = Assembly(f"{self.name}_copy")

        # Copy all parts
        for part in self.parts:
            new_part = part.copy()
            new_assembly.add_part(new_part)

        return new_assembly

    def clear(self):
        """Remove all parts from the assembly."""
        # Remove Blender objects
        if self._blender_collection:
            for obj in list(self._blender_collection.objects):
                remove_object(obj, remove_children=True, is_remove_data=True)

        # Clear parts list
        for part in self.parts[:]:  # Create a copy of the list to iterate over
            self.remove_part(part)

    def delete(self):
        """Delete the assembly and all its parts from Blender."""
        self.clear()

        # Remove the collection
        if self._blender_collection:
            remove_collection(self._blender_collection, remove_children=True)
            self._blender_collection = None

    def export_stl(self, file_path: str, tolerance: float = 0.1):
        """Export the assembly to STL format."""
        export_objects(self._get_all_blender_objects(), file_path)

    def export_obj(self, filepath: str):
        """Export the assembly to OBJ format."""
        export_objects(self._get_all_blender_objects(), filepath)

    def __len__(self):
        """Get the number of parts in the assembly."""
        return len(self.parts)

    def __repr__(self):
        return f"<Assembly(name='{self.name}'): {len(self.parts)} parts>"
