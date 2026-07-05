"""Build123D gallery example: Vase.

https://build123d.readthedocs.io/en/stable/examples_1.html

A vase revolved from a line/arc/spline profile, hollowed through its top
opening and filleted. A custom CodeToCAD part overriding build_native().

Dimensions are in meters (CodeToCAD's base unit), hence the MM factor.
"""

import build123d as bd

from codetocad_integrations.build123d import Part3D

MM = 0.001


class Vase(Part3D):
    def build_native(self) -> bd.Part:
        l1 = bd.Line((0, 0), (12 * MM, 0))
        l2 = bd.RadiusArc(l1 @ 1, (15 * MM, 20 * MM), 50 * MM)
        l3 = bd.Spline(
            l2 @ 1,
            (22 * MM, 40 * MM),
            (20 * MM, 50 * MM),
            tangents=(l2 % 1, (-0.75, 1)),
        )
        l4 = bd.RadiusArc(l3 @ 1, l3 @ 1 + bd.Vector(0, 5 * MM), 5 * MM)
        l5 = bd.Spline(
            l4 @ 1,
            l4 @ 1 + bd.Vector(2.5 * MM, 2.5 * MM),
            l4 @ 1 + bd.Vector(0, 5 * MM),
            tangents=(l4 % 1, (-1, 0)),
        )
        outline = l1 + l2 + l3 + l4 + l5
        outline += bd.Polyline(
            l5 @ 1,
            l5 @ 1 + bd.Vector(0, 1 * MM),
            (0, (l5 @ 1).Y + 1 * MM),
            l1 @ 0,
        )

        profile = bd.make_face(outline.edges())
        vase = bd.revolve(profile, bd.Axis.Y)
        vase = bd.offset(
            vase, openings=vase.faces().sort_by(bd.Axis.Y).last, amount=-1 * MM
        )

        top_edges = (
            vase.edges()
            .filter_by(bd.GeomType.CIRCLE)
            .filter_by_position(bd.Axis.Y, 60 * MM, 62 * MM)
        )
        vase = bd.fillet(top_edges, radius=0.25 * MM)
        vase = bd.fillet(vase.edges().sort_by(bd.Axis.Y).first, radius=0.5 * MM)

        # Stand the vase upright (revolved about the Y axis).
        return bd.Rot(90, 0, 0) * vase


if __name__ == "__main__":
    vase = Vase(name="vase")
    vase.export("gallery_vase.stl")
    print(f"volume: {vase.get_volume() * 1e9:.0f} mm^3")
