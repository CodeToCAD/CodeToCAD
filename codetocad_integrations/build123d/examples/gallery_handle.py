"""Build123D gallery example: Handle.

https://build123d.readthedocs.io/en/stable/examples_1.html

A handle swept along a spline through multiple cross-sections (circles at
the ends, rounded rectangles in between). A custom CodeToCAD part with a
@location-decorated named location on top.

Dimensions are in meters (CodeToCAD's base unit), hence the MM factor.
"""

import build123d as bd

import codetocad
from codetocad_integrations.build123d import Part3D

MM = 0.001
SEGMENT_COUNT = 6


class Handle(Part3D):
    def build_native(self) -> bd.Part:
        center_line = bd.Spline(
            (-10 * MM, 0, 0),
            (0, 0, 5 * MM),
            (10 * MM, 0, 0),
            tangents=((0, 0, 1), (0, 0, -1)),
            tangent_scalars=(1.5, 1.5),
        )
        sections = bd.Sketch()
        for i in range(SEGMENT_COUNT + 1):
            location = center_line ^ (i / SEGMENT_COUNT)
            if i % SEGMENT_COUNT == 0:
                section = location * bd.Circle(1 * MM)
            else:
                section = location * bd.Rectangle(1.25 * MM, 3 * MM)
                section = bd.fillet(section.vertices(), radius=0.2 * MM)
            sections += section
        return bd.sweep(sections, path=center_line, multisection=True)

    @codetocad.location
    def grip_center(self):
        return codetocad.CubeLocations.TOP_CENTER


if __name__ == "__main__":
    handle = Handle(name="handle")
    handle.export("gallery_handle.stl")
    print(f"volume: {handle.get_volume() * 1e9:.1f} mm^3")
    for loc in handle.get_locations():
        print(f"location {loc.name}: {tuple(round(v, 5) for v in loc.to_tuple())}")
