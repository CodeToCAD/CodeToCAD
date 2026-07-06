"""Common fasteners that can build() their Part3D or apply their features in
the federated application."""

from __future__ import annotations

from enum import Enum

from codetocad.location import Location
from codetocad.parts import Part3D
from codetocad.units import LengthMeters, LengthWithUnit


class CommonFasteners(Enum):
    """Value is ``(kind, thread diameter in meters, default length/thickness
    in meters)``."""

    M2_BOLT = ("bolt", 0.002, 0.008)
    M3_BOLT = ("bolt", 0.003, 0.012)
    M4_BOLT = ("bolt", 0.004, 0.016)
    M5_BOLT = ("bolt", 0.005, 0.020)
    M6_BOLT = ("bolt", 0.006, 0.025)
    M8_BOLT = ("bolt", 0.008, 0.030)
    M3_NUT = ("nut", 0.003, 0.0024)
    M5_NUT = ("nut", 0.005, 0.0047)
    M3_WASHER = ("washer", 0.003, 0.0005)
    M5_WASHER = ("washer", 0.005, 0.001)
    NO4_WOOD_SCREW = ("wood_screw", 0.0028, 0.016)
    NO8_WOOD_SCREW = ("wood_screw", 0.0042, 0.025)

    @property
    def kind(self) -> str:
        return self.value[0]

    @property
    def diameter(self) -> LengthMeters:
        return LengthMeters(self.value[1])

    @property
    def length(self) -> LengthMeters:
        return LengthMeters(self.value[2])

    def build(self, length: LengthWithUnit | None = None) -> Part3D:
        """Build a simplified Part3D of this fastener (a cylinder proxy; a
        federated backend can substitute an exact model)."""
        from codetocad.primitives import cylinder

        body_length = (
            LengthMeters(length) if length is not None else self.length
        )
        if self.kind in ("nut", "washer"):
            radius = self.diameter.value  # outer radius approximation
        else:
            radius = self.diameter.value / 2
        part = cylinder(radius=radius, height=body_length)
        part.name = self.name.lower()
        return part

    def apply_to(self, part: Part3D, location: Location) -> Part3D:
        """Apply this fastener's feature (a clearance hole, ~10% over the
        thread radius) to ``part`` at ``location``."""
        return part.hole(location, radius=self.diameter * 0.55, amount=self.length)
