"""
Blender-specific wire presets.
"""

from typing import TYPE_CHECKING
from codetocad.interfaces.cad.wire.wire_presets import WirePresetsInterface
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.adapters.blender.blender_actions.geometry import (
    create_rectangle_curve,
    create_circle_curve,
    create_regular_polygon_curve,
    create_polyline_curve,
    create_center_arc_curve,
    create_three_point_arc_curve,
    create_radius_arc_curve,
    create_tangent_arc_curve,
    create_spline_curve,
    create_bezier_curve,
    create_polar_line_curve,
    create_fillet_polyline_curve,
    create_ellipse_curve,
    create_polygon_curve,
    create_rectangle_rounded_curve,
    create_triangle_curve,
    create_trapezoid_curve,
    create_text_curve,
)

if TYPE_CHECKING:
    from codetocad.adapters.blender.cad.sketch.sketch import Sketch
    from codetocad.adapters.blender.cad.wire.wire import Wire


class BlenderWirePresets(WirePresetsInterface):
    """Blender-specific wire presets that use native Blender curve creation."""

    def rectangle(self, x: LengthType, y: LengthType) -> "Wire":
        """Create a rectangular wire using Blender primitives."""
        from codetocad.adapters.blender.cad.wire.wire import Wire

        # Create wire with native Blender rectangle curve
        native_curve = create_rectangle_curve(x, y)
        wire = Wire(self.sketch, name=f"rectangle_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def circle(self, radius: LengthType) -> "Wire":
        """Create a circular wire using Blender primitives."""
        from codetocad.adapters.blender.cad.wire.wire import Wire

        # Create wire with native Blender circle curve
        native_curve = create_circle_curve(radius)
        wire = Wire(self.sketch, name=f"circle_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def regular_polygon(
        self, radius: LengthType, side_count: int, rotation: float = 0
    ) -> "Wire":
        """Create a regular polygon wire using Blender primitives."""
        from codetocad.adapters.blender.cad.wire.wire import Wire

        # Create wire with native Blender regular polygon curve
        native_curve = create_regular_polygon_curve(radius, side_count, rotation)
        wire = Wire(self.sketch, name=f"polygon_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polyline(self, points: list[tuple[float, float]]) -> "Wire":
        """Create a polyline wire using Blender primitives."""
        from codetocad.adapters.blender.cad.wire.wire import Wire

        # Create wire with native Blender polyline curve
        native_curve = create_polyline_curve(points)
        wire = Wire(self.sketch, name=f"polyline_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a center arc wire using Blender primitives.

        Args:
            center: Center point of the arc (x, y, z)
            radius: Arc radius
            start_angle: Starting angle in degrees from x-axis
            arc_size: Angular size of arc in degrees
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_center_arc_curve(center, radius, start_angle, arc_size)
        wire = Wire(self.sketch, name=f"center_arc_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def three_point_arc(
        self,
        start: tuple[float, float, float],
        mid: tuple[float, float, float],
        end: tuple[float, float, float],
    ) -> "Wire":
        """Create a three-point arc wire using Blender primitives.

        Args:
            start: Start point of the arc
            mid: Middle point the arc passes through
            end: End point of the arc
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_three_point_arc_curve(start, mid, end)
        wire = Wire(self.sketch, name=f"three_point_arc_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a radius arc wire using Blender primitives.

        Args:
            start_point: Start point of the arc
            end_point: End point of the arc
            radius: Arc radius
            short_sagitta: If True, selects the short sagitta (height of arc from chord)
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_radius_arc_curve(
            start_point, end_point, radius, short_sagitta
        )
        wire = Wire(self.sketch, name=f"radius_arc_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a tangent arc wire using Blender primitives.

        Args:
            start: Start point of the arc
            end: End point of the arc
            tangent: Tangent vector to constrain the arc
            tangent_from_first: Apply tangent to first point if True, else to end point
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_tangent_arc_curve(start, end, tangent, tangent_from_first)
        wire = Wire(self.sketch, name=f"tangent_arc_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a spline wire using Blender primitives.

        Args:
            points: List of points defining the spline
            tangents: Optional tangent directions at points
            periodic: Make the spline periodic (closed) if True
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_spline_curve(points, tangents, periodic)
        wire = Wire(self.sketch, name=f"spline_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def bezier(
        self,
        control_points: list[tuple[float, float, float]],
        weights: list[float] | None = None,
    ) -> "Wire":
        """Create a bezier curve wire using Blender primitives.

        Args:
            control_points: List of control points defining the bezier curve
            weights: Optional weights for rational bezier curves
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_bezier_curve(control_points, weights)
        wire = Wire(self.sketch, name=f"bezier_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a polar line wire using Blender primitives.

        Args:
            start: Start point of the line
            length: Length of the line
            angle: Angle in degrees from the x-axis
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_polar_line_curve(start, length, angle)
        wire = Wire(self.sketch, name=f"polar_line_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def fillet_polyline(
        self,
        points: list[tuple[float, float, float]],
        radius: LengthType,
        close: bool = False,
    ) -> "Wire":
        """Create a filleted polyline wire using Blender primitives.

        Args:
            points: List of points defining the polyline
            radius: Fillet radius for corners
            close: Close the polyline if True
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_fillet_polyline_curve(points, radius, close)
        wire = Wire(self.sketch, name=f"fillet_polyline_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create text outlines as wire geometry using Blender primitives.

        Args:
            text: Text string to render
            font_size: Size of the font in model units
            font: Font name (default: "Arial")
            font_path: Optional path to specific font file
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_text_curve(text, font_size, font, font_path)
        wire = Wire(self.sketch, name=f"text_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    # 2D Shape preset methods
    def ellipse(
        self, x_radius: LengthType, y_radius: LengthType, rotation: float = 0
    ) -> "Wire":
        """Create an ellipse wire using Blender primitives.

        Args:
            x_radius: X-axis radius of the ellipse
            y_radius: Y-axis radius of the ellipse
            rotation: Rotation angle in degrees
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_ellipse_curve(x_radius, y_radius, rotation)
        wire = Wire(self.sketch, name=f"ellipse_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def polygon(self, points: list[tuple[float, float, float]]) -> "Wire":
        """Create a polygon wire using Blender primitives.

        Args:
            points: List of points defining the polygon vertices
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_polygon_curve(points)
        wire = Wire(self.sketch, name=f"polygon_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire

    def rectangle_rounded(
        self, width: LengthType, height: LengthType, radius: LengthType
    ) -> "Wire":
        """Create a rounded rectangle wire using Blender primitives.

        Args:
            width: Rectangle width
            height: Rectangle height
            radius: Corner radius for rounding
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_rectangle_rounded_curve(width, height, radius)
        wire = Wire(self.sketch, name=f"rounded_rect_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a triangle wire using Blender primitives.

        Args:
            a, b, c: Side lengths
            A, B, C: Interior angles in degrees (opposite to sides a, b, c respectively)

        Note: Provide one side length and any two other values (sides or angles).
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_triangle_curve(a, b, c, A, B, C)
        wire = Wire(self.sketch, name=f"triangle_{native_curve.name}")
        wire.blender_curve = native_curve

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
        """Create a trapezoid wire using Blender primitives.

        Args:
            width: Major width of the trapezoid
            height: Height of the trapezoid
            left_side_angle: Bottom left interior angle in degrees
            right_side_angle: Bottom right interior angle in degrees (symmetric if None)
        """
        from codetocad.adapters.blender.cad.wire.wire import Wire

        native_curve = create_trapezoid_curve(
            width, height, left_side_angle, right_side_angle
        )
        wire = Wire(self.sketch, name=f"trapezoid_{native_curve.name}")
        wire.blender_curve = native_curve

        if self.sketch:
            self.sketch.wires.append(wire)
        return wire
