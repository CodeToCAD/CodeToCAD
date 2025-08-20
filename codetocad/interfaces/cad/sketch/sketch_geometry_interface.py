"""
Geometry operations interface for Sketch objects.
"""

from abc import ABC


class SketchGeometryInterface(ABC):
    """Interface for sketch geometry operations."""

    def __init__(self, sketch: "SketchInterface"):
        self.sketch = sketch

    def bounding_box(
        self,
    ) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Get the bounding box of the entire sketch."""
        if not self.sketch.wires:
            return ((0, 0, 0), (0, 0, 0))

        # Get bounding boxes of all wires
        wire_boxes = [wire.geometry.bounding_box() for wire in self.sketch.wires]

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
        return all(wire.geometry.is_closed() for wire in self.sketch.wires)

    def total_length(self) -> float:
        """Get the total length of all wires in the sketch."""
        return sum(wire.geometry.length() for wire in self.sketch.wires)
