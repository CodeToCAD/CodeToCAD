"""Joint objects returned by assembly constraint methods.

``Assembly3D.fixed()``, ``.revolute()`` and ``.prismatic()`` each return a
``Joint`` recording the parts and locations they connect. Once the assembly is
handed to a ``simulate()`` backend, the backend *binds* each joint to the live
simulation, so the same object you got at build time can drive the joint:

    hinge = base.revolute(pivot, arm, pivot)
    sim = simulate(base)
    hinge.move_to("90deg")     # position-control the actuator
    hinge.set_velocity("30rpm")

Before the joint is bound (no simulation yet) the control methods raise; the
metadata attributes are always available.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from codetocad.units import (
    AngleRadians,
    AngleWithUnit,
    AngularSpeedRadiansPerSecond,
    AngularSpeedWithUnit,
    LengthMeters,
    LengthWithUnit,
    LinearSpeedMetersPerSecond,
    LinearSpeedWithUnit,
)

if TYPE_CHECKING:
    from codetocad.location import Location
    from codetocad.parts import Part3D
    from codetocad.simulation import Simulation


class Joint:
    """A kinematic connection between two parts, recorded at assembly time.

    Subclasses (:class:`FixedJoint`, :class:`RevoluteJoint`,
    :class:`PrismaticJoint`) add the motion-control API a live simulation can
    honour. The ``parent_part``/``child_part`` and ``location``/
    ``other_location`` attributes describe what the joint connects."""

    joint_type = "fixed"

    def __init__(
        self,
        parent_part: "Part3D",
        child_part: "Part3D",
        location: "Location",
        other_location: "Location",
        *,
        name: str | None = None,
        min_limits=None,
        max_limits=None,
    ):
        self.parent_part = parent_part
        self.child_part = child_part
        self.location = location
        self.other_location = other_location
        self.name = name
        self.min_limits = min_limits
        self.max_limits = max_limits
        #: Set by a simulation backend once the assembly is simulated.
        self._simulation: "Simulation | None" = None
        self._joint_name: str | None = None

    def _bind(self, simulation: "Simulation", joint_name: str) -> None:
        """Attach this joint to a running simulation. Called by the backend."""
        self._simulation = simulation
        self._joint_name = joint_name

    @property
    def is_bound(self) -> bool:
        return self._simulation is not None

    def _sim(self) -> "Simulation":
        if self._simulation is None or self._joint_name is None:
            raise RuntimeError(
                f"Joint {self.name or self.joint_type!r} is not bound to a "
                "running simulation; pass its assembly to simulate() first, "
                "then control the joint."
            )
        return self._simulation

    def __repr__(self) -> str:
        parent = getattr(self.parent_part, "name", self.parent_part)
        child = getattr(self.child_part, "name", self.child_part)
        return (
            f"{type(self).__name__}(name={self.name!r}, parent={parent!r}, "
            f"child={child!r})"
        )


class FixedJoint(Joint):
    """A rigid weld between two parts. Carries no motion."""

    joint_type = "fixed"


class RevoluteJoint(Joint):
    """A hinge joint rotating about a single axis."""

    joint_type = "revolute"

    def move_to(
        self, angle: AngleWithUnit, *, force: float | None = None
    ) -> "RevoluteJoint":
        """Position-control the joint towards ``angle`` (e.g. ``"90deg"``).
        ``force`` caps the actuator torque where the backend supports it
        (PyBullet); it is ignored otherwise."""
        self._command(AngleRadians(angle).value, force)
        return self

    def move_by(
        self, angle: AngleWithUnit, *, force: float | None = None
    ) -> "RevoluteJoint":
        """Position-control the joint to its current angle plus ``angle``."""
        sim = self._sim()
        target = sim.get_joint_value(self._joint_name) + AngleRadians(angle).value
        self._command(target, force)
        return self

    def _command(self, value: float, force: float | None) -> None:
        kwargs = {} if force is None else {"force": force}
        self._sim()._command_joint_target(self._joint_name, value, **kwargs)

    def set_velocity(self, w: AngularSpeedWithUnit) -> "RevoluteJoint":
        """Velocity-control the joint at ``w`` (e.g. ``"30rpm"``, ``"1rad/s"``)."""
        self._sim().set_joint_velocity(
            self._joint_name, AngularSpeedRadiansPerSecond(w).value
        )
        return self

    def get_angle(self) -> AngleRadians:
        """The joint's current angle."""
        return AngleRadians(self._sim().get_joint_value(self._joint_name))


class PrismaticJoint(Joint):
    """A sliding joint translating along a single axis."""

    joint_type = "prismatic"

    def move_to(
        self, position: LengthWithUnit, *, force: float | None = None
    ) -> "PrismaticJoint":
        """Position-control the joint towards ``position`` (e.g. ``"5cm"``).
        ``force`` caps the actuator thrust where the backend supports it
        (PyBullet); it is ignored otherwise."""
        self._command(LengthMeters(position).value, force)
        return self

    def move_by(
        self, distance: LengthWithUnit, *, force: float | None = None
    ) -> "PrismaticJoint":
        """Position-control the joint to its current position plus ``distance``."""
        sim = self._sim()
        target = sim.get_joint_value(self._joint_name) + LengthMeters(distance).value
        self._command(target, force)
        return self

    def _command(self, value: float, force: float | None) -> None:
        kwargs = {} if force is None else {"force": force}
        self._sim()._command_joint_target(self._joint_name, value, **kwargs)

    def set_velocity(self, v: LinearSpeedWithUnit) -> "PrismaticJoint":
        """Velocity-control the joint at ``v`` (e.g. ``"10mm/s"``)."""
        self._sim().set_joint_velocity(
            self._joint_name, LinearSpeedMetersPerSecond(v).value
        )
        return self

    def get_position(self) -> LengthMeters:
        """The joint's current position."""
        return LengthMeters(self._sim().get_joint_value(self._joint_name))


#: Maps a constraint operation name to the Joint subclass it produces.
JOINT_CLASSES = {
    "fixed": FixedJoint,
    "revolute": RevoluteJoint,
    "prismatic": PrismaticJoint,
}
