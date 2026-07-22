"""Generate 2D technical (CAD) drawings from a Part3D or a whole assembly.

A drawing projects a part's mesh into standard orthographic views (front, top,
right) plus an isometric view and lays them out on an SVG sheet. It works for a
single part or a whole assembly interchangeably: the assembled member meshes
are projected together -- exactly the geometry that ``Part3D.export()`` writes
to STL -- so ``part.generate_drawing(...)`` draws the same thing it would
export.

Each solid is drawn from two families of edges:

* *feature edges* -- sharp creases (a dihedral angle steeper than
  ``crease_angle``) and open boundary edges. These are view-independent, so
  they appear in every view. A cube's twelve edges are feature edges; a
  cylinder's two rim circles are feature edges.
* *silhouette edges* -- for the view direction, the edges where the surface
  turns away from the viewer (one adjoining face points toward the camera, the
  other away). These trace the smooth outline of curved surfaces: the straight
  sides of a cylinder seen from the front, the circle of a sphere.

Together they give clean line drawings without a CAD kernel: a box reads as a
rectangle, a cylinder as a rectangle from the side and a circle from the end, a
sphere as a circle in every view. Every edge is drawn as a visible solid line
-- there is no hidden-line removal, so edges behind the solid are not dashed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from html import escape
from pathlib import Path

import numpy as np

#: Named orthographic/pictorial views as ``(camera_direction, page_up)``, both
#: world vectors. ``camera_direction`` points from the object toward the camera
#: (so ``front`` looks along +Y from the -Y side); ``page_up`` is the world
#: direction drawn upward on the page. Right-handed screen axes are derived from
#: these, so all views share a single projection routine.
STANDARD_VIEWS: dict[str, tuple[tuple[float, float, float], tuple[float, float, float]]] = {
    "front": ((0.0, -1.0, 0.0), (0.0, 0.0, 1.0)),
    "back": ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    "top": ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
    "bottom": ((0.0, 0.0, -1.0), (0.0, 1.0, 0.0)),
    "right": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
    "left": ((-1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
    "iso": ((1.0, 1.0, 1.0), (0.0, 0.0, 1.0)),
}

#: The default sheet: the three principal orthographic views plus an isometric.
DEFAULT_VIEWS = ("front", "top", "right", "iso")

_DEFAULT_CREASE_ANGLE = math.radians(15.0)

# -- geometry: projection and edge extraction --


def _view_basis(
    camera_direction, page_up
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Right-handed screen basis ``(right, up, view_dir)`` for a camera looking
    at the object from ``camera_direction`` with ``page_up`` drawn upward.
    ``right`` and ``up`` span the picture plane; ``view_dir`` points at the
    camera. Falls back to a sensible up when ``page_up`` is parallel to the
    view direction."""
    view_dir = np.asarray(camera_direction, dtype=float)
    view_dir = view_dir / np.linalg.norm(view_dir)
    up = np.asarray(page_up, dtype=float)
    right = np.cross(up, view_dir)
    magnitude = float(np.linalg.norm(right))
    if magnitude < 1e-9:
        # page_up is (anti)parallel to the view; pick any other up direction.
        alternate = (1.0, 0.0, 0.0) if abs(view_dir[0]) < 0.9 else (0.0, 1.0, 0.0)
        right = np.cross(alternate, view_dir)
        magnitude = float(np.linalg.norm(right))
    right = right / magnitude
    screen_up = np.cross(view_dir, right)
    return right, screen_up, view_dir


def _mesh_topology(
    triangles: np.ndarray, tol: float = 1e-7
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Weld a triangle soup into ``(points, faces, normals)``: unique vertex
    positions, triangles as vertex-index triples, and unit face normals.
    Vertices closer than ``tol`` (meters) are merged so shared edges are found
    across neighbouring triangles."""
    vertices = triangles.reshape(-1, 3)
    keys = np.round(vertices / tol).astype(np.int64)
    _unique, first_index, inverse = np.unique(
        keys, axis=0, return_index=True, return_inverse=True
    )
    points = vertices[first_index]
    faces = inverse.reshape(-1, 3)
    v0, v1, v2 = points[faces[:, 0]], points[faces[:, 1]], points[faces[:, 2]]
    normals = np.cross(v1 - v0, v2 - v0)
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.where(lengths == 0, 1.0, lengths)
    return points, faces, normals


def _edge_faces(faces: np.ndarray) -> dict[tuple[int, int], list[int]]:
    """Map each undirected edge (a sorted vertex-index pair) to the indices of
    the faces that use it."""
    edges: dict[tuple[int, int], list[int]] = {}
    for face_index, (a, b, c) in enumerate(faces.tolist()):
        for start, end in ((a, b), (b, c), (c, a)):
            key = (start, end) if start < end else (end, start)
            edges.setdefault(key, []).append(face_index)
    return edges


def drawing_edges(
    triangles: np.ndarray,
    view_dir: np.ndarray,
    crease_angle: float = _DEFAULT_CREASE_ANGLE,
) -> np.ndarray:
    """The 3D line segments to draw for ``triangles`` seen along ``view_dir``:
    feature edges (creases sharper than ``crease_angle`` and open boundaries)
    plus the view's silhouette edges. Returns an ``(N, 2, 3)`` array of segment
    endpoints (empty ``(0, 2, 3)`` for an empty mesh)."""
    if triangles is None or len(triangles) == 0:
        return np.zeros((0, 2, 3))
    points, faces, normals = _mesh_topology(triangles)
    edges = _edge_faces(faces)
    direction = np.asarray(view_dir, dtype=float)
    direction = direction / np.linalg.norm(direction)
    cos_threshold = math.cos(crease_angle)
    facing = normals @ direction
    segments: list[tuple[int, int]] = []
    for (start, end), adjacent in edges.items():
        if len(adjacent) != 2:
            draw = True  # open boundary or non-manifold edge
        else:
            first, second = adjacent
            crease = float(normals[first] @ normals[second]) < cos_threshold
            silhouette = facing[first] * facing[second] < 0.0
            draw = crease or silhouette
        if draw:
            segments.append((start, end))
    if not segments:
        return np.zeros((0, 2, 3))
    index = np.array(segments)
    return np.stack([points[index[:, 0]], points[index[:, 1]]], axis=1)


# -- assembled drawing --


@dataclass
class View:
    """One projected view: its name and its 2D line segments, in projection
    meters ``(u, v)`` with ``u`` rightward and ``v`` upward."""

    name: str
    segments: np.ndarray  # (N, 2, 2)

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """``(u_min, u_max, v_min, v_max)`` of the drawn segments (a unit box
        when the view is empty)."""
        if len(self.segments) == 0:
            return (0.0, 1.0, 0.0, 1.0)
        points = self.segments.reshape(-1, 2)
        return (
            float(points[:, 0].min()),
            float(points[:, 0].max()),
            float(points[:, 1].min()),
            float(points[:, 1].max()),
        )

    @property
    def width(self) -> float:
        u_min, u_max, _, _ = self.bounds
        return u_max - u_min

    @property
    def height(self) -> float:
        _, _, v_min, v_max = self.bounds
        return v_max - v_min


@dataclass
class Drawing:
    """A set of projected views of one part or assembly, renderable to SVG."""

    name: str
    views: list[View]
    overall: tuple[float, float, float]  # bounding-box size (X, Y, Z) in meters

    def to_svg(self, sheet_width: int = 1123, sheet_height: int = 794) -> str:
        """Render the views to an SVG sheet (A4 landscape at 96dpi by default),
        laid out in third-angle arrangement with a border, per-view labels,
        overall dimensions on the front view and a title block."""
        return _render_svg(self, sheet_width, sheet_height)

    def layout_segments(self) -> np.ndarray:
        """Every view's line segments placed in the sheet layout, in meters
        with ``y`` pointing up -- the drawing's 2D geometry, free of any SVG
        styling. Returns an ``(N, 2, 2)`` array. This is what a ``Part2D``
        carrying the drawing exposes for editing or for a backend to rebuild as
        native curves."""
        gap = _layout_gap(self.views)
        placements = _view_placements(self.views, gap)
        pieces: list[np.ndarray] = []
        for view in self.views:
            if len(view.segments) == 0:
                continue
            offset_x, offset_y = placements[view.name]
            u_min, _, v_min, _ = view.bounds
            shifted = view.segments.copy()
            shifted[..., 0] += offset_x - u_min
            shifted[..., 1] += offset_y - v_min
            pieces.append(shifted)
        return np.concatenate(pieces) if pieces else np.zeros((0, 2, 2))

    def to_part2d(self, name: str | None = None):
        """Wrap this drawing in a :class:`~codetocad.parts.Part2D` (primitive
        kind ``"drawing"``), so it can be edited like any sketch and exported
        with ``part.export("sheet.svg")``. ``name`` overrides the drawing's own
        name for the part and its title block."""
        from codetocad.parts import Part2D

        part = Part2D(name=name or self.name)
        part._primitive = {"kind": "drawing", "drawing": self}
        return part

    def export_svg(self, location: str, name: str | None = None) -> str:
        """Write the SVG sheet to ``location`` (which must end in ``.svg``).
        ``name`` updates the title block first."""
        if name:
            self.name = name
        suffix = Path(location).suffix.lower()
        if suffix != ".svg":
            raise ValueError(
                f"A drawing exports to an .svg sheet, not {suffix!r}"
            )
        Path(location).write_text(self.to_svg(), encoding="utf-8")
        return location


def drawing_from_meshes(
    meshes: list[np.ndarray],
    name: str,
    views=DEFAULT_VIEWS,
    crease_angle: float = _DEFAULT_CREASE_ANGLE,
) -> Drawing:
    """Build a :class:`Drawing` by projecting each mesh in ``meshes`` (each an
    ``(N, 3, 3)`` triangle array, already in assembled world position) into
    every named view. Edges are found per mesh, so separate assembly members
    never share false edges."""
    view_names = list(views)
    built: list[View] = []
    for view_name in view_names:
        camera = STANDARD_VIEWS[view_name]
        right, screen_up, view_dir = _view_basis(*camera)
        projected: list[np.ndarray] = []
        for triangles in meshes:
            edges = drawing_edges(triangles, view_dir, crease_angle)
            if len(edges) == 0:
                continue
            points = edges.reshape(-1, 3)
            uv = np.column_stack([points @ right, points @ screen_up])
            projected.append(uv.reshape(-1, 2, 2))
        segments = (
            np.concatenate(projected) if projected else np.zeros((0, 2, 2))
        )
        built.append(View(view_name, segments))
    if meshes:
        all_points = np.concatenate([mesh.reshape(-1, 3) for mesh in meshes])
        overall = tuple((all_points.max(axis=0) - all_points.min(axis=0)).tolist())
    else:
        overall = (0.0, 0.0, 0.0)
    return Drawing(name=name, views=built, overall=overall)


# -- SVG rendering --

_MARGIN = 28  # sheet border inset, px
_TITLE_HEIGHT = 60  # title block height, px
_GAP_FRACTION = 0.18  # gap between views, as a fraction of the largest extent
_LABEL_OFFSET = 18  # gap between a view and its label, px
_DIM_OFFSET = 48  # gap between the front view and its dimension lines, px


def _format_length(meters: float) -> str:
    """A tidy length label: millimeters below one meter, meters above."""
    if abs(meters) < 1.0:
        text = f"{meters * 1000:.1f}".rstrip("0").rstrip(".")
        return f"{text} mm"
    return f"{meters:.4g} m"


def _layout_gap(views: list[View]) -> float:
    """The spacing between views: a fraction of the largest view extent."""
    largest = max((max(v.width, v.height) for v in views), default=1.0) or 1.0
    return _GAP_FRACTION * largest


def _view_placements(
    views: list[View], gap: float
) -> dict[str, tuple[float, float]]:
    """Offset (in projection meters, y-up) of each view's ``(u_min, v_min)``
    corner. The standard views take a third-angle arrangement (top above front,
    right to the right of front, isometric upper-right); anything else flows to
    the right. Offsets are normalised so the smallest corner sits at (0, 0)."""
    size = {view.name: (view.width, view.height) for view in views}
    names = [view.name for view in views]
    placed: dict[str, tuple[float, float]] = {}
    if "front" in names:
        front_w, front_h = size["front"]
        placed["front"] = (0.0, 0.0)
        if "top" in names:
            placed["top"] = (0.0, front_h + gap)
        if "right" in names:
            placed["right"] = (front_w + gap, 0.0)
        if "iso" in names:
            placed["iso"] = (front_w + gap, front_h + gap)
    # Flow any views not placed above into a row to the right of everything.
    cursor = max((x + size[n][0] for n, (x, _) in placed.items()), default=0.0)
    for view in views:
        if view.name in placed:
            continue
        cursor += gap
        placed[view.name] = (cursor, 0.0)
        cursor += size[view.name][0]
    min_x = min(x for x, _ in placed.values())
    min_y = min(y for _, y in placed.values())
    return {n: (x - min_x, y - min_y) for n, (x, y) in placed.items()}


def _render_svg(drawing: Drawing, sheet_width: int, sheet_height: int) -> str:
    views = drawing.views
    gap = _layout_gap(views)
    placements = _view_placements(views, gap)

    content_w_m = max(
        (placements[v.name][0] + v.width for v in views), default=1.0
    ) or 1.0
    content_h_m = max(
        (placements[v.name][1] + v.height for v in views), default=1.0
    ) or 1.0

    # Fit the layout into the sheet, leaving room for the border, dimension
    # lines and the title block.
    area_left = _MARGIN + _DIM_OFFSET + 12
    area_right = sheet_width - _MARGIN - 12
    area_top = _MARGIN + 12
    area_bottom = sheet_height - _MARGIN - _TITLE_HEIGHT - _DIM_OFFSET - 12
    scale = min(
        (area_right - area_left) / content_w_m,
        (area_bottom - area_top) / content_h_m,
    )
    content_h_px = content_h_m * scale
    view_bounds = {view.name: view.bounds for view in views}

    def to_px(view: View, u: float, v: float) -> tuple[float, float]:
        offset_x, offset_y = placements[view.name]
        u_min, _, v_min, _ = view_bounds[view.name]
        x = area_left + (offset_x + (u - u_min)) * scale
        # Flip v: SVG's y axis points down.
        y = area_top + content_h_px - (offset_y + (v - v_min)) * scale
        return x, y

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sheet_width}" '
        f'height="{sheet_height}" viewBox="0 0 {sheet_width} {sheet_height}" '
        f'font-family="sans-serif">',
        f'<rect x="0" y="0" width="{sheet_width}" height="{sheet_height}" '
        f'fill="white"/>',
        f'<rect x="{_MARGIN}" y="{_MARGIN}" '
        f'width="{sheet_width - 2 * _MARGIN}" '
        f'height="{sheet_height - 2 * _MARGIN}" fill="none" stroke="black" '
        f'stroke-width="1.5"/>',
    ]

    for view in views:
        commands: list[str] = []
        for (u0, v0), (u1, v1) in view.segments.tolist():
            x0, y0 = to_px(view, u0, v0)
            x1, y1 = to_px(view, u1, v1)
            commands.append(f"M{x0:.2f} {y0:.2f}L{x1:.2f} {y1:.2f}")
        if commands:
            parts.append(
                f'<path d="{"".join(commands)}" fill="none" stroke="black" '
                f'stroke-width="1"/>'
            )
        u_min, u_max, v_min, _ = view.bounds
        center_x, _ = to_px(view, (u_min + u_max) / 2, v_min)
        _, label_y = to_px(view, u_min, v_min)
        parts.append(
            f'<text x="{center_x:.2f}" y="{label_y + _LABEL_OFFSET:.2f}" '
            f'text-anchor="middle" font-size="13" '
            f'fill="black">{view.name.upper()}</text>'
        )

    parts.extend(_front_dimensions(drawing, to_px, area_left, scale))
    parts.append(_title_block(drawing, sheet_width, sheet_height))
    parts.append("</svg>")
    return "\n".join(parts)


def _front_dimensions(drawing: Drawing, to_px, area_left: float, scale: float):
    """Overall width and height dimension lines along the outer (bottom and
    left) edges of the front view. Returns an empty list when there is no
    front view."""
    front = next((v for v in drawing.views if v.name == "front"), None)
    if front is None or len(front.segments) == 0:
        return []
    u_min, u_max, v_min, v_max = front.bounds
    left_x, bottom_y = to_px(front, u_min, v_min)
    right_x, _ = to_px(front, u_max, v_min)
    _, top_y = to_px(front, u_min, v_max)
    out: list[str] = []
    out.append(
        _horizontal_dimension(
            left_x, right_x, bottom_y + _DIM_OFFSET, _format_length(u_max - u_min)
        )
    )
    out.append(
        _vertical_dimension(
            top_y, bottom_y, left_x - _DIM_OFFSET, _format_length(v_max - v_min)
        )
    )
    return out


def _horizontal_dimension(x0: float, x1: float, y: float, label: str) -> str:
    """A dimension line from ``x0`` to ``x1`` at height ``y``, with arrowheads,
    extension ticks and centered text above it."""
    arrow = 6
    mid = (x0 + x1) / 2
    return (
        f'<g stroke="black" stroke-width="0.75" fill="black" font-size="12">'
        f'<line x1="{x0:.2f}" y1="{y:.2f}" x2="{x1:.2f}" y2="{y:.2f}"/>'
        f'<path d="M{x0:.2f} {y:.2f}l{arrow} {-arrow / 2:.2f}l0 {arrow}z"/>'
        f'<path d="M{x1:.2f} {y:.2f}l{-arrow} {-arrow / 2:.2f}l0 {arrow}z"/>'
        f'<text x="{mid:.2f}" y="{y - 4:.2f}" text-anchor="middle" '
        f'stroke="none">{escape(label)}</text>'
        f"</g>"
    )


def _vertical_dimension(y0: float, y1: float, x: float, label: str) -> str:
    """A dimension line from ``y0`` to ``y1`` at abscissa ``x``, with
    arrowheads and text rotated alongside it."""
    arrow = 6
    mid = (y0 + y1) / 2
    return (
        f'<g stroke="black" stroke-width="0.75" fill="black" font-size="12">'
        f'<line x1="{x:.2f}" y1="{y0:.2f}" x2="{x:.2f}" y2="{y1:.2f}"/>'
        f'<path d="M{x:.2f} {y0:.2f}l{-arrow / 2:.2f} {arrow}l{arrow} 0z"/>'
        f'<path d="M{x:.2f} {y1:.2f}l{-arrow / 2:.2f} {-arrow}l{arrow} 0z"/>'
        f'<text x="{x - 4:.2f}" y="{mid:.2f}" text-anchor="middle" '
        f'stroke="none" transform="rotate(-90 {x - 4:.2f} {mid:.2f})">'
        f"{escape(label)}</text>"
        f"</g>"
    )


def _title_block(drawing: Drawing, sheet_width: int, sheet_height: int) -> str:
    """A title block in the bottom-right corner: part name and overall size."""
    width = 260
    x = sheet_width - _MARGIN - width
    y = sheet_height - _MARGIN - _TITLE_HEIGHT
    length_x, length_y, length_z = drawing.overall
    size = (
        f"{_format_length(length_x)} × {_format_length(length_y)} "
        f"× {_format_length(length_z)}"
    )
    return (
        f'<g font-family="sans-serif">'
        f'<rect x="{x}" y="{y}" width="{width}" height="{_TITLE_HEIGHT}" '
        f'fill="none" stroke="black" stroke-width="1"/>'
        f'<line x1="{x}" y1="{y + _TITLE_HEIGHT / 2}" x2="{x + width}" '
        f'y2="{y + _TITLE_HEIGHT / 2}" stroke="black" stroke-width="0.75"/>'
        f'<text x="{x + 10}" y="{y + 20}" font-size="14" font-weight="bold" '
        f'fill="black">{escape(drawing.name)}</text>'
        f'<text x="{x + 10}" y="{y + 45}" font-size="12" fill="black">'
        f'SIZE  {escape(size)}</text>'
        f"</g>"
    )
