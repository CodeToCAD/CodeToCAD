"""A "CodeToCAD" logo plate: text embossed on a plate, modeled with
Build123D and rendered to a PNG with the Open3D integration.

    codetocad embossed_text_logo.py
"""

from codetocad_integrations.build123d import make_cube, make_text
from codetocad_integrations.open3d import render

length, width, thickness = "140mm", "40mm", "6mm"
font_size, font_height = "18mm", "3mm"

if __name__ == "__main__":
    plate = make_cube(length, width, thickness)

    logo = make_text("CodeToCAD", font="Arial", size=font_size).extrude(font_height)
    plate.union(plate.top_center, logo, logo.bottom_center)

    render(plate, path="images/embossed_text_logo.png", front=(0,-0.5,1.5), up=(0,0,1.))
    print(f"volume: {plate.get_volume() * 1e9:.0f} mm^3")
