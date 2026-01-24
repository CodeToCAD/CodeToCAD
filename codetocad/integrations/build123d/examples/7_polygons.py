"""
Example 7: Polygons
You can create RegularPolygon for each stack point if you would like.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#polygons
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex
from codetocad.integrations.build123d.cad import Shape, Draw
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    a, b, c = 60, 80, 5

    polygons = [
        loc * bd.RegularPolygon(radius=2 * c, side_count=6)
        for loc in bd.Locations((0, 3 * c), (0, -3 * c))
    ]
    sk7 = bd.Rectangle(a, b) - polygons
    ex7 = bd.extrude(sk7, amount=c)
    return ex7


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    a, b, c = 60, 80, 5

    center = Vertex(x=0, y=0, z=0)

    # Create rectangle
    rect = Draw.rectangle(center, width=a, height=b)
    rect_solid = Shape.extrude(rect, height=c)

    # Create hexagons at offset positions and subtract
    positions = [(0, 3 * c), (0, -3 * c)]

    for x, y in positions:
        hex_center = Vertex(x=x, y=y, z=0)
        hexagon = Draw.polygon(hex_center, radius=2 * c, sides=6)
        hex_solid = Shape.extrude(hexagon, height=c)
        rect_solid = Shape.subtract(rect_solid, hex_solid)

    return rect_solid


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.native_ref.volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)
