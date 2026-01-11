"""
Example 6: Using Point Lists
Sometimes you need to create a number of features at various Locations.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#using-point-lists
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex
from codetocad.integrations.build123d.cad import Shape, Draw
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    a, b, c = 80, 60, 10

    sk6 = [loc * bd.Circle(c) for loc in bd.Locations((b, 0), (0, b), (-b, 0), (0, -b))]
    ex6 = bd.extrude(bd.Circle(a) - sk6, c)
    return ex6


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    a, b, c = 80, 60, 10

    center = Vertex(x=0, y=0, z=0)

    # Create main circle
    main_circle = Draw.circle(center, radius=a)
    main_solid = Shape.extrude(main_circle, height=c)

    # Create circles at each point location and subtract
    points = [(b, 0), (0, b), (-b, 0), (0, -b)]

    for x, y in points:
        hole_center = Vertex(x=x, y=y, z=0)
        hole_circle = Draw.circle(hole_center, radius=c)
        hole_solid = Shape.extrude(hole_circle, height=c)
        main_solid = Shape.subtract(main_solid, hole_solid)

    return main_solid


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.native.volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)

