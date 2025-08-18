from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class SketchGetInterface:
    def __init__(self, sketch: "SketchInterface"):
        self.sketch = sketch

    def wire(self, i) -> "WireInterface":
        return self.sketch.wires[i]
