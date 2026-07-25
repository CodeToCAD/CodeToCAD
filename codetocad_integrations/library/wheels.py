"""Wheels, tires, casters, omni / mecanum wheels and tracks -- what a
mobile robot rolls on. Each returns a ``Part3D`` at the real diameter /
width with a ``bore_mm`` (or hub interface) and a ``circumference_mm``
helper for odometry.
"""

from __future__ import annotations

import math

from ._base import (
    MM,
    BODY_BLACK,
    BODY_TIRE,
    BODY_YELLOW,
    PassivePart,
    register,
)

RUBBER_DENSITY = 1200.0


class Wheel(PassivePart):
    category = "wheel"

    def _setup(self, diameter_mm, width_mm, bore_mm, hub):
        self.diameter_mm = diameter_mm
        self.width_mm = width_mm
        self.bore_mm = bore_mm
        self.hub = hub
        self.circumference_mm = math.pi * diameter_mm

    def distance_per_rev_mm(self) -> float:
        """Ground distance covered in one wheel revolution (odometry)."""
        return self.circumference_mm


def wheel(
    diameter_mm: float, width_mm: float, *, bore_mm: float = 6.0,
    hub: str = "D-shaft", kind: str = "wheel", color=BODY_TIRE,
    name: str | None = None,
) -> Wheel:
    """A generic wheel/tire of the given diameter and width."""
    w = Wheel(name or f"wheel_{int(diameter_mm)}x{int(width_mm)}")
    mass = math.pi * (diameter_mm * MM / 2) ** 2 * (width_mm * MM) * RUBBER_DENSITY * 0.6
    w.build_cylinder(diameter_mm, width_mm, mass_kg=mass, color=color,
                     notes=f"{kind}, {diameter_mm:g} mm dia x {width_mm:g} mm")
    w._setup(diameter_mm, width_mm, bore_mm, hub)
    w.category = kind if kind in ("omni_wheel", "mecanum_wheel", "caster") else "wheel"
    return w


# slug, (dia, width), bore, hub, kind, color, mfr, pn, notes
_WHEELS = [
    ("tt_wheel_65mm", (65, 26), 5.4, "TT dual-flat", "wheel", BODY_TIRE,
     "Generic", "65mm TT", "yellow-motor rubber wheel"),
    ("robot_wheel_60mm", (60, 8), 4, "D-shaft", "wheel", BODY_TIRE,
     "Generic", "60mm", "small robot wheel for N20/D-shaft"),
    ("rc_tire_100mm", (100, 40, ), 12, "hex 12mm", "wheel", BODY_TIRE,
     "Generic", "100mm hex", "RC crawler rubber tire"),
    ("scooter_wheel_200mm", (200, 45), 8, "hub bearing", "wheel", BODY_TIRE,
     "Generic", "200mm PU", "scooter / rover polyurethane wheel"),
    ("pololu_wheel_90mm", (90, 10), 3, "3mm D", "wheel", BODY_TIRE,
     "Pololu", "90x10mm", "Pololu wheel for micro metal gearmotors"),
    ("omni_wheel_58mm", (58, 25), 6, "hub", "omni_wheel", BODY_YELLOW,
     "Generic", "58mm omni", "single-row omni wheel (holonomic drive)"),
    ("omni_wheel_38mm", (38, 20), 4, "hub", "omni_wheel", BODY_YELLOW,
     "Generic", "38mm omni", "small omni wheel"),
    ("mecanum_wheel_80mm", (80, 40), 6, "hub 4-hole", "mecanum_wheel", BODY_BLACK,
     "Generic", "80mm mecanum", "mecanum wheel (strafing drive) -- handed"),
    ("mecanum_wheel_100mm", (100, 50), 12, "hub", "mecanum_wheel", BODY_BLACK,
     "Generic", "100mm mecanum", "large mecanum wheel"),
    ("caster_ball_25mm", (25, 25), 0, "M3 mount plate", "caster", BODY_BLACK,
     "Generic", "25mm ball", "ball-transfer caster (undriven support)"),
    ("caster_wheel_swivel_50mm", (50, 20), 0, "top plate", "caster", BODY_BLACK,
     "Generic", "50mm swivel", "swivel caster wheel"),
    ("track_link_set", (80, 30), 0, "sprocket", "track", BODY_BLACK,
     "Generic", "tank track", "rubber tank-track loop segment"),
]


def _make(row):
    slug, dims, bore, hub, kind, color, mfr, pn, notes = row
    dia, width = dims[0], dims[1]

    def factory():
        w = wheel(dia, width, bore_mm=bore, hub=hub, kind=kind, color=color,
                  name=slug)
        w.manufacturer = mfr
        w.part_number = pn
        w.notes = notes
        return w

    factory.__doc__ = (
        f"{notes}. {dia:g} mm dia x {width:g} mm, {bore:g} mm bore "
        f"({hub}). {mfr} {pn}."
    )
    return register(slug, kind if kind != "wheel" else "wheel", factory,
                    manufacturer=mfr, part_number=pn, summary=notes)


for _row in _WHEELS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = ["Wheel", "wheel"] + [f"get_{r[0]}" for r in _WHEELS]
