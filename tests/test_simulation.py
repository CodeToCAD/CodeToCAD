import math

import pytest

from codetocad import Lighting, Location, cube, cylinder, extract_links, sphere
from codetocad.simulation import ensure_binary_stl


def build_pendulum():
    mount = cube("6cm", "6cm", "4cm", start_location=Location(z="52cm"))
    mount.name = "mount"
    rod = cylinder("1cm", "40cm", start_location=Location(z="30cm"))
    rod.name = "rod"
    bob = sphere("5cm", start_location=Location(z="10cm"))
    bob.name = "bob"
    pivot = Location.from_euler(0, 0, "50cm", x_deg=-90, name="pivot")
    mount.revolute(pivot, rod, pivot)
    rod.fixed(Location(z="10cm"), bob, Location(z="10cm"))
    return mount


def test_constraints_recorded_in_operations():
    mount = build_pendulum()
    kinds = [op["operation"] for op in mount.operations]
    assert kinds == ["revolute"]
    assert mount.operations[0]["other_part"].name == "rod"


def test_extract_links_tree():
    links = extract_links(build_pendulum())
    assert [link.name for link in links] == ["mount", "rod", "bob"]
    rod = links[1]
    assert rod.parent.name == "mount"
    assert rod.joint.joint_type == "revolute"
    assert rod.joint.name == "pivot"
    # Anchor at the pivot; axis rotated from Z onto Y by x_deg=-90.
    assert rod.frame == pytest.approx((0, 0, 0.5))
    assert rod.joint.axis == pytest.approx((0, 1, 0), abs=1e-9)
    bob = links[2]
    assert bob.joint.joint_type == "fixed"
    assert bob.parent.name == "rod"


def test_link_mass_and_inertia():
    links = extract_links(build_pendulum())
    rod = links[1]
    # No material: water density fallback = volume * 1000.
    assert rod.mass == pytest.approx(math.pi * 0.01**2 * 0.4 * 1000)
    assert all(value > 0 for value in rod.inertia_diagonal)
    assert rod.center_of_mass == pytest.approx((0, 0, 0.3))


def test_joint_limits_extracted():
    base = cube(1, 1, 1)
    arm = cylinder(0.1, 1)
    base.revolute(
        Location(z=0.5, name="j1"), arm, Location(z=0.5),
        min_limits=-1.5, max_limits=1.5,
    )
    links = extract_links(base)
    assert links[1].joint.lower == -1.5
    assert links[1].joint.upper == 1.5


def test_build_urdf_and_mjcf_documents():
    from codetocad_integrations.mujoco import build_mjcf
    from codetocad_integrations.pybullet import build_urdf

    links = extract_links(build_pendulum())
    for link in links:
        link.mesh_path = f"/tmp/assets/{link.name}.stl"

    urdf = build_urdf(links, name="pendulum")
    assert '<robot name="pendulum">' in urdf
    assert '<joint name="pivot" type="continuous">' in urdf
    assert '<axis xyz="0 1 0"' in urdf
    assert urdf.count("<link") == 3

    mjcf = build_mjcf(links, name="pendulum", actuated=False)
    assert '<body name="rod" pos="0 0 0.5">' in mjcf
    assert 'type="hinge"' in mjcf
    assert "<actuator>" not in mjcf
    mjcf_actuated = build_mjcf(links, name="pendulum", actuated=True)
    assert '<position name="pivot_actuator" joint="pivot"' in mjcf_actuated


def test_lighting_defaults():
    light = Lighting(color=(1.0, 0.5, 0.0), intensity=0.5)
    assert light.diffuse == pytest.approx((0.5, 0.25, 0.0))


def test_ensure_binary_stl(tmp_path):
    path = tmp_path / "box.stl"
    cube(0.1, 0.1, 0.1).export(str(path))
    assert path.read_bytes().startswith(b"solid")
    ensure_binary_stl(path)
    content = path.read_bytes()
    assert not content.startswith(b"solid")
    triangle_count = int.from_bytes(content[80:84], "little")
    assert triangle_count == 12
    ensure_binary_stl(path)  # idempotent on binary files
    assert path.read_bytes() == content


def test_geometry_backends_skip_constraints():
    pytest.importorskip("build123d")
    from codetocad_integrations.build123d import make_cube, make_cylinder

    base = make_cube("10cm", "10cm", "4cm")
    arm = make_cylinder("1cm", "10cm", start_location=Location(z="9cm"))
    base.revolute(Location(z="4cm", name="j1"), arm, Location(z="4cm"))
    # Building geometry must not choke on the constraint operation.
    assert base.get_volume() == pytest.approx(0.1 * 0.1 * 0.04)
