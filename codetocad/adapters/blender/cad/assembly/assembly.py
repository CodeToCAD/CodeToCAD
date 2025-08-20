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


if TYPE_CHECKING:
    import bpy
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class Assembly(AssemblyInterface):
    """Blender implementation of AssemblyInterface."""

    def __init__(self, name: str | None = None):
        # Initialize parent interface first
        super().__init__()

        # Blender-specific properties
        self.name = name or f"assembly_{str(uuid4())[:8]}"
        self._blender_collection: bpy.types.Collection | None = None

        # Initialize parent interface properties
        self.parts: list["PartInterface"] = []  # type: ignore
        self.add = AssemblyAdd(self)
        self.get = AssemblyGet(self)

        # Override method group properties with Blender-specific implementations
        from codetocad.adapters.blender.cad.assembly.assembly_geometry import (
            AssemblyGeometry,
        )
        from codetocad.adapters.blender.cad.assembly.assembly_transform import (
            AssemblyTransform,
        )
        from codetocad.adapters.blender.cad.assembly.assembly_export import (
            AssemblyExport,
        )

        self.geometry = AssemblyGeometry(self)
        self.transform = AssemblyTransform(self)
        self.export = AssemblyExport(self)

        # Create Blender representation
        self._create_blender_assembly()

    def set_name(self, name: str):
        """Set the assembly name."""
        self.name = name

    def add_part(self, part: "PartInterface"):
        """Add a part to the assembly."""
        if part not in self.parts:
            self.parts.append(part)
            if self not in part.member_assemblies:
                part.member_assemblies.append(self)

    def remove_part(self, part: "PartInterface"):
        """Remove a part from the assembly."""
        if part in self.parts:
            self.parts.remove(part)
            if self in part.member_assemblies:
                part.member_assemblies.remove(self)

    def get_part_by_name(self, name: str) -> "PartInterface | None":
        """Get a part by name."""
        for part in self.parts:
            if part.name == name:
                return part
        return None

    def get_part_by_index(self, index: int) -> "PartInterface":
        """Get a part by index."""
        return self.parts[index]

    def _create_blender_assembly(self):
        """Create a Blender collection to represent this assembly."""
        if self.name is None:
            return
        try:
            create_collection(self.name)
            self._blender_collection = get_collection(self.name)
        except Exception:
            # Collection might already exist
            self._blender_collection = get_collection_or_none(self.name)

    def _get_collection(self) -> "bpy.types.Collection | None":
        """Get the Blender collection representing this assembly."""
        return self._blender_collection

    def hide(self):
        """Hide the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = True

    def show(self):
        """Show the assembly in Blender."""
        if self._blender_collection:
            self._blender_collection.hide_viewport = False

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

    def __len__(self):
        """Get the number of parts in the assembly."""
        return len(self.parts)

    def __repr__(self):
        return f"<Assembly(name='{self.name}'): {len(self.parts)} parts>"
