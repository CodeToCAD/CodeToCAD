"""Exercises the Blender adapter end-to-end. Run inside Blender:

    blender --background --factory-startup --python-exit-code 1 \
        --python tests/blender_smoke_script.py

(test_blender.py does this automatically.)
"""

import math

from codetocad import Location, aluminum_material
from codetocad_integrations.blender import ensure_blender

ensure_blender()  # resets the scene (we are already inside Blender)

from codetocad_integrations.blender import (  # noqa: E402
    make_circle,
    make_cube,
    make_cylinder,
    make_import,
    make_rectangle,
    make_text,
)


def approx(actual, expected, rel):
    assert math.isclose(actual, expected, rel_tol=rel), (
        f"expected ~{expected}, got {actual}"
    )


# 1. Cube volume/area
cube = make_cube("10cm", "10cm", "10cm")
approx(cube.get_volume(), 0.001, 1e-6)
approx(cube.get_area(), 0.06, 1e-6)

# 2. The README example: hole through a plate
plate = make_cube("10cm", "10cm", "5cm")
plate.hole(plate.top_center, radius_or_shape="4cm", amount="5cm")
approx(plate.get_volume(), 0.1 * 0.1 * 0.05 - math.pi * 0.04**2 * 0.05, 5e-3)
plate.export("smoke_cube.stl")

# 2b. Square hole from a Part2D profile, drilled through everything
square_plate = make_cube("10cm", "10cm", "5cm")
square_plate.hole(
    square_plate.top_center, make_rectangle("4cm", "4cm"), throughAll=True
)
approx(square_plate.get_volume(), 0.1 * 0.1 * 0.05 - 0.04 * 0.04 * 0.05, 5e-3)

# 3. Shelled cup (solidify with a top opening)
cup = make_cylinder("2cm", "5cm")
cup.shell("5mm", start_at_location=cup.top_center)
solid = math.pi * 0.02**2 * 0.05
cavity = math.pi * 0.015**2 * 0.045
approx(cup.get_volume(), solid - cavity, 5e-2)

# 4. Boolean union with anchor alignment (stacked cubes)
a = make_cube("4cm", "4cm", "4cm")
b = make_cube("4cm", "4cm", "4cm")
a.union(a.top_center, b, b.bottom_center)
approx(a.get_volume(), 2 * 0.04**3, 1e-3)

# 5. Fillet all edges shrinks the cube
rounded = make_cube("4cm", "4cm", "4cm")
rounded.fillet(amount="5mm")
assert 0 < rounded.get_volume() < 0.04**3

# 6. Chamfer only the top edges, selected with a bounded query
chamfered = make_cube("4cm", "4cm", "4cm")
top_edges = chamfered.get_edges(
    chamfered.top_front_left, chamfered.top_back_right, tolerance=1e-3
)
assert len(top_edges) == 4, f"expected 4 top edges, got {len(top_edges)}"
chamfered.chamfer(edges=top_edges, amount="5mm")
assert 0 < chamfered.get_volume() < 0.04**3

# 7. Transform moves the object (and its cube locations)
mover = make_cube("2cm", "2cm", "2cm")
mover.transform(relative=Location(x="50cm"))
bbox_min, bbox_max = mover.get_bounding_box()
approx(bbox_min.x, 0.49, 1e-6)
approx(bbox_max.x, 0.51, 1e-6)

# 8. Native geometry queries
vertex = cube.get_vertex(cube.top_back_right)
for value, expected in zip(vertex.location.to_tuple(), (0.05, 0.05, 0.05)):
    approx(value, expected, 1e-6)
face = cube.get_face(cube.top_center)
assert face.native is not None

# 9. Extruded text spans the requested height
label = make_text("Hi", font="default", size="2cm").extrude("4mm")
t_min, t_max = label.get_bounding_box()
approx(t_max.z - t_min.z, 0.004, 1e-3)
assert label.get_volume() > 0

# 9b. Duplicate and patterns (instances unioned into the mesh)
row = make_cube("2cm", "2cm", "2cm")
row.linear_pattern(3, Location(x="5cm"))
approx(row.get_volume(), 3 * 0.02**3, 1e-3)

ring = make_cylinder("1cm", "2cm")
ring.transform(relative=Location(x="6cm"))
ring.circular_pattern(4, 90)
approx(ring.get_volume(), 4 * math.pi * 0.01**2 * 0.02, 5e-3)

twin = row.duplicate("row_twin")
twin.transform(relative=Location(y="10cm"))
approx(twin.get_volume(), 3 * 0.02**3, 1e-3)
approx(row.get_volume(), 3 * 0.02**3, 1e-3)

# 9c. Revolve a profile into a solid (full-turn tube and a partial arc)
tube = make_rectangle("2cm", "3cm", Location(x="10cm")).revolve()
approx(tube.get_volume(), math.pi * (0.11**2 - 0.09**2) * 0.03, 5e-3)
tmin, tmax = tube.get_bounding_box()
approx(tmax.x, 0.11, 5e-3)

wedge = make_circle("1cm", Location(x="5cm")).revolve(90)
approx(wedge.get_volume(), 0.25 * 2 * math.pi**2 * 0.05 * 0.01**2, 5e-2)

# 10. Material and mass
block = make_cube("10cm", "10cm", "10cm")
block.set_material(aluminum_material())
approx(block.get_mass().value, 2.7, 1e-6)

# 11. STL import roundtrip
imported = make_import("smoke_cube.stl")
approx(imported.get_volume(), plate.get_volume(), 1e-3)

# 12. Scene export
block.export("smoke_scene.blend")

print("BLENDER_SMOKE_OK")
