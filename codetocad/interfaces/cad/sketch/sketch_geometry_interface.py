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
        return self.sketch.get_bounding_box()

    def is_closed(self) -> bool:
        """Check if all wires in the sketch are closed."""
        return self.sketch.is_closed()

    def total_length(self) -> float:
        """Get the total length of all wires in the sketch."""
        return self.sketch.total_length()
