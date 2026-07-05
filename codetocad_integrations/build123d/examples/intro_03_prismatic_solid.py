"""Build123D introductory example 3: An extruded prismatic solid.

https://build123d.readthedocs.io/en/latest/introductory_examples.html

Original:
    sk3 = Circle(60) - Rectangle(80 / 2, 60 / 2)
    ex3 = extrude(sk3, amount=2 * 10)

Translated to CodeToCAD sketches, extrusion and a boolean subtract.
"""

from codetocad import Location
from codetocad_integrations.build123d import make_circle, make_rectangle

length, width, thickness = "80mm", "60mm", "10mm"

if __name__ == "__main__":
    solid = make_circle(width).extrude("2 * 10mm")
    slot = make_rectangle("80mm / 2", "60mm / 2").extrude("2 * 10mm")
    solid.subtract(Location(), slot, Location())
    solid.export("intro_03_prismatic_solid.stl")
    print(f"volume: {solid.get_volume() * 1e9:.0f} mm^3")
