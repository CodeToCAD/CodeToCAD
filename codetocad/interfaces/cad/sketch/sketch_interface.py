from abc import ABC
from codetocad.interfaces.cad.sketch.sketch_get import SketchGetInterface
from codetocad.interfaces.cad.sketch.sketch_geometry_interface import (
    SketchGeometryInterface,
)
from codetocad.interfaces.cad.sketch.sketch_operations_interface import (
    SketchOperationsInterface,
)
from codetocad.interfaces.cad.wire.wire_interface import WireInterface
from codetocad.interfaces.cad.wire.wire_add import WireAddInterface
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface


class SketchInterface(ABC):
    def __init__(self):
        self.wires: list[WireInterface] = []
        self.preset = WirePresetsInterface(WireInterface, self)
        self.get = SketchGetInterface(self)
        self.name: str | None = None

        # Method group properties
        self.geometry = SketchGeometryInterface(self)
        self.operations = SketchOperationsInterface(self)

    def add(self, wire: WireInterface):
        """
        Adds a Wire to the Sketch.
        """
        self.wires.append(wire)

    @property
    def draw(self):
        """Draw on the last wire in the sketch. If no wire exists, create a new one."""
        wire = self.wires[-1] if self.wires else None

        if not wire:
            wire = WireInterface(self)

            self.add(wire)

        return WireAddInterface(wire)

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

    def make_face(self) -> object | None:
        """Create a face from the sketch if possible."""
        # This is adapter-specific and should be implemented by concrete classes
        return None

    def clear(self):
        """Remove all wires from the sketch."""
        self.wires.clear()

    def copy(self) -> "SketchInterface":
        """Create a copy of the sketch."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific sketch type
        raise NotImplementedError("copy must be implemented by concrete classes")

    def __repr__(self):
        return f"<Sketch: {len(self.wires)} wires, {sum([len(wire.edges) for wire in self.wires])} edges>"
