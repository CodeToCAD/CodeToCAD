import bpy
from typing import TYPE_CHECKING

from codetocad.interfaces.cad.assembly.assembly_add import AssemblyAddInterface
from codetocad.adapters.blender.blender_actions.collections import (
    get_collection_or_none,
    link_object_to_collection,
    unlink_object_from_collection,
)

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
        part_obj = part.get_blender_object()
        if part_obj:
            assembly_collection = get_collection_or_none(self.assembly.name)
            if assembly_collection:
                # Add to assembly collection if not already there
                if part_obj.name not in assembly_collection.objects:
                    link_object_to_collection(part_obj, assembly_collection)

                    # Remove from scene collection to avoid duplication
                    scene_collection = bpy.context.scene.collection
                    if part_obj.name in scene_collection.objects:
                        unlink_object_from_collection(part_obj, scene_collection)
