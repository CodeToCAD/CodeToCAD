"""Generate a 2D technical drawing (SVG) from a Blender assembly.

``part.generate_drawing()`` works on any Part3D, and — like ``export()`` — on a
whole assembly: here a base plate with two standoffs fixed on top is projected
into standard third-angle views (front, top, right) plus an isometric view. It
returns an editable ``Part2D`` that we export to an SVG sheet.

    codetocad technical_drawing.py

The drawing itself is projected by CodeToCAD's core, so this example does not
even need Blender to build — but running it under Blender confirms the same
parts drive both the model and the drawing.
"""

from codetocad import Location
from codetocad_integrations.blender import ensure_blender, make_cube, make_cylinder

if __name__ == "__main__":
    ensure_blender()

    base = make_cube("60mm", "40mm", "6mm")
    base.name = "Standoff Plate"
    for x in ("-20mm", "20mm"):
        # Each standoff is modeled at the origin, then its base (z = -10mm, half
        # its 20mm height) is fixed onto the plate's top face at (x, 3mm).
        standoff = make_cylinder("5mm", "20mm")
        base.fixed(Location(x=x, z="3mm"), standoff, Location(z="-10mm"))

    drawing = base.generate_drawing()
    drawing.export("technical_drawing.svg")
    print("wrote technical_drawing.svg")
