from typing import TYPE_CHECKING, Type
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.cad.sketch.sketch import Sketch
    from codetocad.cad.wire.wire import Wire


class WirePresets:
    """
    Constructs a Wire with preset shapes.
    This class is used to create common part shapes like rectangles, circles and arcs.
    If a Sketch is provided, the created Wire will be added to that Sketch.
    """

    def __init__(self, cls: Type["Wire"], sketch: "Sketch|None"):
        self.cls = cls
        self.sketch = sketch

    def rectangle(self, x: LengthType, y: LengthType) -> "Wire":
        wire = self.cls(self.sketch)
        wire.add.point("0", "0")
        wire.add.line_to(x, "0")
        wire.add.line_to(x, y)
        wire.add.line_to("0", y)
        wire.add.line_to("0", "0")
        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
