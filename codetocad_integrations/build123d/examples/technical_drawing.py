"""Generate a 2D technical drawing (SVG) from a Build123D part.

``part.generate_drawing()`` projects the part into standard third-angle views
(front, top, right) plus an isometric view and hands back an editable
``Part2D`` — a sketch you can transform, rename and export like any other.
Because the Build123D adapter tessellates its *native* OpenCascade solid, the
drawing reflects Build123D-only features: the counterbored hole below shows up
as circles in the top and isometric views, not just the plate outline.

Run with ``codetocad technical_drawing.py`` (requires the build123d extra:
``uv sync --extra build123d``). It writes ``technical_drawing.svg`` next to
where it is run.
"""

from codetocad import Location
from codetocad_integrations.build123d import make_cube

if __name__ == "__main__":
    bracket = make_cube("80mm", "60mm", "12mm")
    bracket.name = "Bracket"
    # A Build123D hole — a core-only STL export could not draw this, but the
    # native tessellation can.
    bracket.hole(bracket.top_center, radius_or_shape="9mm", amount="12mm")

    # generate_drawing() returns a Part2D, so the drawing is editable geometry.
    drawing = bracket.generate_drawing()
    drawing.name = "Bracket - Rev A"  # updates the sheet's title block
    drawing.transform(relative=Location(x="5mm"))  # nudge it on the sheet

    drawing.export("technical_drawing.svg")
    print("wrote technical_drawing.svg")
