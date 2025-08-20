from typing import TYPE_CHECKING
from codetocad.interfaces.cad.assembly.assembly_part import AssemblyPartInterface


if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class AssemblyGetInterface:
    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly

        self.part = AssemblyPartInterface(assembly)
        self.parts = self.assembly.parts
