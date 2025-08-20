"""
build123d implementation of WireInterface.
"""

from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from codetocad.interfaces.cad.wire.wire_interface import WireInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.cad.edge.edge import Edge
from codetocad.adapters.build123d.cad.vertex.vertex import Vertex
from codetocad.adapters.build123d.cad.wire.wire_add import WireAdd
from codetocad.adapters.build123d.cad.wire.wire_constraint import WireConstraint
from codetocad.adapters.build123d.cad.wire.wire_preset_class_property import (
    _WirePresetClassProperty,
)
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_wire_from_edges,
    create_rectangle_wire,
    create_circle_wire,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.part.part import Part
    from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
    import build123d as bd


class Wire(WireInterface, metaclass=_WirePresetClassProperty):
    """build123d implementation of WireInterface."""

    def __init__(
        self,
        sketch: "Sketch|None" = None,
        name: str | None = None,
        native_instance: "bd.Wire | None" = None,
    ):
        # Initialize the parent interface first
        super().__init__(sketch)

        # build123d-specific properties
        self.name = name or f"wire_{str(uuid4())[:8]}"
        self.native_instance = native_instance

        self.member_sketches: list["Sketch"] = [sketch] if sketch is not None else []  # type: ignore

        self.edges: list[Edge] = []  # type: ignore

        self.add = WireAdd(self)
        self.get = WireGetInterface(self)
        self.constraint = WireConstraint(self)

        # If no native instance provided, it will be created when edges are added

    def _update_native_wire(self):
        """Update the native build123d wire from the current edges."""
        if self.edges:
            try:
                # Extract native build123d edges
                native_edges = [edge.native_instance for edge in self.edges]
                self.native_instance = create_wire_from_edges(native_edges)
            except Exception as e:
                # If wire creation fails, keep the individual edges
                print(f"Warning: Could not create wire from edges: {e}")

    def __repr__(self):
        return f"Wire({len(self.edges)} edges, closed={self.geometry.is_closed()})"
