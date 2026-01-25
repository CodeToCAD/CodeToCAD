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
    """Translate an object by the specified distances.

    If the object is a Vertex or Edge with a parent solid, the solid will be
    automatically rebuilt with the modified vertex/edge position.

    Args:
        obj: The object to translate (Vertex, Edge, or Solid)
        x: Distance to translate along X axis
        y: Distance to translate along Y axis
        z: Distance to translate along Z axis

    Returns:
        The translated object. If obj is a Vertex/Edge with a parent solid,
        returns the rebuilt Solid instead.
    """
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
    translated_obj = _wrap_native(obj, translated_native)

    # Check if this vertex/edge has a parent solid and auto-rebuild
    parent_native = obj.get_native("parent")
    if parent_native is not None:
        # Create parent Solid wrapper
        parent_solid = Solid(is_hidden=False)
        parent_solid.set_native(parent_native)

        if isinstance(obj, Vertex) and isinstance(translated_obj, Vertex):
            return rebuild_solid_with_modified_vertex(
                parent_solid, obj, translated_obj
            )
        elif isinstance(obj, Edge) and isinstance(translated_obj, Edge):
            # Check if this is a face (Edge with sub_edges) or a simple edge
            if obj.sub_edges is not None:
                # This is a face - use face rebuild function
                return rebuild_solid_with_modified_face(
                    parent_solid, obj, translated_obj
                )
            else:
                return rebuild_solid_with_modified_edge(
                    parent_solid, obj, translated_obj
                )

    return translated_obj


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


def rebuild_solid_with_modified_vertex(
    solid: Solid,
    original_vertex: Vertex,
    new_vertex: Vertex,
) -> Solid:
    """
    Rebuild a solid by modifying a vertex position.

    This works by:
    1. Finding the base face of the solid (bottom face for extruded solids)
    2. Extracting the outer wire from that face
    3. Modifying edges that contain the target vertex (using native object identity)
    4. Rebuilding the wire and face
    5. Extruding to create a new solid

    Args:
        solid: The original solid to modify
        original_vertex: The vertex to move (must be on the base face)
        new_vertex: The new position for the vertex

    Returns:
        A new Solid with the modified geometry
    """
    native_solid = solid.get_native()
    if native_solid is None:
        raise ValueError("Solid has no native build123d object")

    # Get the native build123d vertex for identity comparison
    native_orig_vertex = original_vertex.get_native()
    if native_orig_vertex is None:
        raise ValueError("Original vertex has no native build123d object")

    # 1. Get the base face (bottom face for extruded solids)
    faces = native_solid.faces()
    # Sort by Z to get bottom face
    base_face = sorted(faces, key=lambda f: f.center().Z)[0]

    # 2. Get the outer wire and its edges
    outer_wire = base_face.outer_wire()
    original_edges = outer_wire.edges()

    # 3. Get new vertex position
    # Vertex coordinates from selectors are already in mm (build123d units)
    new_x = float(new_vertex.x)
    new_y = float(new_vertex.y)
    new_z = float(new_vertex.z)

    # 4. Rebuild edges with modified vertex using native object identity
    new_edges = []

    for edge in original_edges:
        verts = edge.vertices()
        start_vert = verts[0]
        end_vert = verts[1] if len(verts) > 1 else start_vert
        start = start_vert.center()
        end = end_vert.center()

        # Check if start vertex is the EXACT vertex we want to modify
        start_x, start_y, start_z = start.X, start.Y, start.Z
        if native_orig_vertex.is_same(start_vert):
            start_x, start_y, start_z = new_x, new_y, new_z

        # Check if end vertex is the EXACT vertex we want to modify
        end_x, end_y, end_z = end.X, end.Y, end.Z
        if native_orig_vertex.is_same(end_vert):
            end_x, end_y, end_z = new_x, new_y, new_z

        # Create new edge
        new_edge = bd.Line((start_x, start_y, start_z), (end_x, end_y, end_z)).edge()
        new_edges.append(new_edge)

    # 5. Rebuild wire and face
    new_wire = bd.Wire(new_edges)
    new_face = bd.Face(new_wire)

    # 6. Calculate extrusion height from original solid
    bbox = native_solid.bounding_box()
    height = bbox.max.Z - bbox.min.Z

    # 7. Extrude to create new solid
    # The face normal may point down (-Z), so we need to check and use negative
    # height if needed to extrude upward (in +Z direction)
    face_normal_z = new_face.normal_at().Z
    if face_normal_z < 0:
        # Normal points down, use negative height to extrude upward
        new_native = bd.extrude(new_face, -height)
    else:
        new_native = bd.extrude(new_face, height)

    # Wrap in CodeToCAD Solid
    result = Solid(is_hidden=solid.is_hidden)
    result.set_native(new_native)
    return result


def rebuild_solid_with_modified_edge(
    solid: Solid,
    original_edge: Edge,
    new_edge: Edge,
) -> Solid:
    """
    Rebuild a solid by replacing an edge with a modified version.

    When an edge is moved, the vertices it shares with adjacent edges must also
    be updated. This function maps original vertex positions to new positions
    and updates ALL edges that share those vertices, maintaining a connected wire.

    Uses native object identity to identify exactly which edge/vertices to modify.

    Args:
        solid: The original solid to modify
        original_edge: The edge to replace (must be on the base face)
        new_edge: The new edge to use

    Returns:
        A new Solid with the modified geometry
    """
    native_solid = solid.get_native()
    if native_solid is None:
        raise ValueError("Solid has no native build123d object")

    # Get the native build123d edge for identity comparison
    native_orig_edge = original_edge.get_native()
    if native_orig_edge is None:
        raise ValueError("Original edge has no native build123d object")

    # Get the native vertices from the original edge for identity comparison
    native_orig_verts = native_orig_edge.vertices()
    native_v1 = native_orig_verts[0] if len(native_orig_verts) > 0 else None
    native_v2 = native_orig_verts[1] if len(native_orig_verts) > 1 else native_v1

    # 1. Get the base face (bottom face for extruded solids)
    faces = native_solid.faces()
    base_face = sorted(faces, key=lambda f: f.center().Z)[0]

    # 2. Get the outer wire and its edges
    outer_wire = base_face.outer_wire()
    original_edges = outer_wire.edges()

    # 3. Get the new vertex positions
    new_v1_pos = (float(new_edge.v1.x), float(new_edge.v1.y), float(new_edge.v1.z))
    new_v2_pos = (float(new_edge.v2.x), float(new_edge.v2.y), float(new_edge.v2.z))

    # 4. Rebuild all edges, mapping vertices to new positions using native identity
    new_edges = []

    for edge in original_edges:
        verts = edge.vertices()
        start_vert = verts[0]
        end_vert = verts[1] if len(verts) > 1 else start_vert
        start = start_vert.center()
        end = end_vert.center()

        # Check if this vertex matches one of the original edge's vertices
        start_pos = (start.X, start.Y, start.Z)
        end_pos = (end.X, end.Y, end.Z)

        if native_v1 is not None and native_v1.is_same(start_vert):
            start_pos = new_v1_pos
        elif native_v2 is not None and native_v2.is_same(start_vert):
            start_pos = new_v2_pos

        if native_v1 is not None and native_v1.is_same(end_vert):
            end_pos = new_v1_pos
        elif native_v2 is not None and native_v2.is_same(end_vert):
            end_pos = new_v2_pos

        rebuilt_edge = bd.Line(start_pos, end_pos).edge()
        new_edges.append(rebuilt_edge)

    # 5. Rebuild wire and face
    new_wire = bd.Wire(new_edges)
    new_face = bd.Face(new_wire)

    # 6. Calculate extrusion height from original solid
    bbox = native_solid.bounding_box()
    height = bbox.max.Z - bbox.min.Z

    # 7. Extrude to create new solid
    # The face normal may point down (-Z), so we need to check and use negative
    # height if needed to extrude upward (in +Z direction)
    face_normal_z = new_face.normal_at().Z
    if face_normal_z < 0:
        # Normal points down, use negative height to extrude upward
        new_native = bd.extrude(new_face, -height)
    else:
        new_native = bd.extrude(new_face, height)

    # Wrap in CodeToCAD Solid
    result = Solid(is_hidden=solid.is_hidden)
    result.set_native(new_native)
    return result


def rebuild_solid_with_modified_face(
    solid: Solid,
    original_face: Edge,
    new_face: Edge,
) -> Solid:
    """
    Rebuild a solid by replacing a face with a modified version.

    When a face is moved, all vertices of that face need to be mapped to their
    new positions. This function maps original vertex positions to new positions
    for ALL vertices in the face and updates the solid accordingly.

    Uses native object identity to identify exactly which vertices to modify.

    Args:
        solid: The original solid to modify
        original_face: The face to replace (represented as an Edge with sub_edges)
        new_face: The new face to use (with the same structure as original_face)

    Returns:
        A new Solid with the modified geometry
    """
    native_solid = solid.get_native()
    if native_solid is None:
        raise ValueError("Solid has no native build123d object")

    # Get the native face object
    native_orig_face = original_face.get_native("face")
    if native_orig_face is None:
        # Fallback to default native (wire)
        native_orig_face = original_face.get_native()
    if native_orig_face is None:
        raise ValueError("Original face has no native build123d object")

    # Build a vertex mapping from original face vertices to new face vertices
    # using native object identity
    orig_sub_edges = original_face.sub_edges or [original_face]
    new_sub_edges = new_face.sub_edges or [new_face]

    # Map native vertices to their new positions
    vertex_new_pos: "dict[int, tuple[float, float, float]]" = {}

    for orig_edge, new_edge in zip(orig_sub_edges, new_sub_edges):
        native_orig = orig_edge.get_native()
        if native_orig is None:
            continue
        orig_verts = native_orig.vertices()

        # Get new positions from the translated edge
        new_v1_pos = (float(new_edge.v1.x), float(new_edge.v1.y), float(new_edge.v1.z))
        new_v2_pos = (float(new_edge.v2.x), float(new_edge.v2.y), float(new_edge.v2.z))

        if len(orig_verts) >= 1:
            vertex_new_pos[id(orig_verts[0].wrapped)] = new_v1_pos
        if len(orig_verts) >= 2:
            vertex_new_pos[id(orig_verts[1].wrapped)] = new_v2_pos

    # 1. Get the base face (bottom face for extruded solids)
    faces = native_solid.faces()
    base_face = sorted(faces, key=lambda f: f.center().Z)[0]

    # 2. Get the outer wire and its edges
    outer_wire = base_face.outer_wire()
    original_edges = outer_wire.edges()

    # 3. Rebuild all edges, mapping vertices to new positions using native identity
    new_edges = []

    for edge in original_edges:
        verts = edge.vertices()
        start_vert = verts[0]
        end_vert = verts[1] if len(verts) > 1 else start_vert
        start = start_vert.center()
        end = end_vert.center()

        # Check if this vertex should be mapped to a new position
        start_pos = (start.X, start.Y, start.Z)
        end_pos = (end.X, end.Y, end.Z)

        start_id = id(start_vert.wrapped)
        end_id = id(end_vert.wrapped)

        if start_id in vertex_new_pos:
            start_pos = vertex_new_pos[start_id]
        if end_id in vertex_new_pos:
            end_pos = vertex_new_pos[end_id]

        rebuilt_edge = bd.Line(start_pos, end_pos).edge()
        new_edges.append(rebuilt_edge)

    # 4. Rebuild wire and face
    new_wire = bd.Wire(new_edges)
    new_face_bd = bd.Face(new_wire)

    # 5. Calculate extrusion height from original solid
    bbox = native_solid.bounding_box()
    height = bbox.max.Z - bbox.min.Z

    # 6. Extrude to create new solid
    # The face normal may point down (-Z), so we need to check and use negative
    # height if needed to extrude upward (in +Z direction)
    face_normal_z = new_face_bd.normal_at().Z
    if face_normal_z < 0:
        # Normal points down, use negative height to extrude upward
        new_native = bd.extrude(new_face_bd, -height)
    else:
        new_native = bd.extrude(new_face_bd, height)

    # Wrap in CodeToCAD Solid
    result = Solid(is_hidden=solid.is_hidden)
    result.set_native(new_native)
    return result


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
