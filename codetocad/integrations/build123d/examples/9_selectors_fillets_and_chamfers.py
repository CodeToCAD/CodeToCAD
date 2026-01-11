"""
Example 9: Selectors, Fillets, and Chamfers
This example introduces chamfer() and fillet() which can "bevel" and "round" edges.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#selectors-fillets-and-chamfers
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Vertex, Solid
from codetocad.integrations.build123d.cad import Shape
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0

    ex9 = bd.Part() + bd.Box(length, width, thickness)
    ex9 = bd.chamfer(ex9.edges().group_by(bd.Axis.Z)[-1], length=4)
    ex9 = bd.fillet(ex9.edges().filter_by(bd.Axis.Z), radius=5)
    return ex9


def main() -> Solid:
    """CodeToCAD implementation using Shape class.

    Note: For fillet and chamfer, we need to work with the native
    build123d objects since edge selection requires the solid context.
    """
    length, width, thickness = 80.0, 60.0, 10.0

    # Create the box
    center = Vertex(x=0, y=0, z=0)
    box = Shape.cuboid(center, width=length, height=width, depth=thickness)

    # Get native part for edge operations
    native_part = box.native

    # Apply chamfer to top edges (highest Z group)
    native_part = bd.chamfer(native_part.edges().group_by(bd.Axis.Z)[-1], length=4)

    # Apply fillet to vertical edges (filtered by Z axis)
    native_part = bd.fillet(native_part.edges().filter_by(bd.Axis.Z), radius=5)

    # Wrap result back in Solid
    result = Solid(is_hidden=False)
    result.native = native_part

    return result


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.native.volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)

