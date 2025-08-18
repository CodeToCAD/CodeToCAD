from typing import TYPE_CHECKING
from codetocad.interfaces.cad.assembly.assembly_part import AssemblyPart


if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly import Assembly


class AssemblyGet:
    def __init__(self, assembly: "Assembly"):
        self.assembly = assembly

        self.part = AssemblyPart(assembly)
        self.parts = self.assembly.parts
