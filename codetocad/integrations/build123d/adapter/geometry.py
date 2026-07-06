"""
Geometry creation and manipulation functions for build123d.
"""

from typing import Tuple
import build123d as bd
from codetocad.core.dimensions.length_expression import LengthType, LengthExp


def create_vertex(x: LengthType, y: LengthType, z: LengthType = 0) -> bd.Vertex:
    """Create a build123d Vertex from coordinates."""
    x_val = float(LengthExp(x))
    y_val = float(LengthExp(y))
    z_val = float(LengthExp(z))
    return bd.Vertex(x_val, y_val, z_val)


def create_edge_from_vertices(v1: bd.Vertex, v2: bd.Vertex) -> bd.Edge:
    """Create a build123d Edge from two vertices."""
    line = bd.Line(v1, v2)
    edge = line.edge()
    if edge is None:
        raise ValueError("Failed to create edge from vertices")
    return edge


def create_line_edge(
    start: tuple[float, float, float], end: tuple[float, float, float]
) -> bd.Edge:
    """Create a line edge between two points."""
    line = bd.Line(start, end)
    edge = line.edge()
    if edge is None:
        raise ValueError("Failed to create edge from line")
    return edge


def create_arc_edge(
    start: tuple[float, float, float],
    mid: tuple[float, float, float],
    end: tuple[float, float, float],
) -> bd.Edge:
    """Create an arc edge through three points."""
    arc = bd.ThreePointArc(start, mid, end)
    edge = arc.edge()
    if edge is None:
        raise ValueError("Failed to create edge from arc")
    return edge


def create_center_arc_edge(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    center_x: float,
    center_y: float,
    center_z: float = 0,
) -> bd.Edge:
    """Create an arc edge from start to end with specified center point.

    Args:
        start: Start point of the arc
        end: End point of the arc
        center_x: X coordinate of arc center
        center_y: Y coordinate of arc center
        center_z: Z coordinate of arc center (default 0)

    Returns:
        build123d Edge representing the arc
    """
    import math

    # Calculate radius from center to start point
    radius = math.sqrt((start[0] - center_x) ** 2 + (start[1] - center_y) ** 2)

    # Calculate start angle
    start_angle = math.degrees(math.atan2(start[1] - center_y, start[0] - center_x))

    # Calculate end angle
    end_angle = math.degrees(math.atan2(end[1] - center_y, end[0] - center_x))

    # Calculate arc size (can be positive or negative for direction)
    arc_size = end_angle - start_angle

    # Normalize to reasonable arc (prefer shorter arc unless crossing 180)
    if arc_size > 180:
        arc_size -= 360
    elif arc_size < -180:
        arc_size += 360

    center = (center_x, center_y, center_z)
    arc = bd.CenterArc(center, radius, start_angle, arc_size)
    edge = arc.edge()
    if edge is None:
        raise ValueError("Failed to create edge from center arc")
    return edge


def create_wire_from_edges(edges: list[bd.Edge]) -> bd.Wire:
    """Create a build123d Wire from a list of edges."""
    return bd.Wire(edges)


def create_rectangle_wire(width: LengthType, height: LengthType) -> bd.Rectangle:
    """Create a rectangular wire."""
    w = float(LengthExp(width))
    h = float(LengthExp(height))
    return bd.Rectangle(w, h)


def create_circle_wire(radius: LengthType) -> bd.Circle:
    """Create a circular wire."""
    r = float(LengthExp(radius))
    return bd.Circle(r)


def create_regular_polygon_wire(
    radius: LengthType, side_count: int, rotation: float = 0
) -> bd.RegularPolygon:
    """Create a regular polygon wire."""
    r = float(LengthExp(radius))
    return bd.RegularPolygon(radius=r, side_count=side_count, rotation=rotation)


def create_polyline_wire(points: list[tuple[float, float]]) -> bd.Polyline:
    """Create a polyline wire from a list of points."""
    return bd.Polyline(*points)


# Arc creation functions
def create_center_arc_wire(
    center: tuple[float, float, float],
    radius: LengthType,
    start_angle: float,
    arc_size: float,
) -> bd.CenterArc:
    """Create a center arc wire."""
    r = float(LengthExp(radius))
    return bd.CenterArc(center, r, start_angle, arc_size)


def create_three_point_arc_wire(
    start: tuple[float, float, float],
    mid: tuple[float, float, float],
    end: tuple[float, float, float],
) -> bd.ThreePointArc:
    """Create a three-point arc wire."""
    return bd.ThreePointArc(start, mid, end)


def create_radius_arc_wire(
    start_point: tuple[float, float, float],
    end_point: tuple[float, float, float],
    radius: LengthType,
    short_sagitta: bool = True,
) -> bd.RadiusArc:
    """Create a radius arc wire."""
    r = float(LengthExp(radius))
    return bd.RadiusArc(start_point, end_point, r, short_sagitta)


def create_tangent_arc_wire(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    tangent: tuple[float, float, float],
    tangent_from_first: bool = True,
) -> bd.TangentArc:
    """Create a tangent arc wire."""
    return bd.TangentArc(
        start, end, tangent=tangent, tangent_from_first=tangent_from_first
    )


# Curve creation functions
def create_spline_wire(
    points: list[tuple[float, float, float]],
    tangents: list[tuple[float, float, float]] | None = None,
    periodic: bool = False,
) -> bd.Spline:
    """Create a spline wire."""
    return bd.Spline(*points, tangents=tangents, periodic=periodic)


def create_bezier_wire(
    control_points: list[tuple[float, float, float]],
    weights: list[float] | None = None,
) -> bd.Bezier:
    """Create a bezier curve wire."""
    return bd.Bezier(*control_points, weights=weights)


# Line creation functions
def create_polar_line_wire(
    start: tuple[float, float, float],
    length: LengthType,
    angle: float,
) -> bd.PolarLine:
    """Create a polar line wire."""
    length_val = float(LengthExp(length))
    return bd.PolarLine(start, length_val, angle)


def create_fillet_polyline_wire(
    points: list[tuple[float, float, float]],
    radius: LengthType,
    close: bool = False,
) -> bd.FilletPolyline:
    """Create a filleted polyline wire."""
    r = float(LengthExp(radius))
    return bd.FilletPolyline(*points, radius=r, close=close)


# 2D Shape creation functions
def create_ellipse_wire(
    x_radius: LengthType, y_radius: LengthType, rotation: float = 0
) -> bd.Ellipse:
    """Create an ellipse wire."""
    x_r = float(LengthExp(x_radius))
    y_r = float(LengthExp(y_radius))
    return bd.Ellipse(x_r, y_r, rotation=rotation)


def create_polygon_wire(points: list[tuple[float, float, float]]) -> bd.Polygon:
    """Create a polygon wire from points."""
    return bd.Polygon(*points)


def create_rectangle_rounded_wire(
    width: LengthType, height: LengthType, radius: LengthType
) -> bd.RectangleRounded:
    """Create a rounded rectangle wire."""
    w = float(LengthExp(width))
    h = float(LengthExp(height))
    r = float(LengthExp(radius))
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
    w = float(LengthExp(width))
    h = float(LengthExp(height))
    return bd.Trapezoid(w, h, left_side_angle, right_side_angle)


def create_text_wire(
    text: str,
    font_size: LengthType,
    font: str = "Arial",
    font_path: str | None = None,
) -> bd.Sketch:
    """Create text as a Sketch with multiple faces (one per letter/glyph).

    Returns a Sketch object containing all faces of the text. Each face
    properly includes inner wires (holes) for letters like O, P, A, B, etc.
    This allows proper extrusion of text where holes are preserved.
    """
    font_size_val = float(LengthExp(font_size))
    # Create text sketch - build123d Text is a Sketch with faces that include holes
    text_sketch = bd.Text(
        txt=text, font_size=font_size_val, font=font, font_path=font_path
    )
    return text_sketch


def _get_wire_from_native(native: "bd.Wire | bd.Sketch") -> bd.Wire:
    """Extract a wire from a native build123d object.

    Args:
        native: A build123d Wire or Sketch object

    Returns:
        A Wire extracted from the object
    """
    if isinstance(native, bd.Sketch):
        return native.wires()[0]
    return native


def create_face_from_wire(wire: "bd.Wire | bd.Sketch") -> bd.Face:
    """Create a face from a wire or sketch.

    Args:
        wire: A build123d Wire or Sketch object (Circle, Rectangle, etc. are Sketches)

    Returns:
        A Face created from the wire/sketch
    """
    # If it's a Sketch (Circle, Rectangle, etc.), get the face directly
    if isinstance(wire, bd.Sketch):
        return wire.face()
    # Otherwise it's a Wire - create face from it
    return bd.Face(wire)


def create_face_with_holes(
    outer: "bd.Wire | bd.Sketch",
    inner_wires: "list[bd.Wire | bd.Sketch]",
) -> bd.Face:
    """Create a face from an outer wire with inner wires as holes.

    Args:
        outer: The outer boundary wire or sketch
        inner_wires: List of inner wires/sketches that define holes

    Returns:
        A Face with holes cut out
    """
    outer_wire = _get_wire_from_native(outer)
    inner_bd_wires = [_get_wire_from_native(w) for w in inner_wires]
    return bd.Face(outer_wire, inner_bd_wires)


def extrude_face(face: bd.Face, distance: LengthType) -> bd.Part:
    """Extrude a face to create a solid."""
    dist = float(LengthExp(distance))
    return bd.extrude(face, dist)


def create_cube(x: LengthType, y: LengthType, z: LengthType) -> bd.Box:
    """Create a cube solid."""
    x_val = float(LengthExp(x))
    y_val = float(LengthExp(y))
    z_val = float(LengthExp(z))
    return bd.Box(x_val, y_val, z_val)


def create_cylinder(radius: LengthType, height: LengthType) -> bd.Cylinder:
    """Create a cylinder solid."""
    r = float(LengthExp(radius))
    h = float(LengthExp(height))
    return bd.Cylinder(r, h)


def create_sphere(radius: LengthType) -> bd.Sphere:
    """Create a sphere solid."""
    r = float(LengthExp(radius))
    return bd.Sphere(r)


def union(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean union of two solids."""
    return solid1 + solid2


def difference(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean difference of two solids."""
    return solid1 - solid2


def intersection(solid1: bd.Part, solid2: bd.Part) -> bd.Compound:
    """Perform boolean intersection of two solids."""
    return solid1 & solid2
