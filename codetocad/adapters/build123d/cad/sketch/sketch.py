"""
build123d implementation of SketchInterface.
"""

from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.adapters.build123d.cad.sketch.sketch_get import SketchGet
from codetocad.adapters.build123d.build123d_actions.sketch_operations import (
    create_sketch_context,
    get_sketch_wires,
    get_sketch_faces,
    make_face_from_sketch,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.wire.wire import Wire
    import build123d as bd


class Sketch(SketchInterface):
    """build123d implementation of SketchInterface."""

    def __init__(
        self, name: str | None = None, native_instance: "bd.BuildSketch | None" = None
    ):
        # build123d-specific properties
        self.name = name or f"sketch_{str(uuid4())[:8]}"
        self.native_instance = native_instance

        # Initialize parent interface properties
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        self.wires: list[Wire] = []  # type: ignore
        self.preset = WirePresetsInterface(Wire, self)
        self.get = SketchGet(self)

        # Create build123d sketch context if not provided
        if self.native_instance is None:
            self.native_instance = create_sketch_context()

    def add(self, wire: "Wire"):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

        # Add the wire to the member sketches
        if self not in wire.member_sketches:
            wire.member_sketches.append(self)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire
        from codetocad.adapters.build123d.cad.wire.wire_add import WireAdd

        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = Wire(self)
            self.add(wire)

        return WireAdd(wire)

    def get_bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire sketch."""
        if not self.wires:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all wires
        wire_boxes = [wire.get_bounding_box() for wire in self.wires]

        # Find overall min and max
        min_x = min(box[0][0] for box in wire_boxes)
        min_y = min(box[0][1] for box in wire_boxes)
        min_z = min(box[0][2] for box in wire_boxes)

        max_x = max(box[1][0] for box in wire_boxes)
        max_y = max(box[1][1] for box in wire_boxes)
        max_z = max(box[1][2] for box in wire_boxes)

        return ((min_x, min_y, min_z), (max_x, max_y, max_z))

    def is_closed(self) -> bool:
        """Check if all wires in the sketch are closed."""
        return all(wire.is_closed() for wire in self.wires)

    def total_length(self) -> float:
        """Get the total length of all wires in the sketch."""
        return sum(wire.length() for wire in self.wires)

    def make_face(self) -> Optional["bd.Face"]:
        """Create a face from the sketch if possible."""
        if not self.wires:
            return None

        try:
            return make_face_from_sketch(self.native_instance)
        except Exception as e:
            print(f"Warning: Could not create face from sketch: {e}")
            return None

    def clear(self):
        """Remove all wires from the sketch."""
        self.wires.clear()

    def copy(self) -> "Sketch":
        """Create a copy of the sketch."""
        new_sketch = Sketch(name=f"{self.name}_copy")

        # Copy all wires
        for wire in self.wires:
            # Create a new wire with the same edges
            from codetocad.adapters.build123d.cad.wire.wire import Wire

            new_wire = Wire(new_sketch)

            # Copy edges
            for edge in wire.edges:
                from codetocad.adapters.build123d.cad.edge.edge import Edge
                from codetocad.adapters.build123d.cad.vertex.vertex import Vertex

                # Create new vertices with same positions
                v1 = Vertex(
                    edge.v1.position[0], edge.v1.position[1], edge.v1.position[2]
                )
                v2 = Vertex(
                    edge.v2.position[0], edge.v2.position[1], edge.v2.position[2]
                )
                new_edge = Edge(v1, v2)
                new_wire.edges.append(new_edge)

            new_wire._update_native_wire()
            new_sketch.add(new_wire)

        return new_sketch

    def __repr__(self):
        return f"<Sketch: {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
