from typing import TYPE_CHECKING, Type
from codetocad.core.dimensions.length_expression import LengthType

if TYPE_CHECKING:
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface
    from codetocad.interfaces.cad.wire.wire_interface import WireInterface


class WirePresetsInterface:
    """
    Constructs a WireInterface with preset shapes.
    This class is used to create common part shapes like rectangles, circles and arcs.
    If a SketchInterface is provided, the created WireInterface will be added to that SketchInterface.
    """

    def __init__(self, cls: Type["WireInterface"], sketch: "SketchInterface|None"):
        self.cls = cls
        self.sketch = sketch

    def rectangle(self, x: LengthType, y: LengthType) -> "WireInterface":
        wire = self.cls(self.sketch)
        wire.add.line_to(x, "0")
        wire.add.line_to(x, y)
        wire.add.line_to("0", y)
        wire.add.line_to("0", "0")
        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def circle(self, radius: LengthType) -> "WireInterface":
        """Create a circular wire with the given radius."""
        # This is a base implementation that creates a circular approximation using line segments
        # Concrete implementations should override this with proper circle creation
        import math

        wire = self.cls(self.sketch)

        # Create a circle approximation with 32 segments
        segments = 32
        r = float(radius)

        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = r * math.cos(angle)
            y = r * math.sin(angle)

            if i == 0:
                # Move to first point
                wire.add.point(x, y, 0)
            else:
                wire.add.line_to(x, y, 0)

        # Close the circle
        wire.add.close()

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def regular_polygon(
        self, radius: LengthType, side_count: int, rotation: float = 0
    ) -> "WireInterface":
        """Create a regular polygon wire with the given radius and number of sides."""
        # This is a base implementation that creates a polygon approximation using line segments
        # Concrete implementations should override this with proper polygon creation
        import math

        wire = self.cls(self.sketch)

        # Create a regular polygon with the specified number of sides
        r = float(radius)
        rotation_rad = math.radians(rotation)

        # Calculate vertices
        vertices = []
        for i in range(side_count):
            angle = 2 * math.pi * i / side_count + rotation_rad
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            vertices.append((x, y))

        # Create edges connecting the vertices
        for i in range(side_count):
            x, y = vertices[i]
            if i == 0:
                # Move to first point
                wire.add.point(x, y, 0)
            else:
                wire.add.line_to(x, y, 0)

        # Close the polygon
        wire.add.close()

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
