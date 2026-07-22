import math

import pytest

import codetocad
from codetocad import (
    CommonFasteners,
    CubeLocations,
    Location,
    aluminum_material,
    capacitor,
    circle,
    cube,
    cylinder,
    led,
    rectangle,
    resistor,
    sphere,
)
from codetocad.topology import Edge, Vertex


def test_cube_analysis():
    part = cube(2, 3, 4)
    assert part.get_volume() == pytest.approx(24)
    assert part.get_area() == pytest.approx(2 * (6 + 12 + 8))


def test_cylinder_and_sphere_volume():
    assert cylinder(1, 2).get_volume() == pytest.approx(2 * math.pi)
    assert sphere(1).get_volume() == pytest.approx(4 / 3 * math.pi)


def test_2d_has_no_volume():
    with pytest.raises(ValueError):
        rectangle(1, 2).get_volume()


def test_extrude_rectangle_becomes_cube():
    part3d = rectangle("2cm", "3cm").extrude("4cm")
    assert isinstance(part3d, codetocad.Part3D)
    assert part3d.get_volume() == pytest.approx(0.02 * 0.03 * 0.04)


def test_extrude_circle_becomes_cylinder():
    part3d = circle(1).extrude(2)
    assert part3d.get_volume() == pytest.approx(2 * math.pi)


def test_draft_cube_is_a_frustum():
    # 2x2 base, 4 tall, 10deg draft: top face insets by 4*tan(10) per side.
    part = cube(2, 2, 4, draft_angle=10)
    inset = 4 * math.tan(math.radians(10))
    top = 2 - 2 * inset
    expected = 4 / 6 * (2 * 2 + 4 * (2 - inset) ** 2 + top**2)
    assert part.get_volume() == pytest.approx(expected)
    # Positive draft leaves the base (widest cross-section) bounding it.
    bbox_min, bbox_max = part.get_bounding_box()
    assert (bbox_max.x - bbox_min.x) == pytest.approx(2)


def test_draft_cylinder_is_a_cone_frustum():
    part = cylinder(1, 2, draft_angle=15)
    top = 1 - 2 * math.tan(math.radians(15))
    assert part.get_volume() == pytest.approx(
        math.pi * 2 / 3 * (1 + top + top**2)
    )


def test_extrude_with_draft():
    part = rectangle(2, 2).extrude(4, draft_angle=10)
    assert part._primitive["kind"] == "cube"
    assert part.get_volume() == cube(2, 2, 4, draft_angle=10).get_volume()


def test_draft_too_steep_is_rejected():
    with pytest.raises(ValueError, match="too steep"):
        cube(2, 2, 10, draft_angle=45).get_volume()


def test_revolve_rectangle_becomes_tube():
    # A rectangle offset from the Y axis, revolved a full turn, is a tube
    # (annular cylinder): V = pi * (r_out^2 - r_in^2) * height.
    part3d = rectangle(2, 3, Location(5, 0, 0)).revolve()
    assert isinstance(part3d, codetocad.Part3D)
    assert part3d.get_volume() == pytest.approx(math.pi * (6**2 - 4**2) * 3)
    assert part3d.get_volume() == pytest.approx(2 * math.pi * 5 * 2 * 3)  # Pappus


def test_revolve_circle_becomes_torus():
    part3d = circle(1, Location(5, 0, 0)).revolve()
    assert part3d.get_volume() == pytest.approx(2 * math.pi**2 * 5 * 1**2)


def test_partial_revolve_scales_with_angle():
    quarter = rectangle(2, 3, Location(5, 0, 0)).revolve(90)
    assert quarter.get_volume() == pytest.approx(0.25 * 2 * math.pi * 5 * 2 * 3)


def test_revolve_around_edge_matches_axis():
    y_axis = Edge(Vertex(Location(0, 0, 0)), Vertex(Location(0, 1, 0)))
    around_edge = rectangle(2, 3, Location(5, 0, 0)).revolve(360, y_axis)
    around_axis = rectangle(2, 3, Location(5, 0, 0)).revolve(360, "y")
    assert around_edge.get_volume() == pytest.approx(around_axis.get_volume())


def test_revolve_bounding_box_from_mesh():
    part3d = rectangle(2, 3, Location(5, 0, 0)).revolve()
    bbox_min, bbox_max = part3d.get_bounding_box()
    assert bbox_min.to_tuple() == pytest.approx((-6, -1.5, -6))
    assert bbox_max.to_tuple() == pytest.approx((6, 1.5, 6))


def test_revolve_profile_crossing_axis_is_rejected():
    # Rejected by revolve() itself, so a CAD kernel never sees the bad sweep
    # (OCCT reports it only as an opaque "BRep_API: command not done").
    with pytest.raises(ValueError, match="passes through it"):
        rectangle(2, 3).revolve()


def test_revolve_offset_along_the_axis_still_crosses_it():
    # Sliding a profile *along* the revolve axis never moves it away from the
    # axis; the error should say which direction actually would.
    with pytest.raises(ValueError, match="offset the sketch along y"):
        circle(1, Location(5, 0, 0)).revolve(180, axis="x")


def test_revolve_profile_touching_axis_sweeps_a_solid():
    # A rectangle with one edge *on* the axis is the usual way to revolve a
    # solid: touching the axis is allowed, only crossing it is not.
    cylinder_ = rectangle(1, 2, Location(0.5, 0, 0)).revolve(360, axis="y")
    assert cylinder_.get_volume() == pytest.approx(math.pi * 1**2 * 2)


def test_revolve_angle_out_of_range():
    with pytest.raises(ValueError, match="within"):
        rectangle(2, 3, Location(5, 0, 0)).revolve(0)


def test_revolve_zero_length_edge():
    degenerate = Edge(Vertex(Location(0, 0, 0)), Vertex(Location(0, 0, 0)))
    with pytest.raises(ValueError, match="zero-length"):
        rectangle(2, 3, Location(5, 0, 0)).revolve(360, degenerate)


def test_boolean_ledger():
    a, b, c = cube(1, 1, 1), cube(1, 1, 1), cube(1, 1, 1)
    a.subtract(Location(), b, Location())
    a.union(Location(), c, Location())
    assert a.boolean_ledger.subtracted_parts == [b]
    assert a.boolean_ledger.unioned_parts == [c]
    assert set(a.boolean_ledger.all_parts) == {b, c}


def test_transform_requires_exactly_one_argument():
    part = cube(1, 1, 1)
    with pytest.raises(ValueError):
        part.transform()
    with pytest.raises(ValueError):
        part.transform(absolute=Location(), relative=Location())
    part.transform(relative=Location(x=1))
    assert len(part.ledger.transformations) == 1


def test_shell_fillet_chamfer_hole_recorded():
    part = cylinder("2cm", "5cm")
    part.shell(thickness="5mm")
    part.fillet(amount="1mm")
    part.chamfer(amount="1mm")
    part.hole(Location(), radius_or_shape="2mm", amount="1cm")
    operations = [op["operation"] for op in part.operations]
    assert operations == ["shell", "fillet", "chamfer", "hole"]
    assert part.operations[0]["thickness"].value == pytest.approx(0.005)


def test_hole_requires_exactly_one_of_amount_or_end_location():
    part = cube(1, 1, 1)
    with pytest.raises(ValueError):
        part.hole(Location(), radius_or_shape="1mm")
    with pytest.raises(ValueError):
        part.hole(Location(), radius_or_shape="1mm", amount=1, end_location=Location())


def test_geometry_queries_on_cube():
    part = cube(2, 2, 2)
    vertex = part.get_vertex(CubeLocations.TOP_BACK_RIGHT.to_location(part))
    assert vertex.location.to_tuple() == pytest.approx((1, 1, 1))
    face = part.get_face(CubeLocations.TOP_CENTER.to_location(part))
    assert face.center.to_tuple() == pytest.approx((0, 0, 1))
    edge = part.get_edge(CubeLocations.TOP_FRONT.to_location(part))
    assert edge.midpoint.to_tuple() == pytest.approx((0, -1, 1))
    with pytest.raises(ValueError):
        part.get_vertex(Location(5, 5, 5))
    top_face_vertices = part.get_vertices(
        CubeLocations.TOP_FRONT_LEFT.to_location(part),
        CubeLocations.TOP_BACK_RIGHT.to_location(part),
    )
    assert len(top_face_vertices) == 4


def test_material_mass_from_density():
    part = cube(0.1, 0.1, 0.1)
    part.set_material(aluminum_material())
    assert part.get_mass().value == pytest.approx(2700 * 0.001)
    assert part.get_density().value == pytest.approx(2700)


def test_assembly_constraints():
    a, b = cube(1, 1, 1), cube(1, 1, 1)
    a.fixed(Location(), b, Location())
    a.revolute(Location(), b, Location())
    assert a.ledger.fixed_constraints == [b]
    assert a.ledger.revolute_constraints == [b]
    assert a.ledger.all_parts == [b]


def test_ecad_components():
    light = led()
    assert light.forward_voltage == pytest.approx(2.0)
    r = resistor(resistance=470)
    assert r.resistance == 470
    c = capacitor(capacitance=1e-6, voltage_rating=25)
    assert c.capacitance == pytest.approx(1e-6)
    assert c.voltage_rating == 25
    assert light.get_volume() > 0


def test_fasteners():
    bolt = CommonFasteners.M3_BOLT.build()
    assert bolt.get_volume() == pytest.approx(math.pi * 0.0015**2 * 0.012)
    plate = cube("2cm", "2cm", "5mm")
    CommonFasteners.M3_BOLT.apply_to(plate, Location())
    assert plate.operations[0]["operation"] == "hole"


def test_export_stl(tmp_path):
    destination = tmp_path / "box.stl"
    cube(1, 1, 1).export(str(destination))
    content = destination.read_text()
    assert content.startswith("solid")
    assert content.count("facet normal") == 12

    cylinder_path = tmp_path / "cyl.stl"
    cylinder(1, 1).export(str(cylinder_path))
    assert cylinder_path.read_text().startswith("solid")


def test_blank_part_requires_build_override():
    with pytest.raises(NotImplementedError):
        codetocad.Part3D().build()
    assert cube(1, 1, 1).build() is not None


def test_duplicate_is_independent():
    part = cube(1, 2, 3)
    part.name = "original"
    part.set_material(aluminum_material())
    part.shell(thickness="1mm")
    copy = part.duplicate()
    assert copy.name == "original_copy"
    assert copy.get_volume() == pytest.approx(part.get_volume())
    assert copy.material is part.material
    # Changes to the copy do not leak back into the original.
    copy.transform(relative=Location(x=1))
    copy.hole(Location(), radius_or_shape="1mm", amount="1cm")
    assert [op["operation"] for op in part.operations] == ["shell"]
    assert len(part.ledger.transformations) == 0
    assert part._origin.x == pytest.approx(0)
    assert part.duplicate(name="explicit").name == "explicit"


def test_linear_pattern_expands_mesh_and_bounding_box():
    part = cube(1, 1, 1).linear_pattern(3, Location(x=2))
    assert part.operations[0]["operation"] == "linear_pattern"
    bbox_min, bbox_max = part.get_bounding_box()
    assert bbox_min.x == pytest.approx(-0.5)
    assert bbox_max.x == pytest.approx(4.5)
    assert bbox_max.y == pytest.approx(0.5)
    # 3 instances x 12 triangles per cube.
    assert part._generate_mesh().shape == (36, 3, 3)


def test_circular_pattern_rotates_about_center():
    part = cube(1, 1, 1, start_location=Location(x=2)).circular_pattern(
        4, "90deg", center=Location(), axis="z"
    )
    operation = part.operations[0]
    assert operation["separation_angle"].value == pytest.approx(math.pi / 2)
    assert operation["axis"] == pytest.approx((0, 0, 1))
    bbox_min, bbox_max = part.get_bounding_box()
    assert bbox_min.x == pytest.approx(-2.5)
    assert bbox_max.x == pytest.approx(2.5)
    assert bbox_max.y == pytest.approx(2.5)


def test_pattern_validation():
    with pytest.raises(ValueError):
        cube(1, 1, 1).linear_pattern(0, Location(x=1))
    with pytest.raises(ValueError):
        cube(1, 1, 1).circular_pattern(0, 90)
    with pytest.raises(ValueError):
        cube(1, 1, 1).circular_pattern(4, 90, axis="w")
    with pytest.raises(ValueError):
        cube(1, 1, 1).circular_pattern(4, 90, axis=(0, 0, 0))


def test_patterned_export_stl(tmp_path):
    destination = tmp_path / "row.stl"
    cube(1, 1, 1).linear_pattern(4, Location(y=3)).export(str(destination))
    assert destination.read_text().count("facet normal") == 4 * 12


def test_export_includes_assembly(tmp_path):
    holder = cube(1, 1, 1)
    lid = cube(1, 1, 0.2, start_location=Location(z=0.6))
    hinge = Location(0, -0.5, 0.5)
    holder.revolute(hinge, lid, hinge)

    destination = tmp_path / "assembly.stl"
    holder.export(str(destination))
    assert destination.read_text().count("facet normal") == 2 * 12

    alone = tmp_path / "holder_only.stl"
    holder.export(str(alone), include_assembly=False)
    assert alone.read_text().count("facet normal") == 12

    assert codetocad.export_single_part(
        holder, str(tmp_path / "single.stl")
    ) == str(tmp_path / "single.stl")
    assert (tmp_path / "single.stl").read_text().count("facet normal") == 12


def test_export_assembly_applies_snap_shift(tmp_path):
    base = cube(1, 1, 1)
    attachment = cube(1, 1, 1)  # modeled at the origin, snapped up a level
    base.fixed(Location(z=1), attachment, Location())

    destination = tmp_path / "snapped.stl"
    base.export(str(destination))
    heights = [
        float(line.split()[3])
        for line in destination.read_text().splitlines()
        if line.strip().startswith("vertex")
    ]
    assert max(heights) == pytest.approx(1.5)
    assert min(heights) == pytest.approx(-0.5)
