"""Build123D introductory example 9: Selectors, Fillets, and Chamfers.

https://build123d.readthedocs.io/en/latest/introductory_examples.html

Original:
    ex9 = Box(80, 60, 10)
    ex9 = chamfer(ex9.edges().group_by(Axis.Z)[-1], length=4)
    ex9 = fillet(ex9.edges().filter_by(Axis.Z), radius=5)

Translated to CodeToCAD: edges are selected with bounded geometry queries
instead of build123d selectors. The vertical edges are filleted first, then
the top loop is chamfered.
"""

from codetocad import Location
from codetocad_integrations.build123d import make_cube

if __name__ == "__main__":
    part = make_cube("80mm", "60mm", "10mm")

    # The four vertical edges have their midpoints on the z=0 midplane.
    vertical_edges = part.get_edges(
        Location("-40mm", "-30mm", 0), Location("40mm", "30mm", 0), tolerance=1e-3
    )
    part.fillet(edges=vertical_edges, amount="5mm")

    # All edges of the top face (straight edges and the new fillet arcs).
    top_edges = part.get_edges(
        part.top_front_left, part.top_back_right, tolerance=1e-3
    )
    part.chamfer(edges=top_edges, amount="4mm")

    part.export("intro_09_fillet_chamfer.stl")
    print(f"volume: {part.get_volume() * 1e9:.0f} mm^3")
