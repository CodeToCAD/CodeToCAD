import numpy as np
import pytest

from codetocad import Location, cube

pytest.importorskip("open3d")

import codetocad_integrations.open3d.viewer as viewer


def _assembly():
    base = cube(0.2, 0.2, 0.2, Location())
    base.name = "base"
    arm = cube(0.4, 0.1, 0.1, Location(x=1.0))
    arm.name = "arm"
    base.fixed(base.right_center, arm, arm.left_center)
    return base, arm


def test_show_expands_assembly_into_sub_parts():
    base, _arm = _assembly()
    meshes = viewer._assembly_meshes(base)
    # Root plus the one constrained sub-part.
    assert len(meshes) == 2
    # The arm mesh is placed in its snapped assembly position (centre near x=0.3).
    centers = sorted(float(np.asarray(m.vertices).mean(0)[0]) for m in meshes)
    assert centers[0] == pytest.approx(0.0, abs=1e-6)
    assert centers[1] == pytest.approx(0.3, abs=1e-6)


def test_plain_part_shows_just_itself():
    assert len(viewer._assembly_meshes(cube(1, 1, 1))) == 1


def test_highlight_geometries_for_each_type():
    part = cube(1, 1, 1)
    scale = 0.1
    assert len(viewer._highlight_geometries(part.top_center, scale)) == 2  # sphere+triad
    assert len(viewer._highlight_geometries(part.get_vertex(part.top_back_right), scale)) == 1
    assert len(viewer._highlight_geometries(part.get_edge(part.top_front), scale)) == 1
    # A quad face: 4 boundary segments + centre marker.
    assert len(viewer._highlight_geometries(part.get_face(part.top_center), scale)) == 5


def test_highlight_rejects_unknown_type():
    with pytest.raises(TypeError):
        viewer._highlight_geometries([object()], 0.1)
