"""
build123d-specific sketch get operations.
"""

from typing import TYPE_CHECKING

from codetocad.interfaces.cad.sketch.sketch_get import SketchGetInterface

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
    from codetocad.adapters.build123d.cad.wire.wire import Wire


class SketchGet(SketchGetInterface):
    """build123d-specific sketch get operations."""

    def __init__(self, sketch: "Sketch"):
        self.sketch = sketch

    def wire(self, i) -> "Wire":
        """Get a wire by index."""
        return self.sketch.wires[i]

    def wires(self) -> list["Wire"]:
        """Get all wires in the sketch."""
        return self.sketch.wires

    def wire_count(self) -> int:
        """Get the number of wires in the sketch."""
        return len(self.sketch.wires)

    def edge_count(self) -> int:
        """Get the total number of edges in all wires."""
        return sum(len(wire.edges) for wire in self.sketch.wires)

    def vertex_count(self) -> int:
        """Get the total number of unique vertices in all wires."""
        all_vertices = []
        for wire in self.sketch.wires:
            for vertex in wire.get_vertices():
                if vertex not in all_vertices:
                    all_vertices.append(vertex)
        return len(all_vertices)
