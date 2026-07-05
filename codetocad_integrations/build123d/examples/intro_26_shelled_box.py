"""Build123D introductory example 26: Offset Part To Create Thin features.

https://build123d.readthedocs.io/en/latest/introductory_examples.html

Original:
    ex26 = Box(80, 60, 10)
    topf = ex26.faces().sort_by().last
    ex26 = offset(ex26, amount=-2, openings=topf)

Translated to CodeToCAD's shell() with an opening at the top face.
"""

from codetocad_integrations.build123d import make_cube

length, width, thickness, wall = "80mm", "60mm", "10mm", "2mm"

if __name__ == "__main__":
    box = make_cube(length, width, thickness)
    box.shell(wall, start_at_location=box.top_center)
    box.export("intro_26_shelled_box.stl")
    print(f"volume: {box.get_volume() * 1e9:.0f} mm^3")
