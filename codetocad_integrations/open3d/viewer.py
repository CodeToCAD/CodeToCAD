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

from codetocad.location import Location
from codetocad.parts import Part3D
from codetocad.simulation import export_single_part, extract_links
from codetocad.topology import Edge, Face, Vertex

_DEFAULT_COLOR = (0.62, 0.66, 0.7)
#: Vivid accent for highlighted geometry, so it stands out against parts.
_HIGHLIGHT_COLOR = (1.0, 0.35, 0.0)


def to_mesh(part: Part3D) -> o3d.geometry.TriangleMesh:
    """Export ``part`` and load it as an Open3D ``TriangleMesh`` with
    computed vertex normals and the part's material color (if any)."""
    with tempfile.TemporaryDirectory(prefix="codetocad_open3d_") as tmp:
        path = Path(tmp) / f"{part.name or 'part'}.stl"
        export_single_part(part, str(path))
        mesh = o3d.io.read_triangle_mesh(str(path))
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color(_part_color(part))
    return mesh


def _assembly_meshes(part: Part3D) -> list[o3d.geometry.TriangleMesh]:
    """Meshes for ``part`` and every sub-part constrained to it (a whole
    assembly), each placed in its assembled position. A part with no
    constraints yields just itself."""
    try:
        links = extract_links(part)
    except Exception:
        # Not a walkable assembly (e.g. a custom part) -- show it as-is.
        return [to_mesh(part)]
    meshes = []
    for link in links:
        mesh = to_mesh(link.part)
        # Place the part in its assembled, initially-posed position (joint
        # starting angles rotate the sub-tree; identity when there are none).
        matrix = link.assembly_matrix
        if not np.allclose(matrix, np.eye(4)):
            mesh.transform(matrix)
        meshes.append(mesh)
    return meshes


def _part_color(part: Part3D) -> tuple[float, float, float]:
    material = getattr(part, "material", None)
    color_rgba = getattr(material, "color_rgba", None) if material else None
    return color_rgba.to_tuple()[:3] if color_rgba is not None else _DEFAULT_COLOR


def _scene_scale(geometries: list) -> float:
    """A characteristic length for sizing highlight markers: ~3% of the
    combined bounding-box diagonal (with a sane fallback for an empty scene)."""
    points = [
        np.asarray(g.vertices) for g in geometries if hasattr(g, "vertices")
    ]
    points = [p for p in points if len(p)]
    if not points:
        return 0.01
    stacked = np.concatenate(points)
    diagonal = float(np.linalg.norm(stacked.max(0) - stacked.min(0)))
    return max(diagonal * 0.03, 1e-3)


def _location_point(location: Location) -> np.ndarray:
    return np.array(location.to_tuple(), dtype=float)


def _sphere(center: np.ndarray, radius: float) -> o3d.geometry.TriangleMesh:
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    sphere.translate(center)
    sphere.compute_vertex_normals()
    sphere.paint_uniform_color(_HIGHLIGHT_COLOR)
    return sphere


def _segment(p0: np.ndarray, p1: np.ndarray, radius: float):
    """A thin cylinder spanning ``p0``-``p1`` (open3d lines ignore width, so a
    cylinder reads as a bold edge)."""
    vector = np.asarray(p1, float) - np.asarray(p0, float)
    length = float(np.linalg.norm(vector))
    if length < 1e-12:
        return _sphere((p0 + p1) / 2, radius)
    cylinder = o3d.geometry.TriangleMesh.create_cylinder(
        radius=radius, height=length
    )
    # create_cylinder is centered at the origin along +Z; align it to the edge.
    z = np.array([0.0, 0.0, 1.0])
    direction = vector / length
    rotation_axis = np.cross(z, direction)
    sin = float(np.linalg.norm(rotation_axis))
    cos = float(np.dot(z, direction))
    if sin > 1e-9:
        rotation_axis /= sin
        matrix = o3d.geometry.get_rotation_matrix_from_axis_angle(
            rotation_axis * np.arctan2(sin, cos)
        )
        cylinder.rotate(matrix, center=(0, 0, 0))
    elif cos < 0:
        cylinder.rotate(
            o3d.geometry.get_rotation_matrix_from_axis_angle((np.pi, 0, 0)),
            center=(0, 0, 0),
        )
    cylinder.translate((np.asarray(p0, float) + np.asarray(p1, float)) / 2)
    cylinder.compute_vertex_normals()
    cylinder.paint_uniform_color(_HIGHLIGHT_COLOR)
    return cylinder


def _highlight_geometries(items, scale: float) -> list:
    """Marker geometries for each highlighted Location/Vertex/Edge/Face:
    a sphere at a point, a bold cylinder for an edge, the outline plus centre
    for a face, and a coordinate triad (showing +Z) for an oriented
    Location."""
    if isinstance(items, (Location, Vertex, Edge, Face)):
        items = [items]
    geometries = []
    for item in items:
        if isinstance(item, Location):
            point = _location_point(item)
            geometries.append(_sphere(point, scale * 0.5))
            frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=scale * 3)
            quat = item.quat  # (x, y, z, w) -> open3d wants (w, x, y, z)
            frame.rotate(
                o3d.geometry.get_rotation_matrix_from_quaternion(
                    (quat[3], quat[0], quat[1], quat[2])
                ),
                center=(0, 0, 0),
            )
            frame.translate(point)
            geometries.append(frame)
        elif isinstance(item, Vertex):
            geometries.append(_sphere(_location_point(item.location), scale * 0.6))
        elif isinstance(item, Edge):
            geometries.append(
                _segment(
                    _location_point(item.start.location),
                    _location_point(item.end.location),
                    scale * 0.2,
                )
            )
        elif isinstance(item, Face):
            loop = [_location_point(v.location) for v in item.vertices]
            for start, end in zip(loop, loop[1:] + loop[:1]):
                geometries.append(_segment(start, end, scale * 0.2))
            geometries.append(_sphere(_location_point(item.center), scale * 0.4))
        else:
            raise TypeError(
                f"Cannot highlight {type(item).__name__}; pass a Location, "
                "Vertex, Edge or Face"
            )
    return geometries


def show(
    *parts: Part3D,
    window_name: str = "CodeToCAD",
    show_assemblies: bool = True,
    highlight: list[Location | Face | Edge | Vertex] | None = None,
) -> None:
    """Open an interactive Open3D window displaying one or more parts. Each
    part is expanded into its full assembly -- the part plus every sub-part
    joined to it by a constraint -- unless ``show_assemblies=False``.

    ``highlight`` is a list of ``Location``, ``Vertex``, ``Edge`` or ``Face``
    objects (e.g. from ``part.get_face(...)`` or a cube location) to overlay
    markers on, so you can see exactly where they land. A single object is
    also accepted."""
    geometries = []
    for part in parts:
        geometries.extend(
            _assembly_meshes(part) if show_assemblies else [to_mesh(part)]
        )
    if highlight is not None:
        geometries.extend(_highlight_geometries(highlight, _scene_scale(geometries)))
    o3d.visualization.draw_geometries(
        geometries,
        window_name=window_name,
        mesh_show_back_face=True,
    )


def render(
    *parts: Part3D,
    path: str,
    width: int = 1000,
    height: int = 800,
    background: tuple[float, float, float] = (0.6,0.6,0.6),
    front: tuple[float, float, float] = (0,0.5,0),
    up: tuple[float, float, float] = (0.0, 0.0, 0.5),
    zoom: float = 0.7,
    highlight: list[Location | Face | Edge | Vertex] | None = None,
) -> str:
    """Render one or more parts to a PNG with an offscreen Open3D window
    (nothing is shown on screen), viewed from an isometric-ish angle so
    surface relief (embossing, fillets, holes, ...) is visible. ``highlight``
    is a list of Location/Vertex/Edge/Face objects to overlay markers on (a
    single object is also accepted). Returns ``path``."""
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=width, height=height, visible=False)
    try:
        geometries = []
        for part in parts:
            geometries.extend(_assembly_meshes(part))
        if highlight is not None:
            geometries.extend(
                _highlight_geometries(highlight, _scene_scale(geometries))
            )
        for geometry in geometries:
            vis.add_geometry(geometry)
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
