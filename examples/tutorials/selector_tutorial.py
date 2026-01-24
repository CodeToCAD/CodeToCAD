"""
Tutorial: Topology Selectors

This tutorial demonstrates how to use the topology selector functions to find
vertices, edges, and faces in 3D objects based on cardinal directions.

The selectors work by calculating a target position from a CardinalDirection
and the object's bounding box, then finding geometry elements within a search
radius of that position.
"""

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex
from codetocad.core.enums import CardinalDirection
from codetocad.integrations.build123d.cad import Shape
from codetocad.integrations.build123d.cad.selectors import (
    find_vertex,
    find_edge,
    find_face,
    find_shape,
)
from codetocad.integrations.open3d import show_in_open3d


def main() -> Solid:
    """Demonstrate all four selector functions."""
    # Create a simple 20x20x20 box centered at origin
    center = Vertex(x=0, y=0, z=0)
    box = Shape.cuboid(center, width=20, height=20, depth=20)

    print("=" * 60)
    print("TOPOLOGY SELECTORS TUTORIAL")
    print("=" * 60)
    print("\nCreated a 20x20x20 box centered at origin\n")

    # =========================================================================
    # 1. find_vertex() - Find vertices at cardinal positions
    # =========================================================================
    print("-" * 60)
    print("1. FIND_VERTEX - Find vertices at cardinal positions")
    print("-" * 60)

    # Find the top-front-right corner vertex
    # Note: Shape.cuboid extrudes from z=0 upward, so box spans z=0 to z=20
    vertices = find_vertex(box, CardinalDirection.TOP_FRONT_RIGHT)
    if vertices:
        v = vertices[0]
        print(f"\n  TOP_FRONT_RIGHT vertex: ({v.x}, {v.y}, {v.z})")

    # Find the bottom-back-left corner vertex
    vertices = find_vertex(box, CardinalDirection.BOTTOM_BACK_LEFT)
    if vertices:
        v = vertices[0]
        print(f"\n  BOTTOM_BACK_LEFT vertex: ({v.x}, {v.y}, {v.z})")

    # Using from_string() to create CardinalDirection from string
    direction = CardinalDirection.from_string("top-left")
    vertices = find_vertex(box, direction)
    if vertices:
        v = vertices[0]
        print(f"\n  Using from_string('top-left'): ({v.x}, {v.y}, {v.z})")

    # =========================================================================
    # 2. find_edge() - Find edges at cardinal positions
    # =========================================================================
    print("\n" + "-" * 60)
    print("2. FIND_EDGE - Find edges at cardinal positions")
    print("-" * 60)

    # Find the top-front edge
    edges = find_edge(box, CardinalDirection.FRONT_TOP)
    if edges:
        e = edges[0]
        print(f"\n  FRONT_TOP edge:")
        print(f"    From: ({e.v1.x}, {e.v1.y}, {e.v1.z})")
        print(f"    To:   ({e.v2.x}, {e.v2.y}, {e.v2.z})")

    # Find the left-back edge
    edges = find_edge(box, CardinalDirection.LEFT_BACK)
    if edges:
        e = edges[0]
        print(f"\n  LEFT_BACK edge:")
        print(f"    From: ({e.v1.x}, {e.v1.y}, {e.v1.z})")
        print(f"    To:   ({e.v2.x}, {e.v2.y}, {e.v2.z})")

    # =========================================================================
    # 3. find_face() - Find faces at cardinal positions
    # =========================================================================
    print("\n" + "-" * 60)
    print("3. FIND_FACE - Find faces (returned as outer boundary Edge)")
    print("-" * 60)

    # Find the top face
    faces = find_face(box, CardinalDirection.TOP_CENTER)
    if faces:
        print(f"\n  TOP_CENTER: Found {len(faces)} face(s)")
        f = faces[0]
        print(f"    Outer wire boundary: ({f.v1.x}, {f.v1.y}, {f.v1.z})")
        # The original bd.Face is stored in native_parent_ref
        if f.native_parent_ref:
            print(f"    Native face available: {type(f.native_parent_ref).__name__}")

    # Find the front face
    faces = find_face(box, CardinalDirection.FRONT_CENTER)
    if faces:
        print(f"\n  FRONT_CENTER: Found {len(faces)} face(s)")

    # =========================================================================
    # 4. find_shape() - Find any topology element at cardinal positions
    # =========================================================================
    print("\n" + "-" * 60)
    print("4. FIND_SHAPE - Find any element (vertex, edge, or face boundary)")
    print("-" * 60)

    # Find any element at the top-front-right corner with custom search radius
    shapes = find_shape(box, CardinalDirection.TOP_FRONT_RIGHT, search_radius="5mm")
    print(f"\n  TOP_FRONT_RIGHT with 5mm radius:")
    print(f"    Found {len(shapes)} element(s)")
    for i, s in enumerate(shapes[:3]):  # Show first 3
        print(f"    {i+1}. {type(s).__name__}")

    # Find elements at the center (should find nothing for a solid box)
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="5mm")
    print(f"\n  CENTER with 5mm radius (inside solid, no geometry):")
    print(f"    Found {len(shapes)} element(s)")

    # Find elements with larger search radius to capture more
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="15mm")
    print(f"\n  CENTER with 15mm radius (larger, captures nearby geometry):")
    print(f"    Found {len(shapes)} element(s)")

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE")
    print("=" * 60)

    return box


if __name__ == "__main__":
    solid = main()
    # Uncomment to visualize:
    # show_in_open3d(solid)
