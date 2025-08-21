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

    # Arc preset methods - base implementations using line segments
    def center_arc(
        self,
        center: tuple[float, float, float],
        radius: LengthType,
        start_angle: float,
        arc_size: float,
    ) -> "WireInterface":
        """Create a center arc wire. Base implementation using line segments."""
        import math

        wire = self.cls(self.sketch)

        # Convert to radians
        start_rad = math.radians(start_angle)
        arc_rad = math.radians(arc_size)

        # Create arc approximation with line segments
        segments = max(
            8, int(abs(arc_size) / 10)
        )  # At least 8 segments, more for larger arcs
        r = float(radius)
        cx, cy, cz = center

        for i in range(segments + 1):
            angle = start_rad + (arc_rad * i / segments)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)

            if i == 0:
                wire.add.point(x, y, cz)
            else:
                wire.add.line_to(x, y, cz)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def three_point_arc(
        self,
        start: tuple[float, float, float],
        mid: tuple[float, float, float],
        end: tuple[float, float, float],
    ) -> "WireInterface":
        """Create a three-point arc wire. Base implementation using line segments."""
        # For base implementation, create a simple approximation
        wire = self.cls(self.sketch)

        # Simple approximation: create line segments through the points
        wire.add.point(start[0], start[1], start[2])
        wire.add.line_to(mid[0], mid[1], mid[2])
        wire.add.line_to(end[0], end[1], end[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def radius_arc(
        self,
        start_point: tuple[float, float, float],
        end_point: tuple[float, float, float],
        radius: LengthType,
        short_sagitta: bool = True,
    ) -> "WireInterface":
        """Create a radius arc wire. Base implementation using line segments."""
        # For base implementation, create a simple line
        wire = self.cls(self.sketch)
        wire.add.point(start_point[0], start_point[1], start_point[2])
        wire.add.line_to(end_point[0], end_point[1], end_point[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def tangent_arc(
        self,
        start: tuple[float, float, float],
        end: tuple[float, float, float],
        tangent: tuple[float, float, float],
        tangent_from_first: bool = True,
    ) -> "WireInterface":
        """Create a tangent arc wire. Base implementation using line segments."""
        # For base implementation, create a simple line
        wire = self.cls(self.sketch)
        wire.add.point(start[0], start[1], start[2])
        wire.add.line_to(end[0], end[1], end[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # Curve preset methods - base implementations using line segments
    def spline(
        self,
        points: list[tuple[float, float, float]],
        tangents: list[tuple[float, float, float]] | None = None,
        periodic: bool = False,
    ) -> "WireInterface":
        """Create a spline wire. Base implementation using line segments."""
        wire = self.cls(self.sketch)

        # Simple approximation: connect points with line segments
        for i, point in enumerate(points):
            if i == 0:
                wire.add.point(point[0], point[1], point[2])
            else:
                wire.add.line_to(point[0], point[1], point[2])

        if periodic and len(points) > 2:
            # Close the spline
            first_point = points[0]
            wire.add.line_to(first_point[0], first_point[1], first_point[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def bezier(
        self,
        control_points: list[tuple[float, float, float]],
        weights: list[float] | None = None,
    ) -> "WireInterface":
        """Create a bezier curve wire. Base implementation using line segments."""
        wire = self.cls(self.sketch)

        # Simple approximation: connect control points with line segments
        for i, point in enumerate(control_points):
            if i == 0:
                wire.add.point(point[0], point[1], point[2])
            else:
                wire.add.line_to(point[0], point[1], point[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # Line preset methods
    def polar_line(
        self,
        start: tuple[float, float, float],
        length: LengthType,
        angle: float,
    ) -> "WireInterface":
        """Create a polar line wire."""
        import math

        wire = self.cls(self.sketch)

        # Calculate end point
        length_val = float(length)
        angle_rad = math.radians(angle)
        end_x = start[0] + length_val * math.cos(angle_rad)
        end_y = start[1] + length_val * math.sin(angle_rad)
        end_z = start[2]

        wire.add.point(start[0], start[1], start[2])
        wire.add.line_to(end_x, end_y, end_z)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def fillet_polyline(
        self,
        points: list[tuple[float, float, float]],
        radius: LengthType,
        close: bool = False,
    ) -> "WireInterface":
        """Create a filleted polyline wire. Base implementation without fillets."""
        wire = self.cls(self.sketch)

        # Simple approximation: create polyline without fillets
        for i, point in enumerate(points):
            if i == 0:
                wire.add.point(point[0], point[1], point[2])
            else:
                wire.add.line_to(point[0], point[1], point[2])

        if close and len(points) > 2:
            first_point = points[0]
            wire.add.line_to(first_point[0], first_point[1], first_point[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # 2D Shape preset methods - base implementations using line segments
    def ellipse(
        self, x_radius: LengthType, y_radius: LengthType, rotation: float = 0
    ) -> "WireInterface":
        """Create an ellipse wire. Base implementation using line segments."""
        import math

        wire = self.cls(self.sketch)

        # Create ellipse approximation with line segments
        segments = 32
        x_r = float(x_radius)
        y_r = float(y_radius)
        rotation_rad = math.radians(rotation)

        for i in range(segments):
            angle = 2 * math.pi * i / segments
            # Ellipse parametric equations
            x = x_r * math.cos(angle)
            y = y_r * math.sin(angle)

            # Apply rotation
            if rotation != 0:
                x_rot = x * math.cos(rotation_rad) - y * math.sin(rotation_rad)
                y_rot = x * math.sin(rotation_rad) + y * math.cos(rotation_rad)
                x, y = x_rot, y_rot

            if i == 0:
                wire.add.point(x, y, 0)
            else:
                wire.add.line_to(x, y, 0)

        # Close the ellipse
        wire.add.close()

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polygon(self, points: list[tuple[float, float, float]]) -> "WireInterface":
        """Create a polygon wire from points."""
        wire = self.cls(self.sketch)

        for i, point in enumerate(points):
            if i == 0:
                wire.add.point(point[0], point[1], point[2])
            else:
                wire.add.line_to(point[0], point[1], point[2])

        # Close the polygon
        if len(points) > 2:
            first_point = points[0]
            wire.add.line_to(first_point[0], first_point[1], first_point[2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def rectangle_rounded(
        self, width: LengthType, height: LengthType, radius: LengthType
    ) -> "WireInterface":
        """Create a rounded rectangle wire. Base implementation without rounding."""
        # For base implementation, create a regular rectangle
        return self.rectangle(width, height)

    def triangle(
        self,
        a: float | None = None,
        b: float | None = None,
        c: float | None = None,
        A: float | None = None,
        B: float | None = None,
        C: float | None = None,
    ) -> "WireInterface":
        """Create a triangle wire. Base implementation creates equilateral triangle."""
        import math

        wire = self.cls(self.sketch)

        # Simple implementation: create equilateral triangle if no parameters given
        side_length = a or b or c or 1.0
        height = side_length * math.sqrt(3) / 2

        # Triangle vertices
        points = [
            (0, 0, 0),
            (side_length, 0, 0),
            (side_length / 2, height, 0),
        ]

        for i, point in enumerate(points):
            if i == 0:
                wire.add.point(point[0], point[1], point[2])
            else:
                wire.add.line_to(point[0], point[1], point[2])

        # Close the triangle
        wire.add.line_to(points[0][0], points[0][1], points[0][2])

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def trapezoid(
        self,
        width: LengthType,
        height: LengthType,
        left_side_angle: float,
        right_side_angle: float | None = None,
    ) -> "WireInterface":
        """Create a trapezoid wire. Base implementation creates rectangle."""
        # For base implementation, create a rectangle
        return self.rectangle(width, height)

    def text(
        self,
        text: str,
        font_size: float,
        font: str = "Arial",
        font_path: str | None = None,
    ) -> "WireInterface":
        """Create text outlines as wire geometry.

        Args:
            text: Text string to render
            font_size: Size of the font in model units
            font: Font name (default: "Arial")
            font_path: Optional path to specific font file

        Returns:
            WireInterface representing the text outline

        Note: Base implementation creates a simple rectangular placeholder.
        Concrete implementations should override with proper text rendering.
        """
        # Base implementation: create a simple rectangular placeholder
        # representing the approximate text bounds
        text_width = len(text) * font_size * 0.6  # Rough approximation
        text_height = font_size

        wire = self.cls(self.sketch)

        # Create a simple rectangle as placeholder
        wire.add.point(0, 0, 0)
        wire.add.line_to(text_width, 0, 0)
        wire.add.line_to(text_width, text_height, 0)
        wire.add.line_to(0, text_height, 0)
        wire.add.line_to(0, 0, 0)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
