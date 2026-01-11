"""
Build123d implementation of Draw class for 2D sketching operations.
"""

import math

import build123d as bd

from codetocad.core.cad.sketch import Draw as BaseDraw
from codetocad.core.cad.vertex_edge_solid import CurveType, Edge, Vertex
from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.dimensions.length_expression import LengthExp, LengthType

from codetocad.integrations.build123d.adapter.geometry import (
    create_rectangle_wire,
    create_circle_wire,
    create_trapezoid_wire,
    create_text_wire,
)


class Draw(BaseDraw):
    """Build123d implementation of Draw operations."""

    def __new__(cls, *args, **kwargs):
        raise TypeError("Do not instantiate a Draw class, use its methods instead.")

    @staticmethod
    def line(v1: Vertex, v2: Vertex) -> Edge:
        """Create a straight line between two vertices."""
        edge = Edge(v1=v1, v2=v2)
        # Create the native build123d line
        start = v1.to_tuple()
        end = v2.to_tuple()
        native_line = bd.Line(start, end)
        edge.native = native_line
        return edge

    @staticmethod
    def rectangle(center: Vertex, width: LengthType, height: LengthType) -> Edge:
        """Create a rectangle centered at the given vertex."""
        # Use parent class logic for the Edge structure
        start_x = LengthExp(width) / 2
        start_y = LengthExp(height) / 2

        line1 = Draw.line(
            Vertex(x=center._x - start_x, y=center._y - start_y, z=center._z),
            Vertex(x=center._x + start_x, y=center._y - start_y, z=center._z),
        )
        line2 = Draw.line(
            line1.v2,
            Vertex(x=center._x + start_x, y=center._y + start_y, z=center._z),
        )
        line3 = Draw.line(
            line2.v2,
            Vertex(x=center._x - start_x, y=center._y + start_y, z=center._z),
        )
        line4 = Draw.line(line3.v2, line1.v1)

        edge = Edge(v1=line1.v1, v2=line4.v2, sub_edges=[line1, line2, line3, line4])

        # Create native build123d rectangle
        native_rect = create_rectangle_wire(width, height)
        # Move to center position
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        native_rect = native_rect.moved(bd.Location((cx, cy, cz)))
        edge.native = native_rect

        return edge

    @staticmethod
    def circle(
        center: Vertex,
        radius: LengthType,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create a full circle."""
        # Create Edge with arc sub-edges from parent
        arc_edge = BaseDraw._arc(center, radius, 0, "360deg", curve_type)

        # Create native build123d circle
        native_circle = create_circle_wire(radius)
        # Move to center position
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        native_circle = native_circle.moved(bd.Location((cx, cy, cz)))
        arc_edge.native = native_circle

        return arc_edge

    @staticmethod
    def _arc(
        center: Vertex,
        radius: LengthType,
        start_angle: AngleType,
        end_angle: AngleType,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc from center point with start and end angles (internal method)."""
        # Use parent class for the Edge structure
        arc_edge = BaseDraw._arc(center, radius, start_angle, end_angle, curve_type)

        # Create native build123d arc
        r = float(LengthExp(radius))
        start_deg = math.degrees(Angle(start_angle).value)
        end_deg = math.degrees(Angle(end_angle).value)
        arc_size = end_deg - start_deg

        cx, cy, cz = center._x.value, center._y.value, center._z.value
        native_arc = bd.CenterArc((cx, cy, cz), r, start_deg, arc_size)
        arc_edge.native = native_arc

        return arc_edge

    @staticmethod
    def arc(
        start: Vertex,
        mid: Vertex,
        end: Vertex,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc passing through three points (start, mid, end)."""
        # Use parent class for the Edge structure
        arc_edge = BaseDraw.arc(start, mid, end, curve_type)

        # Create native build123d three-point arc
        native_arc = bd.ThreePointArc(start.to_tuple(), mid.to_tuple(), end.to_tuple())
        arc_edge.native = native_arc

        return arc_edge

    @staticmethod
    def arc_center(
        start: Vertex,
        end: Vertex,
        radius: LengthType,
        short_sagitta: bool = True,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc from start to end with a given radius."""
        # Use parent class for the Edge structure
        arc_edge = BaseDraw.arc_center(start, end, radius, short_sagitta, curve_type)

        # Create native build123d radius arc
        r = float(LengthExp(radius))
        native_arc = bd.RadiusArc(start.to_tuple(), end.to_tuple(), r, short_sagitta)
        arc_edge.native = native_arc

        return arc_edge

    @staticmethod
    def tangent_arc(
        start: Vertex,
        end: Vertex,
        tangent: Vertex,
        tangent_from_first: bool = True,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create an arc from start to end with a specified tangent direction."""
        # Use parent class for the Edge structure
        arc_edge = BaseDraw.tangent_arc(start, end, tangent, tangent_from_first, curve_type)

        # Create native build123d tangent arc
        native_arc = bd.TangentArc(
            start.to_tuple(),
            end.to_tuple(),
            tangent=tangent.to_tuple(),
            tangent_from_first=tangent_from_first,
        )
        arc_edge.native = native_arc

        return arc_edge

    @staticmethod
    def polygon(
        center: Vertex, radius: LengthType, sides: int, rotation: AngleType = 0
    ) -> Edge:
        """Create a regular polygon with the given number of sides."""
        # Use parent class for the Edge structure
        poly_edge = BaseDraw.polygon(center, radius, sides, rotation)
        
        # Create native build123d polygon
        r = float(LengthExp(radius))
        rot_deg = math.degrees(Angle(rotation).value)
        native_poly = bd.RegularPolygon(radius=r, side_count=sides, rotation=rot_deg)
        
        # Move to center position
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        native_poly = native_poly.moved(bd.Location((cx, cy, cz)))
        poly_edge.native = native_poly
        
        return poly_edge

    @staticmethod
    def text(text: str, font: str, size: LengthType) -> Edge:
        """Create a text string."""
        native_text = create_text_wire(text, size, font)
        
        # Create a simple edge wrapper
        edge = Edge(
            v1=Vertex(x=0, y=0, z=0),
            v2=Vertex(x=0, y=0, z=0),
        )
        edge.native = native_text
        return edge

    @staticmethod
    def trapezoid(center: Vertex, width: LengthType, height: LengthType, angle: AngleType) -> Edge:
        """Create a trapezoid."""
        angle_deg = math.degrees(Angle(angle).value)
        native_trap = create_trapezoid_wire(width, height, angle_deg)
        
        # Move to center position
        cx, cy, cz = center._x.value, center._y.value, center._z.value
        native_trap = native_trap.moved(bd.Location((cx, cy, cz)))
        
        # Create edge wrapper
        edge = Edge(
            v1=Vertex(x=center._x - LengthExp(width)/2, y=center._y - LengthExp(height)/2, z=center._z),
            v2=Vertex(x=center._x - LengthExp(width)/2, y=center._y - LengthExp(height)/2, z=center._z),
        )
        edge.native = native_trap
        return edge

    @staticmethod
    def spline(
        points: "list[Vertex]",
        closed: bool = False,
        curve_type: CurveType = CurveType.BEZIER,
    ) -> Edge:
        """Create a smooth spline through the given points."""
        # Use parent class for the Edge structure
        spline_edge = BaseDraw.spline(points, closed, curve_type)

        # Create native build123d spline
        point_tuples = [p.to_tuple() for p in points]
        if closed and point_tuples[0] != point_tuples[-1]:
            point_tuples = point_tuples + [point_tuples[0]]

        native_spline = bd.Spline(*point_tuples, periodic=closed)
        spline_edge.native = native_spline

        return spline_edge

    @staticmethod
    def import_file(file_path: str) -> Edge:  # noqa: ARG004
        """Import an edge from a file."""
        # build123d doesn't have direct 2D import, raise not implemented
        _ = file_path  # Acknowledge parameter for API compatibility
        raise NotImplementedError("2D edge import is not yet implemented for build123d")

    @staticmethod
    def export_file(edge: Edge, file_path: str) -> None:
        """Export an edge to a file."""
        native = edge.native
        if native is None:
            raise ValueError("Edge has no native build123d object")

        # Export as SVG if 2D
        if file_path.lower().endswith('.svg'):
            bd.export_svg(native, file_path)
        else:
            raise ValueError(f"Unsupported 2D export format: {file_path}")

