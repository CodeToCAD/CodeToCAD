"""
Example 5: Moving the current working point
Using Locations/Positions we can place objects at different places.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#moving-the-current-working-point
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex
from codetocad.integrations.build123d.cad import Shape, Draw
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    a, b, c, d = 90, 45, 15, 7.5

    sk5 = bd.Circle(a) - bd.Pos(b, 0.0) * bd.Rectangle(c, c) - bd.Pos(0.0, b) * bd.Circle(d)
    ex5 = bd.extrude(sk5, c)
    return ex5


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    a, b, c, d = 90, 45, 15, 7.5

    center = Vertex(x=0, y=0, z=0)

    # Create main circle
    main_circle = Draw.circle(center, radius=a)

    # Create rectangle at offset position
    rect_center = Vertex(x=b, y=0.0, z=0)
    rect = Draw.rectangle(rect_center, width=c, height=c)

    # Create small circle at offset position
    small_circle_center = Vertex(x=0.0, y=b, z=0)
    small_circle = Draw.circle(small_circle_center, radius=d)

    # Extrude each and perform subtractions
    main_solid = Shape.extrude(main_circle, height=c)
    rect_solid = Shape.extrude(rect, height=c)
    small_circle_solid = Shape.extrude(small_circle, height=c)

    result = Shape.subtract(main_solid, rect_solid)
    result = Shape.subtract(result, small_circle_solid)

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

