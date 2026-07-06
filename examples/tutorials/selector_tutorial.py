"""
Tutorial: Topology Selectors

This tutorial demonstrates how to use the topology selector functions to find
vertices, edges, and faces in 3D objects based on cardinal directions.

The selectors work by calculating a target position from a CardinalDirection
and the object's bounding box, then finding geometry elements within a search
radius of that position.

Each sub-example is visualized independently - close the window to continue.
"""

from codetocad.core import Solid, Vertex, Edge, PresetMaterial
from codetocad.core.dimensions.point import Point
from codetocad.core.enums import CardinalDirection
from codetocad.core.enums.cardinal_directions import offset
from codetocad.integrations.build123d.cad import Shape
from codetocad.integrations.build123d.cad.selectors import (
    find_vertex,
    find_edge,
    find_face,
    find_shape,
)
from codetocad.integrations.open3d import (
    show_in_open3d,
    ColoredVertex,
    ColoredEdge,
    ColoredFace,
)


# Predefined colors for visualization
RED = (1.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
YELLOW = (1.0, 1.0, 0.0)
CYAN = (0.0, 1.0, 1.0)
MAGENTA = (1.0, 0.0, 1.0)
ORANGE = (1.0, 0.5, 0.0)
GRAY = (0.5, 0.5, 0.5)


def _create_box() -> Solid:
    """Create a simple 20x20x20 box centered at origin."""
    center = Vertex(x=0, y=0, z=0)
    return Shape.cuboid(center, width=20, height=20, depth=20)


def _visualize(
    box: Solid,
    title: str,
    vertices: "list[Vertex] | None" = None,
    edges: "list[Edge] | None" = None,
    faces: "list[Edge] | None" = None,
    cardinal_label: "str | None" = None,
) -> None:
    """Visualize the box with optional highlighted elements.

    Args:
        box: The solid to visualize
        title: Title for the visualization
        vertices: List of vertices to highlight
        edges: List of edges to highlight
        faces: List of faces to highlight
        cardinal_label: Optional cardinal direction label to display on elements
    """
    print(f"\n  Visualizing: {title}")
    print("    Coordinate frame: X=Red, Y=Green, Z=Blue")

    colored_vertices = [
        ColoredVertex(vertex=v, color=RED, label=cardinal_label)
        for v in (vertices or [])
    ]
    colored_edges = [
        ColoredEdge(edge=e, color=GREEN, label=cardinal_label) for e in (edges or [])
    ]
    colored_faces = [ColoredFace(face=f, color=BLUE) for f in (faces or [])]

    show_in_open3d(
        box,
        color=GRAY,
        vertices=colored_vertices,
        edges=colored_edges,
        faces=colored_faces,
        vertex_radius=1.5,
        edge_radius=0.8,
        show_coordinate_frame=True,
    )


def example_find_vertex_left_center() -> None:
    """Find vertex at LEFT_CENTER corner."""
    print("\n--- find_vertex: LEFT_CENTER ---")
    box = _create_box()
    cardinal = CardinalDirection.LEFT_CENTER
    vertices = find_vertex(box, cardinal)
    print(f"  Found {len(vertices)} vertex(es)")
    for i, v in enumerate(vertices):
        print(f"    {i+1}. ({v.x}, {v.y}, {v.z})")
    if vertices:
        _visualize(
            box,
            f"LEFT_CENTER - {len(vertices)} vertex(es) (RED)",
            vertices=vertices,
            cardinal_label=cardinal.name,
        )


def example_find_vertex_top_front_right() -> None:
    """Find vertex at TOP_FRONT_RIGHT corner."""
    print("\n--- find_vertex: TOP_FRONT_RIGHT ---")
    box = _create_box()
    cardinal = CardinalDirection.TOP_FRONT_RIGHT
    vertices = find_vertex(box, cardinal)
    print(f"  Found {len(vertices)} vertex(es)")
    for i, v in enumerate(vertices):
        print(f"    {i+1}. ({v.x}, {v.y}, {v.z})")
    if vertices:
        _visualize(
            box,
            f"TOP_FRONT_RIGHT - {len(vertices)} vertex(es) (RED)",
            vertices=vertices,
            cardinal_label=cardinal.name,
        )


def example_find_vertex_bottom_back_left() -> None:
    """Find vertex at BOTTOM_BACK_LEFT corner."""
    print("\n--- find_vertex: BOTTOM_BACK_LEFT ---")
    box = _create_box()
    cardinal = CardinalDirection.BOTTOM_BACK_LEFT
    vertices = find_vertex(box, cardinal)
    print(f"  Found {len(vertices)} vertex(es)")
    for i, v in enumerate(vertices):
        print(f"    {i+1}. ({v.x}, {v.y}, {v.z})")
    if vertices:
        _visualize(
            box,
            f"BOTTOM_BACK_LEFT - {len(vertices)} vertex(es) (RED)",
            vertices=vertices,
            cardinal_label=cardinal.name,
        )


def example_find_vertex_from_string() -> None:
    """Find vertex using from_string() method."""
    print("\n--- find_vertex: Using from_string('top-left') ---")
    box = _create_box()
    cardinal = CardinalDirection.from_string("top-left")
    vertices = find_vertex(box, cardinal)
    print(f"  Found {len(vertices)} vertex(es)")
    for i, v in enumerate(vertices):
        print(f"    {i+1}. ({v.x}, {v.y}, {v.z})")
    if vertices:
        _visualize(
            box,
            f"TOP_LEFT via from_string - {len(vertices)} vertex(es) (RED)",
            vertices=vertices,
            cardinal_label=cardinal.name,
        )


def example_find_edge_front_top() -> None:
    """Find edge at FRONT_TOP position."""
    print("\n--- find_edge: FRONT_TOP ---")
    box = _create_box()
    cardinal = CardinalDirection.FRONT_TOP
    edges = find_edge(box, cardinal)
    print(f"  Found {len(edges)} edge(s)")
    for i, e in enumerate(edges):
        print(
            f"    {i+1}. ({e.v1.x}, {e.v1.y}, {e.v1.z}) -> ({e.v2.x}, {e.v2.y}, {e.v2.z})"
        )
    if edges:
        _visualize(
            box,
            f"FRONT_TOP - {len(edges)} edge(s) (GREEN)",
            edges=edges,
            cardinal_label=cardinal.name,
        )


def example_find_edge_left() -> None:
    """Find edge at LEFT_CENTER position."""
    print("\n--- find_edge: LEFT_CENTER ---")
    box = _create_box()
    cardinal = CardinalDirection.LEFT_CENTER
    edges = find_edge(box, cardinal, search_radius="20mm")
    print(f"  Found {len(edges)} edge(s)")
    for i, e in enumerate(edges):
        print(
            f"    {i+1}. ({e.v1.x}, {e.v1.y}, {e.v1.z}) -> ({e.v2.x}, {e.v2.y}, {e.v2.z})"
        )
    if edges:
        _visualize(
            box,
            f"LEFT_CENTER - {len(edges)} edge(s) (GREEN)",
            edges=edges,
            cardinal_label=cardinal.name,
        )


def example_find_edge_left_back() -> None:
    """Find edge at LEFT_BACK position."""
    print("\n--- find_edge: LEFT_BACK ---")
    box = _create_box()
    cardinal = CardinalDirection.LEFT_BACK
    edges = find_edge(box, cardinal, search_radius="20mm")
    print(f"  Found {len(edges)} edge(s)")
    for i, e in enumerate(edges):
        print(
            f"    {i+1}. ({e.v1.x}, {e.v1.y}, {e.v1.z}) -> ({e.v2.x}, {e.v2.y}, {e.v2.z})"
        )
    if edges:
        _visualize(
            box,
            f"LEFT_BACK - {len(edges)} edge(s) (GREEN)",
            edges=edges,
            cardinal_label=cardinal.name,
        )


def example_find_edge_bottom_right() -> None:
    """Find edge at BOTTOM_RIGHT position."""
    print("\n--- find_edge: BOTTOM_RIGHT ---")
    box = _create_box()
    cardinal = CardinalDirection.BOTTOM_RIGHT
    edges = find_edge(box, cardinal)
    print(f"  Found {len(edges)} edge(s)")
    for i, e in enumerate(edges):
        print(
            f"    {i+1}. ({e.v1.x}, {e.v1.y}, {e.v1.z}) -> ({e.v2.x}, {e.v2.y}, {e.v2.z})"
        )
    if edges:
        _visualize(
            box,
            f"BOTTOM_RIGHT - {len(edges)} edge(s) (GREEN)",
            edges=edges,
            cardinal_label=cardinal.name,
        )


def example_find_face_top() -> None:
    """Find face at TOP_CENTER position."""
    print("\n--- find_face: TOP_CENTER ---")
    box = _create_box()
    cardinal = CardinalDirection.TOP_CENTER
    faces = find_face(box, cardinal)
    print(f"  Found {len(faces)} face(s)")
    for i, f in enumerate(faces):
        sub_count = len(f.sub_edges) if f.sub_edges else 0
        print(f"    {i+1}. Face with {sub_count} boundary edges")
        if f.get_native("face"):
            print(f"       Native type: {type(f.get_native('face')).__name__}")
    if faces:
        _visualize(
            box,
            f"TOP_CENTER - {len(faces)} face(s) (BLUE)",
            faces=faces,
            cardinal_label=cardinal.name,
        )


def example_find_face_front() -> None:
    """Find face at FRONT_CENTER position."""
    print("\n--- find_face: FRONT_CENTER ---")
    box = _create_box()
    cardinal = CardinalDirection.FRONT_CENTER
    faces = find_face(box, cardinal)
    print(f"  Found {len(faces)} face(s)")
    for i, f in enumerate(faces):
        sub_count = len(f.sub_edges) if f.sub_edges else 0
        print(f"    {i+1}. Face with {sub_count} boundary edges")
    if faces:
        _visualize(
            box,
            f"FRONT_CENTER - {len(faces)} face(s) (BLUE)",
            faces=faces,
            cardinal_label=cardinal.name,
        )


def example_find_face_right() -> None:
    """Find face at RIGHT_CENTER position."""
    print("\n--- find_face: RIGHT_CENTER ---")
    box = _create_box()
    faces = find_face(box, CardinalDirection.RIGHT_CENTER)
    print(f"  Found {len(faces)} face(s)")
    for i, f in enumerate(faces):
        sub_count = len(f.sub_edges) if f.sub_edges else 0
        print(f"    {i+1}. Face with {sub_count} boundary edges")
    if faces:
        _visualize(box, f"RIGHT_CENTER - {len(faces)} face(s) (BLUE)", faces=faces)


def example_find_shape_small_radius() -> None:
    """Find elements at TOP_FRONT_RIGHT with small search radius."""
    print("\n--- find_shape: TOP_FRONT_RIGHT (5mm radius) ---")
    box = _create_box()
    shapes = find_shape(box, CardinalDirection.TOP_FRONT_RIGHT, search_radius="5mm")
    print(f"  Found {len(shapes)} element(s):")
    for i, s in enumerate(shapes[:5]):
        print(f"    {i+1}. {type(s).__name__}")

    found_vertices = [s for s in shapes if isinstance(s, Vertex)]
    found_edges = [s for s in shapes if isinstance(s, Edge)]
    _visualize(box, "TOP_FRONT_RIGHT (5mm)", vertices=found_vertices, edges=found_edges)


def example_find_shape_center() -> None:
    """Find elements at CENTER with small search radius (includes solid)."""
    print("\n--- find_shape: CENTER (5mm radius) ---")
    box = _create_box()
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="5mm")
    print(f"  Found {len(shapes)} element(s):")
    for s in shapes:
        print(f"    - {type(s).__name__}")

    found_vertices = [s for s in shapes if isinstance(s, Vertex)]
    found_edges = [s for s in shapes if isinstance(s, Edge)]
    _visualize(
        box, "CENTER (5mm) - includes Solid", vertices=found_vertices, edges=found_edges
    )


def example_find_shape_large_radius() -> None:
    """Find all elements with large search radius."""
    print("\n--- find_shape: CENTER (100mm radius - all elements) ---")
    box = _create_box()
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="100mm")
    type_counts: dict[str, int] = {}
    for s in shapes:
        t = type(s).__name__
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  Found {len(shapes)} element(s)")
    print(f"  Type counts: {type_counts}")

    found_vertices = [s for s in shapes if isinstance(s, Vertex)][:4]
    found_edges = [s for s in shapes if isinstance(s, Edge)][:4]
    _visualize(
        box, "All elements (100mm radius)", vertices=found_vertices, edges=found_edges
    )


def example_offset_basic() -> None:
    """Demonstrate basic offset() with Point."""
    print("\n--- offset: Basic usage with Point ---")
    box = _create_box()

    # offset() now takes a Point for 3D offset
    desc1 = offset(CardinalDirection.TOP_LEFT, Point(x="5mm", y=0, z=0))
    print(f"  offset(TOP_LEFT, Point(x='5mm')) = '{desc1}'")

    desc2 = offset(CardinalDirection.CENTER, Point(x=0, y=0, z="10mm"))
    print(f"  offset(CENTER, Point(z='10mm')) = '{desc2}'")

    desc3 = offset(CardinalDirection.BOTTOM_FRONT, Point(x="2mm", y="3mm", z="1mm"))
    print(f"  offset(BOTTOM_FRONT, Point(x='2mm', y='3mm', z='1mm')) = '{desc3}'")

    # Find vertex at TOP_LEFT and visualize
    vertices = find_vertex(box, CardinalDirection.TOP_LEFT)
    if vertices:
        _visualize(box, "TOP_LEFT with offset descriptor", vertices=[vertices[0]])


def example_offset_face_directions() -> None:
    """Demonstrate offset() for all face directions."""
    print("\n--- offset: Face directions with Point offsets ---")
    box = _create_box()

    face_directions = [
        CardinalDirection.TOP_CENTER,
        CardinalDirection.BOTTOM_CENTER,
        CardinalDirection.FRONT_CENTER,
        CardinalDirection.BACK_CENTER,
        CardinalDirection.LEFT_CENTER,
        CardinalDirection.RIGHT_CENTER,
    ]

    print("  Offset descriptors for cube faces:")
    for direction in face_directions:
        desc = offset(direction, Point(x="3mm", y="3mm", z="3mm"))
        print(f"    {desc}")

    # Find and visualize the TOP face
    faces = find_face(box, CardinalDirection.TOP_CENTER)
    if faces:
        _visualize(box, "TOP_CENTER face with offset", faces=[faces[0]])


def example_offset_with_selectors() -> None:
    """Use offset() with selectors to find elements."""
    print("\n--- offset: Combined with selectors ---")
    box = _create_box()

    # Create offset descriptor
    desc = offset(CardinalDirection.TOP_FRONT_RIGHT, Point(x="1mm", y="1mm", z="1mm"))
    print(f"  Using offset: {desc}")

    # Find vertex at the cardinal direction
    vertices = find_vertex(box, CardinalDirection.TOP_FRONT_RIGHT)
    edges = find_edge(box, CardinalDirection.TOP_RIGHT)

    if vertices:
        v = vertices[0]
        print(f"  Found vertex at: ({v.x}, {v.y}, {v.z})")

    if edges:
        e = edges[0]
        print(
            f"  Found edge: ({e.v1.x}, {e.v1.y}, {e.v1.z}) -> ({e.v2.x}, {e.v2.y}, {e.v2.z})"
        )

    _visualize(
        box,
        "TOP_FRONT_RIGHT with selectors",
        vertices=vertices[:1] if vertices else [],
        edges=edges[:1] if edges else [],
    )


def main() -> None:
    """Run all tutorial examples with independent visualization."""
    print("=" * 60)
    print("TOPOLOGY SELECTORS TUTORIAL")
    print("=" * 60)
    print("\nThis tutorial demonstrates topology selectors and offset functions.")
    print("Each sub-example is visualized independently.")
    print("\nClose each visualization window to continue to the next example.")

    # find_vertex examples
    print("\n" + "=" * 60)
    print("SECTION 1: find_vertex()")
    print("=" * 60)
    example_find_vertex_left_center()
    example_find_vertex_top_front_right()
    example_find_vertex_bottom_back_left()
    example_find_vertex_from_string()

    # find_edge examples
    print("\n" + "=" * 60)
    print("SECTION 2: find_edge()")
    print("=" * 60)
    example_find_edge_front_top()
    example_find_edge_left()
    example_find_edge_left_back()
    example_find_edge_bottom_right()

    # find_face examples
    print("\n" + "=" * 60)
    print("SECTION 3: find_face()")
    print("=" * 60)
    example_find_face_top()
    example_find_face_front()
    example_find_face_right()

    # find_shape examples
    print("\n" + "=" * 60)
    print("SECTION 4: find_shape()")
    print("=" * 60)
    example_find_shape_small_radius()
    example_find_shape_center()
    example_find_shape_large_radius()

    # offset examples
    print("\n" + "=" * 60)
    print("SECTION 5: offset()")
    print("=" * 60)
    example_offset_basic()
    example_offset_face_directions()
    example_offset_with_selectors()

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
