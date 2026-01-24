"""
Example 8: Polylines
Polyline allows creating a shape from a large number of chained points.
This example uses a polyline to create one half of an i-beam shape.
https://build123d.readthedocs.io/en/latest/introductory_examples.html#polylines
"""

import build123d as bd

from codetocad.core.cad.vertex_edge_solid import Solid
from codetocad.core.enums.plane import Plane
from codetocad.integrations.build123d.cad import Shape, Draw
from codetocad.integrations.open3d.adapter.show import show_in_open3d


def original() -> bd.Part:
    """Original build123d algebra mode example."""
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    ln = bd.Polyline(pts)
    ln += bd.mirror(ln, bd.Plane.YZ)

    sk8 = bd.make_face(bd.Plane.YZ * ln)
    ex8 = bd.extrude(sk8, -L).clean()
    return ex8


def main() -> Solid:
    """CodeToCAD implementation using Shape and Draw classes."""
    (L, H, W, t) = (100.0, 20.0, 20.0, 1.0)
    pts = [
        (0, H / 2.0),
        (W / 2.0, H / 2.0),
        (W / 2.0, (H / 2.0 - t)),
        (t / 2.0, (H / 2.0 - t)),
        (t / 2.0, (t - H / 2.0)),
        (W / 2.0, (t - H / 2.0)),
        (W / 2.0, H / -2.0),
        (0, H / -2.0),
    ]

    # Create polyline using Draw class
    polyline = Draw.polyline(pts)

    # Mirror across YZ plane, union with original, and create face
    face = Draw.mirror(polyline, Plane.YZ, union=True, make_face=True, face_plane=Plane.YZ)

    # Extrude the face
    result = Shape.extrude(face, height=-L)

    return result


if __name__ == "__main__":
    original_part = original()
    main_solid = main()

    original_volume = original_part.volume
    main_volume = main_solid.native_ref.volume

    print(f"Original volume: {original_volume}")
    print(f"Main volume: {main_volume}")
    print(f"Volumes match: {abs(original_volume - main_volume) < 0.001}")

    show_in_open3d(main_solid)
