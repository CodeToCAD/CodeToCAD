from typing import TYPE_CHECKING
from codetocad.interfaces.cad.part.part_interface import PartInterface
from codetocad.interfaces.cad.part.part_presets import PartPresetsInterface

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface


class AssemblyAddInterface:
    def __init__(self, assembly: "AssemblyInterface"):
        self.assembly = assembly
        self.preset = PartPresetsInterface(assembly)

    def __call__(self, part: PartInterface):
        """
        Adds a Wire to the Sketch.
        """
        self.assembly.parts.append(part)
