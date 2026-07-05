"""Build123D gallery example: Circuit Board With Holes.

https://build123d.readthedocs.io/en/stable/examples_1.html

A PCB with rows of through-holes and four corner mounting holes.
Translated to CodeToCAD primitives: an extruded rectangle drilled with
hole() operations.
"""

from codetocad import Location
from codetocad_integrations.build123d import make_rectangle

pcb_length, pcb_width, pcb_height = "70mm", "40mm", "3mm"

if __name__ == "__main__":
    pcb = make_rectangle(pcb_length, pcb_width).extrude(pcb_height)

    # Two double-rows of 1mm-radius through-holes.
    for i in range(13):
        x = i * 5 - 30
        for y in (-15, -10, 10, 15):
            pcb.hole(
                Location(f"{x}mm", f"{y}mm", "1.5mm"),
                radius="1mm",
                amount=pcb_height,
            )

    # Four 2mm-radius corner mounting holes on a 60 x 20 grid.
    for x in (-30, 30):
        for y in (-10, 10):
            pcb.hole(
                Location(f"{x}mm", f"{y}mm", "1.5mm"),
                radius="2mm",
                amount=pcb_height,
            )

    pcb.export("gallery_circuit_board.stl")
    print(f"volume: {pcb.get_volume() * 1e9:.0f} mm^3")
