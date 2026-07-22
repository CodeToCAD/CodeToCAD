import math

import pytest

import codetocad
from codetocad import CubeLocations, Location, cube


def test_default_location_identity_quaternion():
    loc = Location()
    assert loc.to_tuple() == (0, 0, 0)
    assert loc.quat == (0, 0, 0, 1)


def test_location_parses_units():
    loc = Location(x="2cm", y="1in", z=0.5)
    assert loc.x.value == pytest.approx(0.02)
    assert loc.y.value == pytest.approx(0.0254)
    assert loc.z.value == pytest.approx(0.5)


def test_from_euler_yaw_90():
    loc = Location.from_euler(z_deg=90)
    assert loc.quat_z == pytest.approx(math.sqrt(2) / 2)
    assert loc.quat_w == pytest.approx(math.sqrt(2) / 2)


def test_translate_and_rotate_chain():
    loc = Location().translate(x="1cm").translate(x="1cm", z="1mm")
    assert loc.x.value == pytest.approx(0.02)
    assert loc.z.value == pytest.approx(0.001)
    loc.rotate(z_deg=90).rotate(z_deg=-90)
    assert loc.quat_w == pytest.approx(1.0)


def test_cube_locations_resolve_on_part():
    part = cube(2, 4, 6)
    top = CubeLocations.TOP_CENTER.to_location(part)
    assert top.to_tuple() == pytest.approx((0, 0, 3))
    corner = CubeLocations.BOTTOM_FRONT_LEFT.to_location(part)
    assert corner.to_tuple() == pytest.approx((-1, -2, -3))


def test_cube_locations_lowercase_access():
    assert CubeLocations.top_center is CubeLocations.TOP_CENTER


def _plus_z(location):
    from codetocad.location import quat_rotate_vector

    return tuple(round(v, 6) for v in quat_rotate_vector(location.quat, (0, 0, 1)))


def test_cube_location_first_face_is_plus_z():
    part = cube(2, 4, 6)
    # The first-named face's outward normal becomes +Z.
    assert _plus_z(CubeLocations.TOP_CENTER.to_location(part)) == (0, 0, 1)
    assert _plus_z(CubeLocations.BOTTOM_CENTER.to_location(part)) == (0, 0, -1)
    assert _plus_z(CubeLocations.BACK_CENTER.to_location(part)) == (0, 1, 0)


def test_cube_location_reordered_permutation_differs_in_orientation():
    part = cube(2, 4, 6)
    back_bottom = CubeLocations.BACK_BOTTOM.to_location(part)
    bottom_back = CubeLocations.BOTTOM_BACK.to_location(part)
    # Same edge midline position...
    assert back_bottom.to_tuple() == bottom_back.to_tuple() == pytest.approx((0, 2, -3))
    # ...but oriented normal to the first-named face.
    assert _plus_z(back_bottom) == (0, 1, 0)  # out the back
    assert _plus_z(bottom_back) == (0, 0, -1)  # down


def test_cube_location_vertical_edges_and_corner_aliases():
    part = cube(2, 2, 2)
    # Vertical edges (all 12 present now) and every token order resolvable.
    assert CubeLocations.FRONT_LEFT.to_location(part).to_tuple() == pytest.approx(
        (-1, -1, 0)
    )
    assert CubeLocations.TOP_LEFT_FRONT is CubeLocations.TOP_FRONT_LEFT


def test_cube_location_expr_translate():
    part = cube(2, 2, 2)
    loc = CubeLocations.top_center.translate(x="2cm", y="2mm").to_location(part)
    assert loc.to_tuple() == pytest.approx((0.02, 0.002, 1.0))


def test_location_decorator_collected():
    class MyPart(codetocad.Part3D):
        def build(self):
            return self

        @codetocad.location
        def probe_point(self):
            return codetocad.CubeLocations.TOP_CENTER.translate(z="1cm")

    part = MyPart()
    part._primitive = {"kind": "cube", "length": 2, "width": 2, "height": 2}
    locations = part.get_locations()
    assert len(locations) == 1
    assert locations[0].to_tuple() == pytest.approx((0, 0, 1.01))


def test_transform_updates_cube_locations():
    part = cube(2, 2, 2)
    part.transform(relative=Location(x=1))
    top = CubeLocations.TOP_CENTER.to_location(part)
    assert top.to_tuple() == pytest.approx((1, 0, 1))
