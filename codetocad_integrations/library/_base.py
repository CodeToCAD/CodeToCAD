"""Shared building blocks for the actuator / sensor library.

Every catalog part is a plain :class:`codetocad.Part3D` (so it exports,
draws, gets a bounding box and joins into assemblies like any other part),
carrying:

- **Real geometry** built from primitives at datasheet millimetre
  dimensions (a square NEMA can, a round gimbal can, a servo case, ...).
- **A moving element** where the real device has one: rotary actuators get
  an output *shaft* attached with a :class:`RevoluteJoint`, linear
  actuators get a *rod* on a :class:`PrismaticJoint`. That joint is what a
  simulation drives, so the shaft actually turns / the rod actually slides.
- **The motor-control mixin** for its type (``StepperMotorMixin``,
  ``BLDCMotorMixin``, ``DCMotorMixin`` or the servo mixin below), so the
  part *is* its own actuator: ``motor.set_velocity(...)`` /
  ``motor.move_steps(...)`` / ``servo.set_angle(...)`` bind straight to a
  ``Microcontroller`` pin.
- **Power requirements** — nominal voltage, current, torque, speed — in a
  :class:`PowerSpec` on ``part.power`` and echoed onto the mixin's own
  datasheet attributes (``nominal_voltage``, ``holding_torque_nm``, ...).

Specs are nominal values taken from manufacturer datasheets and are meant
for planning / simulation, not for certification.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Callable

from codetocad import Location, MaterialBase, Part3D, Vec4, cube, cylinder
from codetocad.mixins import (
    ActuatorMixin,
    BLDCMotorMixin,
    DCMotorMixin,
    StepperMotorMixin,
)

MM = 0.001  # datasheet millimetres -> metres

# A few reusable finishes so parts read at a glance in a viewer.
BODY_BLACK = Vec4(0.10, 0.10, 0.12, 1.0)
BODY_STEEL = Vec4(0.62, 0.64, 0.66, 1.0)
BODY_BLUE = Vec4(0.15, 0.28, 0.55, 1.0)
BODY_RED = Vec4(0.55, 0.12, 0.12, 1.0)
SHAFT_STEEL = Vec4(0.75, 0.76, 0.78, 1.0)
PCB_GREEN = Vec4(0.10, 0.35, 0.18, 1.0)
LENS_DARK = Vec4(0.05, 0.05, 0.08, 1.0)
BODY_ALU = Vec4(0.80, 0.82, 0.85, 1.0)
BODY_BRASS = Vec4(0.72, 0.56, 0.22, 1.0)
BODY_COPPER = Vec4(0.72, 0.45, 0.20, 1.0)
BODY_WHITE = Vec4(0.92, 0.92, 0.94, 1.0)
BODY_YELLOW = Vec4(0.85, 0.72, 0.10, 1.0)
BODY_TIRE = Vec4(0.12, 0.12, 0.13, 1.0)


@dataclass(frozen=True)
class PowerSpec:
    """Electrical + mechanical operating point of an actuator.

    Fields are optional so each device fills in what its datasheet quotes.
    Torques are in newton-metres, currents in amps, voltages in volts,
    speeds in rpm.
    """

    nominal_voltage_v: float | None = None
    current_a: float | None = None  # rated / continuous per phase or winding
    peak_current_a: float | None = None
    power_w: float | None = None
    holding_torque_nm: float | None = None  # steppers
    stall_torque_nm: float | None = None  # brushed DC / servo
    rated_torque_nm: float | None = None  # continuous working torque
    no_load_speed_rpm: float | None = None
    kv_rpm_per_v: float | None = None  # BLDC

    def as_dict(self) -> dict[str, float]:
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name) is not None
        }


@dataclass
class CatalogEntry:
    """A registered catalog item: its ``get_*`` factory plus metadata used
    for search / listing without instantiating anything."""

    slug: str
    getter: str  # the public factory name, e.g. "get_nema_23"
    category: str
    factory: Callable[[], "LibraryPart3D"]
    manufacturer: str | None = None
    part_number: str | None = None
    summary: str = ""


#: Every registered catalog item, keyed by slug (e.g. ``"nema_23"``).
CATALOG: dict[str, CatalogEntry] = {}


def register(
    slug: str,
    category: str,
    factory: Callable[[], "LibraryPart3D"],
    *,
    manufacturer: str | None = None,
    part_number: str | None = None,
    summary: str = "",
) -> Callable[[], "LibraryPart3D"]:
    """Register ``factory`` under ``slug`` and return it renamed to
    ``get_<slug>`` so modules can expose it directly."""
    getter = f"get_{slug}"
    factory.__name__ = getter
    factory.__qualname__ = getter
    if slug in CATALOG:
        raise ValueError(f"Duplicate catalog slug {slug!r}")
    CATALOG[slug] = CatalogEntry(
        slug=slug,
        getter=getter,
        category=category,
        factory=factory,
        manufacturer=manufacturer,
        part_number=part_number,
        summary=summary,
    )
    return factory


class LibraryPart3D(Part3D):
    """Base for every catalog part: a ``Part3D`` that also remembers what it
    is (category, manufacturer, part number) and what it needs to run
    (``power``). Subclasses add the moving element and control mixin."""

    category: str = "component"

    def _init_library(
        self,
        *,
        mass_kg: float,
        color: Vec4,
        manufacturer: str | None = None,
        part_number: str | None = None,
        power: PowerSpec | None = None,
        datasheet_url: str | None = None,
        notes: str | None = None,
    ) -> None:
        self.manufacturer = manufacturer
        self.part_number = part_number
        self.power = power or PowerSpec()
        self.datasheet_url = datasheet_url
        self.notes = notes
        self.set_material(
            MaterialBase(self.name or "component", mass=mass_kg, color_rgba=color)
        )
        self._apply_power_to_mixin()

    def _apply_power_to_mixin(self) -> None:
        """Mirror the ``PowerSpec`` onto whatever motor-mixin datasheet
        attributes this subclass inherits, so the standard control API sees
        real numbers."""
        p = self.power
        if isinstance(self, StepperMotorMixin):
            if p.holding_torque_nm is not None:
                self.holding_torque_nm = p.holding_torque_nm
        if isinstance(self, DCMotorMixin):
            if p.nominal_voltage_v is not None:
                self.nominal_voltage = p.nominal_voltage_v
            if p.no_load_speed_rpm is not None:
                self.no_load_speed_rpm = p.no_load_speed_rpm
            if p.stall_torque_nm is not None:
                self.stall_torque_nm = p.stall_torque_nm
        if isinstance(self, BLDCMotorMixin):
            if p.kv_rpm_per_v is not None:
                self.kv_rating = p.kv_rpm_per_v

    def get_power_requirements(self) -> dict[str, float]:
        """The device's operating point (voltage/current/torque/speed) as a
        plain dict — only the fields its datasheet specifies."""
        return self.power.as_dict()

    def describe(self) -> str:
        """A one-block human summary: identity, size and power."""
        bbox_min, bbox_max = self.get_bounding_box()
        size = tuple(
            round((hi - lo) * 1000, 1)
            for lo, hi in zip(bbox_min.to_tuple(), bbox_max.to_tuple())
        )
        who = " ".join(
            part for part in (self.manufacturer, self.part_number) if part
        )
        lines = [
            f"{self.name}  [{self.category}]" + (f"  ({who})" if who else ""),
            f"  envelope: {size[0]} x {size[1]} x {size[2]} mm",
        ]
        power = self.get_power_requirements()
        if power:
            lines.append(
                "  power: "
                + ", ".join(f"{key}={value}" for key, value in power.items())
            )
        if self.notes:
            lines.append(f"  note: {self.notes}")
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Geometry helpers shared by the actuator subclasses.
# --------------------------------------------------------------------------


def _set_body(part: LibraryPart3D, primitive: Part3D) -> None:
    """Adopt ``primitive`` (a preset cube/cylinder) as ``part``'s own solid."""
    part._primitive = primitive._primitive
    part._origin = primitive._origin
    part._start_origin = primitive._start_origin


def attach_shaft(
    motor: LibraryPart3D,
    *,
    diameter_mm: float,
    length_mm: float,
    base_z: float,
    limits: tuple[float, float] | None = None,
    starting_angle: str | float | None = None,
    color: Vec4 = SHAFT_STEEL,
    shaft_mass_kg: float = 0.002,
):
    """Attach an output shaft above the body top (``base_z``, in metres) and
    hinge it with a revolute joint about the motor axis (+Z). Returns the
    :class:`RevoluteJoint`, and stashes it on ``motor.shaft`` /
    ``motor.shaft_joint``. This is the DOF a simulation spins."""
    length = length_mm * MM
    shaft = cylinder(
        radius=diameter_mm * MM / 2,
        height=length,
        start_location=Location(z=base_z + length / 2),
    )
    shaft.name = f"{motor.name}_shaft"
    shaft.set_material(MaterialBase("shaft", mass=shaft_mass_kg, color_rgba=color))
    axis = Location(z=base_z, name=f"{motor.name}_axis")
    joint = motor.revolute(
        axis,
        shaft,
        axis,
        min_limits=None if limits is None else limits[0],
        max_limits=None if limits is None else limits[1],
        starting_angle=starting_angle,
    )
    motor.shaft = shaft
    motor.shaft_joint = joint
    return joint


def attach_rod(
    actuator: LibraryPart3D,
    *,
    diameter_mm: float,
    stroke_mm: float,
    retracted_len_mm: float,
    base_z: float,
    color: Vec4 = SHAFT_STEEL,
    rod_mass_kg: float = 0.02,
):
    """Attach a push rod above the body and let it slide along +Z between 0
    and ``stroke``. Returns the :class:`PrismaticJoint` (also on
    ``actuator.rod`` / ``actuator.rod_joint``)."""
    length = retracted_len_mm * MM
    rod = cylinder(
        radius=diameter_mm * MM / 2,
        height=length,
        start_location=Location(z=base_z + length / 2),
    )
    rod.name = f"{actuator.name}_rod"
    rod.set_material(MaterialBase("rod", mass=rod_mass_kg, color_rgba=color))
    axis = Location(z=base_z, name=f"{actuator.name}_stroke")
    joint = actuator.prismatic(
        axis, rod, axis, min_limits=0.0, max_limits=stroke_mm * MM
    )
    actuator.rod = rod
    actuator.rod_joint = joint
    return joint


# --------------------------------------------------------------------------
# Servo control mixin (position device; not a free-running motor).
# --------------------------------------------------------------------------


class ServoMixin(ActuatorMixin):
    """Hobby / smart servo actuator: commanded to an *angle*, not a speed.

    ``rotation_range_deg`` is the mechanical travel (e.g. 180 for a standard
    servo, 360 for a smart servo, ``None`` for a continuous-rotation servo
    that instead takes a speed in ``[-1, 1]``)."""

    rotation_range_deg: float | None = 180.0
    continuous: bool = False

    def set_angle(self, degrees: float):
        """Command the output to ``degrees`` (clamped to the travel)."""
        if self.continuous:
            raise ValueError(
                f"{getattr(self, 'name', 'servo')} is continuous-rotation; "
                "use set_speed()"
            )
        span = self.rotation_range_deg
        if span is not None:
            degrees = max(0.0, min(float(span), float(degrees)))
        self._target_angle_deg = float(degrees)
        joint = getattr(self, "shaft_joint", None)
        if joint is not None:
            self._pose_shaft(float(degrees))
        return self.write({"angle_degrees": float(degrees)})

    def get_angle(self) -> float:
        return getattr(self, "_target_angle_deg", 0.0)

    def set_speed(self, fraction: float):
        """Continuous-rotation servos only: -1..1 (sign is direction)."""
        fraction = max(-1.0, min(1.0, float(fraction)))
        self._target_speed = fraction
        return self.write({"speed": fraction})

    def _pose_shaft(self, degrees: float) -> None:
        """Best-effort: remember the commanded pose on the joint so previews
        can reflect it. Simulation drives the joint directly."""
        joint = getattr(self, "shaft_joint", None)
        if joint is not None:
            joint._commanded_degrees = degrees


# --------------------------------------------------------------------------
# Concrete actuator part types. Each is a Part3D + the matching control mixin.
# --------------------------------------------------------------------------


class StepperMotor(LibraryPart3D, StepperMotorMixin):
    """A stepper: square NEMA can with a round output shaft on the top face.

    The frame size names the standard (NEMA 17 == 42 mm frame). Drive it
    open-loop with ``move_steps()`` / ``set_position(degrees)`` through an
    A4988 / DRV8825 / TMC2209-style STEP/DIR driver."""

    category = "stepper"

    def __init__(
        self,
        name: str,
        *,
        frame_mm: float,
        body_length_mm: float,
        shaft_diameter_mm: float,
        shaft_length_mm: float,
        mass_kg: float,
        power: PowerSpec,
        steps_per_revolution: int = 200,
        microsteps: int = 16,
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ):
        super().__init__(name)
        self.steps_per_revolution = steps_per_revolution
        self.microsteps = microsteps
        self.frame_mm = frame_mm
        self.step_angle_deg = 360.0 / steps_per_revolution
        _set_body(self, cube(frame_mm * MM, frame_mm * MM, body_length_mm * MM))
        self._init_library(
            mass_kg=mass_kg,
            color=BODY_STEEL,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )
        attach_shaft(
            self,
            diameter_mm=shaft_diameter_mm,
            length_mm=shaft_length_mm,
            base_z=body_length_mm * MM / 2,
        )


class ServoMotor(LibraryPart3D, ServoMixin):
    """A servo: rectangular case with an output spline on top. ``pwm`` servos
    take 1-2 ms RC pulses; ``serial`` smart servos (Dynamixel / FeeTech)
    take a bus packet — either way ``set_angle()`` is the command."""

    category = "servo"

    def __init__(
        self,
        name: str,
        *,
        case_l_mm: float,
        case_w_mm: float,
        case_h_mm: float,
        shaft_diameter_mm: float,
        shaft_length_mm: float,
        mass_kg: float,
        power: PowerSpec,
        rotation_range_deg: float | None = 180.0,
        continuous: bool = False,
        protocol: str = "pwm",
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ):
        super().__init__(name)
        self.rotation_range_deg = None if continuous else rotation_range_deg
        self.continuous = continuous
        self.protocol = protocol
        _set_body(self, cube(case_l_mm * MM, case_w_mm * MM, case_h_mm * MM))
        self._init_library(
            mass_kg=mass_kg,
            color=BODY_BLACK,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )
        limits = (
            None
            if (continuous or rotation_range_deg is None)
            else (0.0, rotation_range_deg * 3.141592653589793 / 180.0)
        )
        # The output spline sits near one end of the case, not centered.
        attach_shaft(
            self,
            diameter_mm=shaft_diameter_mm,
            length_mm=shaft_length_mm,
            base_z=case_h_mm * MM / 2,
            limits=limits,
            starting_angle=None
            if limits is None
            else f"{rotation_range_deg / 2}deg",
        )


class BLDCMotor(LibraryPart3D, BLDCMotorMixin):
    """A brushless outrunner / gimbal / hub motor: a round can with a shaft.

    Speed follows ``kv`` (rpm per volt, no load). Drive it with an ESC
    (servo-PWM or DShot) or a VESC (``codetocad_integrations.vesc``)."""

    category = "bldc"

    def __init__(
        self,
        name: str,
        *,
        diameter_mm: float,
        body_length_mm: float,
        shaft_diameter_mm: float,
        shaft_length_mm: float,
        mass_kg: float,
        power: PowerSpec,
        pole_pairs: int = 7,
        outrunner: bool = True,
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ):
        super().__init__(name)
        self.pole_pairs = pole_pairs
        self.outrunner = outrunner
        _set_body(
            self, cylinder(radius=diameter_mm * MM / 2, height=body_length_mm * MM)
        )
        self._init_library(
            mass_kg=mass_kg,
            color=BODY_RED if outrunner else BODY_STEEL,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )
        attach_shaft(
            self,
            diameter_mm=shaft_diameter_mm,
            length_mm=shaft_length_mm,
            base_z=body_length_mm * MM / 2,
        )


class DCGearmotor(LibraryPart3D, DCMotorMixin):
    """A brushed DC motor, usually with a gearbox. ``gear_ratio`` reduces
    the raw motor speed to the quoted output ``no_load_speed_rpm``. Drive
    it from an H-bridge (L298N / TB6612 / DRV8871)."""

    category = "dc_gearmotor"

    def __init__(
        self,
        name: str,
        *,
        diameter_mm: float,
        body_length_mm: float,
        shaft_diameter_mm: float,
        shaft_length_mm: float,
        mass_kg: float,
        power: PowerSpec,
        gear_ratio: float = 1.0,
        has_encoder: bool = False,
        gearbox_shape: str = "round",
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ):
        super().__init__(name)
        self.gear_ratio = gear_ratio
        self.has_encoder = has_encoder
        if gearbox_shape == "round":
            _set_body(
                self,
                cylinder(radius=diameter_mm * MM / 2, height=body_length_mm * MM),
            )
        else:  # boxy gearbox (TT motor, 25GA, 37D metal gearbox front)
            _set_body(
                self,
                cube(diameter_mm * MM, diameter_mm * MM, body_length_mm * MM),
            )
        self._init_library(
            mass_kg=mass_kg,
            color=BODY_STEEL,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )
        attach_shaft(
            self,
            diameter_mm=shaft_diameter_mm,
            length_mm=shaft_length_mm,
            base_z=body_length_mm * MM / 2,
        )


class LinearActuator(LibraryPart3D, DCMotorMixin):
    """A powered linear actuator: a body with a rod that extends / retracts
    along its axis. ``extend()`` / ``retract()`` / ``set_stroke(mm)`` drive
    the prismatic rod (``self.rod_joint``)."""

    category = "linear_actuator"

    def __init__(
        self,
        name: str,
        *,
        body_diameter_mm: float,
        body_length_mm: float,
        rod_diameter_mm: float,
        stroke_mm: float,
        mass_kg: float,
        power: PowerSpec,
        speed_mm_s: float | None = None,
        driven_by: str = "brushed DC",
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ):
        super().__init__(name)
        self.stroke_mm = stroke_mm
        self.speed_mm_s = speed_mm_s
        self.driven_by = driven_by
        _set_body(
            self,
            cylinder(radius=body_diameter_mm * MM / 2, height=body_length_mm * MM),
        )
        self._init_library(
            mass_kg=mass_kg,
            color=BODY_STEEL,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )
        attach_rod(
            self,
            diameter_mm=rod_diameter_mm,
            stroke_mm=stroke_mm,
            retracted_len_mm=max(stroke_mm * 0.5, 20.0),
            base_z=body_length_mm * MM / 2,
        )

    def set_stroke(self, millimetres: float):
        """Command the rod to ``millimetres`` of extension (0..stroke)."""
        target = max(0.0, min(self.stroke_mm, float(millimetres)))
        self._target_stroke_mm = target
        return self.write({"stroke_mm": target})

    def extend(self):
        return self.set_stroke(self.stroke_mm)

    def retract(self):
        return self.set_stroke(0.0)


class PassivePart(LibraryPart3D):
    """A non-powered mechanical / sensor body (lead screw, pulley, switch,
    camera housing, ...). Sensor subtypes add a sensor mixin on top."""

    category = "component"

    def _build_body(
        self,
        primitive: Part3D,
        *,
        mass_kg: float,
        color: Vec4,
        power: PowerSpec | None = None,
        manufacturer: str | None = None,
        part_number: str | None = None,
        notes: str | None = None,
    ) -> None:
        _set_body(self, primitive)
        self._init_library(
            mass_kg=mass_kg,
            color=color,
            manufacturer=manufacturer,
            part_number=part_number,
            power=power,
            notes=notes,
        )

    def build_box(
        self, length_mm, width_mm, height_mm, *, mass_kg, color=BODY_STEEL,
        **kwargs,
    ) -> "PassivePart":
        """Give this part a rectangular body (mm) and library metadata."""
        self._build_body(
            cube(length_mm * MM, width_mm * MM, height_mm * MM),
            mass_kg=mass_kg, color=color, **kwargs,
        )
        return self

    def build_cylinder(
        self, diameter_mm, height_mm, *, mass_kg, color=BODY_STEEL, **kwargs,
    ) -> "PassivePart":
        """Give this part a cylindrical body (mm) and library metadata."""
        self._build_body(
            cylinder(radius=diameter_mm * MM / 2, height=height_mm * MM),
            mass_kg=mass_kg, color=color, **kwargs,
        )
        return self


__all__ = [
    "MM",
    "PowerSpec",
    "StepperMotor",
    "ServoMotor",
    "BLDCMotor",
    "DCGearmotor",
    "LinearActuator",
    "PassivePart",
    "CatalogEntry",
    "CATALOG",
    "register",
    "LibraryPart3D",
    "ServoMixin",
    "attach_shaft",
    "attach_rod",
    "cube",
    "cylinder",
    "Location",
    "Vec4",
    "MaterialBase",
    "BODY_BLACK",
    "BODY_STEEL",
    "BODY_BLUE",
    "BODY_RED",
    "SHAFT_STEEL",
    "PCB_GREEN",
    "LENS_DARK",
    "BODY_ALU",
    "BODY_BRASS",
    "BODY_COPPER",
    "BODY_WHITE",
    "BODY_YELLOW",
    "BODY_TIRE",
]
