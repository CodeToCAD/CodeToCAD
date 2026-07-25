"""Navigate a shape with ``CubeLocations`` + ``get_face``/``get_edge``/
``get_vertex``, and ``show(highlight=...)`` each result.

Every ``Part`` exposes the 27 topological locations of its bounding cube -- the
geometric center, 6 face centers, 12 edge midlines and 8 corners -- as
attributes (``cube.top_center``, ``cube.top_front``, ``cube.top_front_left``).
Feeding one to ``get_face``/``get_edge``/``get_vertex`` returns the matching
piece of topology, and ``show(highlight=[...])`` overlays a marker on it so you
can see exactly where it landed.

    # open an interactive window with one feature highlighted:
    codetocad cube_locations.py --show

    # (re)render the images used by cube_locations.md:
    codetocad cube_locations.py

Axis convention (see ``codetocad.CubeLocations``): +x is right, +y is back,
+z is top -- so -x is left, -y is front, -z is bottom. The little RGB triad in
each render is X=red, Y=green, Z=blue.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import open3d as o3d

import codetocad
from codetocad_integrations.open3d import render, show
from codetocad_integrations.open3d.viewer import _highlight_geometries

#: An intentionally asymmetric cube (x != y != z) so the six faces, twelve
#: edges and eight corners are all told apart at a glance.
CUBE_DIMENSIONS = ("60mm", "44mm", "32mm")  # length (x), width (y), height (z)

#: The canonical name of every face center, edge midline and corner. Each is
#: also an attribute on any part (lower-cased), e.g. ``cube.top_center``.
FACE_LOCATIONS = [
    "TOP_CENTER", "BOTTOM_CENTER",
    "FRONT_CENTER", "BACK_CENTER",
    "LEFT_CENTER", "RIGHT_CENTER",
]
EDGE_LOCATIONS = [
    "TOP_FRONT", "TOP_BACK", "TOP_LEFT", "TOP_RIGHT",
    "BOTTOM_FRONT", "BOTTOM_BACK", "BOTTOM_LEFT", "BOTTOM_RIGHT",
    "FRONT_LEFT", "FRONT_RIGHT", "BACK_LEFT", "BACK_RIGHT",
]
VERTEX_LOCATIONS = [
    "TOP_FRONT_LEFT", "TOP_FRONT_RIGHT", "TOP_BACK_LEFT", "TOP_BACK_RIGHT",
    "BOTTOM_FRONT_LEFT", "BOTTOM_FRONT_RIGHT",
    "BOTTOM_BACK_LEFT", "BOTTOM_BACK_RIGHT",
]


def new_cube() -> codetocad.Part3D:
    return codetocad.cube(*CUBE_DIMENSIONS)


def _wireframe(part: codetocad.Part3D) -> o3d.geometry.LineSet:
    """A see-through box outline built from the part's own twelve edges (via
    the public ``get_edge`` API), so a highlighted feature on a hidden face is
    never occluded by a solid mesh."""
    points, lines = [], []
    for name in EDGE_LOCATIONS:
        edge = part.get_edge(getattr(part, name.lower()))
        base = len(points)
        points.append(edge.start.location.to_tuple())
        points.append(edge.end.location.to_tuple())
        lines.append([base, base + 1])
    line_set = o3d.geometry.LineSet(
        o3d.utility.Vector3dVector(np.array(points)),
        o3d.utility.Vector2iVector(np.array(lines)),
    )
    line_set.paint_uniform_color((0.55, 0.6, 0.66))
    return line_set


def _marker_scale(part: codetocad.Part3D) -> float:
    """Marker size: ~3% of the bounding-box diagonal (matches ``show``)."""
    bbox_min, bbox_max = part.get_bounding_box()
    diagonal = float(np.linalg.norm(bbox_max.to_numpy() - bbox_min.to_numpy()))
    return max(diagonal * 0.03, 1e-3)


def _axes_triad(part: codetocad.Part3D) -> o3d.geometry.TriangleMesh:
    bbox_min, _ = part.get_bounding_box()
    scale = _marker_scale(part)
    triad = o3d.geometry.TriangleMesh.create_coordinate_frame(size=scale * 4)
    triad.translate(bbox_min.to_numpy() - scale * 2)
    return triad


def render_feature(part, feature, path: str) -> str:
    """Render the wireframe cube with ``feature`` (a Face/Edge/Vertex) marked
    in orange to ``path``, from a fixed isometric view."""
    geometries = [_wireframe(part), _axes_triad(part)]
    geometries += _highlight_geometries([feature], _marker_scale(part))
    visualizer = o3d.visualization.Visualizer()
    visualizer.create_window(width=760, height=620, visible=False)
    try:
        for geometry in geometries:
            visualizer.add_geometry(geometry)
        option = visualizer.get_render_option()
        option.background_color = np.array([0.1, 0.11, 0.14])
        option.mesh_show_back_face = True
        control = visualizer.get_view_control()
        control.set_front((1.0, -1.0, 0.55))
        control.set_up((0.0, 0.0, 1.0))
        control.set_zoom(0.95)
        visualizer.poll_events()
        visualizer.update_renderer()
        visualizer.capture_screen_image(path, do_render=True)
    finally:
        visualizer.destroy_window()
    return path


def render_guide(out_dir: str = "images") -> None:
    """(Re)generate every image referenced by ``cube_locations.md``."""
    directory = Path(__file__).parent / out_dir
    directory.mkdir(parents=True, exist_ok=True)
    cube = new_cube()
    groups = (
        ("face", FACE_LOCATIONS, cube.get_face),
        ("edge", EDGE_LOCATIONS, cube.get_edge),
        ("vertex", VERTEX_LOCATIONS, cube.get_vertex),
    )
    for kind, names, query in groups:
        for name in names:
            feature = query(getattr(cube, name.lower()))
            path = directory / f"cube_{kind}_{name.lower()}.png"
            render_feature(cube, feature, str(path))
            print(f"wrote {path.name}")


def demo_interactive() -> None:
    """Open an interactive Open3D window per feature -- the everyday workflow.
    ``show(highlight=...)`` accepts a single object or a list of them."""
    cube = new_cube()

    top_face = cube.get_face(cube.top_center)      # the +z face
    top_right_edge = cube.get_edge(cube.top_right)  # the +z / +x edge midline
    corner = cube.get_vertex(cube.top_front_right)  # the +z / -y / +x corner

    show(cube, highlight=[top_face])
    show(cube, highlight=[top_right_edge])
    show(cube, highlight=[corner])
    # ...or all at once, alongside the raw location markers (sphere + normal):
    show(cube, highlight=[top_face, top_right_edge, corner, cube.center])


if __name__ == "__main__":
    if "--show" in sys.argv:
        demo_interactive()
    else:
        render_guide()
