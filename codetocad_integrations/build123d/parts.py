"""Build123D adapter classes for CodeToCAD.

The adapter ``Part3D``/``Part2D`` subclasses replay the operations recorded by
the CodeToCAD API (in order) onto real Build123D solids: base primitive,
booleans, shell, fillet, chamfer, holes and transforms. Geometry queries,
analysis (area/volume/mass) and export all use the native OpenCascade shape.

Units are meters throughout, matching CodeToCAD's core.

Custom shapes: subclass ``Part3D`` and override ``build_native()`` to return
any Build123D ``Part``; all CodeToCAD operations still apply on top of it.
"""

from __future__ import annotations

import math
from pathlib import Path

import build123d as bd
import numpy as np

import codetocad
from codetocad.location import Location, quat_rotate_vector, quat_to_axis_angle
from codetocad.topology import Edge, Face, Vertex
from codetocad.units import LengthMeters, LengthWithUnit
from codetocad.vectors import Vec3


def _vector_to_location(vector) -> Location:
    return Location(float(vector.X), float(vector.Y), float(vector.Z))


def _to_bd_location(location: Location) -> bd.Location:
    axis, angle = quat_to_axis_angle(location.quat)
    return bd.Location(location.to_tuple(), axis, angle)


def _rotation_aligning_z(direction: np.ndarray) -> tuple[tuple[float, float, float], float]:
    """Axis/angle (degrees) rotating +Z onto ``direction`` (unit vector)."""
    z = np.array([0.0, 0.0, 1.0])
    dot = float(np.clip(np.dot(z, direction), -1.0, 1.0))
    axis = np.cross(z, direction)
    magnitude = float(np.linalg.norm(axis))
    if magnitude < 1e-12:
        if dot > 0:
            return ((0.0, 0.0, 1.0), 0.0)
        return ((1.0, 0.0, 0.0), 180.0)
    axis = axis / magnitude
    return (
        (float(axis[0]), float(axis[1]), float(axis[2])),
        math.degrees(math.acos(dot)),
    )


def _base_solid(primitive: dict, start_origin: Vec3) -> bd.Part:
    kind = primitive["kind"]
    if kind == "cube":
        solid = bd.Box(primitive["length"], primitive["width"], primitive["height"])
    elif kind == "cylinder":
        solid = bd.Cylinder(primitive["radius"], primitive["height"])
    elif kind == "sphere":
        solid = bd.Sphere(primitive["radius"])
    elif kind == "extrusion":
        height = primitive["height"]
        sketch = _base_sketch(primitive["profile"])
        solid = bd.Pos(0, 0, -height / 2) * bd.extrude(sketch, amount=height)
    elif kind == "revolution":
        origin = primitive["profile_origin"]
        sketch = bd.Pos(*origin) * _base_sketch(primitive["profile"])
        axis = bd.Axis(primitive["axis_point"], primitive["axis_direction"])
        solid = bd.revolve(
            sketch, axis=axis, revolution_arc=math.degrees(primitive["angle"])
        )
    elif kind == "imported":
        solid = _import_shape(primitive["file_path"])
    else:
        raise NotImplementedError(
            f"Build123D adapter cannot build a {kind!r} primitive"
        )
    return bd.Pos(start_origin.x, start_origin.y, start_origin.z) * solid


def _base_sketch(primitive: dict) -> bd.Sketch:
    kind = primitive["kind"]
    if kind == "rectangle":
        return bd.Rectangle(primitive["width"], primitive["height"])
    if kind == "circle":
        return bd.Circle(primitive["radius"])
    if kind == "text":
        return bd.Text(
            primitive["text"],
            font_size=primitive["size"],
            font=primitive["font"],
        )
    raise NotImplementedError(
        f"Build123D adapter cannot build a {kind!r} sketch"
    )


def _import_shape(file_path: str) -> bd.Part:
    suffix = Path(file_path).suffix.lower()
    if suffix in (".stl", ".3mf"):
        shapes = bd.Mesher().read(file_path)
        return shapes[0] if len(shapes) == 1 else bd.Compound(children=shapes)
    if suffix in (".step", ".stp"):
        return bd.import_step(file_path)
    raise NotImplementedError(f"Cannot import {suffix!r} files with Build123D")


class Part3D(codetocad.Part3D):
    """A CodeToCAD Part3D federated to Build123D."""

    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._native: bd.Part | None = None
        self._native_op_count = -1

    # -- building --

    def build_native(self) -> bd.Part:
        """The base solid, before CodeToCAD operations are applied. Override
        this in a subclass to define a custom shape with the Build123D API."""
        if self._primitive is None:
            raise NotImplementedError(
                "Override build_native() to return a build123d Part for this "
                "shape"
            )
        return _base_solid(self._primitive, self._start_origin)

    def build(self):
        """Build the shape in Build123D, replaying all recorded operations."""
        solid = self.build_native()
        origin = np.array(self._start_origin.to_tuple())
        for operation in self.operations:
            solid, origin = self._apply_operation(solid, origin, operation)
        if self.material is not None and self.material.color_rgba is not None:
            solid.color = bd.Color(*self.material.color_rgba.to_tuple())
        self._native = solid
        self._native_op_count = len(self.operations)
        return self

    def get_native(self) -> bd.Part:
        """The Build123D solid, (re)building it if operations changed."""
        if self._native is None or self._native_op_count != len(self.operations):
            self.build()
        return self._native

    # -- operation replay --

    def _apply_operation(self, solid, origin: np.ndarray, operation: dict):
        name = operation["operation"]
        if name in codetocad.CONSTRAINT_OPERATIONS:
            # Assembly constraints don't change geometry; simulation
            # integrations turn them into joints.
            return solid, origin
        if name == "hole":
            return self._apply_hole(solid, operation), origin
        if name == "shell":
            return self._apply_shell(solid, operation), origin
        if name in ("fillet", "chamfer"):
            return self._apply_fillet_chamfer(solid, operation), origin
        if name in ("subtract", "union", "intersect"):
            return self._apply_boolean(solid, operation), origin
        if name in codetocad.PATTERN_OPERATIONS:
            return self._apply_pattern(solid, operation), origin
        if name == "transform":
            return self._apply_transform(solid, origin, operation)
        raise NotImplementedError(
            f"Build123D adapter cannot apply operation {name!r}"
        )

    def _apply_hole(self, solid, operation: dict):
        start_location = self.resolve_location(operation["start_location"])
        radius = operation["radius"].value
        start = start_location.to_numpy()
        if operation["end_location"] is not None:
            end = self.resolve_location(operation["end_location"]).to_numpy()
            depth = float(np.linalg.norm(end - start))
            direction = (end - start) / depth
        else:
            depth = operation["amount"].value
            # Drill along the location's -Z normal (into the part by default).
            direction = quat_rotate_vector(start_location.quat, (0.0, 0.0, -1.0))
            if start_location.inverted:
                direction = -direction
            end = start + direction * depth
        center = (start + end) / 2
        axis, angle = _rotation_aligning_z(direction)
        cutter = bd.Location(tuple(center), axis, angle) * bd.Cylinder(radius, depth)
        return solid - cutter

    def _apply_shell(self, solid, operation: dict):
        thickness = operation["thickness"].value
        openings = None
        if operation["start_at_location"] is not None:
            target = self.resolve_location(operation["start_at_location"])
            openings = self._nearest_native(
                solid.faces(), target, "face to open the shell at"
            )
        return bd.offset(solid, amount=-thickness, openings=openings)

    def _apply_fillet_chamfer(self, solid, operation: dict):
        native_edges = []
        current_edges = solid.edges()
        for edge in operation["edges"] or []:
            reference = (
                _vector_to_location(edge.native.center())
                if edge.native is not None
                else edge.midpoint
            )
            native_edges.append(
                self._nearest_native(current_edges, reference, "edge")
            )
        for face in operation["faces"] or []:
            reference = (
                _vector_to_location(face.native.center())
                if face.native is not None
                else face.center
            )
            native_face = self._nearest_native(solid.faces(), reference, "face")
            native_edges.extend(native_face.edges())
        if not native_edges:
            native_edges = list(current_edges)
        amount = operation["amount"].value
        if operation["operation"] == "fillet":
            return bd.fillet(native_edges, radius=amount)
        return bd.chamfer(native_edges, length=amount)

    def _apply_boolean(self, solid, operation: dict):
        other = operation["other_part"]
        other_solid = adapt(other).get_native() if not isinstance(other, Part3D) else other.get_native()
        location = operation["location"]
        other_location = operation["other_location"]
        if location is not None and other_location is not None:
            anchor = self.resolve_location(location).to_numpy()
            other_anchor = other.resolve_location(other_location).to_numpy()
            offset = anchor - other_anchor
            other_solid = bd.Pos(*offset) * other_solid
        if operation["operation"] == "subtract":
            return solid - other_solid
        if operation["operation"] == "union":
            return solid + other_solid
        return solid & other_solid

    def _apply_pattern(self, solid, operation: dict):
        count = operation["count"]
        result = solid
        if operation["operation"] == "linear_pattern":
            offset = operation["offset"].to_numpy()
            for i in range(1, count):
                result = result + bd.Pos(*(offset * i)) * solid
            return result
        center = operation["center"].to_numpy()
        axis = operation["axis"]
        step_deg = math.degrees(operation["separation_angle"].value)
        for i in range(1, count):
            rotated = bd.Pos(*center) * (
                bd.Location((0, 0, 0), axis, step_deg * i)
                * (bd.Pos(*(-center)) * solid)
            )
            result = result + rotated
        return result

    def _apply_transform(self, solid, origin: np.ndarray, operation: dict):
        location: Location = operation["location"]
        translation = location.to_numpy()
        if operation["mode"] == "absolute":
            delta = translation - origin
            origin = translation
        else:
            delta = translation
            origin = origin + delta
        solid = bd.Pos(*delta) * solid
        axis, angle = quat_to_axis_angle(location.quat)
        if abs(angle) > 1e-9:
            # Rotate about the part's current origin.
            solid = bd.Pos(*origin) * (
                bd.Location((0, 0, 0), axis, angle) * (bd.Pos(*(-origin)) * solid)
            )
        return solid, origin

    @staticmethod
    def _nearest_native(shapes, target: Location, what: str):
        shapes = list(shapes)
        if not shapes:
            raise ValueError(f"The solid has no {what}")
        centers = np.array(
            [[s.center().X, s.center().Y, s.center().Z] for s in shapes]
        )
        distances = np.linalg.norm(centers - target.to_numpy(), axis=1)
        return shapes[int(np.argmin(distances))]

    # -- geometry queries on native topology --

    def _native_vertices(self) -> list[Vertex]:
        return [
            Vertex(_vector_to_location(v.center()), native=v)
            for v in self.get_native().vertices()
        ]

    def _native_edges(self) -> list[Edge]:
        edges = []
        for edge in self.get_native().edges():
            start, end = edge.position_at(0), edge.position_at(1)
            edges.append(
                Edge(
                    Vertex(_vector_to_location(start)),
                    Vertex(_vector_to_location(end)),
                    native=edge,
                )
            )
        return edges

    def _native_faces(self) -> list[Face]:
        return [
            Face(
                [_native_vertex(v) for v in face.vertices()],
                native=face,
            )
            for face in self.get_native().faces()
        ]

    def get_vertex(self, location, tolerance: float = 1e-2) -> Vertex:
        return self._nearest(
            self._native_vertices(),
            lambda v: v.location,
            self._resolve(location),
            tolerance,
        )

    def get_edge(self, location, tolerance: float = 1e-2) -> Edge:
        return self._nearest(
            self._native_edges(),
            lambda e: _vector_to_location(e.native.center()),
            self._resolve(location),
            tolerance,
        )

    def get_face(self, location, tolerance: float = 1e-2) -> Face:
        return self._nearest(
            self._native_faces(),
            lambda f: _vector_to_location(f.native.center()),
            self._resolve(location),
            tolerance,
        )

    def get_vertices(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_vertices(), lambda v: v.location, locations, tolerance
        )

    def get_edges(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_edges(),
            lambda e: _vector_to_location(e.native.center()),
            locations,
            tolerance,
        )

    def get_faces(self, location1, location2, location3=None, location4=None, tolerance: float = 1e-2):
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        return self._filter_bounded(
            self._native_faces(),
            lambda f: _vector_to_location(f.native.center()),
            locations,
            tolerance,
        )

    # -- analysis and export on the native solid --

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        box = self.get_native().bounding_box()
        return (
            Vec3(box.min.X, box.min.Y, box.min.Z),
            Vec3(box.max.X, box.max.Y, box.max.Z),
        )

    def get_volume(self) -> float:
        return float(self.get_native().volume)

    def get_area(self) -> float:
        return float(self.get_native().area)

    def export(self, location: str) -> str:
        solid = self.get_native()
        suffix = Path(location).suffix.lower()
        if suffix == ".stl":
            bd.export_stl(solid, location)
        elif suffix in (".step", ".stp"):
            bd.export_step(solid, location)
        elif suffix == ".3mf":
            mesher = bd.Mesher()
            mesher.add_shape(solid)
            mesher.write(location)
        else:
            raise ValueError(
                f"Unsupported export format {suffix!r}; use .stl, .step or .3mf"
            )
        return location


def _native_vertex(native) -> Vertex:
    return Vertex(_vector_to_location(native.center()), native=native)


class Part2D(codetocad.Part2D):
    """A CodeToCAD Part2D (sketch) federated to Build123D."""

    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._native: bd.Sketch | None = None

    def build_native(self) -> bd.Sketch:
        if self._primitive is None:
            raise NotImplementedError(
                "Override build_native() to return a build123d Sketch for "
                "this shape"
            )
        sketch = _base_sketch(self._primitive)
        return bd.Pos(self._start_origin.x, self._start_origin.y) * sketch

    def build(self):
        self._native = self.build_native()
        return self

    def get_native(self) -> bd.Sketch:
        if self._native is None:
            self.build()
        return self._native

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        box = self.get_native().bounding_box()
        return (
            Vec3(box.min.X, box.min.Y, box.min.Z),
            Vec3(box.max.X, box.max.Y, box.max.Z),
        )

    def get_area(self) -> float:
        return float(self.get_native().area)

    def extrude(self, height: LengthWithUnit) -> Part3D:
        return adapt(super().extrude(height))

    def revolve(self, angle=360, axis="y") -> Part3D:
        return adapt(super().revolve(angle, axis))


class ElectricalComponent(Part3D, codetocad.ECADMixin):
    def __init__(self, name: str | None = None, description: str | None = None):
        super().__init__(name, description)
        self._init_ecad()


def adapt(part) -> Part2D | Part3D:
    """Adapt any core CodeToCAD part (with its recorded operations, material,
    ledgers, ...) into a Build123D-federated part."""
    if isinstance(part, (Part2D, Part3D)):
        return part
    if isinstance(part, codetocad.ElectricalComponent):
        adapter_class = ElectricalComponent
    elif isinstance(part, codetocad.Part2D):
        adapter_class = Part2D
    elif isinstance(part, codetocad.Part3D):
        adapter_class = Part3D
    else:
        raise TypeError(f"Cannot adapt {type(part).__name__} to Build123D")
    adapted = adapter_class(part.name, part.description)
    state = dict(part.__dict__)
    state.pop("_native", None)
    adapted.__dict__.update(state)
    return adapted


# -- factories --


def make_cube(
    length: LengthWithUnit,
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part3D:
    """Calls Build123D's ``Box(length, width, height)`` in ``build()``."""
    return adapt(codetocad.cube(length, width, height, start_location))


make_box = make_cube


def make_cylinder(
    radius: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part3D:
    return adapt(codetocad.cylinder(radius, height, start_location))


def make_sphere(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part3D:
    return adapt(codetocad.sphere(radius, start_location))


def make_import(
    file_path: str, start_location: Location | None = None
) -> Part3D:
    return adapt(codetocad.import_file(file_path, start_location))


def make_rectangle(
    width: LengthWithUnit,
    height: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    return adapt(codetocad.rectangle(width, height, start_location))


def make_circle(
    radius: LengthWithUnit, start_location: Location | None = None
) -> Part2D:
    return adapt(codetocad.circle(radius, start_location))


def make_text(
    text: str,
    font: str,
    size: LengthWithUnit,
    start_location: Location | None = None,
) -> Part2D:
    return adapt(codetocad.text(text, font, size, start_location))


def make_led(**kwargs) -> ElectricalComponent:
    return adapt(codetocad.led(**kwargs))


def make_resistor(resistance: float, **kwargs) -> ElectricalComponent:
    return adapt(codetocad.resistor(resistance, **kwargs))


def make_capacitor(capacitance: float, **kwargs) -> ElectricalComponent:
    return adapt(codetocad.capacitor(capacitance, **kwargs))


def make_fastener(
    fastener: codetocad.CommonFasteners, length: LengthWithUnit | None = None
) -> Part3D:
    return adapt(fastener.build(length))
