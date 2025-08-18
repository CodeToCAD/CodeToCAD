from typing import TYPE_CHECKING, Type
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class WirePresetsInterface:
    """
    Constructs a WireInterface with preset shapes.
    This class is used to create common part shapes like rectangles, circles and arcs.
    If a SketchInterface is provided, the created WireInterface will be added to that SketchInterface.
    """

    def __init__(self, cls: Type["WireInterface"], sketch: "SketchInterface|None"):
        self.cls = cls
        self.sketch = sketch

    def rectangle(self, x: LengthType, y: LengthType) -> "WireInterface":
        wire = self.cls(self.sketch)
        wire.add.line_to(x, "0")
        wire.add.line_to(x, y)
        wire.add.line_to("0", y)
        wire.add.line_to("0", "0")
        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
