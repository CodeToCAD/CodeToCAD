"""
Example 3: An extruded prismatic solid
Build a prismatic solid using extrusion.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#an-extruded-prismatic-solid
"""

import build123d as bd


from codetocad.core import Solid, Vertex
from codetocad.integrations.build123d import Shape, Draw
from codetocad.integrations.open3d import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0

    sk3 = bd.Circle(width) - bd.Rectangle(length / 2, width / 2)
    ex3 = bd.extrude(sk3, amount=2 * thickness)
    return ex3


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    length, width, thickness = 80.0, 60.0, 10.0

    center = Vertex(x=0, y=0, z=0)

    # Create circle sketch
    circle_edge = Draw.circle(center, radius=width)

    # Create rectangle to subtract
    rect_edge = Draw.rectangle(center, width=length / 2, height=width / 2)

    # Extrude the circle
    circle_solid = Shape.extrude(circle_edge, height=2 * thickness)

    # Extrude the rectangle
    rect_solid = Shape.extrude(rect_edge, height=2 * thickness)

    # Subtract rectangle from circle
    result = Shape.subtract(circle_solid, rect_solid)

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
