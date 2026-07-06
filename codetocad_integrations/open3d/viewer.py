"""Convert any CodeToCAD Part3D to an Open3D mesh and display/render it.

Open3D isn't a CAD kernel, so unlike the Build123D/Blender adapters this
doesn't replay booleans/fillets/etc. Any Part3D federated by one of those
(or a plain core part) is exported to a temporary mesh file and loaded as
an Open3D ``TriangleMesh``.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import open3d as o3d

from codetocad.parts import Part3D

_DEFAULT_COLOR = (0.62, 0.66, 0.7)


def to_mesh(part: Part3D) -> o3d.geometry.TriangleMesh:
    """Export ``part`` and load it as an Open3D ``TriangleMesh`` with
    computed vertex normals and the part's material color (if any)."""
    with tempfile.TemporaryDirectory(prefix="codetocad_open3d_") as tmp:
        path = Path(tmp) / f"{part.name or 'part'}.stl"
        part.export(str(path))
        mesh = o3d.io.read_triangle_mesh(str(path))
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color(_part_color(part))
    return mesh


def _part_color(part: Part3D) -> tuple[float, float, float]:
    material = getattr(part, "material", None)
    color_rgba = getattr(material, "color_rgba", None) if material else None
    return color_rgba.to_tuple()[:3] if color_rgba is not None else _DEFAULT_COLOR


def show(*parts: Part3D, window_name: str = "CodeToCAD") -> None:
    """Open an interactive Open3D window displaying one or more parts."""
    o3d.visualization.draw_geometries(
        [to_mesh(part) for part in parts],
        window_name=window_name,
        mesh_show_back_face=True,
    )


def render(
    *parts: Part3D,
    path: str,
    width: int = 1000,
    height: int = 800,
    background: tuple[float, float, float] = (0.97, 0.97, 0.98),
    front: tuple[float, float, float] = (-0.5, -0.75, 0.65),
    up: tuple[float, float, float] = (0.0, 0.0, 1.0),
    zoom: float = 0.7,
) -> str:
    """Render one or more parts to a PNG with an offscreen Open3D window
    (nothing is shown on screen), viewed from an isometric-ish angle so
    surface relief (embossing, fillets, holes, ...) is visible. Returns
    ``path``."""
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=width, height=height, visible=False)
    try:
        for part in parts:
            vis.add_geometry(to_mesh(part))
        opt = vis.get_render_option()
        opt.background_color = np.asarray(background)
        opt.mesh_show_back_face = True
        opt.mesh_shade_option = o3d.visualization.MeshShadeOption.Color
        ctr = vis.get_view_control()
        ctr.set_front(front)
        ctr.set_up(up)
        ctr.set_zoom(zoom)
        vis.poll_events()
        vis.update_renderer()
        vis.capture_screen_image(path, do_render=True)
    finally:
        vis.destroy_window()
    return path
