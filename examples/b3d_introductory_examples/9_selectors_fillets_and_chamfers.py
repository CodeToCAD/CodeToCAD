"""
Example 9: Selectors, Fillets, and Chamfers
This example introduces chamfer() and fillet() which can "bevel" and "round" edges.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#selectors-fillets-and-chamfers
"""

import build123d as bd


from codetocad.core import Solid, Vertex, Axis
from codetocad.integrations.build123d import Shape
from codetocad.integrations.open3d import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0

    ex9 = bd.Part() + bd.Box(length, width, thickness)
    ex9 = bd.chamfer(ex9.edges().group_by(bd.Axis.Z)[-1], length=4)
    ex9 = bd.fillet(ex9.edges().filter_by(bd.Axis.Z), radius=5)
    return ex9


def main() -> Solid:
    """CodeToCAD implementation using Shape class."""
    length, width, thickness = 80.0, 60.0, 10.0

    # Create the box
    center = Vertex(x=0, y=0, z=0)
    box = Shape.cuboid(center, width=length, height=width, depth=thickness)

    # Get top edges (highest Z group) and apply chamfer
    top_edges = Shape.edges(box, group_axis=Axis.Z, group_index=-1)
    box = Shape.chamfer(box, length=4, edges=top_edges)

    # Get vertical edges (parallel to Z axis) and apply fillet
    vertical_edges = Shape.edges(box, filter_axis=Axis.Z)
    box = Shape.fillet(box, radius=5, edges=vertical_edges)

    return box


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.get_native().volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)
