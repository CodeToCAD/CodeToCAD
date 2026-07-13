import math

import pytest

bd = pytest.importorskip("build123d")

import codetocad
from codetocad import CommonFasteners, Location
from codetocad_integrations.build123d import (
    Part3D,
    adapt,
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
    cube.hole(cube.top_center, radius="4cm", amount="5cm")
    expected = 0.1 * 0.1 * 0.05 - math.pi * 0.04**2 * 0.05
    assert cube.get_volume() == pytest.approx(expected, rel=1e-6)

    destination = tmp_path / "my_cube.stl"
    cube.export(str(destination))
    assert destination.exists() and destination.stat().st_size > 0


def test_hole_between_locations():
    cube = make_cube(1, 1, 1)
    cube.hole(cube.top_center, radius=0.1, end_location=cube.bottom_center)
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


def test_custom_build_native_with_operations():
    class Bracket(Part3D):
        def build_native(self):
            return bd.Box(0.08, 0.06, 0.01)

    bracket = Bracket(name="bracket")
    bracket.hole(Location(z=0.005), radius=0.002, amount=0.01)
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
    box.hole(box.top_center, radius=0.1, amount=1)
    expected = 1 - math.pi * 0.1**2
    copy = box.duplicate("box2")
    assert isinstance(copy, Part3D)
    assert copy.get_volume() == pytest.approx(expected, rel=1e-6)
    copy.transform(relative=Location(x=5))
    assert box.get_volume() == pytest.approx(expected, rel=1e-6)
    assert box.top_center.x.value == pytest.approx(0)
    assert copy.top_center.x.value == pytest.approx(5)
