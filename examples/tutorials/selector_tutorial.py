"""
Tutorial: Topology Selectors

This tutorial demonstrates how to use the topology selector functions to find
vertices, edges, and faces in 3D objects based on cardinal directions.

The selectors work by calculating a target position from a CardinalDirection
and the object's bounding box, then finding geometry elements within a search
radius of that position.

Visualization: Found elements are marked with small spheres at vertex positions
and cylinders along edges to make them easier to identify.
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex, Edge
from codetocad.core.enums import CardinalDirection
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


def _get_coord(val) -> float:
    """Extract float value from a coordinate (handles both float and LengthType)."""
    if isinstance(val, (int, float)):
        return float(val)
    # Handle LengthType (could be LengthExp or str)
    if hasattr(val, "value"):
        return float(val.value)
    return float(val)


def create_vertex_marker(vertex: Vertex, radius: float = 0.5) -> "bd.Part":
    """Create a small sphere marker at a vertex position (for ocp_vscode)."""
    x = _get_coord(vertex.x)
    y = _get_coord(vertex.y)
    z = _get_coord(vertex.z)
    return bd.Sphere(radius).moved(bd.Location((x, y, z)))


def create_edge_marker(edge: Edge, radius: float = 0.3) -> "bd.Part":
    """Create a cylinder marker along an edge."""
    # Get edge endpoints as floats
    x1 = _get_coord(edge.v1.x)
    y1 = _get_coord(edge.v1.y)
    z1 = _get_coord(edge.v1.z)
    x2 = _get_coord(edge.v2.x)
    y2 = _get_coord(edge.v2.y)
    z2 = _get_coord(edge.v2.z)

    p1 = bd.Vector(x1, y1, z1)
    p2 = bd.Vector(x2, y2, z2)

    # Create a cylinder along the edge
    length = (p2 - p1).length
    if length < 0.001:
        # Degenerate edge, create a sphere instead
        return bd.Sphere(radius).moved(bd.Location((x1, y1, z1)))

    # Create cylinder at origin, then move and rotate to align with edge
    cyl = bd.Cylinder(radius, length)

    # Move to midpoint and align with edge direction
    midpoint = (p1 + p2) / 2
    direction = (p2 - p1).normalized()

    # Calculate rotation to align Z axis with edge direction
    z_axis = bd.Vector(0, 0, 1)
    if abs(direction.dot(z_axis)) < 0.9999:
        rotation_axis = z_axis.cross(direction)
        angle = z_axis.get_angle(direction)
        cyl = cyl.rotate(bd.Axis.Z, 0).rotate(bd.Axis((0, 0, 0), rotation_axis), angle)
    elif direction.Z < 0:
        # Edge is pointing down, flip the cylinder
        cyl = cyl.rotate(bd.Axis.X, 180)

    cyl = cyl.moved(bd.Location((midpoint.X, midpoint.Y, midpoint.Z)))
    return cyl


def main(visualize: bool = False) -> Solid:
    """Demonstrate all four selector functions with optional visualization.

    Args:
        visualize: If True, creates visual markers for found elements and
                   displays using ocp_vscode (if available).
    """
    # Create a simple 20x20x20 box centered at origin
    center = Vertex(x=0, y=0, z=0)
    box = Shape.cuboid(center, width=20, height=20, depth=20)

    print("=" * 60)
    print("TOPOLOGY SELECTORS TUTORIAL")
    print("=" * 60)
    print("\nCreated a 20x20x20 box centered at origin\n")

    # Collect markers for visualization (ocp_vscode)
    vertex_markers: "list[bd.Part]" = []
    edge_markers: "list[bd.Part]" = []

    # Collect found elements for colored visualization (Open3D)
    found_vertices: list[Vertex] = []
    found_edges: list[Edge] = []
    found_faces: list[Edge] = []  # Faces are returned as Edge boundaries

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
        if visualize:
            vertex_markers.append(create_vertex_marker(v, radius=1.0))
            found_vertices.append(v)

    # Find the bottom-back-left corner vertex
    vertices = find_vertex(box, CardinalDirection.BOTTOM_BACK_LEFT)
    if vertices:
        v = vertices[0]
        print(f"\n  BOTTOM_BACK_LEFT vertex: ({v.x}, {v.y}, {v.z})")
        if visualize:
            vertex_markers.append(create_vertex_marker(v, radius=1.0))
            found_vertices.append(v)

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
        if visualize:
            edge_markers.append(create_edge_marker(e, radius=0.5))
            found_edges.append(e)

    # Find the left-back edge
    edges = find_edge(box, CardinalDirection.LEFT_BACK)
    if edges:
        e = edges[0]
        print(f"\n  LEFT_BACK edge:")
        print(f"    From: ({e.v1.x}, {e.v1.y}, {e.v1.z})")
        print(f"    To:   ({e.v2.x}, {e.v2.y}, {e.v2.z})")
        if visualize:
            edge_markers.append(create_edge_marker(e, radius=0.5))
            found_edges.append(e)

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
        if visualize:
            found_faces.append(f)

    # Find the front face
    faces = find_face(box, CardinalDirection.FRONT_CENTER)
    if faces:
        print(f"\n  FRONT_CENTER: Found {len(faces)} face(s)")
        if visualize:
            found_faces.append(faces[0])

    # =========================================================================
    # 4. find_shape() - Find any element at cardinal positions
    # =========================================================================
    print("\n" + "-" * 60)
    print("4. FIND_SHAPE - Find any element (vertex, edge, solid)")
    print("-" * 60)

    # Find any element at the top-front-right corner with custom search radius
    shapes = find_shape(box, CardinalDirection.TOP_FRONT_RIGHT, search_radius="5mm")
    print(f"\n  TOP_FRONT_RIGHT with 5mm radius:")
    print(f"    Found {len(shapes)} element(s)")
    for i, s in enumerate(shapes[:3]):  # Show first 3
        print(f"    {i+1}. {type(s).__name__}")

    # Find elements at the center (now includes solid if within radius)
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="5mm")
    print(f"\n  CENTER with 5mm radius:")
    print(f"    Found {len(shapes)} element(s)")
    for s in shapes:
        print(f"    - {type(s).__name__}")

    # Find elements with larger search radius to capture all geometry
    shapes = find_shape(box, CardinalDirection.CENTER, search_radius="100mm")
    print(f"\n  CENTER with 100mm radius (captures all geometry):")
    print(f"    Found {len(shapes)} element(s)")
    # Count by type
    type_counts: dict[str, int] = {}
    for s in shapes:
        t = type(s).__name__
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"    Type counts: {type_counts}")

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE")
    print("=" * 60)

    # =========================================================================
    # Visualization (if enabled)
    # =========================================================================
    if visualize:
        print("\n" + "-" * 60)
        print("VISUALIZATION")
        print("-" * 60)

        # Get native box
        native_box = box.native_ref

        # Combine all markers (for ocp_vscode)
        all_markers = vertex_markers + edge_markers

        print(f"\n  Created {len(vertex_markers)} vertex markers (spheres)")
        print(f"  Created {len(edge_markers)} edge markers (cylinders)")

        # Collect colored elements for Open3D visualization
        colored_vertices = [ColoredVertex(vertex=v, color=RED) for v in found_vertices]
        colored_edges = [ColoredEdge(edge=e, color=GREEN) for e in found_edges]
        colored_faces = [ColoredFace(face=f, color=BLUE) for f in found_faces]

        try:
            from ocp_vscode import show

            print("\n  Showing in ocp_vscode viewer...")
            print("  - Box: gray")
            print("  - Vertex markers: spheres at found vertex positions")
            print("  - Edge markers: cylinders along found edges")

            # Show the box and all markers together
            show(native_box, *all_markers, reset_camera=True)

        except ImportError:
            print("\n  ocp_vscode not available. Install with: pip install ocp-vscode")
            print("  Using Open3D visualization with colored markers...")
            print("  - Box: gray")
            print("  - Vertices: RED spheres")
            print("  - Edges: GREEN cylinders")
            print("  - Faces: BLUE boundary cylinders")
            show_in_open3d(
                box,
                vertices=colored_vertices,
                edges=colored_edges,
                faces=colored_faces,
                vertex_radius=1.5,
                edge_radius=0.8,
            )

    return box


if __name__ == "__main__":
    # Set visualize=True to see markers for found elements
    solid = main(visualize=True)
