from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.cad.sketch.sketch import Sketch
    from codetocad.cad.wire.wire import Wire


class SketchGet:
    def __init__(self, sketch: "Sketch"):
        self.sketch = sketch

    def wire(self, i) -> "Wire":
        return self.sketch.wires[i]
