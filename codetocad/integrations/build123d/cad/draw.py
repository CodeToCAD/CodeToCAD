"""
Build123d implementation of Draw class for 2D sketching operations.
"""

import math

import build123d as bd

from codetocad.core import Draw as BaseDraw
from codetocad.core.cad.vertex_edge_solid import CurveType, Edge, Vertex
from codetocad.core.enums.plane import Plane
from codetocad.core.dimensions.angle import Angle, AngleType
from codetocad.core.dimensions.length_expression import LengthExp, LengthType

from codetocad.integrations.build123d.adapter.geometry import (
    create_rectangle_wire,
    create_circle_wire,
    create_trapezoid_wire,
    create_text_wire,
)


def _get_bd_plane_for_sketch(
    center: Vertex, plane: "Plane | Edge" = Plane.XY
) -> "bd.Plane":
    """Get a build123d plane for sketching at the given center position.

    Args:
        center: The center vertex for the sketch
        plane: The plane to create the sketch on (XY, XZ, or YZ) or an Edge representing a Face

    Returns:
        A build123d Plane positioned at the center
    """
    cx, cy, cz = center._x.value, center._y.value, center._z.value

    # If plane is an Edge (representing a Face), extract the native face
    if isinstance(plane, Edge):
        native_face = plane.get_native("face")
        if native_face is not None:
            # Use the face's plane
            return bd.Plane(native_face)
        # Fallback to XY if no face is stored
        return bd.Plane(origin=(cx, cy, cz), x_dir=(1, 0, 0), z_dir=(0, 0, 1))

    # Handle Plane enum
    if plane == Plane.XY:
        return bd.Plane(origin=(cx, cy, cz), x_dir=(1, 0, 0), z_dir=(0, 0, 1))
    elif plane == Plane.XZ:
        return bd.Plane(origin=(cx, cy, cz), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    else:  # YZ
        return bd.Plane(origin=(cx, cy, cz), x_dir=(0, 1, 0), z_dir=(0, 0, 1))


def line(v1: Vertex, v2: Vertex) -> Edge:
    """Create a straight line between two vertices."""
    edge = Edge(v1=v1, v2=v2)
    # Create the native build123d line
    start = v1.to_tuple()
    end = v2.to_tuple()
    native_line = bd.Line(start, end)
    edge.set_native(native_line)
    return edge


def rectangle(
    center: Vertex,
    width: LengthType,
    height: LengthType,
    plane: "Plane | Edge" = Plane.XY,
) -> Edge:
    """Create a rectangle centered at the given vertex.

    Args:
        center: Center vertex of the rectangle
        width: Width of the rectangle
        height: Height of the rectangle
        plane: The plane to create the rectangle on (default: XY) or an Edge representing a Face

    Returns:
        Edge representing the rectangle
    """
    # Use parent class logic for the Edge structure
    start_x = LengthExp(width) / 2
    start_y = LengthExp(height) / 2

    line1 = line(
        Vertex(x=center._x - start_x, y=center._y - start_y, z=center._z),
        Vertex(x=center._x + start_x, y=center._y - start_y, z=center._z),
    )
    line2 = line(
        line1.v2,
        Vertex(x=center._x + start_x, y=center._y + start_y, z=center._z),
    )
    line3 = line(
        line2.v2,
        Vertex(x=center._x - start_x, y=center._y + start_y, z=center._z),
    )
    line4 = line(line3.v2, line1.v1)

    edge = Edge(v1=line1.v1, v2=line4.v2, sub_edges=[line1, line2, line3, line4])

    # Create native build123d rectangle
    native_rect = create_rectangle_wire(width, height)

    cx, cy, cz = center._x.value, center._y.value, center._z.value

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Position on the face's plane
            face_plane = bd.Plane(native_face)
            # Transform the wire to the face's plane
            native_rect = face_plane * native_rect
        else:
            # Fallback to XY plane
            native_rect = native_rect.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XY:
        native_rect = native_rect.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XZ:
        native_rect = native_rect.moved(bd.Location((cx, cy, cz)))
        # Rotate to XZ plane (rotate 90 degrees around X to make Z become Y)
        native_rect = native_rect.rotate(bd.Axis.X, 90)
    else:  # YZ plane
        native_rect = native_rect.moved(bd.Location((cx, cy, cz)))
        # Rotate to YZ plane (rotate 90 degrees around Y to make X become Z)
        native_rect = native_rect.rotate(bd.Axis.Y, -90)

    edge.set_native(native_rect)

    return edge


def circle(
    center: Vertex,
    radius: LengthType,
    curve_type: CurveType = CurveType.BEZIER,
    plane: "Plane | Edge" = Plane.XY,
) -> Edge:
    """Create a full circle.

    Args:
        center: Center vertex of the circle
        radius: Radius of the circle
        curve_type: Type of curve to use (default: BEZIER)
        plane: The plane to create the circle on (default: XY) or an Edge representing a Face

    Returns:
        Edge representing the circle
    """
    # Create Edge with arc sub-edges from parent
    arc_edge = _arc(center, radius, 0, "360deg", curve_type)

    # Create native build123d circle
    native_circle = create_circle_wire(radius)

    cx, cy, cz = center._x.value, center._y.value, center._z.value

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Position on the face's plane
            face_plane = bd.Plane(native_face)
            native_circle = face_plane * native_circle
        else:
            # Fallback to XY plane
            native_circle = native_circle.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XY:
        native_circle = native_circle.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XZ:
        native_circle = native_circle.moved(bd.Location((cx, cy, cz)))
        # Rotate to XZ plane (rotate 90 degrees around X to make Z become Y)
        native_circle = native_circle.rotate(bd.Axis.X, 90)
    else:  # YZ plane
        native_circle = native_circle.moved(bd.Location((cx, cy, cz)))
        # Rotate to YZ plane (rotate 90 degrees around Y to make X become Z)
        native_circle = native_circle.rotate(bd.Axis.Y, -90)

    arc_edge.set_native(native_circle)

    return arc_edge


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
    arc_edge.set_native(native_arc)

    return arc_edge


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
    arc_edge.set_native(native_arc)

    return arc_edge


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
    arc_edge.set_native(native_arc)

    return arc_edge


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
    arc_edge.set_native(native_arc)

    return arc_edge


def polygon(
    center: Vertex,
    radius: LengthType,
    sides: int,
    rotation: AngleType = 0,
    plane: "Plane | Edge" = Plane.XY,
) -> Edge:
    """Create a regular polygon with the given number of sides.

    Args:
        center: Center vertex of the polygon
        radius: Radius of the polygon
        sides: Number of sides (minimum 3)
        rotation: Rotation angle in degrees (default 0)
        plane: The plane to create the polygon on (default: XY) or an Edge representing a Face

    Returns:
        Edge representing the polygon
    """
    # Use parent class for the Edge structure
    poly_edge = BaseDraw.polygon(center, radius, sides, rotation, plane)

    # Create native build123d polygon
    r = float(LengthExp(radius))
    rot_deg = math.degrees(Angle(rotation).value)
    native_poly = bd.RegularPolygon(radius=r, side_count=sides, rotation=rot_deg)

    cx, cy, cz = center._x.value, center._y.value, center._z.value

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Position on the face's plane
            face_plane = bd.Plane(native_face)
            native_poly = face_plane * native_poly
        else:
            # Fallback to XY plane
            native_poly = native_poly.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XY:
        native_poly = native_poly.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XZ:
        native_poly = native_poly.moved(bd.Location((cx, cy, cz)))
        # Rotate to XZ plane (rotate 90 degrees around X to make Z become Y)
        native_poly = native_poly.rotate(bd.Axis.X, 90)
    else:  # YZ plane
        native_poly = native_poly.moved(bd.Location((cx, cy, cz)))
        # Rotate to YZ plane (rotate 90 degrees around Y to make X become Z)
        native_poly = native_poly.rotate(bd.Axis.Y, -90)

    poly_edge.set_native(native_poly)

    return poly_edge


def text(
    text: str,
    font: str,
    size: LengthType,
    center: "Vertex | None" = None,
    plane: "Plane | Edge" = Plane.XY,
) -> Edge:
    """Create a text string.

    Args:
        text: The text string to create
        font: Font name (e.g., "Arial", "Helvetica")
        size: Font size
        center: Optional center vertex for positioning the text
        plane: The plane to create the text on (default: XY) or an Edge representing a Face

    Returns:
        Edge representing the text
    """
    native_text = create_text_wire(text, size, font)

    if center is not None:
        # Move to the specified center position
        cx, cy, cz = center._x.value, center._y.value, center._z.value

        # Handle plane positioning - support both Plane enum and Edge (Face)
        if isinstance(plane, Edge):
            # If plane is an Edge representing a Face, use the face's plane
            native_face = plane.get_native("face")
            if native_face is not None:
                # Position on the face's plane
                face_plane = bd.Plane(native_face)
                native_text = face_plane * native_text
            else:
                # Fallback to XY plane
                native_text = native_text.moved(bd.Location((cx, cy, cz)))
        else:
            # Standard plane positioning
            native_text = native_text.moved(bd.Location((cx, cy, cz)))

        # Update edge vertices to reflect the new position
        # For text, we don't have clear v1/v2, so use a simplified approach
        size_val = float(LengthExp(size))
        edge = Edge(
            v1=Vertex(x=cx - size_val / 2, y=cy, z=cz),
            v2=Vertex(x=cx + size_val / 2, y=cy, z=cz),
        )
    else:
        edge = Edge(
            v1=Vertex(x=0, y=0, z=0),
            v2=Vertex(x=0, y=0, z=0),
        )

    edge.set_native(native_text)
    return edge


def trapezoid(
    center: Vertex,
    width: LengthType,
    height: LengthType,
    angle: AngleType,
    plane: "Plane | Edge" = Plane.XY,
) -> Edge:
    """Create a trapezoid.

    Args:
        center: Center vertex of the trapezoid
        width: Width of the trapezoid
        height: Height of the trapezoid
        angle: Trapezoid angle
        plane: The plane to create the trapezoid on (default: XY) or an Edge representing a Face

    Returns:
        Edge representing the trapezoid
    """
    angle_deg = math.degrees(Angle(angle).value)
    native_trap = create_trapezoid_wire(width, height, angle_deg)

    cx, cy, cz = center._x.value, center._y.value, center._z.value

    # Handle plane positioning - support both Plane enum and Edge (Face)
    if isinstance(plane, Edge):
        # If plane is an Edge representing a Face, use the face's plane
        native_face = plane.get_native("face")
        if native_face is not None:
            # Position on the face's plane
            face_plane = bd.Plane(native_face)
            native_trap = face_plane * native_trap
        else:
            # Fallback to XY plane
            native_trap = native_trap.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XY:
        native_trap = native_trap.moved(bd.Location((cx, cy, cz)))
    elif plane == Plane.XZ:
        native_trap = native_trap.moved(bd.Location((cx, cy, cz)))
        # Rotate to XZ plane (rotate 90 degrees around X to make Z become Y)
        native_trap = native_trap.rotate(bd.Axis.X, 90)
    else:  # YZ plane
        native_trap = native_trap.moved(bd.Location((cx, cy, cz)))
        # Rotate to YZ plane (rotate 90 degrees around Y to make X become Z)
        native_trap = native_trap.rotate(bd.Axis.Y, -90)

    # Create edge wrapper
    edge = Edge(
        v1=Vertex(
            x=center._x - LengthExp(width) / 2,
            y=center._y - LengthExp(height) / 2,
            z=center._z,
        ),
        v2=Vertex(
            x=center._x - LengthExp(width) / 2,
            y=center._y - LengthExp(height) / 2,
            z=center._z,
        ),
    )
    edge.set_native(native_trap)
    return edge


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
    spline_edge.set_native(native_spline)

    return spline_edge


def polyline(points: "list[tuple[float, float]] | list[Vertex]") -> Edge:
    """Create a polyline from a list of points.

    Args:
        points: List of 2D coordinate tuples (x, y) or Vertex objects

    Returns:
        Edge representing the polyline
    """
    # Use parent class for the Edge structure
    poly_edge = BaseDraw.polyline(points)

    # Convert to tuples for build123d
    point_tuples = []
    for p in points:
        if isinstance(p, Vertex):
            point_tuples.append((p._x.value, p._y.value))
        else:
            point_tuples.append(p)

    # Create native build123d polyline
    native_polyline = bd.Polyline(point_tuples)
    poly_edge.set_native(native_polyline)

    return poly_edge


def mirror(
    edge: Edge,
    across: "Plane | Edge",
) -> Edge:
    """Mirror an edge across a plane or edge, with options to union and create a face.

    Args:
        edge: Edge to mirror
        across: Plane (XY, XZ, or YZ) or Edge to mirror across
        union: If True, combine the original and mirrored edges (default True)
        make_face: If True, create a face from the result (default False)
        face_plane: Plane to place the face on (defaults to across if across is a Plane)

    Returns:
        Mirrored edge (combined with original if union=True, as face if make_face=True)
    """
    union: bool = True
    make_face: bool = False
    face_plane: "Plane | None" = None

    native = edge.get_native()
    if native is None:
        raise ValueError("Edge has no native build123d object")

    # Determine the build123d plane for mirroring
    if isinstance(across, Edge):
        # Mirror across an Edge - use the edge's native as the mirror plane
        mirror_native = across.get_native()
        if mirror_native is None:
            raise ValueError("Mirror edge has no native build123d object")
        native_mirrored = bd.mirror(native, mirror_native)
        bd_plane = None  # Will use face_plane for make_face
    else:
        # Mirror across a Plane
        if across == Plane.XY:
            bd_plane = bd.Plane.XY
        elif across == Plane.XZ:
            bd_plane = bd.Plane.XZ
        else:  # YZ
            bd_plane = bd.Plane.YZ
        native_mirrored = bd.mirror(native, bd_plane)

    # Union if requested
    if union:
        native_result = native + native_mirrored
    else:
        native_result = native_mirrored

    # Make face if requested
    if make_face:
        # Determine the face plane
        if face_plane is not None:
            if face_plane == Plane.XY:
                face_bd_plane = bd.Plane.XY
            elif face_plane == Plane.XZ:
                face_bd_plane = bd.Plane.XZ
            else:
                face_bd_plane = bd.Plane.YZ
        elif bd_plane is not None:
            face_bd_plane = bd_plane
        else:
            face_bd_plane = bd.Plane.XY  # Default

        # Transform and make face
        transformed = face_bd_plane * native_result
        native_result = bd.make_face(transformed)

    # Create the result edge
    result_edge = BaseDraw.mirror(edge, across)
    result_edge.set_native(native_result)

    return result_edge


def import_file(file_path: str) -> Edge:  # noqa: ARG004
    """Import an edge from a file."""
    # build123d doesn't have direct 2D import, raise not implemented
    _ = file_path  # Acknowledge parameter for API compatibility
    raise NotImplementedError("2D edge import is not yet implemented for build123d")


def export_file(edge: Edge, file_path: str) -> None:
    """Export an edge to a file."""
    native = edge.get_native()
    if native is None:
        raise ValueError("Edge has no native build123d object")

    # Export as SVG if 2D
    if file_path.lower().endswith(".svg"):
        bd.export_svg(native, file_path)
    else:
        raise ValueError(f"Unsupported 2D export format: {file_path}")
