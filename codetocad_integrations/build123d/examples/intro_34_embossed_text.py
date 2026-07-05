"""Build123D introductory example 34: Embossed and Debossed Text.

https://build123d.readthedocs.io/en/latest/introductory_examples.html

Original: a Box with "Hello" extruded up from the top face and "World" cut
down into it.

Translated to CodeToCAD: text sketches are extruded and then unioned into /
subtracted from the plate using anchor locations.
"""

from codetocad_integrations.build123d import make_cube, make_text

length, width, thickness = "80mm", "60mm", "10mm"
font_size, font_height = "25mm", "4mm"

if __name__ == "__main__":
    plate = make_cube(length, width, thickness)

    hello = make_text("Hello", font="Arial", size=font_size).extrude(font_height)
    # Embossed: sit "Hello" on the top face, above the centerline.
    plate.union(
        plate.top_center.translate(y="8mm"), hello, hello.bottom_center
    )

    world = make_text("World", font="Arial", size=font_size).extrude(font_height)
    # Debossed: sink "World" into the top face, below the centerline.
    plate.subtract(
        plate.top_center.translate(y="-8mm"), world, world.top_center
    )

    plate.export("intro_34_embossed_text.stl")
    print(f"volume: {plate.get_volume() * 1e9:.0f} mm^3")
