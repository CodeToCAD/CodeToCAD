from typing import TYPE_CHECKING
from codetocad.cad.edge.edge import Edge
from codetocad.cad.wire.wire_constraint import WireConstraint
from codetocad.cad.wire.wire_add import WireAdd
from codetocad.cad.wire.wire_operations import WireOperationType, WireOperationExtrude
from codetocad.cad.wire.wire_presets import WirePresets
from codetocad.cad.wire.wire_get import WireGet
from codetocad.core.dimensions.length import LengthType

if TYPE_CHECKING:
    from codetocad.cad.part.part import Part
    from codetocad.cad.sketch.sketch import Sketch


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

        self._operations: list[WireOperationType] = []

    def __repr__(self):
        return f"Wire({self.edges}"

    def _add_operation(self, operation: WireOperationType):
        """INTERNAL USE: Registers an operation to the wire to be consumed by a provider."""
        self._operations.append(operation)

    def extude(self, length: LengthType) -> "Part":
        from codetocad.cad.part.part import Part
        from codetocad.cad.sketch.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self)
        self.member_sketches.append(sketch)

        self._add_operation(WireOperationExtrude(length=length))

        return part
