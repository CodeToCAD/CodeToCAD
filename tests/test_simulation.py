import math

import numpy as np
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


def test_other_location_snaps_child_into_place():
    # Parent at the origin; child modeled a metre away. The constraint
    # snaps the child so its left face meets the parent's right face.
    base = cube(0.2, 0.2, 0.2, start_location=Location())
    base.name = "base"
    arm = cube(0.4, 0.1, 0.1, start_location=Location(x=1.0))
    arm.name = "arm"
    base.fixed(base.right_center, arm, arm.left_center)

    arm_link = extract_links(base)[1]
    # Kinematic frame sits at the parent's location (the joint anchor)...
    assert arm_link.frame == pytest.approx((0.1, 0, 0))
    # ...while the geometry attaches at the child's other_location.
    assert arm_link.mesh_frame == pytest.approx((0.8, 0, 0))
    assert arm_link.shift == pytest.approx((-0.7, 0, 0))
    # The assembled arm centre lands so the faces touch at x=0.1.
    assert (arm_link.center_of_mass + arm_link.shift) == pytest.approx((0.3, 0, 0))


def test_resolve_joint_by_name_or_child_part():
    from codetocad.simulation import Simulation

    base = cube(0.2, 0.2, 0.2)
    base.name = "base"
    arm = cylinder(0.02, 0.4)
    arm.name = "arm"
    base.revolute(Location(z=0.1, name="shoulder"), arm, Location(z=0.1))
    sim = Simulation(base)
    # A joint name passes through; the joined child part resolves to it.
    assert sim._resolve_joint_name("shoulder") == "shoulder"
    assert sim._resolve_joint_name(arm) == "shoulder"
    with pytest.raises(KeyError, match="movable joint"):
        sim._resolve_joint_name(base)


def test_simulation_common_params_stored_on_base():
    from codetocad.simulation import Simulation

    sim = Simulation(cube(1, 1, 1), ground_plane=True)
    assert sim.ground_plane is True
    assert sim.output_dir.exists()  # a temp dir was resolved by the base


def test_other_location_default_is_backward_compatible():
    # location == other_location (every part modeled in place) => no shift,
    # and geometry attaches at the kinematic frame as before.
    for link in extract_links(build_pendulum()):
        assert link.shift == pytest.approx((0, 0, 0))
        assert link.mesh_frame == pytest.approx(tuple(link.frame))


def test_starting_angle_bakes_into_assembly_pose():
    # A revolute joint's starting_angle rotates the child sub-tree about the
    # joint anchor for geometry export/preview (simulation applies it as
    # joint state instead, so shift/mesh_frame stay put).
    base = cube(0.2, 0.2, 0.2, start_location=Location(z=0.1))
    base.name = "base"
    arm = cube(0.05, 0.05, 0.4, start_location=Location(z=0.4))
    arm.name = "arm"
    pivot = Location.from_euler(0, 0, 0.2, x_deg=-90, name="hinge")  # axis -> Y
    base.revolute(pivot, arm, pivot, starting_angle="90deg")

    arm_link = extract_links(base)[1]
    matrix = arm_link.assembly_matrix
    # The arm's modeled centre (0, 0, 0.4), 0.2 above the pivot, swings out to
    # +X at pivot height when the hinge opens 90deg about Y.
    center = matrix @ np.array([0.0, 0.0, 0.4, 1.0])
    assert center[:3] == pytest.approx((0.2, 0.0, 0.2), abs=1e-6)
    # shift alone (the simulation placement) is unchanged.
    assert arm_link.shift == pytest.approx((0, 0, 0))


def test_no_starting_angle_pose_reduces_to_shift():
    # Without any starting values, the assembly pose is a pure translation by
    # shift (identity rotation) -- backward compatible with the old behaviour.
    for link in extract_links(build_pendulum()):
        assert link.pose_rotation == pytest.approx((0, 0, 0, 1))
        assert link.pose_offset == pytest.approx(tuple(link.shift))
        assert link.assembly_matrix[:3, 3] == pytest.approx(tuple(link.shift))


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
