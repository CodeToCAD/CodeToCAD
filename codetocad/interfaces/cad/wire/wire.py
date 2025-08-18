from typing import TYPE_CHECKING
from codetocad.interfaces.cad.edge.edge import Edge
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraint
from codetocad.interfaces.cad.wire.wire_add import WireAdd
from codetocad.interfaces.cad.wire.wire_presets import WirePresets
from codetocad.interfaces.cad.wire.wire_get import WireGet
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part import Part
    from codetocad.interfaces.cad.sketch.sketch import Sketch


class _WirePresetClassProperty(type):
    """Metaclass to provide a preset property for the Wire class."""

    @property
    def preset(self):
        return WirePresets(Wire, None)


class Wire(metaclass=_WirePresetClassProperty):
    """Wire class representing a collection of edges and operations."""

    def __init__(self, sketch: "Sketch|None"):
        if sketch is not None:
            self.member_sketches: list[Sketch] = [sketch]

        self.edges: list[Edge] = []
        self.add = WireAdd(self)
        self.get = WireGet(self)
        self.constraint = WireConstraint(self)

    def __repr__(self):
        return f"Wire({self.edges}"

    def extude(self, length: LengthType) -> "Part":
        from codetocad.interfaces.cad.part.part import Part
        from codetocad.interfaces.cad.sketch.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self)
        self.member_sketches.append(sketch)

        return part
