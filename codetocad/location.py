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

from .units import AngleRadians, AngleWithUnit, LengthMeters, LengthWithUnit


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
    rx = _angle_to_radians(x_deg, floats_are_degrees=True)
    ry = _angle_to_radians(y_deg, floats_are_degrees=True)
    rz = _angle_to_radians(z_deg, floats_are_degrees=True)
    cx, sx = math.cos(rx / 2), math.sin(rx / 2)
    cy, sy = math.cos(ry / 2), math.sin(ry / 2)
    cz, sz = math.cos(rz / 2), math.sin(rz / 2)
    return (
        sx * cy * cz - cx * sy * sz,
        cx * sy * cz + sx * cy * sz,
        cx * cy * sz - sx * sy * cz,
        cx * cy * cz + sx * sy * sz,
    )


def quat_multiply(
    a: tuple[float, float, float, float], b: tuple[float, float, float, float]
) -> tuple[float, float, float, float]:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    )


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
            math.sqrt(
                (self.x.value - other.x.value) ** 2
                + (self.y.value - other.y.value) ** 2
                + (self.z.value - other.z.value) ** 2
            )
        )

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x.value, self.y.value, self.z.value)


class _CubeLocationsMeta(EnumMeta):
    """Allows lowercase member access, e.g. ``CubeLocations.top_center``."""

    def __getattr__(cls, name):
        # Only called when normal lookup fails (e.g. lowercase member names).
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name) from None


class CubeLocations(Enum, metaclass=_CubeLocationsMeta):
    """The 23 topological locations and geometric centers of a cube.

    Member values are ``(x, y, z)`` half-extent multipliers relative to the
    bounding-box center. -x is left, +y is back, +z is top.
    """

    CENTER = (0, 0, 0)

    # 6 face centers
    TOP_CENTER = (0, 0, 1)
    BOTTOM_CENTER = (0, 0, -1)
    FRONT_CENTER = (0, -1, 0)
    BACK_CENTER = (0, 1, 0)
    LEFT_CENTER = (-1, 0, 0)
    RIGHT_CENTER = (1, 0, 0)

    # 8 corners
    TOP_FRONT_LEFT = (-1, -1, 1)
    TOP_FRONT_RIGHT = (1, -1, 1)
    TOP_BACK_LEFT = (-1, 1, 1)
    TOP_BACK_RIGHT = (1, 1, 1)
    BOTTOM_FRONT_LEFT = (-1, -1, -1)
    BOTTOM_FRONT_RIGHT = (1, -1, -1)
    BOTTOM_BACK_LEFT = (-1, 1, -1)
    BOTTOM_BACK_RIGHT = (1, 1, -1)

    # 8 edge midlines
    TOP_FRONT = (0, -1, 1)
    TOP_BACK = (0, 1, 1)
    TOP_LEFT = (-1, 0, 1)
    TOP_RIGHT = (1, 0, 1)
    BOTTOM_FRONT = (0, -1, -1)
    BOTTOM_BACK = (0, 1, -1)
    BOTTOM_LEFT = (-1, 0, -1)
    BOTTOM_RIGHT = (1, 0, -1)

    def to_location(self, part) -> Location:
        """Calculate the Location on ``part`` based on its bounding box."""
        bbox_min, bbox_max = part.get_bounding_box()
        fx, fy, fz = self.value
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
        return Location(
            center[0] + fx * half[0],
            center[1] + fy * half[1],
            center[2] + fz * half[2],
            name=self.name.lower(),
        )

    def translate(
        self,
        x: LengthWithUnit = 0,
        y: LengthWithUnit = 0,
        z: LengthWithUnit = 0,
    ) -> "CubeLocationExpr":
        return CubeLocationExpr(base=self).translate(x, y, z)

    def rotate(
        self,
        x_deg: AngleWithUnit = 0,
        y_deg: AngleWithUnit = 0,
        z_deg: AngleWithUnit = 0,
    ) -> "CubeLocationExpr":
        return CubeLocationExpr(base=self).rotate(x_deg, y_deg, z_deg)


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
