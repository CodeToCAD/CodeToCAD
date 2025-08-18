from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.sketch.sketch import Sketch
    from codetocad.interfaces.cad.wire.wire import Wire


class SketchGet:
    def __init__(self, sketch: "Sketch"):
        self.sketch = sketch

    def wire(self, i) -> "Wire":
        return self.sketch.wires[i]
