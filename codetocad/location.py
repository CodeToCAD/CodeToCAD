"""Locations: 6-dof positions/orientations used to query geometry, transform
solids and select the location of assembly operations.

``CubeLocations`` are shortcuts to the 23 topological locations and geometric
centers of a bounding cube (8 corners, 6 face centers, 8 edge midlines and the
geometric center). They can be used to quickly navigate any shape.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum, EnumMeta
from typing import Callable

import numpy as np

from codetocad.units import AngleRadians, AngleWithUnit, LengthMeters, LengthWithUnit


def _angle_to_radians(value: AngleWithUnit, *, floats_are_degrees: bool) -> float:
    """Convert an angle input to radians.

    Bare numbers passed to ``*_deg`` parameters are treated as degrees;
    strings and ``AngleRadians`` carry their own unit.
    """
    if isinstance(value, (int, float)):
        return math.radians(value) if floats_are_degrees else float(value)
    return AngleRadians(value).value


def euler_to_quat(
    x_deg: AngleWithUnit = 0, y_deg: AngleWithUnit = 0, z_deg: AngleWithUnit = 0
) -> tuple[float, float, float, float]:
    """Convert intrinsic roll(x)-pitch(y)-yaw(z) angles to a quaternion
    ``(x, y, z, w)``. Bare numbers are degrees; strings may carry units."""
    half_angles = (
        np.array(
            [
                _angle_to_radians(x_deg, floats_are_degrees=True),
                _angle_to_radians(y_deg, floats_are_degrees=True),
                _angle_to_radians(z_deg, floats_are_degrees=True),
            ]
        )
        / 2
    )
    (cx, cy, cz), (sx, sy, sz) = np.cos(half_angles), np.sin(half_angles)
    return (
        float(sx * cy * cz - cx * sy * sz),
        float(cx * sy * cz + sx * cy * sz),
        float(cx * cy * sz - sx * sy * cz),
        float(cx * cy * cz + sx * sy * sz),
    )


def quat_to_axis_angle(
    quat: tuple[float, float, float, float],
) -> tuple[tuple[float, float, float], float]:
    """Convert a quaternion ``(x, y, z, w)`` to a rotation ``(axis, degrees)``."""
    vector = np.array(quat[:3])
    magnitude = float(np.linalg.norm(vector))
    if magnitude < 1e-12:
        return ((0.0, 0.0, 1.0), 0.0)
    angle = 2.0 * math.atan2(magnitude, quat[3])
    axis = vector / magnitude
    return ((float(axis[0]), float(axis[1]), float(axis[2])), math.degrees(angle))


def quat_rotate_vector(
    quat: tuple[float, float, float, float], vector: tuple[float, float, float]
) -> np.ndarray:
    """Rotate a 3-vector by a quaternion ``(x, y, z, w)``."""
    q_vec = np.array(quat[:3])
    v = np.asarray(vector, dtype=np.float64)
    return v + 2.0 * np.cross(q_vec, np.cross(q_vec, v) + quat[3] * v)


def quat_multiply(
    a: tuple[float, float, float, float], b: tuple[float, float, float, float]
) -> tuple[float, float, float, float]:
    av, aw = np.array(a[:3]), a[3]
    bv, bw = np.array(b[:3]), b[3]
    vector = aw * bv + bw * av + np.cross(av, bv)
    scalar = aw * bw - float(np.dot(av, bv))
    return (float(vector[0]), float(vector[1]), float(vector[2]), float(scalar))


@dataclass
class Location:
    x: LengthWithUnit = 0
    y: LengthWithUnit = 0
    z: LengthWithUnit = 0
    quat_x: AngleWithUnit = 0
    quat_y: AngleWithUnit = 0
    quat_z: AngleWithUnit = 0
    quat_w: AngleWithUnit = 1
    inverted: bool = False
    """If inverted is true, the unit normal will point in the negative direction."""
    snap_to_geometry: bool = False
    """If snap_to_geometry is true, the Location will be evaluated to the
    closest euclidean location on the geometry."""
    name: str | None = None
    """A descriptive name of this location."""

    def __post_init__(self):
        self.x = LengthMeters(self.x)
        self.y = LengthMeters(self.y)
        self.z = LengthMeters(self.z)
        self.quat_x = _angle_to_radians(self.quat_x, floats_are_degrees=False)
        self.quat_y = _angle_to_radians(self.quat_y, floats_are_degrees=False)
        self.quat_z = _angle_to_radians(self.quat_z, floats_are_degrees=False)
        self.quat_w = _angle_to_radians(self.quat_w, floats_are_degrees=False)

    @classmethod
    def from_euler(
        cls,
        x: LengthWithUnit = 0,
        y: LengthWithUnit = 0,
        z: LengthWithUnit = 0,
        x_deg: AngleWithUnit = 0,
        y_deg: AngleWithUnit = 0,
        z_deg: AngleWithUnit = 0,
        inverted: bool = False,
        snap_to_geometry: bool = False,
        name: str | None = None,
    ) -> "Location":
        quat = euler_to_quat(x_deg, y_deg, z_deg)
        return cls(
            x,
            y,
            z,
            *quat,
            inverted=inverted,
            snap_to_geometry=snap_to_geometry,
            name=name,
        )

    @property
    def quat(self) -> tuple[float, float, float, float]:
        return (self.quat_x, self.quat_y, self.quat_z, self.quat_w)

    def rotate(
        self,
        x_deg: AngleWithUnit = 0,
        y_deg: AngleWithUnit = 0,
        z_deg: AngleWithUnit = 0,
    ) -> "Location":
        rotation = euler_to_quat(x_deg, y_deg, z_deg)
        self.quat_x, self.quat_y, self.quat_z, self.quat_w = quat_multiply(
            rotation, self.quat
        )
        return self

    def translate(
        self,
        x: LengthWithUnit = 0,
        y: LengthWithUnit = 0,
        z: LengthWithUnit = 0,
    ) -> "Location":
        self.x = self.x + LengthMeters(x)
        self.y = self.y + LengthMeters(y)
        self.z = self.z + LengthMeters(z)
        return self

    #: ``offset`` reads more naturally than ``translate`` when nudging a
    #: location away from a face/edge it was resolved from.
    offset = translate

    def copy(self) -> "Location":
        return Location(
            self.x,
            self.y,
            self.z,
            self.quat_x,
            self.quat_y,
            self.quat_z,
            self.quat_w,
            inverted=self.inverted,
            snap_to_geometry=self.snap_to_geometry,
            name=self.name,
        )

    def distance_to(self, other: "Location") -> LengthMeters:
        return LengthMeters(
            float(np.linalg.norm(self.to_numpy() - other.to_numpy()))
        )

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x.value, self.y.value, self.z.value)

    def to_numpy(self) -> np.ndarray:
        return np.array(
            [self.x.value, self.y.value, self.z.value], dtype=np.float64
        )


class _CubeLocationsMeta(EnumMeta):
    """Allows lowercase member access, e.g. ``CubeLocations.top_center``."""

    def __getattr__(cls, name):
        # Only called when normal lookup fails (e.g. lowercase member names).
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name) from None


# Each face token maps to (axis index, sign); its outward normal is the signed
# unit axis. -x is left, +y is back, +z is top.
_CUBE_FACES: dict[str, tuple[int, int]] = {
    "RIGHT": (0, 1), "LEFT": (0, -1),
    "BACK": (1, 1), "FRONT": (1, -1),
    "TOP": (2, 1), "BOTTOM": (2, -1),
}


def _face_normal(token: str) -> tuple[float, float, float]:
    axis, sign = _CUBE_FACES[token]
    normal = [0.0, 0.0, 0.0]
    normal[axis] = float(sign)
    return tuple(normal)


def _quat_aligning_z(
    normal: tuple[float, float, float],
) -> tuple[float, float, float, float]:
    """Shortest-arc quaternion ``(x, y, z, w)`` rotating +Z onto ``normal``.
    A zero normal (the geometric center) yields identity."""
    vector = np.asarray(normal, dtype=np.float64)
    magnitude = float(np.linalg.norm(vector))
    if magnitude < 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    vector = vector / magnitude
    dot = float(np.clip(vector[2], -1.0, 1.0))
    if dot > 1.0 - 1e-12:
        return (0.0, 0.0, 0.0, 1.0)
    if dot < -1.0 + 1e-12:
        return (1.0, 0.0, 0.0, 0.0)  # 180deg about X
    axis = np.cross((0.0, 0.0, 1.0), vector)
    axis = axis / np.linalg.norm(axis)
    half = math.acos(dot) / 2.0
    sin_half = math.sin(half)
    return (
        float(axis[0] * sin_half),
        float(axis[1] * sin_half),
        float(axis[2] * sin_half),
        float(math.cos(half)),
    )


def _cube_location_members() -> dict[str, tuple[float, ...]]:
    """All 27 topological locations of a cube (center, 6 faces, 12 edges,
    8 corners), each named by its face tokens in every order. A member's value
    is ``(px, py, pz, nx, ny, nz)``: the position multipliers plus the outward
    normal of the *first-named* face (which becomes the location's +Z). Names
    that share a position and first face collapse to one member (aliases)."""
    from itertools import combinations, permutations, product

    members: dict[str, tuple[float, ...]] = {"CENTER": (0, 0, 0, 0, 0, 0)}
    faces_by_axis = {
        axis: [tok for tok, (a, _) in _CUBE_FACES.items() if a == axis]
        for axis in (2, 1, 0)  # z, y, x -> canonical token order
    }
    # canonical rank: TOP/BOTTOM (z) before FRONT/BACK (y) before LEFT/RIGHT (x)
    rank = {tok: -_CUBE_FACES[tok][0] for tok in _CUBE_FACES}
    for count in (1, 2, 3):
        for axes in combinations((2, 1, 0), count):
            for tokens in product(*(faces_by_axis[a] for a in axes)):
                position = [0.0, 0.0, 0.0]
                for tok in tokens:
                    axis, sign = _CUBE_FACES[tok]
                    position[axis] = float(sign)
                if count == 1:  # face center
                    (token,) = tokens
                    members[f"{token}_CENTER"] = (*position, *_face_normal(token))
                    continue
                # Order permutations so the fully canonical name is first and,
                # within each first token, the canonical remainder leads.
                ordered = sorted(
                    permutations(tokens),
                    key=lambda perm: (rank[perm[0]], [rank[t] for t in perm[1:]]),
                )
                for perm in ordered:
                    name = "_".join(perm)
                    members.setdefault(name, (*position, *_face_normal(perm[0])))
    return members


def _cube_to_location(self, part) -> Location:
    """Calculate the oriented Location on ``part`` from its bounding box. The
    location sits at this cube position with +Z along the first face's
    outward normal."""
    bbox_min, bbox_max = part.get_bounding_box()
    px, py, pz, nx, ny, nz = self.value
    center = (
        (bbox_min.x + bbox_max.x) / 2,
        (bbox_min.y + bbox_max.y) / 2,
        (bbox_min.z + bbox_max.z) / 2,
    )
    half = (
        (bbox_max.x - bbox_min.x) / 2,
        (bbox_max.y - bbox_min.y) / 2,
        (bbox_max.z - bbox_min.z) / 2,
    )
    quat_x, quat_y, quat_z, quat_w = _quat_aligning_z((nx, ny, nz))
    return Location(
        center[0] + px * half[0],
        center[1] + py * half[1],
        center[2] + pz * half[2],
        quat_x,
        quat_y,
        quat_z,
        quat_w,
        name=self.name.lower(),
    )


def _cube_translate(self, x=0, y=0, z=0) -> "CubeLocationExpr":
    return CubeLocationExpr(base=self).translate(x, y, z)


def _cube_rotate(self, x_deg=0, y_deg=0, z_deg=0) -> "CubeLocationExpr":
    return CubeLocationExpr(base=self).rotate(x_deg, y_deg, z_deg)


def _build_cube_locations() -> type:
    namespace = _CubeLocationsMeta.__prepare__("CubeLocations", (Enum,))
    namespace["__doc__"] = (
        "The 27 topological locations of a cube: the geometric center, 6 face "
        "centers, 12 edge midlines and 8 corners. A member's value is "
        "``(px, py, pz, nx, ny, nz)`` -- position multipliers relative to the "
        "bounding-box center plus the outward normal of the first-named face. "
        "The first face's normal becomes the location's +Z axis, so "
        "``BACK_BOTTOM`` points +Z out the back while ``BOTTOM_BACK`` points "
        "+Z down; every token order is available as an alias. -x is left, +y "
        "is back, +z is top."
    )
    for name, value in _cube_location_members().items():
        namespace[name] = value
    namespace["to_location"] = _cube_to_location
    namespace["translate"] = _cube_translate
    namespace["rotate"] = _cube_rotate
    namespace["offset"] = _cube_translate
    return _CubeLocationsMeta("CubeLocations", (Enum,), namespace)


CubeLocations = _build_cube_locations()

# Alias used in some docs/specs.
BoxLocations = CubeLocations


@dataclass
class CubeLocationExpr:
    """A ``CubeLocations`` member with deferred translations/rotations that
    resolve against a part's bounding box via :meth:`to_location`."""

    base: CubeLocations
    _operations: list[Callable[[Location], Location]] = field(default_factory=list)

    def translate(
        self,
        x: LengthWithUnit = 0,
        y: LengthWithUnit = 0,
        z: LengthWithUnit = 0,
    ) -> "CubeLocationExpr":
        self._operations.append(lambda loc: loc.translate(x, y, z))
        return self

    def rotate(
        self,
        x_deg: AngleWithUnit = 0,
        y_deg: AngleWithUnit = 0,
        z_deg: AngleWithUnit = 0,
    ) -> "CubeLocationExpr":
        self._operations.append(lambda loc: loc.rotate(x_deg, y_deg, z_deg))
        return self

    offset = translate

    def to_location(self, part) -> Location:
        resolved = self.base.to_location(part)
        for operation in self._operations:
            resolved = operation(resolved)
        return resolved


_LOCATION_MARKER = "__codetocad_location__"


def location(func):
    """Decorator that marks a method on a Part/Assembly class as a
    user-defined named Location. Collected by ``get_locations()``."""
    setattr(func, _LOCATION_MARKER, True)
    return func


class LocationMixin:
    loc = CubeLocations
    """Quick access to cube locations."""

    # The cube locations are also exposed directly on every part, resolved
    # against its bounding box by __getattr__ below. Declaring them here (as
    # annotations, so there is no runtime cost) lets IDEs autocomplete e.g.
    # ``part.BOTTOM_LEFT``. Mirrors codetocad.CubeLocations.
    BACK_BOTTOM: Location
    BACK_BOTTOM_LEFT: Location
    BACK_BOTTOM_RIGHT: Location
    BACK_CENTER: Location
    BACK_LEFT: Location
    BACK_LEFT_BOTTOM: Location
    BACK_LEFT_TOP: Location
    BACK_RIGHT: Location
    BACK_RIGHT_BOTTOM: Location
    BACK_RIGHT_TOP: Location
    BACK_TOP: Location
    BACK_TOP_LEFT: Location
    BACK_TOP_RIGHT: Location
    BOTTOM_BACK: Location
    BOTTOM_BACK_LEFT: Location
    BOTTOM_BACK_RIGHT: Location
    BOTTOM_CENTER: Location
    BOTTOM_FRONT: Location
    BOTTOM_FRONT_LEFT: Location
    BOTTOM_FRONT_RIGHT: Location
    BOTTOM_LEFT: Location
    BOTTOM_LEFT_BACK: Location
    BOTTOM_LEFT_FRONT: Location
    BOTTOM_RIGHT: Location
    BOTTOM_RIGHT_BACK: Location
    BOTTOM_RIGHT_FRONT: Location
    CENTER: Location
    FRONT_BOTTOM: Location
    FRONT_BOTTOM_LEFT: Location
    FRONT_BOTTOM_RIGHT: Location
    FRONT_CENTER: Location
    FRONT_LEFT: Location
    FRONT_LEFT_BOTTOM: Location
    FRONT_LEFT_TOP: Location
    FRONT_RIGHT: Location
    FRONT_RIGHT_BOTTOM: Location
    FRONT_RIGHT_TOP: Location
    FRONT_TOP: Location
    FRONT_TOP_LEFT: Location
    FRONT_TOP_RIGHT: Location
    LEFT_BACK: Location
    LEFT_BACK_BOTTOM: Location
    LEFT_BACK_TOP: Location
    LEFT_BOTTOM: Location
    LEFT_BOTTOM_BACK: Location
    LEFT_BOTTOM_FRONT: Location
    LEFT_CENTER: Location
    LEFT_FRONT: Location
    LEFT_FRONT_BOTTOM: Location
    LEFT_FRONT_TOP: Location
    LEFT_TOP: Location
    LEFT_TOP_BACK: Location
    LEFT_TOP_FRONT: Location
    RIGHT_BACK: Location
    RIGHT_BACK_BOTTOM: Location
    RIGHT_BACK_TOP: Location
    RIGHT_BOTTOM: Location
    RIGHT_BOTTOM_BACK: Location
    RIGHT_BOTTOM_FRONT: Location
    RIGHT_CENTER: Location
    RIGHT_FRONT: Location
    RIGHT_FRONT_BOTTOM: Location
    RIGHT_FRONT_TOP: Location
    RIGHT_TOP: Location
    RIGHT_TOP_BACK: Location
    RIGHT_TOP_FRONT: Location
    TOP_BACK: Location
    TOP_BACK_LEFT: Location
    TOP_BACK_RIGHT: Location
    TOP_CENTER: Location
    TOP_FRONT: Location
    TOP_FRONT_LEFT: Location
    TOP_FRONT_RIGHT: Location
    TOP_LEFT: Location
    TOP_LEFT_BACK: Location
    TOP_LEFT_FRONT: Location
    TOP_RIGHT: Location
    TOP_RIGHT_BACK: Location
    TOP_RIGHT_FRONT: Location

    def __getattr__(self, name: str) -> Location:
        """Expose cube locations as attributes resolved against this part's
        bounding box, e.g. ``part.top_center`` or ``part.bottom_front_left``."""
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            member = CubeLocations[name.upper()]
        except KeyError:
            raise AttributeError(
                f"{type(self).__name__!r} object has no attribute {name!r}"
            ) from None
        return member.to_location(self)

    def get_locations(self) -> list[Location]:
        """Retrieves user-defined locations in the Part class marked with the
        ``@location`` decorator."""
        results: list[Location] = []
        seen: set[str] = set()
        for klass in type(self).__mro__:
            for attr_name, attr in vars(klass).items():
                if attr_name in seen or not callable(attr):
                    continue
                if getattr(attr, _LOCATION_MARKER, False):
                    seen.add(attr_name)
                    resolved = self.resolve_location(attr(self))
                    if resolved.name is None:
                        resolved.name = attr_name
                    results.append(resolved)
        return results

    def resolve_location(self, value) -> Location:
        """Resolve a Location, CubeLocations member or CubeLocationExpr into a
        concrete Location on this part."""
        if isinstance(value, Location):
            return value
        if isinstance(value, (CubeLocations, CubeLocationExpr)):
            return value.to_location(self)
        raise TypeError(f"Cannot resolve {value!r} into a Location")
