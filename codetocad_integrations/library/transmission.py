"""Passive motion-transmission parts: lead screws, ball screws, ACME
screws, capstan drums and timing pulleys. These convert a motor's rotation
into linear travel (or vice-versa); pair one with a stepper / gearmotor
from this library.

Each returns a :class:`codetocad.Part3D` with the real diameter/length and
a ``travel_per_rev_mm`` attribute, plus ``linear_travel(revolutions)`` to
convert turns into millimetres of motion::

    from codetocad_integrations.library import get_leadscrew_t8_2mm
    screw = get_leadscrew_t8_2mm()
    screw.linear_travel(10)      # -> 20.0 mm for 10 turns
"""

from __future__ import annotations

import math

from ._base import (
    MM,
    BODY_BLACK,
    BODY_STEEL,
    PassivePart,
    cube,
    cylinder,
    register,
)


class Transmission(PassivePart):
    """A passive drive element with a defined linear ``travel_per_rev_mm``.
    Rotary ones (screws, pulleys, capstans) are hinged on a revolute joint
    so a driving motor's shaft can be joined to them and turned."""

    category = "transmission"

    def _configure(
        self,
        *,
        travel_per_rev_mm: float,
        lead_mm: float | None = None,
        pitch_mm: float | None = None,
        starts: int = 1,
    ) -> None:
        self.travel_per_rev_mm = travel_per_rev_mm
        self.lead_mm = lead_mm
        self.pitch_mm = pitch_mm
        self.starts = starts

    def linear_travel(self, revolutions: float) -> float:
        """Millimetres of linear travel for ``revolutions`` turns."""
        return revolutions * self.travel_per_rev_mm

    def revolutions_for(self, millimetres: float) -> float:
        """Turns needed to move ``millimetres``."""
        return millimetres / self.travel_per_rev_mm


# slug, kind, outer_dia_mm, length_mm, lead_mm, pitch_mm, starts, mass_kg,
# mfr, pn, notes  -- travel/rev derived below
_SCREWS = [
    ("leadscrew_t8_2mm", "screw", 8, 300, 2, 2, 1, 0.11, "Generic", "T8 2mm-2mm",
     "T8 lead screw, single-start, 2 mm lead"),
    ("leadscrew_t8_8mm", "screw", 8, 300, 8, 2, 4, 0.11, "Generic", "T8 2mm-8mm",
     "T8 lead screw, 4-start, 8 mm lead (fast Z)"),
    ("leadscrew_t8_1mm", "screw", 8, 300, 1, 1, 1, 0.11, "Generic", "T8 1mm-1mm",
     "T8 lead screw, fine 1 mm lead (high resolution)"),
    ("ballscrew_1204", "ballscrew", 12, 300, 4, 4, 1, 0.28, "Generic", "SFU1204",
     "12 mm ball screw, 4 mm lead"),
    ("ballscrew_1605", "ballscrew", 16, 400, 5, 5, 1, 0.63, "Generic", "SFU1605",
     "16 mm ball screw, 5 mm lead (CNC standard)"),
    ("ballscrew_1610", "ballscrew", 16, 400, 10, 5, 2, 0.63, "Generic", "SFU1610",
     "16 mm ball screw, 10 mm lead (fast)"),
    ("acme_half_10", "screw", 12.7, 300, 2.54, 2.54, 1, 0.30, "Generic",
     '1/2"-10 ACME', "1/2 inch 10-TPI ACME lead screw"),
]

# Pulleys / capstans: travel_per_rev = pitch * teeth (belt) or pi*d (capstan).
# slug, kind, pitch_dia_mm, width_mm, teeth, belt_pitch_mm, mass_kg, mfr, pn,
# notes
_PULLEYS = [
    ("gt2_pulley_20t", "pulley", 12.73, 6, 20, 2, 0.006, "Generic", "GT2-20T",
     "20-tooth GT2 timing pulley (3D-printer belts)"),
    ("gt2_pulley_16t", "pulley", 10.19, 6, 16, 2, 0.005, "Generic", "GT2-16T",
     "16-tooth GT2 timing pulley"),
    ("gt2_idler_20t", "pulley", 12.73, 6, 20, 2, 0.006, "Generic", "GT2 idler",
     "smooth GT2 idler pulley"),
    ("htd5m_pulley_15t", "pulley", 23.87, 9, 15, 5, 0.020, "Generic", "HTD5M-15T",
     "15-tooth HTD-5M timing pulley (higher load)"),
    ("capstan_drum_20mm", "capstan", 20, 25, 0, 0, 0.030, "Generic", "capstan 20",
     "20 mm capstan drum for cable / rope drives"),
    ("capstan_drum_40mm", "capstan", 40, 30, 0, 0, 0.080, "Generic", "capstan 40",
     "40 mm capstan drum for tendon-driven robots"),
]


def _make_screw(row):
    (slug, kind, dia, length, lead, pitch, starts, mass, mfr, pn, notes) = row

    def factory():
        part = Transmission(slug)
        part._build_body(
            cylinder(radius=dia * MM / 2, height=length * MM),
            mass_kg=mass, color=BODY_STEEL,
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        part._configure(
            travel_per_rev_mm=lead, lead_mm=lead, pitch_mm=pitch, starts=starts
        )
        part.subtype = kind
        return part

    factory.__doc__ = (
        f"{notes}. {dia} mm x {length} mm, {lead} mm lead "
        f"({starts}-start) -> {lead} mm travel per turn. {mfr} {pn}."
    )
    return register(slug, "transmission", factory, manufacturer=mfr,
                    part_number=pn, summary=notes)


def _make_pulley(row):
    (slug, kind, pdia, width, teeth, belt_pitch, mass, mfr, pn, notes) = row
    if kind == "capstan":
        travel = math.pi * pdia
        color = BODY_BLACK
    else:
        travel = teeth * belt_pitch
        color = BODY_BLACK

    def factory():
        part = Transmission(slug)
        part._build_body(
            cylinder(radius=pdia * MM / 2, height=width * MM),
            mass_kg=mass, color=color,
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        part._configure(travel_per_rev_mm=round(travel, 3),
                        pitch_mm=belt_pitch or None)
        part.subtype = kind
        part.teeth = teeth or None
        return part

    detail = (
        f"pi*{pdia} = {travel:.1f} mm rope per turn"
        if kind == "capstan"
        else f"{teeth} teeth x {belt_pitch} mm = {travel:.0f} mm belt per turn"
    )
    factory.__doc__ = f"{notes}. {pdia} mm pitch dia; {detail}. {mfr} {pn}."
    return register(slug, "transmission", factory, manufacturer=mfr,
                    part_number=pn, summary=notes)


# Closed-loop timing belts: (slug, pitch_mm, width_mm, pitch_length_mm, teeth, note)
_BELTS = [
    ("gt2_belt_200mm", 2, 6, 200, 100, "GT2 closed-loop belt, 200 mm"),
    ("gt2_belt_280mm", 2, 6, 280, 140, "GT2 closed-loop belt, 280 mm"),
    ("gt2_belt_610mm", 2, 6, 610, 305, "GT2 closed-loop belt, 610 mm"),
    ("gt2_belt_open_6mm", 2, 6, 1000, 500, "GT2 open-ended belt (per metre)"),
    ("htd5m_belt_450mm", 5, 9, 450, 90, "HTD-5M closed-loop belt, 450 mm"),
]


def _make_belt(row):
    slug, pitch, width, length, teeth, note = row

    def factory():
        part = Transmission(slug)
        # An "uncoiled" strip: length x width x ~1.4 mm.
        part._build_body(
            cube(length * MM, width * MM, 1.4 * MM),
            mass_kg=length * width * 1.4 * MM**3 * 1200,
            color=BODY_BLACK,
            part_number=slug,
            notes=note,
        )
        part._configure(travel_per_rev_mm=0.0, pitch_mm=pitch)
        part.subtype = "belt"
        part.pitch_length_mm = length
        part.width_mm = width
        part.teeth = teeth
        return part

    factory.__doc__ = (
        f"{note}. {pitch} mm pitch, {width} mm wide, {teeth} teeth."
    )
    return register(slug, "transmission", factory, part_number=slug, summary=note)


for _row in _SCREWS:
    globals()[f"get_{_row[0]}"] = _make_screw(_row)
for _row in _PULLEYS:
    globals()[f"get_{_row[0]}"] = _make_pulley(_row)
for _row in _BELTS:
    globals()[f"get_{_row[0]}"] = _make_belt(_row)


__all__ = (
    ["Transmission"]
    + [f"get_{r[0]}" for r in _SCREWS]
    + [f"get_{r[0]}" for r in _PULLEYS]
    + [f"get_{r[0]}" for r in _BELTS]
)
