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
        # This is adapter-specific and should be implemented by concrete classes
        return None

    def clear(self):
        """Remove all wires from the sketch."""
        self.sketch.wires.clear()

    def copy(self) -> "SketchInterface":
        """Create a copy of the sketch."""
        # This method should be implemented by concrete classes
        # as it requires creating new instances of the specific sketch type
        raise NotImplementedError("copy must be implemented by concrete classes")
