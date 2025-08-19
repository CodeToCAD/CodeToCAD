from typing import TYPE_CHECKING

from codetocad.interfaces.cad.sketch.sketch_get import SketchGetInterface

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.sketch.sketch import Sketch
    from codetocad.adapters.blender.cad.wire.wire import Wire


class SketchGet(SketchGetInterface):
    """Blender-specific sketch get operations."""

    def __init__(self, sketch: "Sketch"):
        self.sketch = sketch

    def wire(self, i) -> "Wire":
        return self.sketch.wires[i]
