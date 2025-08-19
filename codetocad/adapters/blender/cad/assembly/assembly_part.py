from typing import TYPE_CHECKING

from codetocad.interfaces.cad.assembly.assembly_part import AssemblyPartInterface

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly


class AssemblyPart(AssemblyPartInterface):
    """Blender-specific assembly part operations."""

    def __init__(self, assembly: "Assembly"):
        super().__init__(assembly)
