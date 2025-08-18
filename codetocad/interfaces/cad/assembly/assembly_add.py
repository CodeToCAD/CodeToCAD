from typing import TYPE_CHECKING
from codetocad.interfaces.cad.part.part import Part
from codetocad.interfaces.cad.part.part_presets import PartPresets

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly import Assembly


class AssemblyAdd:
    def __init__(self, assembly: "Assembly"):
        self.assembly = assembly
        self.preset = PartPresets(assembly)

    def __call__(self, part: Part):
        """
        Adds a Wire to the Sketch.
        """
        self.assembly.parts.append(part)
