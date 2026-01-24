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

import open3d as o3d

from codetocad.cli.config import get_temp_stl_export_path
from codetocad.core.cad.vertex_edge_solid import Solid, Vertex
from codetocad.integrations.build123d.cad import Shape
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


def _visualize_transform(before: Solid, after: Solid, title: str) -> None:
    """Visualize before (gray) and after (green) transform overlaid."""
    print(f"\n  Visualizing: {title}")
    print("    Gray = Before, Green = After")

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

    draw([mesh_before, mesh_after])


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


def main() -> None:
    """Run all transform tutorial examples."""
    print("=" * 60)
    print("TRANSFORM OPERATIONS TUTORIAL")
    print("=" * 60)
    print("\nThis tutorial demonstrates transform operations on 3D objects.")
    print("Each example shows before (gray) and after (green) overlaid.")
    print("\nClose each visualization window to continue to the next example.")

    example_translate_solid()
    example_rotate_solid()
    example_scale_solid()
    example_scale_uniform()
    example_combined()

    print("\n" + "=" * 60)
    print("TUTORIAL COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
