"""
Topology selectors for querying geometric elements from CAD objects.

This module provides functions to find vertices, edges, and faces based on
cardinal directions. These are interface functions that should be implemented
by specific CAD integrations (e.g., build123d, Blender).

The selector functions work by:
1. Calculating a target position based on the cardinal direction and the object's bounding box
2. Finding all elements (vertices/edges/faces) within an optional search radius
3. Sorting results by distance from the target position
4. Returning the sorted list of matching elements

Example usage:
    >>> from codetocad.core.cad.selectors import find_vertex, find_face
    >>> from codetocad.core.enums import CardinalDirection
    >>>
    >>> # Find vertices at the top-left corner of a solid
    >>> vertices = find_vertex(my_solid, CardinalDirection.TOP_LEFT)
    >>>
    >>> # Find the top face with a specific search tolerance
    >>> faces = find_face(my_solid, CardinalDirection.TOP_CENTER, search_radius="1mm")
"""

from codetocad.core.cad.sketch import Sketch
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.dimensions.length_expression import LengthType
from codetocad.core.enums.cardinal_directions import CardinalDirection, CardinalOffset


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
            If None, a reasonable default is used based on the object's dimensions.

    Returns:
        A list of Vertex objects sorted by distance from the ideal cardinal position.
        Returns an empty list if no vertices are found within the search radius.

    Example:
        >>> # Find vertices at the top-front corner
        >>> corners = find_vertex(my_box, CardinalDirection.TOP_FRONT)
        >>> if corners:
        ...     print(f"Found {len(corners)} vertices at top-front")
        >>> # Find vertices at an offset position
        >>> corners = find_vertex(my_box, offset(CardinalDirection.TOP_FRONT, Point(x="5mm")))
    """
    raise NotImplementedError("Method not implemented.")


def find_edge(
    obj: "Solid | Edge | Sketch",
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find edges in an object at or near a cardinal direction.

    The cardinal direction typically corresponds to the center point of the edge.
    For example, FRONT_TOP would find edges along the top-front edge of a box.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, a reasonable default is used based on the object's dimensions.

    Returns:
        A list of Edge objects sorted by distance from the ideal cardinal position.
        Returns an empty list if no edges are found within the search radius.

    Example:
        >>> # Find edges along the left side
        >>> left_edges = find_edge(my_box, CardinalDirection.LEFT_CENTER)
    """
    raise NotImplementedError("Method not implemented.")


def find_face(
    obj: Solid,
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Edge]":
    """
    Find faces in a solid at or near a cardinal direction.

    The cardinal direction typically corresponds to the center point of the face.
    For example, TOP_CENTER would find the top face of a box.

    The returned Edge represents the outer boundary wire of the face. The original
    native face object is stored in native_refs["face"] and can be retrieved with
    edge.get_native("face").

    Args:
        obj: The Solid object to search within.
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, a reasonable default is used based on the object's dimensions.

    Returns:
        A list of Edge objects (representing face outer boundaries) sorted by
        distance from the ideal cardinal position. Returns an empty list if no
        faces are found within the search radius.

    Example:
        >>> # Find the top face
        >>> top_faces = find_face(my_box, CardinalDirection.TOP_CENTER)
        >>> if top_faces:
        ...     top_face = top_faces[0]  # Get the closest match (outer wire)
        ...     native_face = top_face.get_native("face")  # Get original face
    """
    raise NotImplementedError("Method not implemented.")


def find_shape(
    obj: "Solid | Edge | Sketch",
    cardinal: "CardinalDirection | CardinalOffset",
    search_radius: "LengthType | None" = None,
) -> "list[Vertex | Edge | Solid]":
    """
    Find any topology element (vertex, edge, or solid) at or near a cardinal direction.

    This is a general-purpose selector that returns all matching topology elements,
    regardless of type. Useful when you want to select whatever is nearest to a
    cardinal position.

    Note: Face boundaries are returned as Edge objects (the outer wire of each face).
    The solid itself is included if its center is within the search radius.

    Args:
        obj: The CAD object to search within (Solid, Edge, or Sketch).
        cardinal: The cardinal direction or CardinalOffset indicating where to search.
            If a CardinalOffset is provided, the offset is applied to the cardinal position.
        search_radius: Optional maximum distance from the ideal cardinal position.
            If None, a reasonable default is used based on the object's dimensions.

    Returns:
        A list of topology elements (Vertex, Edge, or Solid) sorted by distance
        from the ideal cardinal position. Returns an empty list if no elements
        are found within the search radius.

    Example:
        >>> # Find any geometry at the top-left corner
        >>> elements = find_shape(my_box, CardinalDirection.TOP_LEFT)
        >>> for elem in elements:
        ...     print(f"Found: {type(elem).__name__}")
    """
    raise NotImplementedError("Method not implemented.")
