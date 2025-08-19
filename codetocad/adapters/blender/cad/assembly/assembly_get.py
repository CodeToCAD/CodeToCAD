from typing import TYPE_CHECKING

from codetocad.interfaces.cad.assembly.assembly_get import AssemblyGetInterface
from codetocad.adapters.blender.cad.assembly.assembly_part import AssemblyPart

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.assembly.assembly import Assembly


class AssemblyGet(AssemblyGetInterface):
    """Blender-specific assembly get operations."""

    def __init__(self, assembly: "Assembly"):
        self.assembly = assembly
        self.part = AssemblyPart(assembly)
        self.parts = self.assembly.parts
