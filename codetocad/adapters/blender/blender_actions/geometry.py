"""
Geometry creation and manipulation functions for Blender.
"""

import math
from typing import List, Tuple
import bpy
from uuid import uuid4

from codetocad.core.dimensions.length_expression import LengthType, LengthExpression
from codetocad.adapters.blender.blender_actions.curve import create_curve, create_text
from codetocad.adapters.blender.blender_definitions import BlenderCurveTypes
from codetocad.core.dimensions.point import Point


def create_uuid_like_id() -> str:
    """Generate a UUID-like string for naming objects."""
    return str(uuid4())


# Basic shape creation functions
def create_rectangle_curve(width: LengthType, height: LengthType) -> "bpy.types.Curve":
    """Create a rectangular curve."""
    w = float(LengthExpression(width))
    h = float(LengthExpression(height))

    # Create rectangle points
    points = [
        Point(0, 0, 0),
        Point(w, 0, 0),
        Point(w, h, 0),
        Point(0, h, 0),
        Point(0, 0, 0),  # Close the rectangle
    ]

    curve_name = f"rectangle_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_circle_curve(radius: LengthType, segments: int = 32) -> "bpy.types.Curve":
    """Create a circular curve."""
    r = float(LengthExpression(radius))

    # Create circle points
    points = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append(Point(x, y, 0))

    # Close the circle
    points.append(points[0])

    curve_name = f"circle_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_regular_polygon_curve(
    radius: LengthType, side_count: int, rotation: float = 0
) -> "bpy.types.Curve":
    """Create a regular polygon curve."""
    r = float(LengthExpression(radius))
    rotation_rad = math.radians(rotation)

    # Create polygon points
    points = []
    for i in range(side_count):
        angle = 2 * math.pi * i / side_count + rotation_rad
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append(Point(x, y, 0))

    # Close the polygon
    points.append(points[0])

    curve_name = f"polygon_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_polyline_curve(points: List[Tuple[float, float]]) -> "bpy.types.Curve":
    """Create a polyline curve from a list of points."""
    curve_points = [Point(x, y, 0) for x, y in points]

    curve_name = f"polyline_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, curve_points)
    return curve


# Arc creation functions
def create_center_arc_curve(
    center: Tuple[float, float, float],
    radius: LengthType,
    start_angle: float,
    arc_size: float,
    segments: int = 16,
) -> "bpy.types.Curve":
    """Create a center arc curve."""
    r = float(LengthExpression(radius))
    cx, cy, cz = center
    start_rad = math.radians(start_angle)
    arc_rad = math.radians(arc_size)

    # Create arc points
    points = []
    for i in range(segments + 1):
        angle = start_rad + (arc_rad * i / segments)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append(Point(x, y, cz))

    curve_name = f"center_arc_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_three_point_arc_curve(
    start: Tuple[float, float, float],
    mid: Tuple[float, float, float],
    end: Tuple[float, float, float],
    segments: int = 16,
) -> "bpy.types.Curve":
    """Create a three-point arc curve."""
    # For simplicity, create a bezier curve through the three points
    points = [Point(*start), Point(*mid), Point(*end)]

    curve_name = f"three_point_arc_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.BEZIER, points)
    return curve


def create_radius_arc_curve(
    start_point: Tuple[float, float, float],
    end_point: Tuple[float, float, float],
    radius: LengthType,
    short_sagitta: bool = True,
    segments: int = 16,
) -> "bpy.types.Curve":
    """Create a radius arc curve."""
    # For simplicity, create a line between the points
    # A proper implementation would calculate the arc center and create the arc
    points = [Point(*start_point), Point(*end_point)]

    curve_name = f"radius_arc_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_tangent_arc_curve(
    start: Tuple[float, float, float],
    end: Tuple[float, float, float],
    tangent: Tuple[float, float, float],
    tangent_from_first: bool = True,
    segments: int = 16,
) -> "bpy.types.Curve":
    """Create a tangent arc curve."""
    # For simplicity, create a bezier curve with tangent control
    points = [Point(*start), Point(*end)]

    curve_name = f"tangent_arc_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.BEZIER, points)
    return curve


# Curve creation functions
def create_spline_curve(
    points: List[Tuple[float, float, float]],
    tangents: List[Tuple[float, float, float]] | None = None,
    periodic: bool = False,
) -> "bpy.types.Curve":
    """Create a spline curve."""
    curve_points = [Point(*point) for point in points]

    if periodic and len(curve_points) > 2:
        curve_points.append(curve_points[0])  # Close the spline

    curve_name = f"spline_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.NURBS, curve_points)
    return curve


def create_bezier_curve(
    control_points: List[Tuple[float, float, float]],
    weights: List[float] | None = None,
) -> "bpy.types.Curve":
    """Create a bezier curve."""
    curve_points = [Point(*point) for point in control_points]

    curve_name = f"bezier_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.BEZIER, curve_points)
    return curve


# Line creation functions
def create_polar_line_curve(
    start: Tuple[float, float, float],
    length: LengthType,
    angle: float,
) -> "bpy.types.Curve":
    """Create a polar line curve."""
    length_val = float(LengthExpression(length))
    angle_rad = math.radians(angle)

    end_x = start[0] + length_val * math.cos(angle_rad)
    end_y = start[1] + length_val * math.sin(angle_rad)
    end_z = start[2]

    points = [Point(*start), Point(end_x, end_y, end_z)]

    curve_name = f"polar_line_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_fillet_polyline_curve(
    points: List[Tuple[float, float, float]],
    radius: LengthType,
    close: bool = False,
) -> "bpy.types.Curve":
    """Create a filleted polyline curve."""
    # For simplicity, create a regular polyline without fillets
    # A proper implementation would add rounded corners
    curve_points = [Point(*point) for point in points]

    if close and len(curve_points) > 2:
        curve_points.append(curve_points[0])

    curve_name = f"fillet_polyline_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, curve_points)
    return curve


# Text creation function
def create_text_curve(
    text: str,
    font_size: LengthType,
    font: str = "Arial",
    font_path: str | None = None,
) -> "bpy.types.Curve":
    """Create a text curve using Blender's text objects."""
    font_size_val = float(LengthExpression(font_size))
    curve_name = f"text_{create_uuid_like_id()[:8]}"

    return create_text(
        curve_name=curve_name, text=text, size=font_size_val, font_file_path=font_path
    )


# 2D Shape creation functions
def create_ellipse_curve(
    x_radius: LengthType, y_radius: LengthType, rotation: float = 0, segments: int = 32
) -> "bpy.types.Curve":
    """Create an ellipse curve."""
    x_r = float(LengthExpression(x_radius))
    y_r = float(LengthExpression(y_radius))
    rotation_rad = math.radians(rotation)

    # Create ellipse points
    points = []
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

        points.append(Point(x, y, 0))

    # Close the ellipse
    points.append(points[0])

    curve_name = f"ellipse_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_polygon_curve(points: List[Tuple[float, float, float]]) -> "bpy.types.Curve":
    """Create a polygon curve from points."""
    curve_points = [Point(*point) for point in points]

    # Close the polygon
    if len(curve_points) > 2:
        curve_points.append(curve_points[0])

    curve_name = f"polygon_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, curve_points)
    return curve


def create_rectangle_rounded_curve(
    width: LengthType, height: LengthType, radius: LengthType
) -> "bpy.types.Curve":
    """Create a rounded rectangle curve."""
    # For simplicity, create a regular rectangle
    # A proper implementation would add rounded corners
    return create_rectangle_curve(width, height)


def create_triangle_curve(
    a: float | None = None,
    b: float | None = None,
    c: float | None = None,
    A: float | None = None,
    B: float | None = None,
    C: float | None = None,
) -> "bpy.types.Curve":
    """Create a triangle curve defined by sides and/or angles."""
    # Simple implementation: create equilateral triangle if no parameters given
    side_length = a or b or c or 1.0
    height = side_length * math.sqrt(3) / 2

    # Triangle vertices
    points = [
        Point(0, 0, 0),
        Point(side_length, 0, 0),
        Point(side_length / 2, height, 0),
        Point(0, 0, 0),  # Close the triangle
    ]

    curve_name = f"triangle_{create_uuid_like_id()[:8]}"
    spline, curve, _ = create_curve(curve_name, BlenderCurveTypes.POLY, points)
    return curve


def create_trapezoid_curve(
    width: LengthType,
    height: LengthType,
    left_side_angle: float,
    right_side_angle: float | None = None,
) -> "bpy.types.Curve":
    """Create a trapezoid curve."""
    # For simplicity, create a rectangle
    # A proper implementation would calculate trapezoid vertices based on angles
    return create_rectangle_curve(width, height)
