"""
Tutorial: Transform Operations

This tutorial demonstrates how to use the transform functions to translate,
rotate, and scale 3D objects.

Each example shows a before (gray) and after (green) visualization overlaid
to clearly see the effect of the transformation.

Close each visualization window to continue to the next example.
"""

import os
import tempfile
from platform import system

import numpy as np
import open3d as o3d

from codetocad.cli.config import get_temp_stl_export_path
from codetocad.core.cad.vertex_edge_solid import Edge, Solid, Vertex
from codetocad.core.enums import CardinalDirection
from codetocad.integrations.build123d.cad import Shape
from codetocad.integrations.build123d.cad.selectors import (
    find_edge,
    find_face,
    find_vertex,
)
from codetocad.integrations.build123d.cad.shape import export_file
from codetocad.integrations.build123d.cad.transform import (
    rotate,
    scale,
    scale_uniform,
    translate,
)

if system() != "Darwin":
    from open3d.web_visualizer import draw
else:
    from open3d.visualization import draw


def _create_box() -> Solid:
    """Create a simple 20x20x20 box centered at origin."""
    center = Vertex(x=0, y=0, z=0)
    return Shape.cuboid(center, width=20, height=20, depth=20)


def _create_coordinate_frame(
    origin: "tuple[float, float, float]",
    size: float = 15.0,
    radius: float = 0.5,
) -> "list[o3d.geometry.TriangleMesh]":
    """Create coordinate frame axes (X=red, Y=green, Z=blue) at the given origin."""
    geometries = []
    ox, oy, oz = origin

    axis_colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
    axis_directions = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]

    for color, direction in zip(axis_colors, axis_directions):
        cylinder = o3d.geometry.TriangleMesh.create_cylinder(
            radius=radius, height=size * 0.85
        )
        cone = o3d.geometry.TriangleMesh.create_cone(
            radius=radius * 2.5, height=size * 0.15
        )

        z_axis = np.array([0, 0, 1])
        if not np.allclose(direction, z_axis):
            rotation_axis = np.cross(z_axis, direction)
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            angle = np.arccos(np.dot(z_axis, direction))
            rotation_matrix = o3d.geometry.get_rotation_matrix_from_axis_angle(
                rotation_axis * angle
            )
            cylinder.rotate(rotation_matrix, center=[0, 0, 0])
            cone.rotate(rotation_matrix, center=[0, 0, 0])

        cylinder.translate(np.array([ox, oy, oz]) + direction * (size * 0.85 / 2))
        cone.translate(
            np.array([ox, oy, oz]) + direction * (size * 0.85 + size * 0.15 / 2)
        )

        cylinder.paint_uniform_color(list(color))
        cone.paint_uniform_color(list(color))
        cylinder.compute_vertex_normals()
        cone.compute_vertex_normals()

        geometries.append(cylinder)
        geometries.append(cone)

    return geometries


def _visualize_transform(before: Solid, after: Solid, title: str) -> None:
    """Visualize before (gray) and after (green) transform overlaid."""
    print(f"\n  Visualizing: {title}")
    print("    Gray = Before, Green = After")
    print("    Coordinate frame: X=Red, Y=Green, Z=Blue")

    # Export and load "before" mesh (gray)
    export_file(before, str(get_temp_stl_export_path()))
    mesh_before = o3d.io.read_triangle_mesh(str(get_temp_stl_export_path()))
    mesh_before.paint_uniform_color([0.5, 0.5, 0.5])  # Gray
    mesh_before.compute_vertex_normals()

    # Export and load "after" mesh (green)
    after_path = os.path.join(tempfile.gettempdir(), "codetocad_after.stl")
    export_file(after, after_path)
    mesh_after = o3d.io.read_triangle_mesh(after_path)
    mesh_after.paint_uniform_color([0.2, 0.8, 0.2])  # Green
    mesh_after.compute_vertex_normals()

    # Create coordinate frame outside the bounding box
    bbox = mesh_before.get_axis_aligned_bounding_box()
    min_bound = bbox.get_min_bound()
    frame_origin = (min_bound[0] - 10, min_bound[1] - 10, min_bound[2] - 10)
    frame_geoms = _create_coordinate_frame(frame_origin, size=15.0, radius=0.5)

    draw([mesh_before, mesh_after] + frame_geoms)


def _get_coord_value(val) -> float:
    """Extract float value from a coordinate."""
    from codetocad.core.dimensions.length_expression import LengthExp

    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, LengthExp):
        return float(val.value) * 1000  # Convert meters to mm
    if hasattr(val, "value"):
        return float(val.value)
    return float(val)


def _create_vertex_sphere(
    vertex: Vertex, color: "tuple[float, float, float]", radius: float = 1.5
) -> o3d.geometry.TriangleMesh:
    """Create a sphere at a vertex position."""
    x = _get_coord_value(vertex.x)
    y = _get_coord_value(vertex.y)
    z = _get_coord_value(vertex.z)
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    sphere.translate([x, y, z])
    sphere.paint_uniform_color(list(color))
    sphere.compute_vertex_normals()
    return sphere


def _create_edge_cylinder(
    edge: Edge, color: "tuple[float, float, float]", radius: float = 0.8
) -> o3d.geometry.TriangleMesh:
    """Create a cylinder along an edge."""
    import numpy as np

    x1 = _get_coord_value(edge.v1.x)
    y1 = _get_coord_value(edge.v1.y)
    z1 = _get_coord_value(edge.v1.z)
    x2 = _get_coord_value(edge.v2.x)
    y2 = _get_coord_value(edge.v2.y)
    z2 = _get_coord_value(edge.v2.z)

    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    direction = p2 - p1
    length = np.linalg.norm(direction)

    if length < 1e-6:
        return o3d.geometry.TriangleMesh()

    cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=length)
    cylinder.translate([0, 0, length / 2])

    # Align cylinder with edge direction
    z_axis = np.array([0, 0, 1])
    direction_normalized = direction / length
    rotation_axis = np.cross(z_axis, direction_normalized)
    rotation_axis_norm = np.linalg.norm(rotation_axis)

    if rotation_axis_norm > 1e-6:
        rotation_axis = rotation_axis / rotation_axis_norm
        angle = np.arccos(np.clip(np.dot(z_axis, direction_normalized), -1.0, 1.0))
        K = np.array(
            [
                [0, -rotation_axis[2], rotation_axis[1]],
                [rotation_axis[2], 0, -rotation_axis[0]],
                [-rotation_axis[1], rotation_axis[0], 0],
            ]
        )
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        cylinder.rotate(R, center=[0, 0, 0])
    elif np.dot(z_axis, direction_normalized) < 0:
        cylinder.rotate(
            o3d.geometry.get_rotation_matrix_from_xyz([np.pi, 0, 0]), center=[0, 0, 0]
        )

    cylinder.translate(p1)
    cylinder.paint_uniform_color(list(color))
    cylinder.compute_vertex_normals()
    return cylinder


def _visualize_element_transform(
    box: Solid,
    before_vertices: "list[Vertex] | None" = None,
    after_vertices: "list[Vertex] | None" = None,
    before_edges: "list[Edge] | None" = None,
    after_edges: "list[Edge] | None" = None,
    title: str = "",
) -> None:
    """Visualize element transforms with before (red) and after (green) markers."""
    print(f"\n  Visualizing: {title}")
    print("    Red = Before, Green = After")
    print("    Coordinate frame: X=Red, Y=Green, Z=Blue")

    geometries = []

    # Export and load box mesh (gray)
    export_file(box, str(get_temp_stl_export_path()))
    mesh = o3d.io.read_triangle_mesh(str(get_temp_stl_export_path()))
    mesh.paint_uniform_color([0.5, 0.5, 0.5])
    mesh.compute_vertex_normals()
    geometries.append(mesh)

    # Add coordinate frame outside the bounding box
    bbox = mesh.get_axis_aligned_bounding_box()
    min_bound = bbox.get_min_bound()
    frame_origin = (min_bound[0] - 10, min_bound[1] - 10, min_bound[2] - 10)
    frame_geoms = _create_coordinate_frame(frame_origin, size=15.0, radius=0.5)
    geometries.extend(frame_geoms)

    # Add before vertices (red)
    RED = (1.0, 0.0, 0.0)
    GREEN = (0.2, 0.8, 0.2)

    if before_vertices:
        for v in before_vertices:
            geometries.append(_create_vertex_sphere(v, RED))

    # Add after vertices (green)
    if after_vertices:
        for v in after_vertices:
            geometries.append(_create_vertex_sphere(v, GREEN))

    # Add before edges (red)
    if before_edges:
        for e in before_edges:
            geometries.append(_create_edge_cylinder(e, RED))

    # Add after edges (green)
    if after_edges:
        for e in after_edges:
            geometries.append(_create_edge_cylinder(e, GREEN))

    draw(geometries)


def example_translate_solid() -> None:
    """Translate a solid and show before/after overlay."""
    print("\n--- transform: Translate solid ---")
    box = _create_box()
    print("  Original box: centered at origin (20x20x20)")

    translated = translate(box, x="15mm", y="10mm", z="5mm")
    assert isinstance(translated, Solid)
    print("  Translated by: x=15mm, y=10mm, z=5mm")

    _visualize_transform(box, translated, "Translate solid (gray=before, green=after)")


def example_rotate_solid() -> None:
    """Rotate a solid and show before/after overlay."""
    print("\n--- transform: Rotate solid ---")
    box = _create_box()
    print("  Original box: centered at origin")

    rotated = rotate(box, z="45deg")
    assert isinstance(rotated, Solid)
    print("  Rotated by: 45 degrees around Z axis")

    _visualize_transform(
        box, rotated, "Rotate solid 45° around Z (gray=before, green=after)"
    )


def example_scale_solid() -> None:
    """Scale a solid and show before/after overlay."""
    print("\n--- transform: Scale solid ---")
    box = _create_box()
    print("  Original box: 20x20x20")

    scaled = scale(box, x=1.5, y=1.0, z=0.5)
    assert isinstance(scaled, Solid)
    print("  Scaled by: x=1.5, y=1.0, z=0.5")
    print("  Result: 30x20x10")

    _visualize_transform(
        box, scaled, "Scale solid x=1.5, z=0.5 (gray=before, green=after)"
    )


def example_scale_uniform() -> None:
    """Scale a solid uniformly and show before/after overlay."""
    print("\n--- transform: Scale uniform ---")
    box = _create_box()
    print("  Original box: 20x20x20")

    scaled = scale_uniform(box, factor=1.5)
    assert isinstance(scaled, Solid)
    print("  Scaled uniformly by factor 1.5")
    print("  Result: 30x30x30")

    _visualize_transform(box, scaled, "Scale uniform 1.5x (gray=before, green=after)")


def example_combined() -> None:
    """Apply multiple transforms and show before/after overlay."""
    print("\n--- transform: Combined transforms ---")
    box = _create_box()
    print("  Original box: centered at origin")

    step1 = rotate(box, z="30deg")
    assert isinstance(step1, Solid)
    step2 = translate(step1, x="20mm", y="0mm", z="10mm")
    assert isinstance(step2, Solid)
    final = scale_uniform(step2, factor=0.8)
    assert isinstance(final, Solid)
    print("  1. Rotate 30° around Z")
    print("  2. Translate x=20mm, z=10mm")
    print("  3. Scale uniformly by 0.8")

    _visualize_transform(box, final, "Combined transforms (gray=before, green=after)")


# =============================================================================
# SECTION 2: Transform Queried Elements
# =============================================================================


def example_transform_vertex() -> None:
    """Query a vertex and transform it, showing before and after."""
    print("\n--- transform: Query and transform vertex ---")
    box = _create_box()
    print("  Created 20x20x20 box centered at origin")

    # Query the top-front-right vertex
    vertices = find_vertex(box, CardinalDirection.TOP_FRONT_RIGHT)
    if not vertices:
        print("  ERROR: No vertex found at TOP_FRONT_RIGHT")
        return

    original_vertex = vertices[0]
    print(
        f"  Found vertex at TOP_FRONT_RIGHT: "
        f"({_get_coord_value(original_vertex.x):.1f}, "
        f"{_get_coord_value(original_vertex.y):.1f}, "
        f"{_get_coord_value(original_vertex.z):.1f})"
    )

    # Translate the vertex
    translated = translate(original_vertex, x="10mm", y="5mm", z="3mm")
    assert isinstance(translated, Vertex)
    print(
        f"  Translated vertex to: "
        f"({_get_coord_value(translated.x):.1f}, "
        f"{_get_coord_value(translated.y):.1f}, "
        f"{_get_coord_value(translated.z):.1f})"
    )

    _visualize_element_transform(
        box,
        before_vertices=[original_vertex],
        after_vertices=[translated],
        title="Transform vertex (red=before, green=after)",
    )


def example_transform_edge() -> None:
    """Query an edge and transform it, showing before and after."""
    print("\n--- transform: Query and transform edge ---")
    box = _create_box()
    print("  Created 20x20x20 box centered at origin")

    # Query the front-top edge
    # Use a search radius large enough to include both endpoints of the edge
    edges = find_edge(box, CardinalDirection.FRONT_TOP, search_radius="15mm")
    if not edges:
        print("  ERROR: No edge found at FRONT_TOP")
        return

    original_edge = edges[0]
    print(
        f"  Found edge at FRONT_TOP: "
        f"({_get_coord_value(original_edge.v1.x):.1f}, {_get_coord_value(original_edge.v1.y):.1f}, "
        f"{_get_coord_value(original_edge.v1.z):.1f}) -> "
        f"({_get_coord_value(original_edge.v2.x):.1f}, {_get_coord_value(original_edge.v2.y):.1f}, "
        f"{_get_coord_value(original_edge.v2.z):.1f})"
    )

    # Translate the edge
    translated = translate(original_edge, x="0mm", y="5mm", z="10mm")
    assert isinstance(translated, Edge)
    print("  Translated edge by: y=5mm, z=10mm")

    _visualize_element_transform(
        box,
        before_edges=[original_edge],
        after_edges=[translated],
        title="Transform edge (red=before, green=after)",
    )


def example_transform_face() -> None:
    """Query a face and transform it, showing before and after."""
    print("\n--- transform: Query and transform face ---")
    box = _create_box()
    print("  Created 20x20x20 box centered at origin")

    # Query the top face
    faces = find_face(box, CardinalDirection.TOP_CENTER)
    if not faces:
        print("  ERROR: No face found at TOP_CENTER")
        return

    original_face = faces[0]
    print("  Found face at TOP_CENTER")

    # Get face boundary edges for visualization
    original_edges = (
        original_face.sub_edges if original_face.sub_edges else [original_face]
    )

    # Translate the face
    translated = translate(original_face, x="0mm", y="0mm", z="15mm")
    assert isinstance(translated, Edge)
    print("  Translated face by: z=15mm")

    # Get translated boundary edges
    translated_edges = translated.sub_edges if translated.sub_edges else [translated]

    _visualize_element_transform(
        box,
        before_edges=original_edges,
        after_edges=translated_edges,
        title="Transform face (red=before, green=after)",
    )


def main() -> None:
    """Run all transform tutorial examples."""
    print("=" * 60)
    print("TRANSFORM OPERATIONS TUTORIAL")
    print("=" * 60)
    print("\nThis tutorial demonstrates transform operations on 3D objects.")
    print("Each example shows before (gray) and after (green) overlaid.")
    print("\nClose each visualization window to continue to the next example.")

    print("\n" + "-" * 60)
    print("SECTION 1: Transform Solids")
    print("-" * 60)
    example_translate_solid()
    example_rotate_solid()
    example_scale_solid()
    example_scale_uniform()
    example_combined()

    print("\n" + "-" * 60)
    print("SECTION 2: Transform Queried Elements")
    print("-" * 60)
    example_transform_vertex()
    example_transform_edge()
    example_transform_face()

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
