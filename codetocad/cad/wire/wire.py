from typing import TYPE_CHECKING
from codetocad.cad.edge.edge import Edge
from codetocad.cad.wire.wire_constraint import WireConstraint
from codetocad.cad.wire.wire_draw import WireDraw
from codetocad.cad.wire.wire_operations import WireOperation, WireOperationExtrude
from codetocad.cad.wire.wire_presets import WirePresets
from codetocad.cad.wire.wire_get import WireGet
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.cad.part.part import Part
    from codetocad.cad.sketch.sketch import Sketch


class _WirePresetClassProperty(type):
    @property
    def preset(self):
        return WirePresets(Wire, None)


class Wire(metaclass=_WirePresetClassProperty):
    def __init__(self, sketch: "Sketch|None"):
        if sketch is not None:
            self.member_sketches: list[Sketch] = [sketch]

        self.edges: list[Edge] = []
        self.draw = WireDraw(self)
        self.get = WireGet(self)
        self.constraint = WireConstraint(self)

        self.operations: list[WireOperation] = []

    def __repr__(self):
        return f"Wire({self.edges}"

    def extude(self, length: LengthType) -> "Part":
        from codetocad.cad.part.part import Part
        from codetocad.cad.sketch.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self)

        self.operations.append(WireOperationExtrude(length=length))

        return part
