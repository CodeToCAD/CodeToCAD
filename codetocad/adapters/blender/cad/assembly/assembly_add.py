import bpy
from typing import TYPE_CHECKING

from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly
    from codetocad.adapters.blender.cad.part.part import Part
    from codetocad.adapters.blender.cad.part.part_presets import PartPresets


class AssemblyAdd(AssemblyAddInterface):
    """Blender-specific assembly add operations."""

    def __init__(self, assembly: "Assembly"):
        from codetocad.adapters.blender.cad.part.part_presets import PartPresets

        self.assembly = assembly
        self.preset = PartPresets(assembly)

    def __call__(self, part: "Part"):
        """
        Adds a Part to the Assembly.
        """
        self.assembly.parts.append(part)

        # Add part's Blender object to assembly collection
        if part.get_blender_object() and self.assembly.name in bpy.data.collections:
            assembly_collection = bpy.data.collections[self.assembly.name]
            part_obj = part.get_blender_object()

            # Add to assembly collection if not already there
            if part_obj.name not in assembly_collection.objects:
                assembly_collection.objects.link(part_obj)

                # Remove from scene collection to avoid duplication
                if part_obj.name in bpy.context.scene.collection.objects:
                    bpy.context.scene.collection.objects.unlink(part_obj)
