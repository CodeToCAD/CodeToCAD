"""Embossed and debossed text on a plate, built in Blender (the same design
as the Build123D intro example 34 translation).

    codetocad embossed_text.py
"""

from codetocad_integrations.blender import ensure_blender, make_cube, make_text

if __name__ == "__main__":
    ensure_blender()

    plate = make_cube("80mm", "60mm", "10mm")

    hello = make_text("Hello", font="default", size="25mm").extrude("4mm")
    plate.union(plate.top_center.translate(y="8mm"), hello, hello.bottom_center)

    world = make_text("World", font="default", size="25mm").extrude("4mm")
    plate.subtract(plate.top_center.translate(y="-8mm"), world, world.top_center)

    plate.export("embossed_text.stl")
    print(f"volume: {plate.get_volume() * 1e9:.0f} mm^3")
