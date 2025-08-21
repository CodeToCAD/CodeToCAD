"""
build123d-specific wire presets.
"""

from typing import TYPE_CHECKING
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.build123d.build123d_actions.geometry import (
    create_rectangle_wire,
    create_circle_wire,
    create_regular_polygon_wire,
    create_polyline_wire,
    create_center_arc_wire,
    create_three_point_arc_wire,
    create_radius_arc_wire,
    create_tangent_arc_wire,
    create_spline_wire,
    create_bezier_wire,
    create_polar_line_wire,
    create_fillet_polyline_wire,
    create_ellipse_wire,
    create_polygon_wire,
    create_rectangle_rounded_wire,
    create_triangle_wire,
    create_trapezoid_wire,
    create_text_wire,
)

if TYPE_CHECKING:
    from codetocad.adapters.build123d.cad.sketch.sketch import Sketch
    from codetocad.adapters.build123d.cad.wire.wire import Wire


class Build123dWirePresets(WirePresetsInterface):
    """build123d-specific wire presets that use native build123d geometry creation."""

    def rectangle(self, x: LengthType, y: LengthType) -> "Wire":
        """Create a rectangular wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d rectangle
        native_rect = create_rectangle_wire(x, y)
        wire = Wire(self.sketch, native_instance=native_rect)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def circle(self, radius: LengthType) -> "Wire":
        """Create a circular wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d circle
        native_circle = create_circle_wire(radius)
        wire = Wire(self.sketch, native_instance=native_circle)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def regular_polygon(
        self, radius: LengthType, side_count: int, rotation: float = 0
    ) -> "Wire":
        """Create a regular polygon wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d regular polygon
        native_polygon = create_regular_polygon_wire(radius, side_count, rotation)
        wire = Wire(self.sketch, native_instance=native_polygon)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polyline(self, points: list[tuple[float, float]]) -> "Wire":
        """Create a polyline wire using build123d primitives."""
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        # Create wire with native build123d polyline
        native_polyline = create_polyline_wire(points)
        wire = Wire(self.sketch, native_instance=native_polyline)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # Arc preset methods
    def center_arc(
        self,
        center: tuple[float, float, float],
        radius: LengthType,
        start_angle: float,
        arc_size: float,
    ) -> "Wire":
        """Create a center arc wire using build123d primitives.

        Args:
            center: Center point of the arc (x, y, z)
            radius: Arc radius
            start_angle: Starting angle in degrees from x-axis
            arc_size: Angular size of arc in degrees
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_arc = create_center_arc_wire(center, radius, start_angle, arc_size)
        wire = Wire(self.sketch, native_instance=native_arc)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def three_point_arc(
        self,
        start: tuple[float, float, float],
        mid: tuple[float, float, float],
        end: tuple[float, float, float],
    ) -> "Wire":
        """Create a three-point arc wire using build123d primitives.

        Args:
            start: Start point of the arc
            mid: Middle point the arc passes through
            end: End point of the arc
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_arc = create_three_point_arc_wire(start, mid, end)
        wire = Wire(self.sketch, native_instance=native_arc)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def radius_arc(
        self,
        start_point: tuple[float, float, float],
        end_point: tuple[float, float, float],
        radius: LengthType,
        short_sagitta: bool = True,
    ) -> "Wire":
        """Create a radius arc wire using build123d primitives.

        Args:
            start_point: Start point of the arc
            end_point: End point of the arc
            radius: Arc radius
            short_sagitta: If True, selects the short sagitta (height of arc from chord)
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_arc = create_radius_arc_wire(
            start_point, end_point, radius, short_sagitta
        )
        wire = Wire(self.sketch, native_instance=native_arc)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def tangent_arc(
        self,
        start: tuple[float, float, float],
        end: tuple[float, float, float],
        tangent: tuple[float, float, float],
        tangent_from_first: bool = True,
    ) -> "Wire":
        """Create a tangent arc wire using build123d primitives.

        Args:
            start: Start point of the arc
            end: End point of the arc
            tangent: Tangent vector to constrain the arc
            tangent_from_first: Apply tangent to first point if True, else to end point
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_arc = create_tangent_arc_wire(start, end, tangent, tangent_from_first)
        wire = Wire(self.sketch, native_instance=native_arc)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # Curve preset methods
    def spline(
        self,
        points: list[tuple[float, float, float]],
        tangents: list[tuple[float, float, float]] | None = None,
        periodic: bool = False,
    ) -> "Wire":
        """Create a spline wire using build123d primitives.

        Args:
            points: List of points defining the spline
            tangents: Optional tangent directions at points
            periodic: Make the spline periodic (closed) if True
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_spline = create_spline_wire(points, tangents, periodic)
        wire = Wire(self.sketch, native_instance=native_spline)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def bezier(
        self,
        control_points: list[tuple[float, float, float]],
        weights: list[float] | None = None,
    ) -> "Wire":
        """Create a bezier curve wire using build123d primitives.

        Args:
            control_points: List of control points defining the bezier curve
            weights: Optional weights for rational bezier curves
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_bezier = create_bezier_wire(control_points, weights)
        wire = Wire(self.sketch, native_instance=native_bezier)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # Line preset methods
    def polar_line(
        self,
        start: tuple[float, float, float],
        length: LengthType,
        angle: float,
    ) -> "Wire":
        """Create a polar line wire using build123d primitives.

        Args:
            start: Start point of the line
            length: Length of the line
            angle: Angle in degrees from the x-axis
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_line = create_polar_line_wire(start, length, angle)
        wire = Wire(self.sketch, native_instance=native_line)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def fillet_polyline(
        self,
        points: list[tuple[float, float, float]],
        radius: LengthType,
        close: bool = False,
    ) -> "Wire":
        """Create a filleted polyline wire using build123d primitives.

        Args:
            points: List of points defining the polyline
            radius: Fillet radius for corners
            close: Close the polyline if True
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_polyline = create_fillet_polyline_wire(points, radius, close)
        wire = Wire(self.sketch, native_instance=native_polyline)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # 2D Shape preset methods
    def ellipse(
        self, x_radius: LengthType, y_radius: LengthType, rotation: float = 0
    ) -> "Wire":
        """Create an ellipse wire using build123d primitives.

        Args:
            x_radius: X-axis radius of the ellipse
            y_radius: Y-axis radius of the ellipse
            rotation: Rotation angle in degrees
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_ellipse = create_ellipse_wire(x_radius, y_radius, rotation)
        wire = Wire(self.sketch, native_instance=native_ellipse)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polygon(self, points: list[tuple[float, float, float]]) -> "Wire":
        """Create a polygon wire using build123d primitives.

        Args:
            points: List of points defining the polygon vertices
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_polygon = create_polygon_wire(points)
        wire = Wire(self.sketch, native_instance=native_polygon)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def rectangle_rounded(
        self, width: LengthType, height: LengthType, radius: LengthType
    ) -> "Wire":
        """Create a rounded rectangle wire using build123d primitives.

        Args:
            width: Rectangle width
            height: Rectangle height
            radius: Corner radius for rounding
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_rect = create_rectangle_rounded_wire(width, height, radius)
        wire = Wire(self.sketch, native_instance=native_rect)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def triangle(
        self,
        a: float | None = None,
        b: float | None = None,
        c: float | None = None,
        A: float | None = None,
        B: float | None = None,
        C: float | None = None,
    ) -> "Wire":
        """Create a triangle wire using build123d primitives.

        Args:
            a, b, c: Side lengths
            A, B, C: Interior angles in degrees (opposite to sides a, b, c respectively)

        Note: Provide one side length and any two other values (sides or angles).
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_triangle = create_triangle_wire(a, b, c, A, B, C)
        wire = Wire(self.sketch, native_instance=native_triangle)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def trapezoid(
        self,
        width: LengthType,
        height: LengthType,
        left_side_angle: float,
        right_side_angle: float | None = None,
    ) -> "Wire":
        """Create a trapezoid wire using build123d primitives.

        Args:
            width: Major width of the trapezoid
            height: Height of the trapezoid
            left_side_angle: Bottom left interior angle in degrees
            right_side_angle: Bottom right interior angle in degrees (symmetric if None)
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_trapezoid = create_trapezoid_wire(
            width, height, left_side_angle, right_side_angle
        )
        wire = Wire(self.sketch, native_instance=native_trapezoid)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def text(
        self,
        text: str,
        font_size: LengthType,
        font: str = "Arial",
        font_path: str | None = None,
    ) -> "Wire":
        """Create text outlines as wire geometry using build123d primitives.

        Args:
            text: Text string to render
            font_size: Size of the font in model units
            font: Font name (default: "Arial")
            font_path: Optional path to specific font file
        """
        from codetocad.adapters.build123d.cad.wire.wire import Wire

        native_text = create_text_wire(text, font_size, font, font_path)
        wire = Wire(self.sketch, native_instance=native_text)

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
