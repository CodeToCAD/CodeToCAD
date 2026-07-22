"""Build123D introductory example 2: Plate with Hole.

https://build123d.readthedocs.io/en/latest/introductory_examples.html

Original:
    ex2 = Box(80, 60, 10)
    ex2 -= Cylinder(22 / 2, height=10)

Translated to CodeToCAD primitives.
"""

from codetocad_integrations.build123d import make_cube

length, width, thickness = "80mm", "60mm", "10mm"
center_hole_diameter = "22mm"

if __name__ == "__main__":
    plate = make_cube(length, width, thickness)
    plate.hole(plate.top_center, radius_or_shape="22mm / 2", amount=thickness)
    plate.export("intro_02_plate_with_hole.stl")
    print(f"volume: {plate.get_volume() * 1e9:.0f} mm^3")
