"""
Transform operations for build123d geometry objects.

This module implements the transform interface functions for build123d.
"""

import math

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.dimensions.point import Point


def translate(
    obj: "Vertex | Edge | Solid",
    x: LengthType = 0,
    y: LengthType = 0,
    z: LengthType = 0,
) -> "Vertex | Edge | Solid":
    """Translate an object by the specified distances."""
    native = obj.native_ref
    if native is None:
        raise NotImplementedError(
            f"Cannot translate {type(obj).__name__}: no native object available"
        )

    # Convert to mm for build123d (LengthExp returns meters)
    dx = float(LengthExp(x)) * 1000
    dy = float(LengthExp(y)) * 1000
    dz = float(LengthExp(z)) * 1000

    # Translate the native object
    translation = bd.Vector(dx, dy, dz)
    translated_native = native.moved(bd.Location(translation))

    # Create a new object of the same type with the translated native
    return _wrap_native(obj, translated_native)


def translate_by_point(
    obj: "Vertex | Edge | Solid",
    point: Point,
) -> "Vertex | Edge | Solid":
    """Translate an object by a Point offset."""
    return translate(obj, x=point.x, y=point.y, z=point.z)


def rotate(
    obj: "Vertex | Edge | Solid",
    x: AngleType = 0,
    y: AngleType = 0,
    z: AngleType = 0,
) -> "Vertex | Edge | Solid":
    """Rotate an object around the X, Y, and Z axes (Euler angles)."""
    native = obj.native_ref
    if native is None:
        raise NotImplementedError(
            f"Cannot rotate {type(obj).__name__}: no native object available"
        )

    # Convert angles to degrees for build123d
    angle_x = math.degrees(float(Angle(x)))
    angle_y = math.degrees(float(Angle(y)))
    angle_z = math.degrees(float(Angle(z)))

    # Apply rotations in order: X, Y, Z
    result_native = native
    if angle_x != 0:
        result_native = result_native.rotate(bd.Axis.X, angle_x)
    if angle_y != 0:
        result_native = result_native.rotate(bd.Axis.Y, angle_y)
    if angle_z != 0:
        result_native = result_native.rotate(bd.Axis.Z, angle_z)

    return _wrap_native(obj, result_native)


def rotate_around_axis(
    obj: "Vertex | Edge | Solid",
    axis: Edge,
    angle: AngleType,
) -> "Vertex | Edge | Solid":
    """Rotate an object around an arbitrary axis defined by an Edge."""
    native = obj.native_ref
    if native is None:
        raise NotImplementedError(
            f"Cannot rotate {type(obj).__name__}: no native object available"
        )

    # Get axis direction from edge (convert to mm for build123d)
    x1 = float(LengthExp(axis.v1.x)) * 1000
    y1 = float(LengthExp(axis.v1.y)) * 1000
    z1 = float(LengthExp(axis.v1.z)) * 1000
    x2 = float(LengthExp(axis.v2.x)) * 1000
    y2 = float(LengthExp(axis.v2.y)) * 1000
    z2 = float(LengthExp(axis.v2.z)) * 1000

    # Create axis from edge
    axis_bd = bd.Axis((x1, y1, z1), (x2 - x1, y2 - y1, z2 - z1))

    # Convert angle to degrees
    angle_deg = math.degrees(float(Angle(angle)))

    # Rotate
    result_native = native.rotate(axis_bd, angle_deg)

    return _wrap_native(obj, result_native)


def scale(
    obj: "Edge | Solid",
    x: float = 1.0,
    y: float = 1.0,
    z: float = 1.0,
) -> "Edge | Solid":
    """Scale an object by the specified factors."""
    if isinstance(obj, Vertex):
        raise TypeError("Cannot scale a Vertex. Vertices are points with no dimension.")

    native = obj.native_ref
    if native is None:
        raise NotImplementedError(
            f"Cannot scale {type(obj).__name__}: no native object available"
        )

    # Scale the native object
    result_native = bd.scale(native, (x, y, z))

    return _wrap_native(obj, result_native)


def scale_uniform(
    obj: "Edge | Solid",
    factor: float,
) -> "Edge | Solid":
    """Scale an object uniformly by the same factor in all directions."""
    return scale(obj, x=factor, y=factor, z=factor)


def _wrap_native(
    original: "Vertex | Edge | Solid",
    native: "bd.Vertex | bd.Edge | bd.Wire | bd.Face | bd.Solid",
) -> "Vertex | Edge | Solid":
    """Wrap a native build123d object in the appropriate CodeToCAD wrapper."""
    if isinstance(original, Vertex):
        # For vertices, extract coordinates from native
        native_vertex = native  # type: bd.Vertex
        result = Vertex(
            x=float(native_vertex.X),
            y=float(native_vertex.Y),
            z=float(native_vertex.Z),
            is_hidden=original.is_hidden,
        )
        result.native_ref = native
    elif isinstance(original, Edge):
        result = Edge(
            v1=Vertex(x=0, y=0, z=0),  # Placeholder, native has actual geometry
            v2=Vertex(x=0, y=0, z=0),
            is_hidden=original.is_hidden,
        )
        result.native_ref = native
    else:  # Solid
        result = Solid(is_hidden=original.is_hidden)
        result.native_ref = native

    return result
