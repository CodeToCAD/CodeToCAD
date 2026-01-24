"""
Topology selectors for build123d objects.

This module implements the selector functions defined in codetocad.core.cad.selectors
using build123d's geometry query APIs.
"""

import build123d as bd

from codetocad.core.cad.sketch import Sketch
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.length_expression import LengthExp, LengthType
from codetocad.core.enums.cardinal_directions import CardinalDirection
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
    if hasattr(obj, "native_ref") and obj.native_ref is not None:
        return obj.native_ref
    return None


def _get_default_search_radius(bbox: bd.BoundBox) -> float:
    """Calculate a default search radius based on the bounding box diagonal."""
    diagonal = (bbox.max - bbox.min).length
    # Use 10% of the diagonal as default search radius
    return diagonal * 0.1


def _distance_to_point(
    element: "bd.Vertex | bd.Edge | bd.Face", target: bd.Vector
) -> float:
    """Calculate distance from an element's center to a target point."""
    if isinstance(element, bd.Vertex):
        elem_pos = bd.Vector(element.X, element.Y, element.Z)
    else:
        # For edges and faces, use the center
        elem_pos = element.center()
    return (elem_pos - target).length


def _convert_bd_vertex_to_codetocad(bd_vertex: bd.Vertex) -> Vertex:
    """Convert a build123d Vertex to a CodeToCAD Vertex."""
    vertex = Vertex(x=bd_vertex.X, y=bd_vertex.Y, z=bd_vertex.Z)
    vertex.native_ref = bd_vertex
    return vertex


def _convert_bd_edge_to_codetocad(bd_edge: bd.Edge) -> Edge:
    """Convert a build123d Edge to a CodeToCAD Edge."""
    # Get endpoints
    vertices = bd_edge.vertices()
    if len(vertices) >= 2:
        v1 = _convert_bd_vertex_to_codetocad(vertices[0])
        v2 = _convert_bd_vertex_to_codetocad(vertices[1])
    else:
        # For closed curves (circles), use the same vertex
        v1 = (
            _convert_bd_vertex_to_codetocad(vertices[0])
            if vertices
            else Vertex(x=0, y=0, z=0)
        )
        v2 = v1

    edge = Edge(v1=v1, v2=v2)
    edge.native_ref = bd_edge
    return edge


def _convert_bd_face_to_codetocad(bd_face: bd.Face) -> Edge:
    """Convert a build123d Face to a CodeToCAD Edge representing the outer boundary.

    The returned Edge represents the outer wire of the face. The original bd.Face
    is stored in native_parent_ref for later retrieval if needed.
    """
    # Get the outer wire of the face
    outer_wire = bd_face.outer_wire()

    # Get the vertices of the outer wire to create Edge endpoints
    wire_vertices = outer_wire.vertices()
    if len(wire_vertices) >= 2:
        v1 = _convert_bd_vertex_to_codetocad(wire_vertices[0])
        v2 = _convert_bd_vertex_to_codetocad(wire_vertices[1])
    elif wire_vertices:
        # For closed single-vertex curves, use the same vertex
        v1 = _convert_bd_vertex_to_codetocad(wire_vertices[0])
        v2 = v1
    else:
        # Fallback for empty wire
        v1 = Vertex(x=0, y=0, z=0)
        v2 = v1

    edge = Edge(v1=v1, v2=v2)
    edge.native_ref = outer_wire  # Store the wire as native_ref
    edge.native_parent_ref = bd_face  # Store the original face for later retrieval
    return edge


def find_vertex(
    obj: "Solid | Edge | Sketch",
    cardinal: CardinalDirection,
    search_radius: "LengthType | None" = None,
) -> "list[Vertex]":
    """
    Find vertices in an object at or near a cardinal direction.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction indicating where to search.
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
    target = _get_cardinal_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = float(LengthExp(search_radius))
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
    return [_convert_bd_vertex_to_codetocad(v) for _, v in results]


def find_edge(
    obj: "Solid | Edge | Sketch",
    cardinal: CardinalDirection,
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find edges in an object at or near a cardinal direction.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction indicating where to search.
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
    target = _get_cardinal_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = float(LengthExp(search_radius))
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
    return [_convert_bd_edge_to_codetocad(e) for _, e in results]


def find_face(
    obj: Solid,
    cardinal: CardinalDirection,
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find faces in a solid at or near a cardinal direction.

    The returned Edge represents the outer boundary wire of the face. The original
    native face object is stored in the Edge's native_parent_ref attribute.

    Args:
        obj: The Solid object to search within.
        cardinal: The cardinal direction indicating where to search.
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
    target = _get_cardinal_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = float(LengthExp(search_radius))
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
    return [_convert_bd_face_to_codetocad(f) for _, f in results]


def find_shape(
    obj: "Solid | Edge | Sketch",
    cardinal: CardinalDirection,
    search_radius: "LengthType | None" = None,
) -> "list[Vertex | Edge]":
    """
    Find any topology element (vertex or edge) at or near a cardinal direction.

    Note: Face boundaries are returned as Edge objects (the outer wire of each face).

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction indicating where to search.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, uses 10% of the object's bounding box diagonal.

    Returns:
        A list of topology elements (Vertex or Edge) sorted by distance
        from the ideal cardinal position. Returns an empty list if no elements
        are found within the search radius.
    """
    native = _get_native_object(obj)
    if native is None:
        return []

    bbox = get_bounding_box(native)
    target = _get_cardinal_position(bbox, cardinal)

    # Determine search radius
    if search_radius is not None:
        radius = float(LengthExp(search_radius))
    else:
        radius = _get_default_search_radius(bbox)

    results: list[tuple[float, "Vertex | Edge"]] = []

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

    results.sort(key=lambda x: x[0])
    return [elem for _, elem in results]
