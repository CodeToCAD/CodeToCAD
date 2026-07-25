"""Couplings, universal joints and bearings -- the parts that connect a
motor shaft to the thing it drives.

Includes **parametric generators**::

    from codetocad_integrations.library.couplings import (
        universal_joint, shaft_coupling, ball_bearing,
    )
    uj = universal_joint(bore_mm=8)        # articulates: uj.bend_joint
    cp = shaft_coupling(5, 8, "jaw")       # 5 mm motor -> 8 mm lead screw
    bg = ball_bearing(bore_mm=8, od_mm=22, width_mm=7)   # a 608

plus registered presets (``lib.get_coupling_5x8_flexible()``,
``lib.get_bearing_608()``, ``lib.get_universal_joint_8mm()``, ...).

The universal joint is modeled as three linked bodies -- input yoke, cross
and output yoke -- with a **revolute ``bend_joint``**, so it genuinely
articulates in a simulation. Couplings and bearings are single-body blanks
at their real outer diameter / length, carrying their bores and ratings.
"""

from __future__ import annotations

import math

from ._base import (
    MM,
    BODY_BLACK,
    BODY_STEEL,
    Location,
    MaterialBase,
    PassivePart,
    cube,
    cylinder,
    register,
)

STEEL_DENSITY = 7850.0


def _cyl_mass(diameter_mm, length_mm, fill=1.0):
    r = diameter_mm * MM / 2
    return math.pi * r * r * (length_mm * MM) * STEEL_DENSITY * fill


class UniversalJoint(PassivePart):
    """A Cardan / universal joint: transmits rotation between two shafts at
    an angle. ``bend_joint`` is a revolute that flexes the output yoke about
    the input (+/-45deg), so it moves in a simulation."""

    category = "universal_joint"


class ShaftCoupling(PassivePart):
    """A shaft coupling joining two bores. ``coupling_type`` is one of
    ``rigid``, ``jaw`` (spider / Lovejoy), ``oldham``, ``helical`` (beam) or
    ``setscrew``."""

    category = "coupling"


class Bearing(PassivePart):
    """A rolling-element bearing (or bushing) blank at its real
    bore / OD / width."""

    category = "bearing"


# --------------------------------------------------------------------------
# Generators
# --------------------------------------------------------------------------


def universal_joint(
    bore_mm: float,
    *,
    outer_diameter_mm: float | None = None,
    length_mm: float | None = None,
    max_angle_deg: float = 45.0,
    name: str | None = None,
) -> UniversalJoint:
    """Build an articulating universal joint sized for ``bore_mm`` shafts."""
    od = outer_diameter_mm if outer_diameter_mm is not None else bore_mm * 2.4
    total = length_mm if length_mm is not None else bore_mm * 5
    yoke_len = total / 2
    uj = UniversalJoint(name or f"universal_joint_{bore_mm:g}mm")
    # Input yoke: a stub whose top sits at the joint centre (z = 0).
    input_yoke = cylinder(
        radius=od * MM / 2, height=yoke_len * MM,
        start_location=Location(z=-yoke_len * MM / 2),
    )
    uj._build_body(
        input_yoke,
        mass_kg=_cyl_mass(od, total, fill=0.6),
        color=BODY_STEEL,
        notes=f"universal joint for {bore_mm} mm shafts (+/-{max_angle_deg}deg)",
    )
    # The cross (spider) at the centre, welded to the input yoke.
    cross = cube(od * 0.9 * MM, od * 0.9 * MM, od * 0.4 * MM)
    cross.name = f"{uj.name}_cross"
    cross.set_material(MaterialBase("cross", mass=0.01, color_rgba=BODY_BLACK))
    uj.fixed(Location(z=0), cross, Location(z=0))
    # Output yoke: bends about X (a Z-axis location rotated 90deg about Y).
    output_yoke = cylinder(
        radius=od * MM / 2, height=yoke_len * MM,
        start_location=Location(z=yoke_len * MM / 2),
    )
    output_yoke.name = f"{uj.name}_output"
    output_yoke.set_material(MaterialBase("output", mass=_cyl_mass(od, yoke_len, 0.6),
                                          color_rgba=BODY_STEEL))
    bend = Location.from_euler(0, 0, 0, y_deg=90, name=f"{uj.name}_bend")
    limit = math.radians(max_angle_deg)
    uj.bend_joint = uj.revolute(bend, output_yoke, bend,
                                min_limits=-limit, max_limits=limit)
    uj.output_yoke = output_yoke
    uj.bore_mm = bore_mm
    uj.outer_diameter_mm = od
    uj.max_angle_deg = max_angle_deg
    return uj


def shaft_coupling(
    bore_a_mm: float,
    bore_b_mm: float,
    coupling_type: str = "jaw",
    *,
    outer_diameter_mm: float | None = None,
    length_mm: float | None = None,
    max_torque_nm: float | None = None,
    name: str | None = None,
) -> ShaftCoupling:
    """Build a shaft coupling from a ``bore_a_mm`` shaft to a ``bore_b_mm``
    shaft. ``coupling_type``: rigid / jaw / oldham / helical / setscrew."""
    big = max(bore_a_mm, bore_b_mm)
    od = outer_diameter_mm if outer_diameter_mm is not None else big * 3
    length = length_mm if length_mm is not None else big * 3.5
    color = BODY_BLACK if coupling_type in ("jaw", "oldham") else BODY_STEEL
    cp = ShaftCoupling(
        name or f"coupling_{bore_a_mm:g}x{bore_b_mm:g}_{coupling_type}"
    )
    cp._build_body(
        cylinder(radius=od * MM / 2, height=length * MM),
        mass_kg=_cyl_mass(od, length, fill=0.7),
        color=color,
        notes=f"{coupling_type} coupling {bore_a_mm}->{bore_b_mm} mm",
    )
    cp.bore_a_mm = bore_a_mm
    cp.bore_b_mm = bore_b_mm
    cp.coupling_type = coupling_type
    cp.outer_diameter_mm = od
    cp.length_mm = length
    cp.max_torque_nm = max_torque_nm
    return cp


def ball_bearing(
    bore_mm: float,
    od_mm: float,
    width_mm: float,
    *,
    kind: str = "deep-groove ball",
    dynamic_load_n: float | None = None,
    name: str | None = None,
) -> Bearing:
    """Build a bearing blank at bore x OD x width (mm)."""
    bearing = Bearing(name or f"bearing_{bore_mm:g}x{od_mm:g}x{width_mm:g}")
    bearing._build_body(
        cylinder(radius=od_mm * MM / 2, height=width_mm * MM),
        # A ring: roughly half the solid-cylinder mass.
        mass_kg=_cyl_mass(od_mm, width_mm, fill=0.5)
        - _cyl_mass(bore_mm, width_mm, fill=0.5),
        color=BODY_STEEL,
        notes=f"{kind} bearing {bore_mm}x{od_mm}x{width_mm} mm",
    )
    bearing.bore_mm = bore_mm
    bearing.outer_diameter_mm = od_mm
    bearing.width_mm = width_mm
    bearing.kind = kind
    bearing.dynamic_load_n = dynamic_load_n
    return bearing


def linear_bearing(
    bore_mm: float, od_mm: float, length_mm: float, *, name: str | None = None
) -> Bearing:
    """Build a linear ball bushing (LMxUU-style) that slides on a rod."""
    b = ball_bearing(bore_mm, od_mm, length_mm, kind="linear ball bushing",
                     name=name or f"linear_bearing_lm{bore_mm:g}uu")
    b.category = "bearing"
    return b


# --------------------------------------------------------------------------
# Presets
# --------------------------------------------------------------------------

# Universal joints by shaft bore.
_UJOINTS = [4, 5, 6, 6.35, 8, 10, 12]

# Shaft couplings: (bore_a, bore_b, type, part_number, note)
_COUPLINGS = [
    (5, 5, "rigid", "rigid-5-5", "rigid clamp coupling"),
    (8, 8, "rigid", "rigid-8-8", "rigid clamp coupling"),
    (5, 8, "jaw", "jaw-5-8", "flexible spider (Lovejoy-style) coupling"),
    (5, 5, "jaw", "jaw-5-5", "flexible spider coupling (NEMA 17 to 5 mm)"),
    (6.35, 8, "jaw", "jaw-635-8", "flexible spider coupling (1/4in to 8 mm)"),
    (8, 10, "jaw", "jaw-8-10", "flexible spider coupling"),
    (5, 8, "helical", "helical-5-8", "helical beam coupling (zero-backlash)"),
    (6.35, 10, "helical", "helical-635-10", "helical beam coupling"),
    (5, 8, "oldham", "oldham-5-8", "Oldham coupling (parallel misalignment)"),
    (5, 5, "setscrew", "setscrew-5-5", "set-screw rigid coupling"),
]

# Bearings: (bore, od, width, series/part, kind)
_BEARINGS = [
    (3, 10, 4, "623", "deep-groove ball"),
    (4, 13, 5, "624", "deep-groove ball"),
    (5, 16, 5, "625", "deep-groove ball"),
    (6, 19, 6, "626", "deep-groove ball"),
    (8, 16, 5, "688", "deep-groove ball"),
    (8, 22, 7, "608", "deep-groove ball (skate/608)"),
    (10, 19, 5, "6800", "thin-section ball"),
    (10, 22, 6, "6900", "thin-section ball"),
    (10, 26, 8, "6000", "deep-groove ball"),
    (12, 28, 8, "6001", "deep-groove ball"),
    (6.35, 12.7, 4.762, "R188", "skate/flywheel ball"),
]

# Linear bushings: (bore, od, length, part)
_LINEAR_BEARINGS = [
    (8, 15, 24, "LM8UU"),
    (10, 19, 29, "LM10UU"),
    (12, 21, 30, "LM12UU"),
]


def _reg_uj(bore):
    slug = f"universal_joint_{bore:g}mm".replace(".", "_")

    def factory(b=bore, name=slug):
        return universal_joint(b, name=name)

    factory.__doc__ = (
        f"Articulating universal joint for {bore} mm shafts (+/-45deg bend)."
    )
    return register(slug, "universal_joint", factory,
                    part_number=f"U-joint {bore}mm",
                    summary=f"universal joint, {bore} mm bore")


def _reg_coupling(a, b, ctype, pn, note):
    slug = f"coupling_{a:g}x{b:g}_{ctype}".replace(".", "_")

    def factory(a=a, b=b, c=ctype, name=slug):
        return shaft_coupling(a, b, c, name=name)

    factory.__doc__ = f"{note}: {a} mm to {b} mm bore."
    return register(slug, "coupling", factory, part_number=pn, summary=note)


def _reg_bearing(bore, od, width, series, kind):
    slug = f"bearing_{series}".lower()

    def factory(bo=bore, o=od, w=width, k=kind, name=slug):
        return ball_bearing(bo, o, w, kind=k, name=name)

    factory.__doc__ = f"{series} bearing: {bore} x {od} x {width} mm, {kind}."
    return register(slug, "bearing", factory, part_number=series, summary=kind)


def _reg_linear_bearing(bore, od, length, pn):
    slug = pn.lower()

    def factory(bo=bore, o=od, l=length, name=slug, p=pn):
        return linear_bearing(bo, o, l, name=name)

    factory.__doc__ = f"{pn} linear ball bushing: {bore} mm rod, {od} x {length} mm."
    return register(slug, "bearing", factory, part_number=pn,
                    summary=f"{pn} linear bushing")


for _b in _UJOINTS:
    globals()[f"get_universal_joint_{_b:g}mm".replace(".", "_")] = _reg_uj(_b)
for _a, _b, _c, _pn, _note in _COUPLINGS:
    globals()[f"get_coupling_{_a:g}x{_b:g}_{_c}".replace(".", "_")] = _reg_coupling(
        _a, _b, _c, _pn, _note
    )
for _bo, _od, _w, _s, _k in _BEARINGS:
    globals()[f"get_bearing_{_s.lower()}"] = _reg_bearing(_bo, _od, _w, _s, _k)
for _bo, _od, _l, _pn in _LINEAR_BEARINGS:
    globals()[f"get_{_pn.lower()}"] = _reg_linear_bearing(_bo, _od, _l, _pn)


__all__ = [
    "UniversalJoint", "ShaftCoupling", "Bearing",
    "universal_joint", "shaft_coupling", "ball_bearing", "linear_bearing",
] + [n for n in list(globals()) if n.startswith("get_")]
