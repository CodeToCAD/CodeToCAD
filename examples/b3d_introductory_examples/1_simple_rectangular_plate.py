"""
Example 1: Simple Rectangular Plate
Just about the simplest possible example, a rectangular Box.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#simple-rectangular-plate
"""

import build123d as bd

from codetocad.core import Solid, Vertex
from codetocad.integrations.build123d import Shape
from codetocad.integrations.open3d import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0
    ex1 = bd.Box(length, width, thickness)
    return ex1


def main() -> Solid:
    """CodeToCAD implementation using Shape class."""
    length, width, thickness = 80.0, 60.0, 10.0

    # Create a cuboid centered at origin
    center = Vertex(x=0, y=0, z=0)
    solid = Shape.cuboid(center, width=length, height=width, depth=thickness)

    return solid


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.native_ref.volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)
