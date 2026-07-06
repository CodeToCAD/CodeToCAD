"""Assembly base classes. Assembly2D and Assembly3D are the base of Part2D
and Part3D respectively."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .ledgers import AssemblyLedger
from .location import Location
from .vectors import Vec3

if TYPE_CHECKING:
    from .parts import Part2D, Part3D


class AssemblyCommon:
    def __init__(self, name: str | None = None, description: str | None = None):
        self.name = name
        self.description = description
        self.ledger = AssemblyLedger()
        self._origin = Vec3()
        self._start_origin = Vec3()

    def build(self):
        """This method must be implemented to create the shape in your target
        modeling application."""
        raise NotImplementedError(
            "Override build() to create this shape in your target modeling "
            "application"
        )

    def export(self, location: str):
        """This method must be implemented to export the shape from your
        target modeling application."""
        raise NotImplementedError(
            "Override export() to export this shape from your target modeling "
            "application"
        )

    def get_bounding_box(self) -> tuple[Vec3, Vec3]:
        """Axis-aligned bounding box as ``(min, max)`` corners in meters."""
        raise NotImplementedError(
            "Override get_bounding_box() for this assembly or part"
        )

    def transform(
        self, *, absolute: Location | None = None, relative: Location | None = None
    ):
        """Translate and/or rotate by the given location. Exactly one of
        ``absolute`` or ``relative`` must be supplied."""
        if (absolute is None) == (relative is None):
            raise ValueError("Supply exactly one of absolute= or relative=")
        transformation = absolute if absolute is not None else relative
        self.ledger.transformations += [transformation]
        if hasattr(self, "operations"):
            self.operations.append(
                {
                    "operation": "transform",
                    "mode": "absolute" if absolute is not None else "relative",
                    "location": transformation,
                }
            )
        offset = Vec3(
            transformation.x.value, transformation.y.value, transformation.z.value
        )
        self._origin = offset if absolute is not None else self._origin + offset
        return self

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"


class _ConstraintRecorder:
    def _record_constraint(
        self, operation, location, other_part, other_location, **extra
    ):
        if hasattr(self, "operations"):
            self.operations.append(
                {
                    "operation": operation,
                    "location": location,
                    "other_part": other_part,
                    "other_location": other_location,
                    **extra,
                }
            )


class Assembly2D(AssemblyCommon, _ConstraintRecorder):
    def coincide(
        self, location: Location, other_part: "Part2D", other_location: Location
    ) -> "Part2D":
        self.ledger.coincide_constraints += [other_part]
        self._record_constraint("coincide", location, other_part, other_location)
        return self

    def parallel(
        self, location: Location, other_part: "Part2D", other_location: Location
    ) -> "Part2D":
        self.ledger.parallel_constraints += [other_part]
        self._record_constraint("parallel", location, other_part, other_location)
        return self

    def perpendicular(
        self, location: Location, other_part: "Part2D", other_location: Location
    ) -> "Part2D":
        self.ledger.perpendicular_constraints += [other_part]
        self._record_constraint(
            "perpendicular", location, other_part, other_location
        )
        return self

    def tangent(
        self, location: Location, other_part: "Part2D", other_location: Location
    ) -> "Part2D":
        self.ledger.tangent_constraints += [other_part]
        self._record_constraint("tangent", location, other_part, other_location)
        return self


class Assembly3D(AssemblyCommon, _ConstraintRecorder):
    def fixed(
        self, location: Location, other_part: "Part3D", other_location: Location
    ) -> "Part3D":
        self.ledger.fixed_constraints += [other_part]
        self._record_constraint("fixed", location, other_part, other_location)
        return self

    def revolute(
        self,
        location: Location,
        other_part: "Part3D",
        other_location: Location,
        min_limits: float | Vec3 | None = None,
        max_limits: float | Vec3 | None = None,
    ) -> "Part3D":
        """Revolute (hinge) joint at ``location``; the joint axis is the
        location's quaternion-rotated Z axis. Limits are in radians."""
        self.ledger.revolute_constraints += [other_part]
        self._record_constraint(
            "revolute",
            location,
            other_part,
            other_location,
            min_limits=min_limits,
            max_limits=max_limits,
        )
        return self

    def prismatic(
        self,
        location: Location,
        other_part: "Part3D",
        other_location: Location,
        min_limits: float | Vec3 | None = None,
        max_limits: float | Vec3 | None = None,
    ) -> "Part3D":
        """Prismatic (sliding) joint at ``location`` along the location's
        quaternion-rotated Z axis. Limits are in meters."""
        self.ledger.prismatic_constraints += [other_part]
        self._record_constraint(
            "prismatic",
            location,
            other_part,
            other_location,
            min_limits=min_limits,
            max_limits=max_limits,
        )
        return self
