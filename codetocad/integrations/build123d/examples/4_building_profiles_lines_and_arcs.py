"""
Example 4: Building Profiles using lines and arcs
Sometimes you need to build complex profiles using lines and arcs.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#building-profiles-using-lines-and-arcs
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid, Vertex, Edge
from codetocad.integrations.build123d.cad import Shape, Draw
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    length, width, thickness = 80.0, 60.0, 10.0

    lines = bd.Curve() + [
        bd.Line((0, 0), (length, 0)),
        bd.Line((length, 0), (length, width)),
        bd.ThreePointArc((length, width), (width, width * 1.5), (0.0, width)),
        bd.Line((0.0, width), (0, 0)),
    ]
    sk4 = bd.make_face(lines)
    ex4 = bd.extrude(sk4, thickness)
    return ex4


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    length, width, thickness = 80.0, 60.0, 10.0

    # Create lines for the profile
    v1 = Vertex(x=0, y=0, z=0)
    v2 = Vertex(x=length, y=0, z=0)
    v3 = Vertex(x=length, y=width, z=0)
    v4 = Vertex(x=0, y=width, z=0)

    line1 = Draw.line(v1, v2)
    line2 = Draw.line(v2, v3)
    arc = Draw.arc(v3, Vertex(x=width, y=width * 1.5, z=0), v4)
    line3 = Draw.line(v4, v1)
    edge = Edge(v1=v1, v2=v1, sub_edges=[line1, line2, arc, line3])

    result = Shape.extrude(edge, height=thickness)

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

