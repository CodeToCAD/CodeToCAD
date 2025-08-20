from typing import TYPE_CHECKING
from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface


class _WirePresetClassPropertyInterface(type):
    """Metaclass to provide a preset property for the WireInterface class."""

    @property
    def preset(self):
        return WirePresetsInterface(WireInterface, None)


class WireInterface(metaclass=_WirePresetClassPropertyInterface):
    """Wire class representing a collection of edges and operations."""

    def __init__(self, sketch: "SketchInterface|None"):
        if sketch is not None:
            self.member_sketches: list[SketchInterface] = [sketch]

        self.edges: list[EdgeInterface] = []
        self.add = WireAddInterface(self)
        self.get = WireGetInterface(self)
        self.constraint = WireConstraintInterface(self)

    def __repr__(self):
        return f"Wire({self.edges}"

    def extude(self, length: LengthType) -> "PartInterface":
        from codetocad.interfaces.cad.part.part_interface import PartInterface
        from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

        part = PartInterface()
        sketch = SketchInterface()
        part.sketch = sketch
        sketch.wires.append(self)
        self.member_sketches.append(sketch)

        return part
