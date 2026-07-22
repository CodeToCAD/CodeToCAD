import math

import numpy as np
import pytest

import codetocad
from codetocad import Location, cube, cylinder, sphere
from codetocad.drawings import (
    STANDARD_VIEWS,
    Drawing,
    drawing_edges,
    drawing_from_meshes,
)


def _view(drawing, name):
    return next(view for view in drawing.views if view.name == name)


def test_generate_drawing_returns_editable_part2d():
    drawing = cube(1, 1, 1).generate_drawing()
    assert isinstance(drawing, codetocad.Part2D)
    assert drawing._primitive["kind"] == "drawing"
    # It is a real sketch: editable (transform) with a sensible bounding box.
    bbox_min, bbox_max = drawing.get_bounding_box()
    assert bbox_max.x > bbox_min.x and bbox_max.y > bbox_min.y
    drawing.transform(relative=Location(x=1))
    shifted_min, _ = drawing.get_bounding_box()
    assert shifted_min.x == pytest.approx(bbox_min.x + 1)


def test_generate_drawing_writes_svg(tmp_path):
    destination = tmp_path / "part.svg"
    # The shortcut location= writes the sheet and still returns the Part2D.
    drawing = cube(1, 1, 1).generate_drawing(str(destination))
    assert isinstance(drawing, codetocad.Part2D)
    content = destination.read_text()
    assert content.startswith("<svg")
    assert content.rstrip().endswith("</svg>")
    for label in ("FRONT", "TOP", "RIGHT", "ISO"):
        assert f">{label}</text>" in content


def test_part2d_drawing_exports_svg(tmp_path):
    destination = tmp_path / "sketch.svg"
    drawing = cube(2, 1, 1).generate_drawing()
    assert drawing.export(str(destination)) == str(destination)
    assert destination.read_text().startswith("<svg")
    # Only SVG makes sense for a drawing sheet.
    with pytest.raises(ValueError):
        drawing.export(str(tmp_path / "sketch.stl"))


def test_orthographic_views_measure_the_right_axes():
    # A 2 (X) x 1 (Y) x 0.5 (Z) box: each view shows the two axes in its plane.
    drawing = drawing_from_meshes(
        [cube(2, 1, 0.5)._generate_mesh()], "box", views=("front", "top", "right")
    )
    front, top, right = (_view(drawing, n) for n in ("front", "top", "right"))
    assert (front.width, front.height) == pytest.approx((2.0, 0.5))  # X, Z
    assert (top.width, top.height) == pytest.approx((2.0, 1.0))  # X, Y
    assert (right.width, right.height) == pytest.approx((1.0, 0.5))  # Y, Z
    assert drawing.overall == pytest.approx((2.0, 1.0, 0.5))


def test_cube_edges_are_the_twelve_creases():
    # Every cube edge is a 90-degree crease, drawn in every view.
    edges = drawing_edges(cube(1, 1, 1)._generate_mesh(), np.array([0.0, -1.0, 0.0]))
    assert len(edges) == 12


def test_sphere_reads_as_a_circle_in_every_view():
    # A sphere has no creases: only its per-view silhouette is drawn, and it is
    # the same size (a great circle) whichever way you look.
    drawing = drawing_from_meshes([sphere(0.5)._generate_mesh()], "ball")
    for view in drawing.views:
        assert len(view.segments) > 0
    for name in ("front", "top", "right"):
        view = _view(drawing, name)
        assert view.width == pytest.approx(1.0, abs=0.05)
        assert view.height == pytest.approx(1.0, abs=0.05)


def test_crease_angle_controls_tessellation_edges():
    # A cylinder's side facets meet at shallow angles: the default keeps them
    # out, a tiny crease angle lets them all in.
    mesh = cylinder(0.5, 1.0)._generate_mesh()
    view_dir = np.array([0.0, -1.0, 0.0])
    default = drawing_edges(mesh, view_dir)
    fine = drawing_edges(mesh, view_dir, crease_angle=math.radians(1.0))
    assert len(fine) > len(default)


def test_drawing_includes_the_whole_assembly(tmp_path):
    holder = cube(1, 1, 1)
    lid = cube(1, 1, 0.2, start_location=Location(z=0.6))
    hinge = Location(0, -0.5, 0.5)
    holder.revolute(hinge, lid, hinge)

    together = drawing_from_meshes(
        holder._assembly_meshes(include_assembly=True), "asm"
    )
    alone = drawing_from_meshes(
        holder._assembly_meshes(include_assembly=False), "asm"
    )
    # The lid adds geometry, so the assembly drawing has more segments and a
    # taller front view than the holder alone.
    assert len(_view(together, "front").segments) > len(
        _view(alone, "front").segments
    )
    assert _view(together, "front").height > _view(alone, "front").height

    destination = tmp_path / "assembly.svg"
    holder.generate_drawing(str(destination), include_assembly=False)
    assert destination.read_text().startswith("<svg")


def test_generate_drawing_from_any_part_in_the_assembly(tmp_path):
    # "Any Part3D even if it is an assembly": the root or a child both draw.
    base = cube(1, 1, 1)
    arm = cylinder(0.2, 1.0, start_location=Location(z=1.0))
    base.fixed(Location(z=0.5), arm, Location(z=-0.5))
    for part, name in ((base, "from_base.svg"), (arm, "from_arm.svg")):
        drawing = part.generate_drawing(str(tmp_path / name))
        assert isinstance(drawing, codetocad.Part2D)
        assert (tmp_path / name).read_text().startswith("<svg")


def test_custom_view_selection():
    drawing = drawing_from_meshes([cube(1, 1, 1)._generate_mesh()], "c", views=("iso",))
    assert [view.name for view in drawing.views] == ["iso"]
    assert all(name in STANDARD_VIEWS for name in ("front", "top", "right", "iso"))


def test_part_without_meshable_geometry_is_rejected(tmp_path):
    with pytest.raises(NotImplementedError):
        codetocad.Part3D().generate_drawing(str(tmp_path / "blank.svg"))


def test_drawing_is_exposed_from_the_package():
    assert codetocad.Drawing is Drawing
    assert isinstance(drawing_from_meshes([], "empty"), Drawing)
