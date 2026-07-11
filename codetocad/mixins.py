"""Mixins that extend the functionality of Part2D and Part3D.

Geometry queries and analysis operate on the part's bounding-box topology by
default; a federated backend (Blender, FreeCAD, Build123D, ...) is expected to
override these with native topology.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np

from codetocad.ledgers import BooleanLedger
from codetocad.location import Location
from codetocad.topology import Edge, Face, Vertex

if TYPE_CHECKING:
    from codetocad.parts import Part3D


class BooleanMixin:
    """CSG boolean operations. Operations are recorded on the
    ``boolean_ledger`` (and in order on ``operations``) for the federated
    application to build."""

    def _init_boolean(self):
        self.boolean_ledger = BooleanLedger()

    def _record_boolean(self, operation, location, other_part, other_location):
        if hasattr(self, "operations"):
            self.operations.append(
                {
                    "operation": operation,
                    "location": location,
                    "other_part": other_part,
                    "other_location": other_location,
                }
            )

    def subtract(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.subtracted_parts += [other_part]
        self._record_boolean("subtract", location, other_part, other_location)
        return self

    def union(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.unioned_parts += [other_part]
        self._record_boolean("union", location, other_part, other_location)
        return self

    def intersect(
        self,
        location: Location | None = None,
        other_part: "Part3D | None" = None,
        other_location: Location | None = None,
    ) -> "Part3D":
        self.boolean_ledger.intersected_parts += [other_part]
        self._record_boolean("intersect", location, other_part, other_location)
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
        points = np.array([key(entity).to_numpy() for entity in entities])
        distances = np.linalg.norm(points - target.to_numpy(), axis=1)
        best_index = int(np.argmin(distances))
        if distances[best_index] > tolerance:
            raise ValueError(
                f"No geometry found within {tolerance} of {target.to_tuple()}"
            )
        return entities[best_index]

    @staticmethod
    def _filter_bounded(entities, key, locations: list[Location], tolerance: float):
        bounds = np.array([loc.to_numpy() for loc in locations])
        lower = bounds.min(axis=0) - tolerance
        upper = bounds.max(axis=0) + tolerance
        points = np.array([key(entity).to_numpy() for entity in entities])
        inside = np.all((points >= lower) & (points <= upper), axis=1)
        return [entity for entity, keep in zip(entities, inside) if keep]

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
        _, _, faces = self._bounding_box_topology()
        return self._filter_bounded(faces, lambda f: f.center, locations, tolerance)

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
        _, edges, _ = self._bounding_box_topology()
        return self._filter_bounded(edges, lambda e: e.midpoint, locations, tolerance)

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
        vertices, _, _ = self._bounding_box_topology()
        return self._filter_bounded(
            vertices, lambda v: v.location, locations, tolerance
        )


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


class SensorMixin:
    """Base sensor mixin: a device that produces values.

    Bind an instance to a ``Microcontroller`` pin with
    ``microcontroller.bind_sensor(sensor, pin=...)``; telemetry received
    over the microcontroller's communication channel then updates
    ``read()`` and is emitted on ``events`` (an ``EventStream``, so it can
    be mapped through ``codetocad.signals`` filters). Without a
    microcontroller, override ``read()`` for direct hardware access."""

    sample_rate_hz: float = 10.0

    @property
    def events(self):
        from codetocad.communication import EventStream

        stream = getattr(self, "_sensor_events", None)
        if stream is None:
            stream = self._sensor_events = EventStream()
        return stream

    def read(self):
        """The latest sample; None before the first one arrives."""
        return getattr(self, "_last_value", None)

    def _update(self, value, t: float | None = None):
        """Record a sample (called by the bound Microcontroller)."""
        self._last_value = value
        self._last_sample_time = t
        self.events.emit(value)
        return value


class ActuatorMixin:
    """Base actuator mixin: a device that accepts commands.

    Bind an instance to a ``Microcontroller`` pin with
    ``microcontroller.bind_actuator(actuator, pin=...)``; ``write()`` then
    sends the command over the microcontroller's communication channel when
    connected (and always records it locally)."""

    def write(self, value):
        self._last_command = value
        binding = getattr(self, "_binding", None)
        if binding is not None:
            binding.send(value)
        return self

    def get_last_command(self):
        return getattr(self, "_last_command", None)


class CameraMixin(SensorMixin):
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


class IMUMixin(SensorMixin):
    """Inertial measurement unit sensor mixin (e.g. MPU6050/MPU9250 over
    I2C). Bound telemetry values are dicts; these helpers pull out the
    conventional keys."""

    def read_acceleration(self):
        """(ax, ay, az) in m/s^2 from the ``accel`` telemetry key."""
        return (self.read() or {}).get("accel")

    def read_angular_velocity(self):
        """(gx, gy, gz) in rad/s from the ``gyro`` telemetry key."""
        return (self.read() or {}).get("gyro")

    def read_magnetic_field(self):
        """(mx, my, mz) in uT from the ``mag`` telemetry key."""
        return (self.read() or {}).get("mag")


class MicrophoneMixin(SensorMixin):
    """Microphone sensor mixin."""

    sample_rate_hz: float = 48000

    def record_audio(self, duration_seconds: float):
        raise NotImplementedError("Override record_audio() for your microphone")


class EncoderMixin(SensorMixin):
    """Rotary encoder sensor (quadrature or single-channel).

    Telemetry values are dicts ``{"count": <ticks>, "rpm": <velocity>}``
    (the micropython integration's encoder routine emits both)."""

    counts_per_revolution: int = 2048

    def read_count(self) -> int | None:
        value = self.read()
        return value.get("count") if isinstance(value, dict) else value

    def read_position_degrees(self) -> float | None:
        count = self.read_count()
        if count is None:
            return None
        return 360.0 * count / self.counts_per_revolution

    def read_velocity_rpm(self) -> float | None:
        value = self.read()
        return value.get("rpm") if isinstance(value, dict) else None


class CurrentSensorMixin(SensorMixin):
    """Current measurement sensor (shunt + amplifier like the INA219/ACS712,
    or a motor driver's current-sense pin read through an ADC).

    ``amps_per_volt`` converts the raw ADC voltage to amps (e.g. the
    ACS712-05B outputs 185 mV/A -> ``amps_per_volt = 1/0.185``);
    ``zero_offset_volts`` is the output at zero current (VCC/2 for
    bidirectional hall sensors)."""

    amps_per_volt: float = 1.0
    zero_offset_volts: float = 0.0

    def read_current(self) -> float | None:
        volts = self.read()
        if volts is None:
            return None
        return (float(volts) - self.zero_offset_volts) * self.amps_per_volt


class MotorMixin(ActuatorMixin):
    """Common motor control API for DC/BLDC/stepper motors.

    Commands are dicts like ``{"velocity_rpm": 100}`` sent to the bound
    microcontroller channel (see ``ActuatorMixin``), where a motor routine
    executes them. Typical hardware protocols the routines target:

    - Brushed DC: H-bridge driver (L298N, TB6612, DRV8871) — one PWM pin
      for magnitude, one direction pin (velocity control; add an
      ``EncoderMixin`` for closed-loop position).
    - Stepper: STEP/DIR driver (A4988, DRV8825, TMC2209) — position moves
      as step counts.
    - BLDC: an ESC via 1-2 ms servo PWM, or a VESC over UART/CAN
      (``codetocad_integrations.vesc``, which drives pyvesc).
    - Current control/measurement: driver current-sense output into an ADC
      (see ``CurrentSensorMixin``)."""

    def set_velocity(self, rpm: float):
        self._target_velocity_rpm = float(rpm)
        return self.write({"velocity_rpm": float(rpm)})

    def get_velocity(self) -> float:
        return getattr(self, "_target_velocity_rpm", 0.0)

    def set_position(self, degrees: float):
        self._target_position_degrees = float(degrees)
        return self.write({"position_degrees": float(degrees)})

    def get_position(self) -> float:
        return getattr(self, "_target_position_degrees", 0.0)

    def set_current(self, amps: float):
        self._target_current_amps = float(amps)
        return self.write({"current_amps": float(amps)})

    def get_current(self) -> float:
        return getattr(self, "_target_current_amps", 0.0)

    def set_duty(self, duty: float):
        """Open-loop duty cycle in [-1, 1] (sign is direction)."""
        return self.write({"duty": float(duty)})

    def stop(self):
        self._target_velocity_rpm = 0.0
        return self.write({"stop": True})


class DCMotorMixin(MotorMixin):
    """Brushed DC motor actuator mixin."""

    nominal_voltage: float | None = None
    stall_torque_nm: float | None = None
    no_load_speed_rpm: float | None = None

    def set_speed(self, rpm: float):
        """Alias of ``set_velocity`` kept for symmetry with datasheets."""
        return self.set_velocity(rpm)

    def get_speed(self) -> float:
        return self.get_velocity()


class BLDCMotorMixin(DCMotorMixin):
    """Brushless DC motor actuator mixin. Drive through an ESC or a VESC
    (``codetocad_integrations.vesc``)."""

    kv_rating: float | None = None
    pole_pairs: int | None = None


class StepperMotorMixin(MotorMixin):
    """Stepper motor actuator mixin (STEP/DIR drivers)."""

    steps_per_revolution: int = 200
    microsteps: int = 16

    def move_steps(self, steps: int):
        return self.write({"steps": int(steps)})

    def set_position(self, degrees: float):
        self._target_position_degrees = float(degrees)
        steps = degrees / 360.0 * self.steps_per_revolution * self.microsteps
        return self.write({"position_steps": int(round(steps))})
