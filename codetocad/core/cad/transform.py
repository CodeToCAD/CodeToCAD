"""
Transform operations for CodeToCAD geometry objects.

This module provides interface functions for transforming Vertex, Edge, and Solid objects.
These are interface functions that should be implemented by specific CAD integrations
(e.g., build123d, Blender).

Example usage:
    >>> from codetocad.core.cad.transform import translate, rotate, scale
    >>> from codetocad.core.dimensions.point import Point
    >>>
    >>> # Translate a solid by specific distances
    >>> translated = translate(my_solid, x="10mm", y="5mm", z=0)
    >>>
    >>> # Rotate a solid around axes
    >>> rotated = rotate(my_solid, x="45deg", y=0, z="90deg")
    >>>
    >>> # Scale a solid
    >>> scaled = scale(my_solid, x=2.0, y=1.0, z=0.5)
"""

from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.angle import AngleType
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.dimensions.point import Point


def translate(
    obj: "Vertex | Edge | Solid",
    x: LengthType = 0,
    y: LengthType = 0,
    z: LengthType = 0,
) -> "Vertex | Edge | Solid":
    """
    Translate an object by the specified distances.

    Args:
        obj: The object to translate (Vertex, Edge, or Solid).
        x: Distance to translate in the X direction.
        y: Distance to translate in the Y direction.
        z: Distance to translate in the Z direction.

    Returns:
        A new translated object of the same type.

    Examples:
        >>> vertex = Vertex(x=0, y=0, z=0)
        >>> translated = translate(vertex, x="10mm", y="5mm", z=0)
        >>> solid = Shape.cuboid(center, 10, 10, 10)
        >>> translated_solid = translate(solid, x=5, y=0, z="2cm")
    """
    raise NotImplementedError("Method not implemented.")


def translate_by_point(
    obj: "Vertex | Edge | Solid",
    point: Point,
) -> "Vertex | Edge | Solid":
    """
    Translate an object by a Point offset.

    Args:
        obj: The object to translate (Vertex, Edge, or Solid).
        point: The Point containing x, y, z translation distances.

    Returns:
        A new translated object of the same type.

    Examples:
        >>> offset = Point(x="10mm", y="5mm", z=0)
        >>> translated = translate_by_point(solid, offset)
    """
    raise NotImplementedError("Method not implemented.")


def rotate(
    obj: "Vertex | Edge | Solid",
    x: AngleType = 0,
    y: AngleType = 0,
    z: AngleType = 0,
) -> "Vertex | Edge | Solid":
    """
    Rotate an object around the X, Y, and Z axes.

    Rotations are applied in the order: X, then Y, then Z (Euler angles).

    Args:
        obj: The object to rotate (Vertex, Edge, or Solid).
        x: Rotation angle around the X axis.
        y: Rotation angle around the Y axis.
        z: Rotation angle around the Z axis.

    Returns:
        A new rotated object of the same type.

    Examples:
        >>> solid = Shape.cuboid(center, 10, 10, 10)
        >>> rotated = rotate(solid, x="45deg", y=0, z="90deg")
        >>> rotated = rotate(solid, x=0, y="1.57rad", z=0)
    """
    raise NotImplementedError("Method not implemented.")


def rotate_around_axis(
    obj: "Vertex | Edge | Solid",
    axis: Edge,
    angle: AngleType,
) -> "Vertex | Edge | Solid":
    """
    Rotate an object around an arbitrary axis defined by an Edge.

    Args:
        obj: The object to rotate (Vertex, Edge, or Solid).
        axis: An Edge defining the rotation axis (from v1 to v2).
        angle: The rotation angle.

    Returns:
        A new rotated object of the same type.

    Examples:
        >>> axis = Edge(v1=Vertex(x=0, y=0, z=0), v2=Vertex(x=0, y=0, z=10))
        >>> rotated = rotate_around_axis(solid, axis, "45deg")
    """
    raise NotImplementedError("Method not implemented.")


def scale(
    obj: "Edge | Solid",
    x: float = 1.0,
    y: float = 1.0,
    z: float = 1.0,
) -> "Edge | Solid":
    """
    Scale an object by the specified factors.

    Args:
        obj: The object to scale (Edge or Solid). Vertices cannot be scaled.
        x: Scale factor in the X direction.
        y: Scale factor in the Y direction.
        z: Scale factor in the Z direction.

    Returns:
        A new scaled object of the same type.

    Examples:
        >>> solid = Shape.cuboid(center, 10, 10, 10)
        >>> scaled = scale(solid, x=2.0, y=1.0, z=0.5)  # Double width, halve height
    """
    raise NotImplementedError("Method not implemented.")


def scale_uniform(
    obj: "Edge | Solid",
    factor: float,
) -> "Edge | Solid":
    """
    Scale an object uniformly by the same factor in all directions.

    Args:
        obj: The object to scale (Edge or Solid).
        factor: The uniform scale factor.

    Returns:
        A new scaled object of the same type.

    Examples:
        >>> solid = Shape.cuboid(center, 10, 10, 10)
        >>> doubled = scale_uniform(solid, 2.0)  # Double size in all directions
    """
    raise NotImplementedError("Method not implemented.")
