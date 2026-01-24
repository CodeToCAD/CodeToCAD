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
    native = obj.get_native()
    if native is None:
        raise NotImplementedError(
            f"Cannot translate {type(obj).__name__}: no native object available"
        )

    # LengthExp returns meters, but build123d uses mm by convention.
    # Convert meters to mm by multiplying by 1000.
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
    native = obj.get_native()
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
    native = obj.get_native()
    if native is None:
        raise NotImplementedError(
            f"Cannot rotate {type(obj).__name__}: no native object available"
        )

    # Get axis direction from edge. LengthExp returns meters, but build123d uses mm.
    # Convert meters to mm by multiplying by 1000.
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

    native = obj.get_native()
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


def _get_vertex_world_position(bd_vertex: "bd.Vertex") -> "tuple[float, float, float]":
    """Get the world position of a build123d vertex, accounting for transformations."""
    # Use center() which gives the correct world coordinates
    center = bd_vertex.center()
    return (float(center.X), float(center.Y), float(center.Z))


def _wrap_native(
    original: "Vertex | Edge | Solid",
    native: "bd.Vertex | bd.Edge | bd.Wire | bd.Face | bd.Solid",
) -> "Vertex | Edge | Solid":
    """Wrap a native build123d object in the appropriate CodeToCAD wrapper."""
    if isinstance(original, Vertex):
        # For vertices, use center() to get world coordinates after transformations
        try:
            center = native.center()
            result = Vertex(
                x=float(center.X),
                y=float(center.Y),
                z=float(center.Z),
                is_hidden=original.is_hidden,
            )
            result.set_native(native)
            return result
        except AttributeError:
            pass
        # Last resort: keep original coordinates
        result = Vertex(
            x=original.x,
            y=original.y,
            z=original.z,
            is_hidden=original.is_hidden,
        )
        result.set_native(native)
        return result
    elif isinstance(original, Edge):
        # For edges, extract actual vertex world coordinates from the transformed shape
        try:
            verts = native.vertices()
            if len(verts) >= 2:
                x1, y1, z1 = _get_vertex_world_position(verts[0])
                x2, y2, z2 = _get_vertex_world_position(verts[1])
                v1 = Vertex(x=x1, y=y1, z=z1)
                v2 = Vertex(x=x2, y=y2, z=z2)
            else:
                v1 = Vertex(x=0, y=0, z=0)
                v2 = Vertex(x=0, y=0, z=0)
        except AttributeError:
            v1 = Vertex(x=0, y=0, z=0)
            v2 = Vertex(x=0, y=0, z=0)

        result = Edge(v1=v1, v2=v2, is_hidden=original.is_hidden)
        result.set_native(native)
        # Copy over face reference if it exists
        original_face = original.get_native("face")
        if original_face is not None:
            result.set_native(native, "face")  # The transformed shape

        # Handle sub_edges for face boundaries
        if original.sub_edges:
            result.sub_edges = []
            try:
                # Get edges from the transformed shape
                edges = native.edges() if hasattr(native, "edges") else []
                for bd_edge in edges:
                    everts = bd_edge.vertices()
                    if len(everts) >= 2:
                        x1, y1, z1 = _get_vertex_world_position(everts[0])
                        x2, y2, z2 = _get_vertex_world_position(everts[1])
                        sub_v1 = Vertex(x=x1, y=y1, z=z1)
                        sub_v2 = Vertex(x=x2, y=y2, z=z2)
                        sub_edge = Edge(v1=sub_v1, v2=sub_v2)
                        sub_edge.set_native(bd_edge)
                        result.sub_edges.append(sub_edge)
            except AttributeError:
                pass

        return result
    else:  # Solid
        result = Solid(is_hidden=original.is_hidden)
        result.set_native(native)
        return result
