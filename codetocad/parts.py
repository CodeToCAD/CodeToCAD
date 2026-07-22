"""Part2D and Part3D.

Parts created from the primitive presets carry a ``_primitive`` description
(kind + dimensions) that powers bounding boxes, geometry queries, analysis and
basic STL export without a federated backend. Feature operations (shell,
fillet, chamfer, hole, booleans) are recorded in ledgers/operation lists for
the federated application to build.
"""

from __future__ import annotations

import copy
import math
import shutil
from pathlib import Path

import numpy as np

from codetocad.assembly import Assembly2D, Assembly3D
from codetocad.drawings import DEFAULT_VIEWS
from codetocad.ledgers import AssemblyLedger, BooleanLedger
from codetocad.simulation import extract_links
from codetocad.location import Location, LocationMixin, _angle_to_radians
from codetocad.materials import MaterialMixin
from codetocad.mixins import BooleanMixin, GeometryAnalysisMixin, GeometryQueryMixin
from codetocad.topology import Edge, Face
from codetocad.units import AngleRadians, AngleWithUnit, LengthMeters, LengthWithUnit
from codetocad.vectors import Vec3

# Meshes are numpy arrays of shape (N, 3, 3): N triangles x 3 vertices x xyz.

#: Pattern operations recorded on ``Part.operations``. Unlike other feature
#: operations, patterns are also baked into core meshes and bounding boxes
#: (they are rigid copies of the base mesh, which needs no CAD kernel).
PATTERN_OPERATIONS = frozenset({"linear_pattern", "circular_pattern"})

_PATTERN_AXES = {"x": (1.0, 0.0, 0.0), "y": (0.0, 1.0, 0.0), "z": (0.0, 0.0, 1.0)}

#: How far (in meters) a profile may reach across the axis of revolution before
#: it counts as crossing it rather than touching it.
_AXIS_TOLERANCE = 1e-9


def _bbox_extent(part, axis: int) -> LengthMeters:
    """Size of ``part``'s axis-aligned bounding box along ``axis`` (0=x, 1=y,
    2=z), as ``LengthMeters``. Returns a stored override if a subclass assigned
    the dimension directly (e.g. a wheel setting its own width)."""
    override = part.__dict__.get(f"_dim_{axis}")
    if override is not None:
        return override
    bbox_min, bbox_max = part.get_bounding_box()
    return LengthMeters(bbox_max.to_tuple()[axis] - bbox_min.to_tuple()[axis])


def _set_bbox_extent(part, axis: int, value: LengthWithUnit) -> None:
    part.__dict__[f"_dim_{axis}"] = LengthMeters(value)


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
        primitive = self._primitive or {}
        if primitive.get("kind") == "drawing":
            segments = primitive["drawing"].layout_segments()
            origin = self._origin
            if len(segments) == 0:
                return _bbox_around(origin, Vec3())
            points = segments.reshape(-1, 2)
            low, high = points.min(axis=0), points.max(axis=0)
            return (
                Vec3(origin.x + low[0], origin.y + low[1], origin.z),
                Vec3(origin.x + high[0], origin.y + high[1], origin.z),
            )
        half = _half_extents(self._primitive)
        return _bbox_around(self._origin, half)

    def export(self, location: str) -> str:
        """Export this sketch. A drawing (from :meth:`Part3D.generate_drawing`)
        writes its SVG sheet; other sketches need a federated backend to build
        and export their geometry."""
        primitive = self._primitive or {}
        if primitive.get("kind") == "drawing":
            return primitive["drawing"].export_svg(location, name=self.name)
        raise NotImplementedError(
            "Override export() to export this shape from your target modeling "
            "application"
        )

    @property
    def width(self) -> LengthMeters:
        """Extent along X (the sketch plane's horizontal axis)."""
        return _bbox_extent(self, 0)

    @width.setter
    def width(self, value: LengthWithUnit) -> None:
        _set_bbox_extent(self, 0, value)

    @property
    def length(self) -> LengthMeters:
        """Extent along Y (the sketch plane's vertical axis)."""
        return _bbox_extent(self, 1)

    @length.setter
    def length(self, value: LengthWithUnit) -> None:
        _set_bbox_extent(self, 1, value)

    def extrude(
        self, height: LengthWithUnit, draft_angle: AngleWithUnit = 0
    ) -> "Part3D":
        """Extrude this profile ``height`` along Z. ``draft_angle`` tapers the
        swept walls away from vertical (bare numbers are degrees): a positive
        draft shrinks the top of the extrusion, the base keeps the profile's
        full size."""
        height_m = LengthMeters(height).value
        draft = _angle_to_radians(draft_angle, floats_are_degrees=True)
        draft_field = {"draft_angle": draft} if draft else {}
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
                    **draft_field,
                }
            elif kind == "circle":
                part._primitive = {
                    "kind": "cylinder",
                    "radius": self._primitive["radius"],
                    "height": height_m,
                    **draft_field,
                }
            else:
                part._primitive = {
                    "kind": "extrusion",
                    "profile": self._primitive,
                    "height": height_m,
                    **draft_field,
                }
        part._origin = Vec3(self._origin.x, self._origin.y, self._origin.z)
        return part

    def revolve(
        self,
        angle: AngleWithUnit = 360,
        axis: str | tuple[float, float, float] | Edge = "y",
    ) -> "Part3D":
        """Revolve this 2D profile about an axis to sweep a solid of
        revolution.

        ``angle`` is the sweep angle -- bare numbers are degrees, strings may
        carry units ("0.5rad"), and the default is a full 360deg turn.
        ``axis`` is the axis of revolution: a main axis ``"x"``, ``"y"`` or
        ``"z"`` (or a direction 3-vector) through the world origin, or an
        :class:`Edge` whose two vertices define the axis line. The profile
        lies in the XY plane, so a non-degenerate solid needs an axis that
        also lies in that plane (the main ``"x"``/``"y"`` axes and coplanar
        edges).
        """
        angle_rad = _angle_to_radians(angle, floats_are_degrees=True)
        if not 0 < angle_rad <= 2 * math.pi + 1e-9:
            raise ValueError("Revolve angle must be within (0, 360] degrees")
        angle_rad = min(angle_rad, 2 * math.pi)
        axis_point, axis_direction = _revolve_axis(axis)
        name = f"{self.name}_revolved" if self.name else None
        part = Part3D(name=name, description=self.description)
        if self._primitive is not None:
            part._primitive = {
                "kind": "revolution",
                "profile": copy.deepcopy(self._primitive),
                "profile_origin": self._origin.to_tuple(),
                "axis_point": axis_point,
                "axis_direction": axis_direction,
                "angle": angle_rad,
            }
            # Fail here rather than deep inside a CAD kernel: an axis running
            # through the profile only surfaces as an opaque kernel error
            # (OCCT: "BRep_API: command not done") at build/mesh time.
            _revolve_centroid_radius(part._primitive)
        # The revolution is defined in world space (the profile carries its own
        # origin and the axis its own line), so the part sits at the world
        # origin rather than inheriting the sketch's placement.
        return part

    def loft(self, *profiles: "Part2D") -> "Part3D":
        """Loft this profile through one or more further cross-sections to
        build a solid that transitions smoothly between them.

        ``self`` is the first cross-section; each :class:`Part2D` in
        ``profiles`` is a subsequent one. Every section is placed at its own
        ``start_location`` (including its Z), so stack them by giving each a
        different height. Needs at least two sections in total.
        """
        sections = [self, *profiles]
        if len(sections) < 2:
            raise ValueError("Loft needs at least two cross-sections")
        name = f"{self.name}_lofted" if self.name else None
        part = Part3D(name=name, description=self.description)
        if all(section._primitive is not None for section in sections):
            part._primitive = {
                "kind": "loft",
                "sections": [
                    {
                        "profile": copy.deepcopy(section._primitive),
                        "origin": section._origin.to_tuple(),
                    }
                    for section in sections
                ],
            }
        # Each section carries its own world placement, so (like a revolution)
        # the lofted solid sits at the world origin.
        return part

    def sweep(self, path: "Edge | list") -> "Part3D":
        """Sweep this profile along ``path`` to build a solid, keeping the
        profile perpendicular to the path's local direction.

        ``path`` is either an :class:`Edge` (a straight segment between its two
        vertices) or a sequence of at least two points -- :class:`Location`
        objects or ``(x, y, z)`` tuples -- forming a polyline. The profile's
        own origin rides along the path; a straight, axis-aligned path is
        therefore equivalent to an :meth:`extrude`.
        """
        points = _sweep_path_points(path)
        name = f"{self.name}_swept" if self.name else None
        part = Part3D(name=name, description=self.description)
        if self._primitive is not None:
            part._primitive = {
                "kind": "sweep",
                "profile": copy.deepcopy(self._primitive),
                "profile_origin": self._origin.to_tuple(),
                "path": points,
            }
        # The path is given in world space, so the swept solid sits at the
        # world origin rather than inheriting the sketch's placement.
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
        primitive = self._primitive or {}
        base_kind = primitive.get("kind")
        # A negative draft flares the top past the base, so the taper (like a
        # revolution or pattern) needs the actual mesh to bound it.
        needs_mesh = (
            base_kind in ("revolution", "loft", "sweep")
            or primitive.get("draft_angle")
            or any(
                op["operation"] in PATTERN_OPERATIONS for op in self.operations
            )
        )
        if needs_mesh:
            triangles = self._generate_mesh()
            if triangles is not None:
                points = triangles.reshape(-1, 3)
                return (Vec3(*points.min(axis=0)), Vec3(*points.max(axis=0)))
        half = _half_extents(self._primitive)
        return _bbox_around(self._origin, half)

    @property
    def length(self) -> LengthMeters:
        """Extent along X."""
        return _bbox_extent(self, 0)

    @length.setter
    def length(self, value: LengthWithUnit) -> None:
        _set_bbox_extent(self, 0, value)

    @property
    def width(self) -> LengthMeters:
        """Extent along Y."""
        return _bbox_extent(self, 1)

    @width.setter
    def width(self, value: LengthWithUnit) -> None:
        _set_bbox_extent(self, 1, value)

    @property
    def height(self) -> LengthMeters:
        """Extent along Z."""
        return _bbox_extent(self, 2)

    @height.setter
    def height(self, value: LengthWithUnit) -> None:
        _set_bbox_extent(self, 2, value)

    def get_volume(self) -> float:
        primitive = self._primitive or {}
        kind = primitive.get("kind")
        if kind == "revolution":
            area, _perimeter = _profile_area_perimeter(self._primitive["profile"])
            return self._primitive["angle"] * _revolve_centroid_radius(
                self._primitive
            ) * area
        if kind in ("loft", "sweep"):
            # No simple analytic form for an arbitrary swept/lofted solid; read
            # the enclosed volume straight off the triangulated surface.
            return _mesh_volume(self._base_mesh())
        if primitive.get("draft_angle"):
            return _drafted_volume(primitive)
        return super().get_volume()

    def get_area(self) -> float:
        primitive = self._primitive or {}
        kind = primitive.get("kind")
        if kind == "revolution":
            area, perimeter = _profile_area_perimeter(self._primitive["profile"])
            radius = _revolve_centroid_radius(self._primitive)
            angle = self._primitive["angle"]
            # Pappus lateral surface swept by the boundary, plus the two flat
            # profile caps when the sweep does not close (angle < 360deg).
            lateral = angle * radius * perimeter
            caps = 0.0 if abs(angle - 2 * math.pi) < 1e-9 else 2 * area
            return lateral + caps
        if kind in ("loft", "sweep"):
            return _mesh_area(self._base_mesh())
        if primitive.get("draft_angle"):
            return _drafted_area(primitive)
        return super().get_area()

    def duplicate(self, name: str | None = None) -> "Part3D":
        """An independent copy of this part: same primitive, recorded
        operations, placement and material. Parts referenced by operations
        (e.g. boolean cutters) are shared, not copied; backend geometry is
        rebuilt lazily on the copy."""
        part = type(self)(
            name=name or (f"{self.name}_copy" if self.name else None),
            description=self.description,
        )
        part._primitive = copy.deepcopy(self._primitive)
        part.operations = [dict(operation) for operation in self.operations]
        part._origin = Vec3(self._origin.x, self._origin.y, self._origin.z)
        part._start_origin = Vec3(
            self._start_origin.x, self._start_origin.y, self._start_origin.z
        )
        part.material = self.material
        part.ledger = AssemblyLedger(
            **{key: list(value) for key, value in vars(self.ledger).items()}
        )
        part.boolean_ledger = BooleanLedger(
            **{key: list(value) for key, value in vars(self.boolean_ledger).items()}
        )
        return part

    def linear_pattern(self, count: int, offset: Location) -> "Part3D":
        """Repeat this part ``count`` times in total (including this
        instance), each instance translated by ``offset`` from the previous
        one. ``offset`` may be a Location or an (x, y, z) sequence."""
        if int(count) < 1:
            raise ValueError("count must be at least 1 (it includes the original)")
        if not isinstance(offset, Location):
            offset = Location(*offset)
        self.operations.append(
            {"operation": "linear_pattern", "count": int(count), "offset": offset}
        )
        return self

    def circular_pattern(
        self,
        count: int,
        separation_angle: AngleWithUnit,
        center: Location | None = None,
        axis: str | tuple[float, float, float] = "z",
    ) -> "Part3D":
        """Repeat this part ``count`` times in total (including this
        instance), each instance rotated ``separation_angle`` further about
        ``axis`` through ``center`` (the origin by default). Bare numbers are
        degrees; strings may carry units ("0.5rad")."""
        if int(count) < 1:
            raise ValueError("count must be at least 1 (it includes the original)")
        self.operations.append(
            {
                "operation": "circular_pattern",
                "count": int(count),
                "separation_angle": AngleRadians(
                    _angle_to_radians(separation_angle, floats_are_degrees=True)
                ),
                "center": (
                    self.resolve_location(center) if center is not None else Location()
                ),
                "axis": _pattern_axis(axis),
            }
        )
        return self

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
        radius_or_shape: "LengthWithUnit | Part2D",
        *,
        amount: LengthWithUnit | None = None,
        end_location: Location | None = None,
        throughAll: bool = False,
    ) -> "Part3D":
        """Drill a hole into this part starting at ``start_location``.

        ``radius_or_shape`` is either a length (a plain round hole of that
        radius) or a :class:`Part2D` sketch, which is swept as the hole's
        cross-section -- pass a rectangle for a square hole or any custom
        sketch for a custom profile. The sketch's own origin is treated as the
        hole's axis.

        The hole's depth is set by exactly one of: ``amount`` (drill this far
        along the location's -Z normal), ``end_location`` (drill until this
        point), or ``throughAll=True`` (cut through all of the part's geometry
        along the drill axis)."""
        profile = radius_or_shape if isinstance(radius_or_shape, Part2D) else None
        depth_args = sum(
            (amount is not None, end_location is not None, bool(throughAll))
        )
        if depth_args != 1:
            raise ValueError(
                "Supply exactly one of amount=, end_location= or throughAll=True"
            )
        self.operations.append(
            {
                "operation": "hole",
                "start_location": start_location,
                "radius": None if profile is not None else LengthMeters(radius_or_shape),
                "profile": profile,
                "amount": LengthMeters(amount) if amount is not None else None,
                "end_location": end_location,
                "through_all": bool(throughAll),
            }
        )
        return self

    def export(self, location: str, include_assembly: bool = True) -> str:
        """Export the base solid as an ASCII STL. When other parts are joined
        to this one by assembly constraints (fixed/revolute/prismatic), the
        whole assembly is exported in assembled positions; pass
        ``include_assembly=False`` to export just this part. Feature
        operations recorded in ledgers (booleans, shell, holes, ...) require
        a federated backend and are not reflected in this mesh."""
        members = (
            self._assembly_members()
            if include_assembly
            else [(self, np.zeros(3))]
        )
        primitive = self._primitive or {}
        if len(members) == 1 and primitive.get("kind") == "imported":
            source = Path(primitive["file_path"])
            if source.suffix.lower() == Path(location).suffix.lower():
                shutil.copyfile(source, location)
                return location
        meshes = self._assembly_meshes(include_assembly)
        _write_ascii_stl(
            location, np.concatenate(meshes), self.name or "codetocad_part"
        )
        return location

    def _assembly_members(self) -> list[tuple["Part3D", np.ndarray]]:
        """This part plus every part joined to it by assembly constraints
        (recursively), each with the translation that assembles it."""
        return [(link.part, link.shift) for link in extract_links(self)]

    def _projection_mesh(self) -> np.ndarray | None:
        """The triangle mesh used to export and to draw this part, in its
        modeled pose. Defaults to the core primitive mesh; federated backends
        override it to tessellate their native solid, so exports and drawings
        reflect backend-only features (booleans, shells, holes, ...)."""
        return self._generate_mesh()

    def _assembly_meshes(self, include_assembly: bool) -> list[np.ndarray]:
        """The triangle mesh of this part -- or of the whole assembly, in
        assembled positions -- as a list of ``(N, 3, 3)`` arrays, one per
        member. Raises ``NotImplementedError`` (like :meth:`export`) for a part
        whose geometry needs a federated backend to mesh."""
        members = (
            self._assembly_members()
            if include_assembly
            else [(self, np.zeros(3))]
        )
        meshes = []
        for part, shift in members:
            triangles = part._projection_mesh()
            if triangles is None:
                raise NotImplementedError(
                    "Override export() to export this shape from your target "
                    "modeling application"
                )
            meshes.append(triangles + shift if np.any(shift) else triangles)
        return meshes

    def generate_drawing(
        self,
        location: str | None = None,
        *,
        views=DEFAULT_VIEWS,
        include_assembly: bool = True,
        crease_angle: AngleWithUnit = 15,
    ) -> "Part2D":
        """A 2D technical (CAD) drawing of this part, as an editable
        :class:`Part2D` (primitive kind ``"drawing"``). Export it to an SVG
        sheet with ``drawing.export("sheet.svg")``, or -- as a shortcut -- pass
        ``location`` here to write it in one call. The solid is projected into
        the named orthographic/pictorial views (front, top, right and isometric
        by default).

        Like :meth:`export`, this draws the whole assembly in assembled
        positions when other parts are joined to this one; pass
        ``include_assembly=False`` to draw just this part. ``views`` selects and
        orders the views (any of :data:`~codetocad.drawings.STANDARD_VIEWS`).
        ``crease_angle`` (bare numbers are degrees) is how sharp a dihedral must
        be to count as a drawn feature edge -- lower it to reveal gentler
        creases, raise it to keep smoothly tessellated surfaces clean.

        Feature operations that need a federated backend (booleans, shell,
        holes, ...) are reflected only when this part is federated to a backend
        that meshes them (e.g. Build123D); the core projects the primitive mesh.
        """
        from codetocad.drawings import drawing_from_meshes

        meshes = self._assembly_meshes(include_assembly)
        crease = _angle_to_radians(crease_angle, floats_are_degrees=True)
        drawing = drawing_from_meshes(
            meshes, self.name or "codetocad_part", views, crease_angle=crease
        )
        part = drawing.to_part2d(name=self.name)
        if location is not None:
            part.export(location)
        return part

    def _generate_mesh(self) -> np.ndarray | None:
        triangles = self._base_mesh()
        if triangles is None:
            return None
        for operation in self.operations:
            if operation["operation"] == "linear_pattern":
                triangles = _linear_pattern_mesh(triangles, operation)
            elif operation["operation"] == "circular_pattern":
                triangles = _circular_pattern_mesh(triangles, operation)
        return triangles

    def _base_mesh(self) -> np.ndarray | None:
        if self._primitive is None:
            return None
        kind = self._primitive["kind"]
        origin = self._origin
        draft = self._primitive.get("draft_angle", 0.0)
        if kind == "cube":
            half = _half_extents(self._primitive)
            return _box_mesh(*_bbox_around(origin, half), draft=draft)
        if kind == "cylinder":
            radius, height = self._primitive["radius"], self._primitive["height"]
            top_radius = (
                _drafted_top(radius, height, draft, "circle") if draft else radius
            )
            return _cylinder_mesh(radius, height, origin, top_radius=top_radius)
        if kind == "sphere":
            return _sphere_mesh(self._primitive["radius"], origin)
        if kind == "revolution":
            return _revolution_mesh(self._primitive)
        if kind == "loft":
            return _loft_mesh(self._primitive)
        if kind == "sweep":
            return _sweep_mesh(self._primitive)
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


def _draft_inset(height: float, draft: float) -> float:
    """How far a drafted wall moves inward over ``height`` (per side).
    Positive draft insets the top; negative flares it."""
    return height * math.tan(draft)


def _drafted_top(base: float, height: float, draft: float, what: str) -> float:
    """The tapered top dimension (radius or half-extent), raising if the draft
    is steep enough to collapse it."""
    top = base - _draft_inset(height, draft)
    if top <= 0:
        raise ValueError(
            f"Draft angle is too steep: it collapses the top {what} of this "
            f"{height:g}m-tall part. Reduce the draft angle or the height."
        )
    return top


def _drafted_volume(primitive: dict) -> float:
    draft, height = primitive["draft_angle"], primitive["height"]
    if primitive["kind"] == "cylinder":
        radius = primitive["radius"]
        top = _drafted_top(radius, height, draft, "circle")
        return math.pi * height / 3 * (radius**2 + radius * top + top**2)
    length, width = primitive["length"], primitive["width"]
    inset = 2 * _draft_inset(height, draft)  # full-dimension reduction
    top_length = _drafted_top(length / 2, height, draft, "face") * 2
    top_width = _drafted_top(width / 2, height, draft, "face") * 2
    mid_length, mid_width = length - inset / 2, width - inset / 2
    # Prismatoid rule (exact for a linearly tapered cross section).
    return (
        height
        / 6
        * (
            length * width
            + 4 * mid_length * mid_width
            + top_length * top_width
        )
    )


def _drafted_area(primitive: dict) -> float:
    draft, height = primitive["draft_angle"], primitive["height"]
    slant = height / math.cos(draft)  # true wall length over the height
    if primitive["kind"] == "cylinder":
        radius = primitive["radius"]
        top = _drafted_top(radius, height, draft, "circle")
        caps = math.pi * (radius**2 + top**2)
        return caps + math.pi * (radius + top) * slant
    length, width = primitive["length"], primitive["width"]
    top_length = _drafted_top(length / 2, height, draft, "face") * 2
    top_width = _drafted_top(width / 2, height, draft, "face") * 2
    caps = length * width + top_length * top_width
    lateral = ((length + top_length) + (width + top_width)) * slant
    return caps + lateral


def _bbox_around(origin: Vec3, half: Vec3) -> tuple[Vec3, Vec3]:
    return (
        Vec3(origin.x - half.x, origin.y - half.y, origin.z - half.z),
        Vec3(origin.x + half.x, origin.y + half.y, origin.z + half.z),
    )


def _pattern_axis(axis) -> tuple[float, float, float]:
    if isinstance(axis, str):
        try:
            return _PATTERN_AXES[axis.lower()]
        except KeyError:
            raise ValueError(
                f"Unknown pattern axis {axis!r}; use 'x', 'y', 'z' or a 3-vector"
            ) from None
    vector = np.asarray(axis, dtype=np.float64)
    magnitude = float(np.linalg.norm(vector))
    if vector.shape != (3,) or magnitude < 1e-12:
        raise ValueError("A pattern axis must be 'x', 'y', 'z' or a non-zero 3-vector")
    vector = vector / magnitude
    return (float(vector[0]), float(vector[1]), float(vector[2]))


def _revolve_axis(
    axis: str | tuple[float, float, float] | Edge,
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Resolve a revolve axis into ``(point_on_axis, unit_direction)``.

    Main axes ("x"/"y"/"z") and bare direction vectors pass through the world
    origin; an :class:`Edge` defines the axis by the line through its two
    vertices."""
    if isinstance(axis, Edge):
        start, end = axis.start.location, axis.end.location
        vector = np.array(
            [
                end.x.value - start.x.value,
                end.y.value - start.y.value,
                end.z.value - start.z.value,
            ]
        )
        magnitude = float(np.linalg.norm(vector))
        if magnitude < 1e-12:
            raise ValueError("Cannot revolve around a zero-length edge")
        vector = vector / magnitude
        point = (start.x.value, start.y.value, start.z.value)
        return point, (float(vector[0]), float(vector[1]), float(vector[2]))
    return (0.0, 0.0, 0.0), _pattern_axis(axis)


def _profile_area_perimeter(profile: dict) -> tuple[float, float]:
    """Planar area and boundary perimeter of a revolvable profile."""
    kind = profile["kind"]
    if kind == "rectangle":
        width, height = profile["width"], profile["height"]
        return width * height, 2 * (width + height)
    if kind == "circle":
        radius = profile["radius"]
        return math.pi * radius**2, 2 * math.pi * radius
    raise NotImplementedError(
        f"Revolved analysis is not available for a {kind!r} profile"
    )


def _revolve_offset_hint(direction: np.ndarray) -> str:
    """Which sketch-plane direction moves a profile away from this axis."""
    perpendicular = [
        name
        for name, unit in (("x", (1.0, 0.0, 0.0)), ("y", (0.0, 1.0, 0.0)))
        if abs(float(np.dot(unit, direction))) < 1e-9
    ]
    if perpendicular:
        return f"offset the sketch along {' or '.join(perpendicular)}"
    return "offset the sketch perpendicular to the axis"


def _revolve_centroid_radius(primitive: dict) -> float:
    """Distance from the profile centroid to the axis line. Raises if the axis
    runs through the profile, which sweeps a self-intersecting solid (and
    breaks the simple Pappus relation).

    A profile that merely *touches* the axis is fine -- that is the usual way
    to revolve a solid, e.g. a rectangle with one edge on the axis sweeps a
    cylinder.

    Relies on rectangle/circle profiles being centered on their origin, so the
    area centroid and boundary (curve) centroid coincide at ``profile_origin``.
    """
    centroid = np.array(primitive["profile_origin"], dtype=np.float64)
    point = np.array(primitive["axis_point"], dtype=np.float64)
    direction = np.array(primitive["axis_direction"], dtype=np.float64)
    relative = centroid - point
    radial = relative - np.dot(relative, direction) * direction
    radius = float(np.linalg.norm(radial))
    crosses = radius < 1e-9  # centroid on the axis => profile straddles it
    boundary = _profile_boundary(primitive["profile"], primitive["profile_origin"])
    if boundary is not None and not crosses:
        radial_unit = radial / radius
        # Signed position of each boundary point along the centroid's radial
        # direction. A strictly negative minimum puts boundary on both sides of
        # the axis, i.e. the axis cuts through the profile's interior; a zero
        # minimum just touches it, which is allowed.
        projections = (
            boundary - point - np.outer((boundary - point) @ direction, direction)
        ) @ radial_unit
        crosses = bool(projections.min() < -_AXIS_TOLERANCE)
    if crosses:
        raise ValueError(
            f"Cannot revolve this {primitive['profile']['kind']} profile: the "
            "axis of revolution passes through it, so the sweep would be "
            f"self-intersecting. {_revolve_offset_hint(direction)} so the whole "
            "profile sits on one side of the axis (touching it is fine)."
        )
    return radius


def _rotation_matrix(axis: tuple[float, float, float], angle: float) -> np.ndarray:
    """Rodrigues rotation matrix about the unit vector ``axis``."""
    x, y, z = axis
    skew = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    return np.eye(3) + math.sin(angle) * skew + (1 - math.cos(angle)) * (skew @ skew)


def _linear_pattern_mesh(triangles: np.ndarray, operation: dict) -> np.ndarray:
    offset = operation["offset"].to_numpy()
    return np.concatenate(
        [triangles + offset * i for i in range(operation["count"])]
    )


def _circular_pattern_mesh(triangles: np.ndarray, operation: dict) -> np.ndarray:
    center = operation["center"].to_numpy()
    angle = operation["separation_angle"].value
    instances = []
    for i in range(operation["count"]):
        rotation = _rotation_matrix(operation["axis"], angle * i)
        instances.append((triangles - center) @ rotation.T + center)
    return np.concatenate(instances)


def _profile_boundary(
    profile: dict, origin: tuple[float, float, float], segments: int = 64
) -> np.ndarray | None:
    """Closed boundary loop of a 2D profile as (M, 3) points in the XY plane,
    positioned at ``origin``. Returns ``None`` for profiles without a simple
    analytic outline (e.g. text)."""
    kind = profile["kind"]
    if kind == "rectangle":
        half_width, half_height = profile["width"] / 2, profile["height"] / 2
        points = np.array(
            [
                (-half_width, -half_height),
                (half_width, -half_height),
                (half_width, half_height),
                (-half_width, half_height),
            ]
        )
    elif kind == "circle":
        angles = np.linspace(0.0, 2 * math.pi, segments, endpoint=False)
        radius = profile["radius"]
        points = np.column_stack([radius * np.cos(angles), radius * np.sin(angles)])
    else:
        return None
    return np.column_stack(
        [
            points[:, 0] + origin[0],
            points[:, 1] + origin[1],
            np.full(len(points), origin[2]),
        ]
    )


def _revolution_mesh(primitive: dict, segments: int = 64) -> np.ndarray | None:
    """Triangulated surface of revolution of the profile boundary about the
    axis, with flat end caps when the sweep does not close a full turn."""
    boundary = _profile_boundary(primitive["profile"], primitive["profile_origin"])
    if boundary is None:
        return None
    point = np.array(primitive["axis_point"], dtype=np.float64)
    direction = np.array(primitive["axis_direction"], dtype=np.float64)
    angle = primitive["angle"]
    full_turn = abs(angle - 2 * math.pi) < 1e-9
    steps = max(2, int(round(segments * angle / (2 * math.pi))))
    thetas = np.linspace(0.0, angle, steps + 1)

    relative = boundary - point
    axial = relative @ direction
    radial = relative - np.outer(axial, direction)
    radius = np.linalg.norm(radial, axis=1)
    radial_unit = np.zeros_like(radial)
    nonzero = radius > 1e-12
    radial_unit[nonzero] = radial[nonzero] / radius[nonzero, None]
    normal_unit = np.cross(np.broadcast_to(direction, radial.shape), radial_unit)
    axis_base = point + np.outer(axial, direction)  # (M, 3), foot on the axis

    cos = np.cos(thetas)[None, :, None]
    sin = np.sin(thetas)[None, :, None]
    # rings[i, j] is boundary point i swept to angle thetas[j].
    rings = axis_base[:, None, :] + radius[:, None, None] * (
        cos * radial_unit[:, None, :] + sin * normal_unit[:, None, :]
    )

    count = len(boundary)
    next_index = (np.arange(count) + 1) % count
    lower = rings[:, :-1]  # (M, steps, 3)
    upper = rings[:, 1:]
    a, b = lower, lower[next_index]
    c, d = upper[next_index], upper
    side = np.concatenate(
        [
            np.stack([a, b, c], axis=-2).reshape(-1, 3, 3),
            np.stack([a, c, d], axis=-2).reshape(-1, 3, 3),
        ]
    )
    if full_turn:
        return side
    return np.concatenate([side, _revolution_caps(rings, next_index)])


def _sweep_path_points(path) -> list[tuple[float, float, float]]:
    """Normalise a sweep ``path`` into a list of at least two distinct 3D
    points. Accepts an :class:`Edge` or a sequence of Locations / 3-tuples."""
    if isinstance(path, Edge):
        start, end = path.start.location, path.end.location
        raw = [
            (start.x.value, start.y.value, start.z.value),
            (end.x.value, end.y.value, end.z.value),
        ]
    else:
        raw = []
        for point in path:
            if isinstance(point, Location):
                raw.append(point.to_tuple())
            else:
                coordinates = tuple(point)
                if len(coordinates) != 3:
                    raise ValueError("Each path point must have three coordinates")
                # Route through Location so coordinates may carry units ("5cm").
                raw.append(Location(*coordinates).to_tuple())
    # Drop consecutive duplicates: a zero-length segment has no direction to
    # orient the profile against.
    points: list[tuple[float, float, float]] = []
    for point in raw:
        if not points or np.linalg.norm(np.subtract(point, points[-1])) > 1e-12:
            points.append(point)
    if len(points) < 2:
        raise ValueError("A sweep path needs at least two distinct points")
    return points


def _align_z_rotation(direction: np.ndarray) -> np.ndarray:
    """Rotation matrix taking +Z onto the unit vector ``direction``."""
    magnitude = float(np.linalg.norm(direction))
    if magnitude < 1e-12:
        return np.eye(3)
    unit = np.asarray(direction, dtype=np.float64) / magnitude
    axis = np.cross((0.0, 0.0, 1.0), unit)
    sin = float(np.linalg.norm(axis))
    cos = float(unit[2])
    if sin < 1e-12:
        # Parallel (identity) or antiparallel (flip Z, keeping a right-handed
        # frame by also flipping Y).
        return np.eye(3) if cos > 0 else np.diag([1.0, -1.0, -1.0])
    axis = axis / sin
    return _rotation_matrix(
        (float(axis[0]), float(axis[1]), float(axis[2])), math.atan2(sin, cos)
    )


def _path_tangents(path: np.ndarray) -> np.ndarray:
    """Unit tangent at each path vertex: the segment direction at the ends, the
    averaged direction of the two adjoining segments in between."""
    segments = np.diff(path, axis=0)
    segments = segments / np.linalg.norm(segments, axis=1, keepdims=True)
    tangents = np.empty_like(path)
    tangents[0] = segments[0]
    tangents[-1] = segments[-1]
    if len(path) > 2:
        averaged = segments[:-1] + segments[1:]
        norms = np.linalg.norm(averaged, axis=1, keepdims=True)
        tangents[1:-1] = np.divide(
            averaged, norms, out=segments[1:].copy(), where=norms > 1e-12
        )
    return tangents


def _resample_loop(loop: np.ndarray, count: int) -> np.ndarray:
    """Resample a closed loop of points to ``count`` points spaced evenly by
    arc length, so loops with different vertex counts can be connected."""
    if len(loop) == count:
        return loop
    closed = np.vstack([loop, loop[:1]])
    distances = np.concatenate(
        [[0.0], np.cumsum(np.linalg.norm(np.diff(closed, axis=0), axis=1))]
    )
    targets = np.linspace(0.0, distances[-1], count, endpoint=False)
    return np.column_stack(
        [np.interp(targets, distances, closed[:, axis]) for axis in range(3)]
    )


def _loop_strip(lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    """Triangulate the band between two equal-length closed loops."""
    count = len(lower)
    next_index = (np.arange(count) + 1) % count
    a, b = lower, lower[next_index]
    c, d = upper[next_index], upper
    return np.concatenate(
        [np.stack([a, b, c], axis=1), np.stack([a, c, d], axis=1)]
    )


def _loop_cap(loop: np.ndarray, at_start: bool) -> np.ndarray:
    """Fan-triangulate a loop into a flat cap, wound to face outward: away from
    the body at the first loop, along the sweep at the last."""
    count = len(loop)
    next_index = (np.arange(count) + 1) % count
    hub = np.broadcast_to(loop.mean(axis=0), loop.shape)
    if at_start:
        return np.stack([hub, loop[next_index], loop], axis=1)
    return np.stack([hub, loop, loop[next_index]], axis=1)


def _tube_from_loops(loops: list[np.ndarray]) -> np.ndarray:
    """Skin a sequence of closed loops into a capped solid surface, connecting
    each loop to the next and closing the two ends."""
    resampled = [_resample_loop(loop, max(len(loop) for loop in loops)) for loop in loops]
    triangles = [
        _loop_strip(resampled[i], resampled[i + 1])
        for i in range(len(resampled) - 1)
    ]
    triangles.append(_loop_cap(resampled[0], at_start=True))
    triangles.append(_loop_cap(resampled[-1], at_start=False))
    return np.concatenate(triangles)


def _loft_mesh(primitive: dict, segments: int = 64) -> np.ndarray | None:
    """Triangulated surface lofted through the section boundary loops, capped
    at the first and last section."""
    loops = []
    for section in primitive["sections"]:
        boundary = _profile_boundary(section["profile"], section["origin"], segments)
        if boundary is None:
            return None
        loops.append(boundary)
    return _tube_from_loops(loops)


def _sweep_mesh(primitive: dict, segments: int = 64) -> np.ndarray | None:
    """Triangulated surface swept by the profile boundary along the path, the
    profile kept perpendicular to the local path tangent."""
    boundary = _profile_boundary(primitive["profile"], (0.0, 0.0, 0.0), segments)
    if boundary is None:
        return None
    path = np.array(primitive["path"], dtype=np.float64)
    tangents = _path_tangents(path)
    loops = [
        point + boundary @ _align_z_rotation(tangent).T
        for point, tangent in zip(path, tangents)
    ]
    return _tube_from_loops(loops)


def _mesh_volume(triangles: np.ndarray | None) -> float:
    """Volume enclosed by a closed, consistently wound triangle mesh, via the
    signed-tetrahedron (divergence) sum."""
    if triangles is None:
        raise NotImplementedError(
            "This part has no analytic geometry; override get_volume()"
        )
    v0, v1, v2 = triangles[:, 0], triangles[:, 1], triangles[:, 2]
    return abs(float(np.einsum("ij,ij->i", v0, np.cross(v1, v2)).sum())) / 6.0


def _mesh_area(triangles: np.ndarray | None) -> float:
    """Total surface area of a triangle mesh."""
    if triangles is None:
        raise NotImplementedError(
            "This part has no analytic geometry; override get_area()"
        )
    cross = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    return float(np.linalg.norm(cross, axis=1).sum()) / 2.0


def _revolution_caps(rings: np.ndarray, next_index: np.ndarray) -> np.ndarray:
    """Fan-triangulated profile caps at the first and last sweep angle, wound
    to face outward from the swept body."""
    start_loop, end_loop = rings[:, 0], rings[:, -1]
    start_center = start_loop.mean(axis=0)
    end_center = end_loop.mean(axis=0)
    start_hub = np.broadcast_to(start_center, start_loop.shape)
    end_hub = np.broadcast_to(end_center, end_loop.shape)
    start_cap = np.stack(
        [start_hub, start_loop[next_index], start_loop], axis=1
    )
    end_cap = np.stack([end_hub, end_loop, end_loop[next_index]], axis=1)
    return np.concatenate([start_cap, end_cap])


def _box_mesh(bbox_min: Vec3, bbox_max: Vec3, draft: float = 0.0) -> np.ndarray:
    x0, y0, z0 = bbox_min.to_tuple()
    x1, y1, z1 = bbox_max.to_tuple()
    # With draft the top face insets by height*tan(draft) on every side; the
    # bottom keeps its full extent. A negative draft flares the top instead.
    inset = _draft_inset(z1 - z0, draft)
    if draft and (x1 - inset <= x0 + inset or y1 - inset <= y0 + inset):
        raise ValueError(
            "Draft angle is too steep: it collapses the top face of this "
            f"{z1 - z0:g}m-tall part. Reduce the draft angle or the height."
        )
    tx0, tx1, ty0, ty1 = x0 + inset, x1 - inset, y0 + inset, y1 - inset
    vertices = np.array(
        [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (tx0, ty0, z1), (tx1, ty0, z1), (tx1, ty1, z1), (tx0, ty1, z1),
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
    radius: float,
    height: float,
    origin: Vec3,
    segments: int = 48,
    top_radius: float | None = None,
) -> np.ndarray:
    if top_radius is None:
        top_radius = radius
    z0, z1 = origin.z - height / 2, origin.z + height / 2
    angles = np.linspace(0.0, 2 * math.pi, segments, endpoint=False)
    cos, sin = np.cos(angles), np.sin(angles)
    bottom = np.column_stack(
        [origin.x + radius * cos, origin.y + radius * sin, np.full(segments, z0)]
    )
    top = np.column_stack(
        [
            origin.x + top_radius * cos,
            origin.y + top_radius * sin,
            np.full(segments, z1),
        ]
    )
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
