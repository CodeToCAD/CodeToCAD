from typing import TYPE_CHECKING
from codetocad.interfaces.cad.sketch.sketch import Sketch
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.assembly.assembly import Assembly
    from codetocad.interfaces.cad.part.part import Part


class PartPresets:
    """
    Constructs a part with preset shapes.
    This class is used to create common part shapes like cubes, cylinders, etc.
    If an assembly is provided, the created part will be added to that assembly.
    """

    def __init__(self, assembly: "Assembly|None" = None):
        self.assembly = assembly

    def cube(self, x: LengthType, y: LengthType, z: LengthType) -> "Part":
        wire = Sketch().preset.rectangle(x, y)
        part = wire.extude(z)

        if self.assembly:
            self.assembly.parts.append(part)

        return part
