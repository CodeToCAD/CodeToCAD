"""
build123d implementation of SketchOperationsInterface.
"""

from codetocad.interfaces.cad.sketch.sketch_operations_interface import (
    SketchOperationsInterface,
)


class SketchOperations(SketchOperationsInterface):
    """build123d implementation of sketch operations."""

    def copy(self) -> "SketchInterface":
        """Create a copy of the sketch."""
        # Import here to avoid circular imports
        from codetocad.adapters.build123d.cad.sketch.sketch import Sketch

        new_sketch = Sketch(f"{self.sketch.name}_copy")

        # Copy all wires
        for wire in self.sketch.wires:
            # For now, we'll create a simple copy - in a full implementation
            # this would properly copy the wire geometry
            new_sketch.wires.append(wire)

        return new_sketch
