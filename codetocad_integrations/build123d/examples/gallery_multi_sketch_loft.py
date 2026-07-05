"""Build123D gallery example: Multi-Sketch Loft.

https://build123d.readthedocs.io/en/stable/examples_1.html

A vase-like "art" piece lofted through a stack of circles of varying radii,
then hollowed with openings at the top and bottom.

Dimensions are in meters (CodeToCAD's base unit), hence the MM factor.
"""

from math import pi, sin

import build123d as bd

from codetocad_integrations.build123d import Part3D

MM = 0.001
SLICE_COUNT = 10


class LoftedArt(Part3D):
    def build_native(self) -> bd.Part:
        art = bd.Sketch()
        for i in range(SLICE_COUNT + 1):
            plane = bd.Plane(origin=(0, 0, i * 3 * MM), z_dir=(0, 0, 1))
            art += plane * bd.Circle((10 * sin(i * pi / SLICE_COUNT) + 5) * MM)
        art = bd.loft(art)
        top_bottom = art.faces().filter_by(bd.GeomType.PLANE)
        return bd.offset(art, openings=top_bottom, amount=0.5 * MM)


if __name__ == "__main__":
    art = LoftedArt(name="art")
    art.export("gallery_multi_sketch_loft.stl")
    print(f"volume: {art.get_volume() * 1e9:.0f} mm^3")
