"""
Example 2: Plate with Hole
A rectangular box, but with a hole added.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#plate-with-hole
"""

import build123d as bd


from codetocad.core import Solid, Vertex
from codetocad.integrations.build123d import Shape
from codetocad.integrations.open3d import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    ex2 = bd.Box(length, width, thickness)
    ex2 -= bd.Cylinder(center_hole_dia / 2, height=thickness)
    return ex2


def main() -> Solid:
    """CodeToCAD implementation using Shape class."""
    length, width, thickness = 80.0, 60.0, 10.0
    center_hole_dia = 22.0

    # Create a cuboid centered at origin
    center = Vertex(x=0, y=0, z=0)
    box = Shape.cuboid(center, width=length, height=width, depth=thickness)

    # Create a cylinder for the hole
    hole = Shape.cylinder(center, radius=center_hole_dia / 2, height=thickness)

    # Subtract the hole from the box
    result = Shape.subtract(box, hole)

    return result


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.get_native().volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)
