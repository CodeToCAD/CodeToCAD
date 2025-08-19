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
        # Blender-specific properties
        self.name = name or f"assembly_{str(uuid4())[:8]}"
        self._blender_collection: bpy.types.Collection | None = None

        # Initialize parent interface properties
        self.parts: list["Part"] = []  # type: ignore
        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

        # Create Blender representation
        self._create_blender_assembly()

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

    def get_bounding_box(self) -> tuple:
        """Get the bounding box of all parts in the assembly."""
        if not self.parts:
            return ((0, 0, 0), (0, 0, 0))

        all_objects = self._get_all_blender_objects()
        if not all_objects:
            return ((0, 0, 0), (0, 0, 0))

        # Calculate combined bounding box
        min_coords = [float("inf")] * 3
        max_coords = [float("-inf")] * 3

        for obj in all_objects:
            bbox = [
                obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box
            ]
            for corner in bbox:
                for i in range(3):
                    min_coords[i] = min(min_coords[i], corner[i])
                    max_coords[i] = max(max_coords[i], corner[i])

        return (tuple(min_coords), tuple(max_coords))

    def hide(self):
        """Hide the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = True

    def show(self):
        """Show the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = False

    def clear(self):
        """Remove all parts from the assembly."""
        # Remove Blender objects
        if self._blender_collection:
            for obj in list(self._blender_collection.objects):
                remove_object(obj, remove_children=True, is_remove_data=True)

        # Clear parts list
        self.parts.clear()

    def delete(self):
        """Delete the assembly and all its parts from Blender."""
        self.clear()

        # Remove the collection
        if self._blender_collection:
            remove_collection(self._blender_collection, remove_children=True)
            self._blender_collection = None

    def export_stl(self, filepath: str):
        """Export the assembly to STL format."""
        export_objects(self._get_all_blender_objects(), filepath)

    def export_obj(self, filepath: str):
        """Export the assembly to OBJ format."""
        export_objects(self._get_all_blender_objects(), filepath)

    def __repr__(self):
        return f"<Assembly(name='{self.name}'): {len(self.parts)} parts>"
