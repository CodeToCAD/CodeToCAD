"""Mixins that extend the functionality of Part2D and Part3D.

Geometry queries and analysis operate on the part's bounding-box topology by
default; a federated backend (Blender, FreeCAD, Build123D, ...) is expected to
override these with native topology.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from .ledgers import BooleanLedger
from .location import Location
from .topology import Edge, Face, Vertex

if TYPE_CHECKING:
    from .parts import Part3D


class BooleanMixin:
    """CSG boolean operations. Operations are recorded on the
    ``boolean_ledger`` for the federated application to build."""

    def _init_boolean(self):
        self.boolean_ledger = BooleanLedger()

    def subtract(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.subtracted_parts += [other_part]
        return self

    def union(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.unioned_parts += [other_part]
        return self

    def intersect(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.intersected_parts += [other_part]
        return self


class GeometryQueryMixin:
    """Query vertices, edges and faces near Locations.

    The default implementation queries the part's bounding-box topology
    (8 vertices, 12 edges, 6 faces)."""

    def _bounding_box_topology(self) -> tuple[list[Vertex], list[Edge], list[Face]]:
        bbox_min, bbox_max = self.get_bounding_box()
        xs = (bbox_min.x, bbox_max.x)
        ys = (bbox_min.y, bbox_max.y)
        zs = (bbox_min.z, bbox_max.z)
        corners = {
            (i, j, k): Vertex(Location(xs[i], ys[j], zs[k]))
            for i in (0, 1)
            for j in (0, 1)
            for k in (0, 1)
        }
        edges = []
        for (i, j, k), vertex in corners.items():
            if i == 0:
                edges.append(Edge(vertex, corners[(1, j, k)]))
            if j == 0:
                edges.append(Edge(vertex, corners[(i, 1, k)]))
            if k == 0:
                edges.append(Edge(vertex, corners[(i, j, 1)]))
        faces = []
        for axis in range(3):
            for side in (0, 1):
                face_vertices = [
                    vertex
                    for key, vertex in corners.items()
                    if key[axis] == side
                ]
                faces.append(Face(face_vertices))
        return list(corners.values()), edges, faces

    @staticmethod
    def _nearest(entities, key, target: Location, tolerance: float):
        if not entities:
            raise ValueError("The part has no topology to query")
        best = min(entities, key=lambda e: key(e).distance_to(target).value)
        if key(best).distance_to(target).value > tolerance:
            raise ValueError(
                f"No geometry found within {tolerance} of {target.to_tuple()}"
            )
        return best

    @staticmethod
    def _bounds_of(locations: list[Location], tolerance: float):
        points = [loc.to_tuple() for loc in locations]
        lower = [min(p[axis] for p in points) - tolerance for axis in range(3)]
        upper = [max(p[axis] for p in points) + tolerance for axis in range(3)]

        def contains(loc: Location) -> bool:
            point = loc.to_tuple()
            return all(lower[axis] <= point[axis] <= upper[axis] for axis in range(3))

        return contains

    def _resolve(self, loc) -> Location:
        if hasattr(self, "resolve_location"):
            return self.resolve_location(loc)
        return loc

    def get_face(self, location: Location, tolerance: float = 1e-2) -> Face:
        _, _, faces = self._bounding_box_topology()
        return self._nearest(faces, lambda f: f.center, self._resolve(location), tolerance)

    def get_edge(self, location: Location, tolerance: float = 1e-2) -> Edge:
        _, edges, _ = self._bounding_box_topology()
        return self._nearest(edges, lambda e: e.midpoint, self._resolve(location), tolerance)

    def get_vertex(self, location: Location, tolerance: float = 1e-2) -> Vertex:
        vertices, _, _ = self._bounding_box_topology()
        return self._nearest(
            vertices, lambda v: v.location, self._resolve(location), tolerance
        )

    def get_faces(
        self,
        location1: Location,
        location2: Location,
        location3: Location | None = None,
        location4: Location | None = None,
        tolerance: float = 1e-2,
    ) -> list[Face]:
        """Get faces bounded by locations."""
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        contains = self._bounds_of(locations, tolerance)
        _, _, faces = self._bounding_box_topology()
        return [face for face in faces if contains(face.center)]

    def get_edges(
        self,
        location1: Location,
        location2: Location,
        location3: Location | None = None,
        location4: Location | None = None,
        tolerance: float = 1e-2,
    ) -> list[Edge]:
        """Get edges bounded by locations."""
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        contains = self._bounds_of(locations, tolerance)
        _, edges, _ = self._bounding_box_topology()
        return [edge for edge in edges if contains(edge.midpoint)]

    def get_vertices(
        self,
        location1: Location,
        location2: Location,
        location3: Location | None = None,
        location4: Location | None = None,
        tolerance: float = 1e-2,
    ) -> list[Vertex]:
        """Get vertices bounded by locations."""
        locations = [self._resolve(l) for l in (location1, location2, location3, location4) if l is not None]
        contains = self._bounds_of(locations, tolerance)
        vertices, _, _ = self._bounding_box_topology()
        return [vertex for vertex in vertices if contains(vertex.location)]


class GeometryAnalysisMixin:
    """Area/volume analysis of the part's base primitive.

    Feature operations (booleans, shells, holes, fillets) are recorded in
    ledgers and are not reflected here; a federated backend should override
    these for exact analysis."""

    def get_area(self) -> float:
        """Surface area (3D) or profile area (2D) in square meters."""
        primitive = getattr(self, "_primitive", None)
        if primitive is None:
            raise NotImplementedError(
                "get_area is not available for this part; override it or use a "
                "federated backend"
            )
        kind = primitive["kind"]
        if kind == "cube":
            length, width, height = (
                primitive["length"],
                primitive["width"],
                primitive["height"],
            )
            return 2 * (length * width + width * height + length * height)
        if kind == "cylinder":
            radius, height = primitive["radius"], primitive["height"]
            return 2 * math.pi * radius * (radius + height)
        if kind == "sphere":
            return 4 * math.pi * primitive["radius"] ** 2
        if kind == "rectangle":
            return primitive["width"] * primitive["height"]
        if kind == "circle":
            return math.pi * primitive["radius"] ** 2
        raise NotImplementedError(f"get_area is not implemented for {kind!r} parts")

    def get_volume(self) -> float:
        """Volume in cubic meters."""
        primitive = getattr(self, "_primitive", None)
        if primitive is None:
            raise NotImplementedError(
                "get_volume is not available for this part; override it or use "
                "a federated backend"
            )
        kind = primitive["kind"]
        if kind == "cube":
            return primitive["length"] * primitive["width"] * primitive["height"]
        if kind == "cylinder":
            return math.pi * primitive["radius"] ** 2 * primitive["height"]
        if kind == "sphere":
            return 4 / 3 * math.pi * primitive["radius"] ** 3
        if kind in ("rectangle", "circle", "text"):
            raise ValueError("2D parts have no volume; extrude them first")
        raise NotImplementedError(f"get_volume is not implemented for {kind!r} parts")


class ECADMixin:
    """Electrical properties for ECAD components. A custom Part3D class can
    inherit this and override the relevant methods."""

    def _init_ecad(self):
        self.voltage_rating: float | None = None
        """Maximum voltage, in volts."""
        self.current_limit: float | None = None
        """Maximum continuous current, in amps."""
        self.resistance: float | None = None
        """Resistance in ohms."""
        self.capacitance: float | None = None
        """Capacitance in farads."""
        self.inductance: float | None = None
        """Inductance in henries."""
        self.forward_voltage: float | None = None
        """Forward voltage drop, in volts (diodes/LEDs)."""
        self.power_rating: float | None = None
        """Power rating in watts."""

    def set_electrical_properties(
        self,
        *,
        voltage_rating: float | None = None,
        current_limit: float | None = None,
        resistance: float | None = None,
        capacitance: float | None = None,
        inductance: float | None = None,
        forward_voltage: float | None = None,
        power_rating: float | None = None,
    ):
        for attr_name, value in (
            ("voltage_rating", voltage_rating),
            ("current_limit", current_limit),
            ("resistance", resistance),
            ("capacitance", capacitance),
            ("inductance", inductance),
            ("forward_voltage", forward_voltage),
            ("power_rating", power_rating),
        ):
            if value is not None:
                setattr(self, attr_name, float(value))
        return self

    def get_electrical_properties(self) -> dict[str, float | None]:
        return {
            "voltage_rating": self.voltage_rating,
            "current_limit": self.current_limit,
            "resistance": self.resistance,
            "capacitance": self.capacitance,
            "inductance": self.inductance,
            "forward_voltage": self.forward_voltage,
            "power_rating": self.power_rating,
        }


class CameraMixin:
    """Camera sensor. Inherit in a custom Part3D class and override the
    relevant methods."""

    resolution: tuple[int, int] = (1920, 1080)
    field_of_view = "60 deg"

    def configure_camera(self, resolution=None, field_of_view=None):
        if resolution is not None:
            self.resolution = resolution
        if field_of_view is not None:
            self.field_of_view = field_of_view
        return self

    def capture_image(self):
        raise NotImplementedError("Override capture_image() for your camera")


class IMUMixin:
    """Inertial measurement unit sensor mixin."""

    def read_acceleration(self):
        raise NotImplementedError("Override read_acceleration() for your IMU")

    def read_angular_velocity(self):
        raise NotImplementedError("Override read_angular_velocity() for your IMU")

    def read_magnetic_field(self):
        raise NotImplementedError("Override read_magnetic_field() for your IMU")


class MicrophoneMixin:
    """Microphone sensor mixin."""

    sample_rate_hz: int = 48000

    def record_audio(self, duration_seconds: float):
        raise NotImplementedError("Override record_audio() for your microphone")


class DCMotorMixin:
    """DC motor actuator mixin."""

    nominal_voltage: float | None = None
    stall_torque_nm: float | None = None
    no_load_speed_rpm: float | None = None

    def set_speed(self, rpm: float):
        self._target_speed_rpm = float(rpm)
        return self

    def get_speed(self) -> float:
        return getattr(self, "_target_speed_rpm", 0.0)


class BLDCMotorMixin(DCMotorMixin):
    """Brushless DC motor actuator mixin."""

    kv_rating: float | None = None
    pole_pairs: int | None = None
