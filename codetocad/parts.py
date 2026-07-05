"""Part2D and Part3D.

Parts created from the primitive presets carry a ``_primitive`` description
(kind + dimensions) that powers bounding boxes, geometry queries, analysis and
basic STL export without a federated backend. Feature operations (shell,
fillet, chamfer, hole, booleans) are recorded in ledgers/operation lists for
the federated application to build.
"""

from __future__ import annotations

import math
import shutil
from pathlib import Path

import numpy as np

from .assembly import Assembly2D, Assembly3D
from .location import Location, LocationMixin
from .materials import MaterialMixin
from .mixins import BooleanMixin, GeometryAnalysisMixin, GeometryQueryMixin
from .topology import Edge, Face
from .units import LengthMeters, LengthWithUnit
from .vectors import Vec3

# Meshes are numpy arrays of shape (N, 3, 3): N triangles x 3 vertices x xyz.


class Part2D(Assembly2D, LocationMixin, GeometryQueryMixin, GeometryAnalysisMixin):
    def __init__(self, name: str | None = None, description: str | None = None):
        Assembly2D.__init__(self, name, description)
        self._primitive: dict | None = None
        self.operations: list[dict] = []

    def build(self):
        """Create the shape in the target modeling application. Parts made
        from primitive presets are declarative and build as-is; blank parts
        must override this."""
        if self._primitive is None:
            raise NotImplementedError(
                "Override build() to create this shape in your target modeling "
                "application"
            )
        return self

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        half = _half_extents(self._primitive)
        return _bbox_around(self._origin, half)

    def extrude(self, height: LengthWithUnit) -> "Part3D":
        height_m = LengthMeters(height).value
        name = f"{self.name}_extruded" if self.name else None
        part = Part3D(name=name, description=self.description)
        if self._primitive is not None:
            kind = self._primitive["kind"]
            if kind == "rectangle":
                part._primitive = {
                    "kind": "cube",
                    "length": self._primitive["width"],
                    "width": self._primitive["height"],
                    "height": height_m,
                }
            elif kind == "circle":
                part._primitive = {
                    "kind": "cylinder",
                    "radius": self._primitive["radius"],
                    "height": height_m,
                }
            else:
                part._primitive = {
                    "kind": "extrusion",
                    "profile": self._primitive,
                    "height": height_m,
                }
        part._origin = Vec3(self._origin.x, self._origin.y, self._origin.z)
        return part


class Part3D(
    Assembly3D, LocationMixin, GeometryQueryMixin, GeometryAnalysisMixin,
    BooleanMixin, MaterialMixin,
):
    def __init__(self, name: str | None = None, description: str | None = None):
        Assembly3D.__init__(self, name, description)
        self._init_boolean()
        self._init_material()
        self._primitive: dict | None = None
        self.operations: list[dict] = []

    def build(self):
        """Create the shape in the target modeling application. Parts made
        from primitive presets are declarative and build as-is; blank parts
        must override this."""
        if self._primitive is None:
            raise NotImplementedError(
                "Override build() to create this shape in your target modeling "
                "application"
            )
        return self

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        half = _half_extents(self._primitive)
        return _bbox_around(self._origin, half)

    def shell(
        self, thickness: LengthWithUnit, start_at_location: Location | None = None
    ) -> "Part3D":
        self.operations.append(
            {
                "operation": "shell",
                "thickness": LengthMeters(thickness),
                "start_at_location": start_at_location,
            }
        )
        return self

    def fillet(
        self,
        edges: list[Edge] | None = None,
        faces: list[Face] | None = None,
        *,
        amount: LengthWithUnit,
    ) -> "Part3D":
        self.operations.append(
            {
                "operation": "fillet",
                "edges": edges,
                "faces": faces,
                "amount": LengthMeters(amount),
            }
        )
        return self

    def chamfer(
        self,
        edges: list[Edge] | None = None,
        faces: list[Face] | None = None,
        *,
        amount: LengthWithUnit,
    ) -> "Part3D":
        self.operations.append(
            {
                "operation": "chamfer",
                "edges": edges,
                "faces": faces,
                "amount": LengthMeters(amount),
            }
        )
        return self

    def hole(
        self,
        start_location: Location,
        radius: LengthWithUnit,
        *,
        amount: LengthWithUnit | None = None,
        end_location: Location | None = None,
    ) -> "Part3D":
        if (amount is None) == (end_location is None):
            raise ValueError("Supply exactly one of amount= or end_location=")
        self.operations.append(
            {
                "operation": "hole",
                "start_location": start_location,
                "radius": LengthMeters(radius),
                "amount": LengthMeters(amount) if amount is not None else None,
                "end_location": end_location,
            }
        )
        return self

    def export(self, location: str) -> str:
        """Export the base solid as an ASCII STL. Feature operations recorded
        in ledgers (booleans, shell, holes, ...) require a federated backend
        and are not reflected in this mesh."""
        primitive = self._primitive or {}
        if primitive.get("kind") == "imported":
            source = Path(primitive["file_path"])
            if source.suffix.lower() == Path(location).suffix.lower():
                shutil.copyfile(source, location)
                return location
        triangles = self._generate_mesh()
        if triangles is None:
            raise NotImplementedError(
                "Override export() to export this shape from your target "
                "modeling application"
            )
        _write_ascii_stl(location, triangles, self.name or "codetocad_part")
        return location

    def _generate_mesh(self) -> np.ndarray | None:
        if self._primitive is None:
            return None
        kind = self._primitive["kind"]
        origin = self._origin
        if kind == "cube":
            bbox_min, bbox_max = self.get_bounding_box()
            return _box_mesh(bbox_min, bbox_max)
        if kind == "cylinder":
            return _cylinder_mesh(
                self._primitive["radius"], self._primitive["height"], origin
            )
        if kind == "sphere":
            return _sphere_mesh(self._primitive["radius"], origin)
        return None


def _half_extents(primitive: dict | None) -> Vec3:
    if primitive is None:
        raise NotImplementedError(
            "This part has no primitive geometry; override get_bounding_box()"
        )
    kind = primitive["kind"]
    if kind == "cube":
        return Vec3(
            primitive["length"] / 2, primitive["width"] / 2, primitive["height"] / 2
        )
    if kind == "cylinder":
        radius = primitive["radius"]
        return Vec3(radius, radius, primitive["height"] / 2)
    if kind == "sphere":
        radius = primitive["radius"]
        return Vec3(radius, radius, radius)
    if kind == "rectangle":
        return Vec3(primitive["width"] / 2, primitive["height"] / 2, 0.0)
    if kind == "circle":
        radius = primitive["radius"]
        return Vec3(radius, radius, 0.0)
    if kind == "text":
        size = primitive["size"]
        return Vec3(size * len(primitive["text"]) / 2, size / 2, 0.0)
    if kind == "extrusion":
        profile_half = _half_extents(primitive["profile"])
        return Vec3(profile_half.x, profile_half.y, primitive["height"] / 2)
    raise NotImplementedError(f"Bounding box is not available for {kind!r} parts")


def _bbox_around(origin: Vec3, half: Vec3) -> tuple[Vec3, Vec3]:
    return (
        Vec3(origin.x - half.x, origin.y - half.y, origin.z - half.z),
        Vec3(origin.x + half.x, origin.y + half.y, origin.z + half.z),
    )


def _box_mesh(bbox_min: Vec3, bbox_max: Vec3) -> np.ndarray:
    x0, y0, z0 = bbox_min.to_tuple()
    x1, y1, z1 = bbox_max.to_tuple()
    vertices = np.array(
        [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
        ],
        dtype=np.float64,
    )
    quads = np.array(
        [
            (0, 3, 2, 1),  # bottom
            (4, 5, 6, 7),  # top
            (0, 1, 5, 4),  # front
            (2, 3, 7, 6),  # back
            (0, 4, 7, 3),  # left
            (1, 2, 6, 5),  # right
        ]
    )
    triangle_indices = np.concatenate(
        [quads[:, (0, 1, 2)], quads[:, (0, 2, 3)]]
    )
    return vertices[triangle_indices]


def _cylinder_mesh(
    radius: float, height: float, origin: Vec3, segments: int = 48
) -> np.ndarray:
    z0, z1 = origin.z - height / 2, origin.z + height / 2
    angles = np.linspace(0.0, 2 * math.pi, segments, endpoint=False)
    xs = origin.x + radius * np.cos(angles)
    ys = origin.y + radius * np.sin(angles)
    bottom = np.column_stack([xs, ys, np.full(segments, z0)])
    top = np.column_stack([xs, ys, np.full(segments, z1)])
    bottom_next = np.roll(bottom, -1, axis=0)
    top_next = np.roll(top, -1, axis=0)
    bottom_center = np.tile((origin.x, origin.y, z0), (segments, 1))
    top_center = np.tile((origin.x, origin.y, z1), (segments, 1))
    return np.concatenate(
        [
            np.stack([bottom, bottom_next, top_next], axis=1),  # side
            np.stack([bottom, top_next, top], axis=1),  # side
            np.stack([bottom_center, bottom_next, bottom], axis=1),  # bottom cap
            np.stack([top_center, top, top_next], axis=1),  # top cap
        ]
    )


def _sphere_mesh(
    radius: float, origin: Vec3, slices: int = 32, stacks: int = 16
) -> np.ndarray:
    phi = np.linspace(0.0, math.pi, stacks + 1)
    theta = np.linspace(0.0, 2 * math.pi, slices + 1)
    phi_grid, theta_grid = np.meshgrid(phi, theta, indexing="ij")
    points = np.stack(
        [
            origin.x + radius * np.sin(phi_grid) * np.cos(theta_grid),
            origin.y + radius * np.sin(phi_grid) * np.sin(theta_grid),
            origin.z + radius * np.cos(phi_grid),
        ],
        axis=-1,
    )
    p00 = points[:-1, :-1].reshape(-1, 3)
    p01 = points[:-1, 1:].reshape(-1, 3)
    p10 = points[1:, :-1].reshape(-1, 3)
    p11 = points[1:, 1:].reshape(-1, 3)
    upper = np.stack([p00, p01, p11], axis=1)
    lower = np.stack([p00, p11, p10], axis=1)
    # Drop degenerate triangles at the poles (first stack for the upper
    # fan, last stack for the lower fan).
    keep_upper = np.repeat(np.arange(stacks) > 0, slices)
    keep_lower = np.repeat(np.arange(stacks) < stacks - 1, slices)
    return np.concatenate([upper[keep_upper], lower[keep_lower]])


def _write_ascii_stl(path: str, triangles: np.ndarray, name: str) -> None:
    edge1 = triangles[:, 1] - triangles[:, 0]
    edge2 = triangles[:, 2] - triangles[:, 0]
    normals = np.cross(edge1, edge2)
    magnitudes = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.where(magnitudes == 0, 1.0, magnitudes)

    lines = [f"solid {name}"]
    for (nx, ny, nz), tri in zip(normals, triangles):
        lines.append(f"  facet normal {nx:e} {ny:e} {nz:e}")
        lines.append("    outer loop")
        for vx, vy, vz in tri:
            lines.append(f"      vertex {vx:e} {vy:e} {vz:e}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    Path(path).write_text("\n".join(lines) + "\n")
