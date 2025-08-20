"""
Operations interface for Sketch objects.
"""

from abc import ABC


class SketchOperationsInterface(ABC):
    """Interface for sketch operations."""

    def __init__(self, sketch: "SketchInterface"):
        self.sketch = sketch

    def make_face(self) -> object | None:
        """Create a face from the sketch if possible."""
        return self.sketch.make_face()

    def clear(self):
        """Remove all wires from the sketch."""
        return self.sketch.clear()

    def copy(self) -> "SketchInterface":
        """Create a copy of the sketch."""
        return self.sketch.copy()
