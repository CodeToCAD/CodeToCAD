"""
Topology selectors for build123d objects.

This module implements the selector functions defined in codetocad.core.cad.selectors
using build123d's geometry query APIs.
"""

import build123d as bd

from codetocad.core.cad.sketch import Sketch
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.enums.cardinal_directions import CardinalDirection, CardinalOffset
from codetocad.integrations.build123d.adapter.transformations import get_bounding_box


def _get_cardinal_position(bbox: bd.BoundBox, cardinal: CardinalDirection) -> bd.Vector:
    """
    Calculate the target position for a cardinal direction based on a bounding box.

    Args:
        bbox: The bounding box of the object.
        cardinal: The cardinal direction.

    Returns:
        A Vector representing the target position.
    """
    # Get bounding box extents
    min_x, min_y, min_z = bbox.min.X, bbox.min.Y, bbox.min.Z
    max_x, max_y, max_z = bbox.max.X, bbox.max.Y, bbox.max.Z
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    # Map cardinal directions to positions
    # X: left=-X, right=+X, center=center_x
    # Y: back=-Y, front=+Y, center=center_y
    # Z: bottom=-Z, top=+Z, center=center_z

    positions = {
        # Center
        CardinalDirection.CENTER: (center_x, center_y, center_z),
        # Top face (Z = max_z)
        CardinalDirection.TOP_CENTER: (center_x, center_y, max_z),
        CardinalDirection.TOP_LEFT: (min_x, center_y, max_z),
        CardinalDirection.TOP_RIGHT: (max_x, center_y, max_z),
        CardinalDirection.TOP_FRONT: (center_x, max_y, max_z),
        CardinalDirection.TOP_BACK: (center_x, min_y, max_z),
        CardinalDirection.TOP_FRONT_LEFT: (min_x, max_y, max_z),
        CardinalDirection.TOP_FRONT_RIGHT: (max_x, max_y, max_z),
        CardinalDirection.TOP_BACK_LEFT: (min_x, min_y, max_z),
        CardinalDirection.TOP_BACK_RIGHT: (max_x, min_y, max_z),
        # Bottom face (Z = min_z)
        CardinalDirection.BOTTOM_CENTER: (center_x, center_y, min_z),
        CardinalDirection.BOTTOM_LEFT: (min_x, center_y, min_z),
        CardinalDirection.BOTTOM_RIGHT: (max_x, center_y, min_z),
        CardinalDirection.BOTTOM_FRONT: (center_x, max_y, min_z),
        CardinalDirection.BOTTOM_BACK: (center_x, min_y, min_z),
        CardinalDirection.BOTTOM_FRONT_LEFT: (min_x, max_y, min_z),
        CardinalDirection.BOTTOM_FRONT_RIGHT: (max_x, max_y, min_z),
        CardinalDirection.BOTTOM_BACK_LEFT: (min_x, min_y, min_z),
        CardinalDirection.BOTTOM_BACK_RIGHT: (max_x, min_y, min_z),
        # Front face (Y = max_y)
        CardinalDirection.FRONT_CENTER: (center_x, max_y, center_z),
        CardinalDirection.FRONT_LEFT: (min_x, max_y, center_z),
        CardinalDirection.FRONT_RIGHT: (max_x, max_y, center_z),
        CardinalDirection.FRONT_TOP: (center_x, max_y, max_z),
        CardinalDirection.FRONT_BOTTOM: (center_x, max_y, min_z),
        # Back face (Y = min_y)
        CardinalDirection.BACK_CENTER: (center_x, min_y, center_z),
        CardinalDirection.BACK_LEFT: (min_x, min_y, center_z),
        CardinalDirection.BACK_RIGHT: (max_x, min_y, center_z),
        CardinalDirection.BACK_TOP: (center_x, min_y, max_z),
        CardinalDirection.BACK_BOTTOM: (center_x, min_y, min_z),
        # Left face (X = min_x)
        CardinalDirection.LEFT_CENTER: (min_x, center_y, center_z),
        CardinalDirection.LEFT_FRONT: (min_x, max_y, center_z),
        CardinalDirection.LEFT_BACK: (min_x, min_y, center_z),
        CardinalDirection.LEFT_TOP: (min_x, center_y, max_z),
        CardinalDirection.LEFT_BOTTOM: (min_x, center_y, min_z),
        # Right face (X = max_x)
        CardinalDirection.RIGHT_CENTER: (max_x, center_y, center_z),
        CardinalDirection.RIGHT_FRONT: (max_x, max_y, center_z),
        CardinalDirection.RIGHT_BACK: (max_x, min_y, center_z),
        CardinalDirection.RIGHT_TOP: (max_x, center_y, max_z),
        CardinalDirection.RIGHT_BOTTOM: (max_x, center_y, min_z),
    }

    pos = positions[cardinal]
    return bd.Vector(pos[0], pos[1], pos[2])


def _get_native_object(obj: "Solid | Edge | Sketch") -> "bd.Shape | None":
    """Extract the native build123d object from a CodeToCAD object."""
    if hasattr(obj, "native") and obj.native is not None:
        return obj.native
    if hasattr(obj, "get_native"):
        native = obj.get_native()
        if native is not None:
            return native
    return None


def _get_default_search_radius(bbox: bd.BoundBox) -> float:
    """Calculate a default search radius based on the bounding box diagonal."""
    return max(
        bbox.max.X - bbox.min.X, bbox.max.Y - bbox.min.Y, bbox.max.Z - bbox.min.Z
    )
    diagonal = (bbox.max - bbox.min).length
    # Use a percentage of the diagonal as default search radius
    return diagonal * 0.1


def _convert_search_radius(search_radius: "LengthType") -> float:
    """Convert a search radius to the same units as build123d coordinates (mm).

    LengthExp converts to meters internally, but build123d uses mm by convention.
    So we multiply by 1000 to convert meters back to mm.
    """
    meters = float(LengthExp(search_radius))
    # Convert meters to millimeters (build123d default unit)
    return meters * 1000


def _get_target_position(
    bbox: bd.BoundBox, cardinal: "CardinalDirection | CardinalOffset"
) -> bd.Vector:
    """
    Calculate the target position from either a CardinalDirection or CardinalOffset.

    If cardinal is a CardinalOffset, the offset is applied to the base cardinal position.
    The offset values are converted from LengthExp (meters) to mm.

    Args:
        bbox: The bounding box of the object.
        cardinal: Either a CardinalDirection or CardinalOffset.

    Returns:
        A Vector representing the target position.
    """
    if isinstance(cardinal, CardinalOffset):
        # Get the base position from the cardinal direction
        base_target = _get_cardinal_position(bbox, cardinal.cardinal)
        # Apply the offset (convert Point coordinates from meters to mm)
        offset_x = float(LengthExp(cardinal.offset.x)) * 1000
        offset_y = float(LengthExp(cardinal.offset.y)) * 1000
        offset_z = float(LengthExp(cardinal.offset.z)) * 1000
        return base_target + bd.Vector(offset_x, offset_y, offset_z)
    else:
        # It's a plain CardinalDirection
        return _get_cardinal_position(bbox, cardinal)


def _distance_to_point(
    element: "bd.Vertex | bd.Edge | bd.Face", target: bd.Vector
) -> float:
    """Calculate distance from an element's center to a target point."""
    if isinstance(element, bd.Vertex):
        elem_pos = bd.Vector(element.X, element.Y, element.Z)
    elif isinstance(element, bd.Edge):
        vertices = element.vertices()
        # elem_pos is the point furthest from the target point
        elem_pos = max(
            vertices, key=lambda v: (bd.Vector(v.X, v.Y, v.Z) - target).length
        )
        elem_pos = bd.Vector(elem_pos.X, elem_pos.Y, elem_pos.Z)
    else:
        # For edges and faces, use the center
        elem_pos = element.center()
    return (elem_pos - target).length


def _convert_bd_vertex_to_codetocad(
    bd_vertex: bd.Vertex,
    parent_solid: "Solid | None" = None,
) -> Vertex:
    """Convert a build123d Vertex to a CodeToCAD Vertex.

    Args:
        bd_vertex: The build123d Vertex to convert
        parent_solid: Optional parent Solid that contains this vertex

    Returns:
        A CodeToCAD Vertex with native and parent references set
    """
    vertex = Vertex(x=bd_vertex.X, y=bd_vertex.Y, z=bd_vertex.Z)
    vertex.set_native(bd_vertex)
    if parent_solid is not None:
        vertex.set_native(parent_solid.get_native(), "parent")
    return vertex


def _convert_bd_edge_to_codetocad(
    bd_edge: bd.Edge,
    parent_solid: "Solid | None" = None,
) -> Edge:
    """Convert a build123d Edge to a CodeToCAD Edge.

    Args:
        bd_edge: The build123d Edge to convert
        parent_solid: Optional parent Solid that contains this edge

    Returns:
        A CodeToCAD Edge with native and parent references set
    """
    # Get endpoints
    vertices = bd_edge.vertices()
    if len(vertices) >= 2:
        v1 = _convert_bd_vertex_to_codetocad(vertices[0], parent_solid)
        v2 = _convert_bd_vertex_to_codetocad(vertices[1], parent_solid)
    else:
        # For closed curves (circles), use the same vertex
        v1 = (
            _convert_bd_vertex_to_codetocad(vertices[0], parent_solid)
            if vertices
            else Vertex(x=0, y=0, z=0)
        )
        v2 = v1

    edge = Edge(v1=v1, v2=v2)
    edge.set_native(bd_edge)
    if parent_solid is not None:
        edge.set_native(parent_solid.get_native(), "parent")
    return edge


def _convert_bd_face_to_codetocad(
    bd_face: bd.Face,
    parent_solid: "Solid | None" = None,
) -> Edge:
    """Convert a build123d Face to a CodeToCAD Edge representing the outer boundary.

    The returned Edge represents the outer wire of the face. The original bd.Face
    is stored in native_refs["face"] for later retrieval if needed.
    The sub_edges list contains all the individual edges of the outer wire.

    Args:
        bd_face: The build123d Face to convert
        parent_solid: Optional parent Solid that contains this face

    Returns:
        A CodeToCAD Edge representing the face boundary with native and parent refs
    """
    # Get the outer wire of the face
    outer_wire = bd_face.outer_wire()

    # Get all edges from the outer wire and convert them to sub_edges
    wire_edges = outer_wire.edges()
    sub_edges: list[Edge] = []
    for bd_edge in wire_edges:
        sub_edge = _convert_bd_edge_to_codetocad(bd_edge, parent_solid)
        sub_edges.append(sub_edge)

    # Get the vertices of the outer wire to create Edge endpoints
    wire_vertices = outer_wire.vertices()
    if len(wire_vertices) >= 2:
        v1 = _convert_bd_vertex_to_codetocad(wire_vertices[0], parent_solid)
        v2 = _convert_bd_vertex_to_codetocad(wire_vertices[1], parent_solid)
    elif wire_vertices:
        # For closed single-vertex curves, use the same vertex
        v1 = _convert_bd_vertex_to_codetocad(wire_vertices[0], parent_solid)
        v2 = v1
    else:
        # Fallback for empty wire
        v1 = Vertex(x=0, y=0, z=0)
        v2 = v1

    edge = Edge(v1=v1, v2=v2, sub_edges=sub_edges if sub_edges else None)
    edge.set_native(outer_wire)  # Store the wire as default native
    edge.set_native(bd_face, "face")  # Store the original face for later retrieval
    if parent_solid is not None:
        edge.set_native(parent_solid.get_native(), "parent")
    return edge


def find_vertex(
    obj: "Solid | Edge | Sketch",
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Vertex]":
    """
    Find vertices in an object at or near a cardinal direction.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, uses 10% of the object's bounding box diagonal.

    Returns:
        A list of Vertex objects sorted by distance from the ideal cardinal position.
        Returns an empty list if no vertices are found within the search radius.
    """
    native = _get_native_object(obj)
    if native is None:
        return []

    bbox = get_bounding_box(native)
    target = _get_target_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = _convert_search_radius(search_radius)
    else:
        radius = _get_default_search_radius(bbox)

    # Get all vertices from the object
    try:
        bd_vertices = native.vertices()
    except AttributeError:
        return []

    # Filter and sort by distance
    results: list[tuple[float, bd.Vertex]] = []
    for v in bd_vertices:
        dist = _distance_to_point(v, target)
        if dist <= radius:
            results.append((dist, v))

    results.sort(key=lambda x: x[0])
    # Pass parent solid if obj is a Solid
    parent_solid = obj if isinstance(obj, Solid) else None
    return [_convert_bd_vertex_to_codetocad(v, parent_solid) for _, v in results]


def find_edge(
    obj: "Solid | Edge | Sketch",
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find edges in an object at or near a cardinal direction.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, uses 10% of the object's bounding box diagonal.

    Returns:
        A list of Edge objects sorted by distance from the ideal cardinal position.
        Returns an empty list if no edges are found within the search radius.
    """
    native = _get_native_object(obj)
    if native is None:
        return []

    bbox = get_bounding_box(native)
    target = _get_target_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = _convert_search_radius(search_radius)
    else:
        radius = _get_default_search_radius(bbox)

    # Get all edges from the object
    try:
        bd_edges = native.edges()
    except AttributeError:
        return []

    # Filter and sort by distance
    results: list[tuple[float, bd.Edge]] = []
    for e in bd_edges:
        dist = _distance_to_point(e, target)
        if dist <= radius:
            results.append((dist, e))

    results.sort(key=lambda x: x[0])
    # Pass parent solid if obj is a Solid
    parent_solid = obj if isinstance(obj, Solid) else None
    return [_convert_bd_edge_to_codetocad(e, parent_solid) for _, e in results]


def find_face(
    obj: Solid,
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find faces in a solid at or near a cardinal direction.

    The returned Edge represents the outer boundary wire of the face. The original
    native face object is stored in native_refs["face"] and can be retrieved with
    edge.get_native("face").

    Args:
        obj: The Solid object to search within.
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, uses 10% of the object's bounding box diagonal.

    Returns:
        A list of Edge objects (representing face outer boundaries) sorted by
        distance from the ideal cardinal position. Returns an empty list if no
        faces are found within the search radius.
    """
    native = _get_native_object(obj)
    if native is None:
        return []

    bbox = get_bounding_box(native)
    target = _get_target_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = _convert_search_radius(search_radius)
    else:
        radius = _get_default_search_radius(bbox)

    # Get all faces from the object
    try:
        bd_faces = native.faces()
    except AttributeError:
        return []

    # Filter and sort by distance
    results: list[tuple[float, bd.Face]] = []
    for f in bd_faces:
        dist = _distance_to_point(f, target)
        if dist <= radius:
            results.append((dist, f))

    results.sort(key=lambda x: x[0])
    # Pass parent solid (obj is always a Solid for find_face)
    return [_convert_bd_face_to_codetocad(f, obj) for _, f in results]


def _convert_bd_solid_to_codetocad(native: "bd.Shape") -> Solid:
    """Convert a build123d Solid/Part to a CodeToCAD Solid."""
    solid = Solid(is_hidden=False)
    solid.set_native(native)
    return solid


def find_shape(
    obj: "Solid | Edge | Sketch",
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Vertex | Edge | Solid]":
    """
    Find any topology element (vertex, edge, or solid) at or near a cardinal direction.

    Note: Face boundaries are returned as Edge objects (the outer wire of each face).
    The solid itself is included if its center is within the search radius.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, uses 10% of the object's bounding box diagonal.

    Returns:
        A list of topology elements (Vertex, Edge, or Solid) sorted by distance
        from the ideal cardinal position. Returns an empty list if no elements
        are found within the search radius.
    """
    native = _get_native_object(obj)
    if native is None:
        return []

    bbox = get_bounding_box(native)
    target = _get_target_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = _convert_search_radius(search_radius)
    else:
        radius = _get_default_search_radius(bbox)

    results: list[tuple[float, "Vertex | Edge | Solid"]] = []

    # Collect vertices
    try:
        for v in native.vertices():
            dist = _distance_to_point(v, target)
            if dist <= radius:
                results.append((dist, _convert_bd_vertex_to_codetocad(v)))
    except AttributeError:
        pass

    # Collect edges
    try:
        for e in native.edges():
            dist = _distance_to_point(e, target)
            if dist <= radius:
                results.append((dist, _convert_bd_edge_to_codetocad(e)))
    except AttributeError:
        pass

    # Collect faces (as Edge representing outer boundary)
    try:
        for f in native.faces():
            dist = _distance_to_point(f, target)
            if dist <= radius:
                results.append((dist, _convert_bd_face_to_codetocad(f)))
    except AttributeError:
        pass

    # Include the solid itself if its center is within the search radius
    # The solid's center is the center of its bounding box
    solid_center = bd.Vector(
        (bbox.min.X + bbox.max.X) / 2,
        (bbox.min.Y + bbox.max.Y) / 2,
        (bbox.min.Z + bbox.max.Z) / 2,
    )
    solid_dist = (solid_center - target).length
    if solid_dist <= radius:
        results.append((solid_dist, _convert_bd_solid_to_codetocad(native)))

    results.sort(key=lambda x: x[0])
    return [elem for _, elem in results]
