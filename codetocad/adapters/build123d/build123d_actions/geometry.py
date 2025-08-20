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
