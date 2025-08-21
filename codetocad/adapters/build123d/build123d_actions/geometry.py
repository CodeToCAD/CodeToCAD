"""
Geometry creation and manipulation functions for build123d.
"""

from typing import List, Tuple
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthType, LengthExpression


def create_vertex(x: LengthType, y: LengthType, z: LengthType = 0) -> bd.Vertex:
    """Create a build123d Vertex from coordinates."""
    x_val = float(LengthExpression(x))
    y_val = float(LengthExpression(y))
    z_val = float(LengthExpression(z))
    return bd.Vertex(x_val, y_val, z_val)


def create_edge_from_vertices(v1: bd.Vertex, v2: bd.Vertex) -> bd.Edge:
    """Create a build123d Edge from two vertices."""
    line = bd.Line(v1, v2)
    edge = line.edge()
    if edge is None:
        raise ValueError("Failed to create edge from vertices")
    return edge


def create_line_edge(
    start: Tuple[float, float, float], end: Tuple[float, float, float]
) -> bd.Edge:
    """Create a line edge between two points."""
    line = bd.Line(start, end)
    edge = line.edge()
    if edge is None:
        raise ValueError("Failed to create edge from line")
    return edge


def create_arc_edge(
    start: Tuple[float, float, float],
    mid: Tuple[float, float, float],
    end: Tuple[float, float, float],
) -> bd.Edge:
    """Create an arc edge through three points."""
    arc = bd.ThreePointArc(start, mid, end)
    edge = arc.edge()
    if edge is None:
        raise ValueError("Failed to create edge from arc")
    return edge


def create_wire_from_edges(edges: List[bd.Edge]) -> bd.Wire:
    """Create a build123d Wire from a list of edges."""
    return bd.Wire(edges)


def create_rectangle_wire(width: LengthType, height: LengthType) -> bd.Rectangle:
    """Create a rectangular wire."""
    w = float(LengthExpression(width))
    h = float(LengthExpression(height))
    return bd.Rectangle(w, h)


def create_circle_wire(radius: LengthType) -> bd.Circle:
    """Create a circular wire."""
    r = float(LengthExpression(radius))
    return bd.Circle(r)


def create_regular_polygon_wire(
    radius: LengthType, side_count: int, rotation: float = 0
) -> bd.RegularPolygon:
    """Create a regular polygon wire."""
    r = float(LengthExpression(radius))
    return bd.RegularPolygon(radius=r, side_count=side_count, rotation=rotation)


def create_polyline_wire(points: List[Tuple[float, float]]) -> bd.Polyline:
    """Create a polyline wire from a list of points."""
    return bd.Polyline(*points)


# Arc creation functions
def create_center_arc_wire(
    center: Tuple[float, float, float],
    radius: LengthType,
    start_angle: float,
    arc_size: float,
) -> bd.CenterArc:
    """Create a center arc wire."""
    r = float(LengthExpression(radius))
    return bd.CenterArc(center, r, start_angle, arc_size)


def create_three_point_arc_wire(
    start: Tuple[float, float, float],
    mid: Tuple[float, float, float],
    end: Tuple[float, float, float],
) -> bd.ThreePointArc:
    """Create a three-point arc wire."""
    return bd.ThreePointArc(start, mid, end)


def create_radius_arc_wire(
    start_point: Tuple[float, float, float],
    end_point: Tuple[float, float, float],
    radius: LengthType,
    short_sagitta: bool = True,
) -> bd.RadiusArc:
    """Create a radius arc wire."""
    r = float(LengthExpression(radius))
    return bd.RadiusArc(start_point, end_point, r, short_sagitta)


def create_tangent_arc_wire(
    start: Tuple[float, float, float],
    end: Tuple[float, float, float],
    tangent: Tuple[float, float, float],
    tangent_from_first: bool = True,
) -> bd.TangentArc:
    """Create a tangent arc wire."""
    return bd.TangentArc(
        start, end, tangent=tangent, tangent_from_first=tangent_from_first
    )


# Curve creation functions
def create_spline_wire(
    points: List[Tuple[float, float, float]],
    tangents: List[Tuple[float, float, float]] | None = None,
    periodic: bool = False,
) -> bd.Spline:
    """Create a spline wire."""
    return bd.Spline(*points, tangents=tangents, periodic=periodic)


def create_bezier_wire(
    control_points: List[Tuple[float, float, float]],
    weights: List[float] | None = None,
) -> bd.Bezier:
    """Create a bezier curve wire."""
    return bd.Bezier(*control_points, weights=weights)


# Line creation functions
def create_polar_line_wire(
    start: Tuple[float, float, float],
    length: LengthType,
    angle: float,
) -> bd.PolarLine:
    """Create a polar line wire."""
    length_val = float(LengthExpression(length))
    return bd.PolarLine(start, length_val, angle)


def create_fillet_polyline_wire(
    points: List[Tuple[float, float, float]],
    radius: LengthType,
    close: bool = False,
) -> bd.FilletPolyline:
    """Create a filleted polyline wire."""
    r = float(LengthExpression(radius))
    return bd.FilletPolyline(*points, radius=r, close=close)


# 2D Shape creation functions
def create_ellipse_wire(
    x_radius: LengthType, y_radius: LengthType, rotation: float = 0
) -> bd.Ellipse:
    """Create an ellipse wire."""
    x_r = float(LengthExpression(x_radius))
    y_r = float(LengthExpression(y_radius))
    return bd.Ellipse(x_r, y_r, rotation=rotation)


def create_polygon_wire(points: List[Tuple[float, float, float]]) -> bd.Polygon:
    """Create a polygon wire from points."""
    return bd.Polygon(*points)


def create_rectangle_rounded_wire(
    width: LengthType, height: LengthType, radius: LengthType
) -> bd.RectangleRounded:
    """Create a rounded rectangle wire."""
    w = float(LengthExpression(width))
    h = float(LengthExpression(height))
    r = float(LengthExpression(radius))
    return bd.RectangleRounded(w, h, r)


def create_triangle_wire(
    a: float | None = None,
    b: float | None = None,
    c: float | None = None,
    A: float | None = None,
    B: float | None = None,
    C: float | None = None,
) -> bd.Triangle:
    """Create a triangle wire defined by sides and/or angles."""
    return bd.Triangle(a=a, b=b, c=c, A=A, B=B, C=C)


def create_trapezoid_wire(
    width: LengthType,
    height: LengthType,
    left_side_angle: float,
    right_side_angle: float | None = None,
) -> bd.Trapezoid:
    """Create a trapezoid wire."""
    w = float(LengthExpression(width))
    h = float(LengthExpression(height))
    return bd.Trapezoid(w, h, left_side_angle, right_side_angle)


def create_text_wire(
    text: str,
    font_size: LengthType,
    font: str = "Arial",
    font_path: str | None = None,
) -> bd.Wire:
    """Create a text wire using build123d primitives."""
    font_size_val = float(LengthExpression(font_size))
    # Create text face and extract its outer wire
    text_face = bd.Text(
        txt=text, font_size=font_size_val, font=font, font_path=font_path
    )
    # Get the outer wire from the text face
    return text_face.wires()[0] if text_face.wires() else bd.Wire()


def create_face_from_wire(wire: bd.Wire) -> bd.Face:
    """Create a face from a wire."""
    return bd.Face(wire)


def extrude_face(face: bd.Face, distance: LengthType) -> bd.Part:
    """Extrude a face to create a solid."""
    dist = float(LengthExpression(distance))
    return bd.extrude(face, dist)


def create_cube(x: LengthType, y: LengthType, z: LengthType) -> bd.Box:
    """Create a cube solid."""
    x_val = float(LengthExpression(x))
    y_val = float(LengthExpression(y))
    z_val = float(LengthExpression(z))
    return bd.Box(x_val, y_val, z_val)


def create_cylinder(radius: LengthType, height: LengthType) -> bd.Cylinder:
    """Create a cylinder solid."""
    r = float(LengthExpression(radius))
    h = float(LengthExpression(height))
    return bd.Cylinder(r, h)


def create_sphere(radius: LengthType) -> bd.Sphere:
    """Create a sphere solid."""
    r = float(LengthExpression(radius))
    return bd.Sphere(r)


def boolean_union(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean union of two solids."""
    return solid1 + solid2


def boolean_difference(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean difference of two solids."""
    return solid1 - solid2


def boolean_intersection(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean intersection of two solids."""
    return solid1 & solid2
