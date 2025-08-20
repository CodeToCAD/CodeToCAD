"""
build123d implementation of WireInterface.
"""

from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from codetocad.interfaces.cad.wire.wire_interface import WireInterface
from codetocad.interfaces.cad.wire.wire_constraint import WireConstraintInterface
from codetocad.interfaces.cad.wire.wire_get import WireGetInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.cad.edge.edge import Edge
from codetocad.adapters.build123d.cad.vertex.vertex import Vertex
from codetocad.adapters.build123d.cad.wire.wire_add import WireAdd
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
        self.constraint = WireConstraintInterface(self)

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

    def is_closed(self) -> bool:
        """Check if the wire is closed."""
        if len(self.edges) < 3:
            return False

        # Check if the last vertex connects to the first vertex
        first_vertex = self.edges[0].v1
        last_vertex = self.edges[-1].v2

        # Use a small tolerance for comparison
        tolerance = 1e-6
        distance = first_vertex.distance_to(last_vertex)
        return distance < tolerance

    def length(self) -> float:
        """Get the total length of the wire."""
        return sum(edge.length() for edge in self.edges)

    def get_vertices(self) -> List[Vertex]:
        """Get all unique vertices in the wire."""
        vertices = []
        for edge in self.edges:
            if edge.v1 not in vertices:
                vertices.append(edge.v1)
            if edge.v2 not in vertices:
                vertices.append(edge.v2)
        return vertices

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the wire as (min_point, max_point)."""
        if not self.edges:
            return ((0, 0, 0), (0, 0, 0))

        vertices = self.get_vertices()
        positions = [v.position for v in vertices]

        min_x = min(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        min_z = min(pos[2] for pos in positions)

        max_x = max(pos[0] for pos in positions)
        max_y = max(pos[1] for pos in positions)
        max_z = max(pos[2] for pos in positions)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def reverse(self) -> "Wire":
        """Create a new wire with reversed direction."""
        reversed_wire = Wire(name=f"{self.name}_reversed")

        # Reverse the order of edges and flip each edge
        for edge in reversed(self.edges):
            reversed_edge = Edge(edge.v2, edge.v1)
            reversed_wire.edges.append(reversed_edge)

        reversed_wire._update_native_wire()
        return reversed_wire

    def extude(self, length: LengthType) -> "Part":
        """Extrude the wire to create a part."""
        from codetocad.adapters.build123d.cad.part.part import Part
        from codetocad.adapters.build123d.cad.sketch.sketch import Sketch

        part = Part()
        sketch = Sketch()
        part.sketch = sketch
        sketch.wires.append(self)
        self.member_sketches.append(sketch)

        # TODO: Implement actual extrusion using build123d
        # For now, just return the part with the sketch

        return part

    def __repr__(self):
        return f"Wire({len(self.edges)} edges, closed={self.is_closed()})"
