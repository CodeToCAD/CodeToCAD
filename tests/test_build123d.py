import math

import pytest

bd = pytest.importorskip("build123d")

import codetocad
from codetocad import CommonFasteners, Location
from codetocad_integrations.build123d import (
    Part3D,
    adapt,
    make_circle,
    make_cube,
    make_cylinder,
    make_import,
    make_led,
    make_rectangle,
    make_sphere,
)


def test_make_cube_native_volume():
    cube = make_cube("10cm", "10cm", "5cm")
    assert cube.get_volume() == pytest.approx(0.1 * 0.1 * 0.05)
    assert isinstance(cube.get_native(), bd.Part)


def test_example_flow_hole_and_export(tmp_path):
    cube = make_cube("10cm", "10cm", "5cm")
    cube.hole(cube.top_center, radius_or_shape="4cm", amount="5cm")
    expected = 0.1 * 0.1 * 0.05 - math.pi * 0.04**2 * 0.05
    assert cube.get_volume() == pytest.approx(expected, rel=1e-6)

    destination = tmp_path / "my_cube.stl"
    cube.export(str(destination))
    assert destination.exists() and destination.stat().st_size > 0


def test_export_includes_assembly(tmp_path):
    holder = make_cube(1, 1, 1)
    lid = make_cube(1, 1, 0.2, start_location=Location(z=0.6))
    hinge = Location(0, -0.5, 0.5)
    holder.revolute(hinge, lid, hinge)

    assembled = tmp_path / "assembly.stl"
    holder.export(str(assembled))
    alone = tmp_path / "holder_only.stl"
    holder.export(str(alone), include_assembly=False)
    assert assembled.stat().st_size > alone.stat().st_size

    step = tmp_path / "assembly.step"
    holder.export(str(step))
    reimported = bd.import_step(str(step))
    box = reimported.bounding_box()
    assert box.max.Z == pytest.approx(0.7, abs=1e-6)  # lid top included
    assert box.min.Z == pytest.approx(-0.5, abs=1e-6)


def test_generate_drawing_reflects_native_hole(tmp_path):
    # The Build123D adapter tessellates its native solid, so a drawing shows
    # the hole (as a circle in the top view) that the core primitive lacks.
    plate = make_cube("80mm", "60mm", "10mm")
    plate.name = "Plate"
    plate.hole(plate.top_center, radius_or_shape="11mm", amount="10mm")

    drawing = plate.generate_drawing()
    assert isinstance(drawing, codetocad.Part2D)
    assert drawing._primitive["kind"] == "drawing"

    solid_plate = make_cube("80mm", "60mm", "10mm")
    top = next(v for v in drawing._primitive["drawing"].views if v.name == "top")
    solid_top = next(
        v
        for v in solid_plate.generate_drawing()._primitive["drawing"].views
        if v.name == "top"
    )
    # The bored plate's top view carries the extra hole circle.
    assert len(top.segments) > len(solid_top.segments)

    destination = tmp_path / "plate.svg"
    assert drawing.export(str(destination)) == str(destination)
    assert destination.read_text().startswith("<svg")


def test_export_bakes_in_starting_angle(tmp_path):
    # A revolute joint's starting_angle should pose the exported assembly, not
    # just the simulation. The lid, modeled flat on top, swings up ~90deg.
    holder = make_cube("20cm", "20cm", "20cm", start_location=Location(z=0.1))
    holder.name = "holder"
    lid = make_cube("20cm", "20cm", "2cm", start_location=Location(z=0.21))
    lid.name = "lid"
    hinge = Location.from_euler(0, -0.1, 0.2, x_deg=-90, name="hinge")  # axis +x? -> Y
    holder.revolute(hinge, lid, hinge, starting_angle="90deg")

    flat = tmp_path / "flat.stl"
    make_cube("20cm", "20cm", "20cm", start_location=Location(z=0.1)).export(
        str(flat), include_assembly=False
    )
    posed = tmp_path / "posed.stl"
    holder.export(str(posed))

    box = bd.import_stl(str(posed)).bounding_box()
    # With the lid swung up, the assembly is taller than the holder alone.
    holder_box = bd.import_stl(str(flat)).bounding_box()
    assert box.max.Z > holder_box.max.Z + 0.1


def test_hole_between_locations():
    cube = make_cube(1, 1, 1)
    cube.hole(cube.top_center, radius_or_shape=0.1, end_location=cube.bottom_center)
    expected = 1 - math.pi * 0.1**2 * 1
    assert cube.get_volume() == pytest.approx(expected, rel=1e-6)


def test_boolean_subtract():
    body = make_cube(1, 1, 1)
    cutter = make_cylinder(0.2, 2)
    body.subtract(Location(), cutter, Location())
    expected = 1 - math.pi * 0.2**2 * 1
    assert body.get_volume() == pytest.approx(expected, rel=1e-6)


def test_boolean_union_with_anchor_alignment():
    a = make_cube(1, 1, 1)
    b = make_cube(1, 1, 1)
    # Stack b so its bottom sits on a's top: no overlap, volumes add.
    a.union(a.top_center, b, b.bottom_center)
    assert a.get_volume() == pytest.approx(2.0, rel=1e-6)


def test_shell_with_opening():
    cup = make_cylinder("2cm", "5cm")
    cup.shell(thickness="5mm", start_at_location=cup.top_center)
    solid_volume = math.pi * 0.02**2 * 0.05
    inner_volume = math.pi * 0.015**2 * 0.045
    assert cup.get_volume() == pytest.approx(solid_volume - inner_volume, rel=1e-3)


def test_fillet_and_chamfer():
    cube = make_cube(1, 1, 1)
    cube.fillet(amount="5cm")  # all edges
    assert cube.get_volume() < 1.0

    cube2 = make_cube(1, 1, 1)
    top_edges = cube2.get_edges(cube2.top_front_left, cube2.top_back_right)
    assert len(top_edges) == 4
    cube2.chamfer(edges=top_edges, amount="5cm")
    assert 0 < cube2.get_volume() < 1.0


def test_transform_moves_native_solid():
    cube = make_cube(1, 1, 1)
    cube.transform(relative=Location(x="50cm"))
    bbox_min, bbox_max = cube.get_bounding_box()
    assert bbox_min.x == pytest.approx(0.0, abs=1e-9)
    assert bbox_max.x == pytest.approx(1.0, abs=1e-9)
    assert cube.top_center.to_tuple() == pytest.approx((0.5, 0, 0.5))


def test_native_geometry_queries():
    cube = make_cube(2, 2, 2)
    face = cube.get_face(cube.top_center)
    assert face.native is not None
    vertex = cube.get_vertex(cube.top_back_right)
    assert vertex.location.to_tuple() == pytest.approx((1, 1, 1))
    edge = cube.get_edge(cube.top_front)
    assert edge.native is not None


def test_extrude_sketch():
    sheet = make_rectangle("2cm", "3cm")
    assert sheet.get_area() == pytest.approx(0.02 * 0.03)
    part = sheet.extrude("1cm")
    assert part.get_volume() == pytest.approx(0.02 * 0.03 * 0.01)


def test_revolve_sketch_native_tube():
    tube = make_rectangle("2cm", "3cm", Location(0.1, 0, 0)).revolve()
    # Native OpenCascade volume of the annular cylinder.
    assert tube.get_volume() == pytest.approx(
        math.pi * (0.11**2 - 0.09**2) * 0.03, rel=1e-6
    )


def test_partial_revolve_native():
    quarter = make_circle("1cm", Location(0.05, 0, 0)).revolve(90)
    assert quarter.get_volume() == pytest.approx(
        0.25 * 2 * math.pi**2 * 0.05 * 0.01**2, rel=1e-4
    )


def test_loft_sketch_native():
    frustum = make_circle("2cm", Location(0, 0, 0)).loft(
        make_circle("1cm", Location(0, 0, "3cm"))
    )
    # Native cone frustum V = pi*h/3 * (R^2 + R*r + r^2).
    assert frustum.get_volume() == pytest.approx(
        math.pi * 0.03 / 3 * (0.02**2 + 0.02 * 0.01 + 0.01**2), rel=1e-6
    )
    assert isinstance(frustum.get_native(), bd.Part)


def test_loft_between_multiple_sections():
    tower = make_rectangle("2cm", "2cm", Location(0, 0, 0)).loft(
        make_rectangle("2cm", "2cm", Location(0, 0, "2cm")),
        make_rectangle("1cm", "1cm", Location(0, 0, "4cm")),
    )
    box = 0.02 * 0.02 * 0.02
    frustum = 0.02 / 6 * (0.02**2 + 4 * 0.015**2 + 0.01**2)
    assert tower.get_volume() == pytest.approx(box + frustum, rel=1e-6)


def test_sweep_sketch_native_matches_extrude():
    swept = make_rectangle("2cm", "3cm").sweep([(0, 0, 0), (0, 0, "5cm")])
    assert swept.get_volume() == pytest.approx(0.02 * 0.03 * 0.05, rel=1e-6)


def test_sweep_along_edge_native():
    from codetocad.topology import Edge, Vertex

    x_axis = Edge(Vertex(Location(0, 0, 0)), Vertex(Location("4cm", 0, 0)))
    swept = make_circle("1cm").sweep(x_axis)
    assert swept.get_volume() == pytest.approx(math.pi * 0.01**2 * 0.04, rel=1e-6)


def test_custom_build_native_with_operations():
    class Bracket(Part3D):
        def build_native(self):
            return bd.Box(0.08, 0.06, 0.01)

    bracket = Bracket(name="bracket")
    bracket.hole(Location(z=0.005), radius_or_shape=0.002, amount=0.01)
    expected = 0.08 * 0.06 * 0.01 - math.pi * 0.002**2 * 0.01
    assert bracket.get_volume() == pytest.approx(expected, rel=1e-6)


def test_import_stl_roundtrip(tmp_path):
    source = tmp_path / "box.stl"
    make_cube(0.1, 0.1, 0.1).export(str(source))
    imported = make_import(str(source))
    assert imported.get_volume() == pytest.approx(0.001, rel=1e-3)


def test_step_export(tmp_path):
    destination = tmp_path / "part.step"
    make_sphere(0.05).export(str(destination))
    assert destination.exists() and destination.stat().st_size > 0


def test_adapted_components_and_material():
    light = make_led()
    assert light.forward_voltage == pytest.approx(2.0)
    assert light.get_volume() == pytest.approx(math.pi * 0.0025**2 * 0.0086, rel=1e-6)

    part = make_cube(0.1, 0.1, 0.1)
    part.set_material(codetocad.aluminum_material())
    assert part.get_mass().value == pytest.approx(2.7, rel=1e-6)

    bolt = adapt(CommonFasteners.M3_BOLT.build())
    assert bolt.get_volume() == pytest.approx(math.pi * 0.0015**2 * 0.012, rel=1e-6)


def test_linear_pattern_native_volume():
    box = make_cube(1, 1, 1)
    box.linear_pattern(3, Location(x=2))
    assert box.get_volume() == pytest.approx(3.0, rel=1e-6)


def test_circular_pattern_after_transform():
    post = make_cylinder(0.2, 1)
    post.transform(relative=Location(x=1))
    post.circular_pattern(4, 90)
    assert post.get_volume() == pytest.approx(4 * math.pi * 0.2**2, rel=1e-6)


def test_duplicate_adapted_part_is_independent():
    box = make_cube(1, 1, 1)
    box.hole(box.top_center, radius_or_shape=0.1, amount=1)
    expected = 1 - math.pi * 0.1**2
    copy = box.duplicate("box2")
    assert isinstance(copy, Part3D)
    assert copy.get_volume() == pytest.approx(expected, rel=1e-6)
    copy.transform(relative=Location(x=5))
    assert box.get_volume() == pytest.approx(expected, rel=1e-6)
    assert box.top_center.x.value == pytest.approx(0)
    assert copy.top_center.x.value == pytest.approx(5)
