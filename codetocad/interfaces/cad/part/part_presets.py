from typing import TYPE_CHECKING
from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly_interface import AssemblyInterface
    from codetocad.interfaces.cad.part.part_interface import PartInterface


class PartPresetsInterface:
    """
    Constructs a part with preset shapes.
    This class is used to create common part shapes like cubes, cylinders, etc.
    If an assembly is provided, the created part will be added to that assembly.
    """

    def __init__(self, assembly: "AssemblyInterface|None" = None):
        self.assembly = assembly

    def cube(self, x: LengthType, y: LengthType, z: LengthType) -> "PartInterface":
        wire = SketchInterface().preset.rectangle(x, y)
        part = wire.extude(z)

        if self.assembly:
            self.assembly.parts.append(part)

        return part
