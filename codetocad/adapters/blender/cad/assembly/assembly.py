import bpy
import mathutils
from typing import TYPE_CHECKING, List
from uuid import uuid4

from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
from codetocad.adapters.blender.cad.assembly.assembly_add import AssemblyAdd
from codetocad.adapters.blender.cad.assembly.assembly_get import AssemblyGet
from codetocad.adapters.blender.blender_actions.collections import create_collection

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.part.part import Part


class Assembly(AssemblyInterface):
    """Blender implementation of AssemblyInterface."""

    def __init__(self, name: str | None = None):
        # Blender-specific properties
        self.name = name or f"assembly_{str(uuid4())[:8]}"
        self._blender_collection: bpy.types.Collection | None = None

        # Initialize parent interface properties
        self.parts: List["Part"] = []
        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

        # Create Blender representation
        self._create_blender_assembly()

    def _create_blender_assembly(self):
        """Create a Blender collection to represent this assembly."""
        try:
            create_collection(self.name)
            self._blender_collection = bpy.data.collections[self.name]
        except Exception:
            # Collection might already exist
            self._blender_collection = bpy.data.collections.get(self.name)

    def get_collection(self) -> "bpy.types.Collection | None":
        """Get the Blender collection representing this assembly."""
        return self._blender_collection

    def get_all_objects(self) -> "list[bpy.types.Object]":
        """Get all Blender objects in this assembly."""
        if self._blender_collection:
            return list(self._blender_collection.objects)
        return []

    def move(self, x: float, y: float, z: float):
        """Move all parts in the assembly."""
        for part in self.parts:
            if part.get_blender_object():
                current_loc = part.get_blender_object().location
                part.get_blender_object().location = (
                    current_loc[0] + x,
                    current_loc[1] + y,
                    current_loc[2] + z,
                )

    def rotate(self, x: float, y: float, z: float):
        """Rotate all parts in the assembly."""
        for part in self.parts:
            if part.get_blender_object():
                current_rot = part.get_blender_object().rotation_euler
                part.get_blender_object().rotation_euler = (
                    current_rot[0] + x,
                    current_rot[1] + y,
                    current_rot[2] + z,
                )

    def scale(self, x: float, y: float = None, z: float = None):
        """Scale all parts in the assembly."""
        y = y or x
        z = z or x

        for part in self.parts:
            if part.get_blender_object():
                current_scale = part.get_blender_object().scale
                part.get_blender_object().scale = (
                    current_scale[0] * x,
                    current_scale[1] * y,
                    current_scale[2] * z,
                )

    def get_bounding_box(self) -> tuple:
        """Get the bounding box of all parts in the assembly."""
        if not self.parts:
            return ((0, 0, 0), (0, 0, 0))

        all_objects = [
            part.get_blender_object()
            for part in self.parts
            if part.get_blender_object()
        ]
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
                self._blender_collection.objects.unlink(obj)
                if obj.data:
                    # Remove mesh data
                    if isinstance(obj.data, bpy.types.Mesh):
                        bpy.data.meshes.remove(obj.data)
                    elif isinstance(obj.data, bpy.types.Curve):
                        bpy.data.curves.remove(obj.data)
                bpy.data.objects.remove(obj)

        # Clear parts list
        self.parts.clear()

    def delete(self):
        """Delete the assembly and all its parts from Blender."""
        self.clear()

        # Remove the collection
        if self._blender_collection:
            bpy.data.collections.remove(self._blender_collection)
            self._blender_collection = None

    def export_stl(self, filepath: str):
        """Export the assembly to STL format."""
        if not self.parts:
            return

        # Select all objects in the assembly
        bpy.ops.object.select_all(action="DESELECT")
        for part in self.parts:
            obj = part.get_blender_object()
            if obj:
                obj.select_set(True)

        # Export selected objects
        bpy.ops.wm.stl_export(filepath=filepath, export_selected_objects=True)

    def export_obj(self, filepath: str):
        """Export the assembly to OBJ format."""
        if not self.parts:
            return

        # Select all objects in the assembly
        bpy.ops.object.select_all(action="DESELECT")
        for part in self.parts:
            obj = part.get_blender_object()
            if obj:
                obj.select_set(True)

        # Export selected objects
        bpy.ops.wm.obj_export(filepath=filepath, export_selected_objects=True)

    def __repr__(self):
        return f"<Assembly(name='{self.name}'): {len(self.parts)} parts>"
