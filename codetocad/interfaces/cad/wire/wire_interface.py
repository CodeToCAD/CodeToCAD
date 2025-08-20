from typing import TYPE_CHECKING
from abc import ABC
from codetocad.interfaces.cad.edge.edge_interface import EdgeInterface
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.interfaces.cad.wire.wire_geometry_interface import WireGeometryInterface
from codetocad.interfaces.cad.wire.wire_operations_interface import (
    WireOperationsInterface,
)
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
    from codetocad.interfaces.cad.vertex.vertex_interface import VertexInterface


from abc import ABCMeta


class _WirePresetClassPropertyInterface(ABCMeta):
    """Metaclass to provide a preset property for the WireInterface class."""

    @property
    def preset(self):
        return WirePresetsInterface(WireInterface, None)


class WireInterface(ABC, metaclass=_WirePresetClassPropertyInterface):
    """Wire class representing a collection of edges and operations."""

    def __init__(self, sketch: "SketchInterface|None"):
        if sketch is not None:
            self.member_sketches: list[SketchInterface] = [sketch]
        else:
            self.member_sketches: list[SketchInterface] = []

        self.edges: list[EdgeInterface] = []
        self.add = WireAddInterface(self)
        self.get = WireGetInterface(self)
        self.constraint = None  # To be overridden by concrete implementations
        self.name: str | None = None

        # Method group properties
        self.geometry = WireGeometryInterface(self)
        self.operations = WireOperationsInterface(self)

    def __repr__(self):
        return f"Wire({len(self.edges)} edges, closed={self.geometry.is_closed()})"
