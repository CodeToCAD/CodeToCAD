"""Gears -- both **parametric generators** and common presets.

The generators build a gear to any spec::

    from codetocad_integrations.library.gears import spur_gear
    pinion = spur_gear(module_mm=1.0, teeth=20)   # 20 mm pitch dia
    wheel  = spur_gear(module_mm=1.0, teeth=60)
    print(pinion.ratio_with(wheel))               # 3.0
    print(pinion.center_distance_to(wheel))       # 40.0 mm

Geometry is a **blank at the tip (addendum) diameter** -- involute teeth
are not cut (the core has no arbitrary-polygon primitive), but every gear
parameter (module, teeth, pitch/outer/root diameter, pressure angle, bore)
is carried on the part and the meshing math (`ratio_with`,
`center_distance_to`) is exact. Blanks at the correct outer diameter and
face width are what you want for layout, clearance and inertia anyway.

Presets cover the common module-1 / module-2 tooth counts plus bevel,
worm and rack parts. All are registered, so ``lib.get_spur_gear_m1_20t()``
and ``lib.list_parts("gear")`` work.
"""

from __future__ import annotations

import math

from ._base import (
    MM,
    BODY_STEEL,
    PassivePart,
    cube,
    cylinder,
    register,
)

STEEL_DENSITY = 7850.0  # kg/m^3, for a nominal blank mass


def _blank_mass(outer_diameter_mm: float, width_mm: float) -> float:
    radius = outer_diameter_mm * MM / 2
    return math.pi * radius * radius * (width_mm * MM) * STEEL_DENSITY


class Gear(PassivePart):
    """A spur / helical gear blank with full involute-gear parameters."""

    category = "gear"

    def _setup(self, module_mm, teeth, pressure_angle_deg, helix_deg, bore_mm):
        self.module_mm = module_mm
        self.teeth = teeth
        self.pressure_angle_deg = pressure_angle_deg
        self.helix_deg = helix_deg
        self.bore_mm = bore_mm
        self.pitch_diameter_mm = module_mm * teeth
        self.outer_diameter_mm = module_mm * (teeth + 2)
        self.root_diameter_mm = module_mm * (teeth - 2.5)

    def ratio_with(self, other: "Gear") -> float:
        """Reduction ratio driving this gear into ``other`` (output/input =
        their tooth ratio)."""
        return other.teeth / self.teeth

    def center_distance_to(self, other: "Gear") -> float:
        """Shaft-to-shaft distance in mm for this gear meshing ``other``
        (same module)."""
        return (self.pitch_diameter_mm + other.pitch_diameter_mm) / 2


class BevelGear(Gear):
    category = "bevel_gear"


class Worm(PassivePart):
    """A worm (screw) that drives a worm wheel. ``starts`` (thread starts)
    sets the ratio: wheel_teeth / starts."""

    category = "worm"

    def ratio_with(self, wheel: "Gear") -> float:
        return wheel.teeth / self.starts


class Rack(PassivePart):
    """A gear rack: a straight bar of teeth. One pinion revolution advances
    the rack by ``pi * module * pinion_teeth`` (== pinion pitch
    circumference); ``travel_per_pinion_rev_mm(pinion)`` computes it."""

    category = "rack"

    def travel_per_pinion_rev_mm(self, pinion: "Gear") -> float:
        return math.pi * pinion.pitch_diameter_mm


# --------------------------------------------------------------------------
# Generators
# --------------------------------------------------------------------------


def spur_gear(
    module_mm: float,
    teeth: int,
    *,
    face_width_mm: float | None = None,
    bore_mm: float = 5.0,
    pressure_angle_deg: float = 20.0,
    helix_deg: float = 0.0,
    name: str | None = None,
    mass_kg: float | None = None,
) -> Gear:
    """Build a spur (``helix_deg=0``) or helical gear. ``module_mm`` is the
    metric module (pitch diameter = module x teeth). Face width defaults to
    a typical ``8 x module``."""
    width = face_width_mm if face_width_mm is not None else max(8 * module_mm, 3)
    outer = module_mm * (teeth + 2)
    gear = Gear(name or f"spur_gear_m{module_mm:g}_{teeth}t")
    gear._setup(module_mm, teeth, pressure_angle_deg, helix_deg, bore_mm)
    gear._build_body(
        cylinder(radius=outer * MM / 2, height=width * MM),
        mass_kg=mass_kg if mass_kg is not None else _blank_mass(outer, width),
        color=BODY_STEEL,
        notes=f"module {module_mm} x {teeth}T {'helical' if helix_deg else 'spur'} gear",
    )
    gear.face_width_mm = width
    return gear


def bevel_gear(
    module_mm: float,
    teeth: int,
    *,
    pitch_angle_deg: float = 45.0,
    face_width_mm: float | None = None,
    bore_mm: float = 6.0,
    name: str | None = None,
) -> BevelGear:
    """Build a bevel gear (a cone frustum blank). ``pitch_angle_deg`` is the
    half-cone angle; a 45deg pair makes a 1:1 right-angle drive."""
    width = face_width_mm if face_width_mm is not None else max(6 * module_mm, 4)
    outer = module_mm * (teeth + 2)
    # A draft on the cylinder tapers it into the bevel cone.
    draft = min(pitch_angle_deg, 60.0)
    gear = BevelGear(name or f"bevel_gear_m{module_mm:g}_{teeth}t")
    gear._setup(module_mm, teeth, 20.0, 0.0, bore_mm)
    gear._build_body(
        cylinder(radius=outer * MM / 2, height=width * MM, draft_angle=draft),
        mass_kg=_blank_mass(outer, width) * 0.7,
        color=BODY_STEEL,
        notes=f"module {module_mm} x {teeth}T bevel gear, {pitch_angle_deg}deg pitch",
    )
    gear.face_width_mm = width
    gear.pitch_angle_deg = pitch_angle_deg
    return gear


def worm(
    module_mm: float,
    *,
    starts: int = 1,
    length_mm: float = 40.0,
    diameter_mm: float | None = None,
    bore_mm: float = 6.0,
    name: str | None = None,
) -> Worm:
    """Build a worm (screw). ``starts`` sets the ratio with its wheel."""
    diameter = diameter_mm if diameter_mm is not None else module_mm * 8
    w = Worm(name or f"worm_m{module_mm:g}_{starts}start")
    w._build_body(
        cylinder(radius=diameter * MM / 2, height=length_mm * MM),
        mass_kg=_blank_mass(diameter, length_mm),
        color=BODY_STEEL,
        notes=f"module {module_mm}, {starts}-start worm",
    )
    w.module_mm = module_mm
    w.starts = starts
    w.lead_mm = module_mm * math.pi * starts
    w.bore_mm = bore_mm
    return w


def gear_rack(
    module_mm: float,
    *,
    length_mm: float = 200.0,
    height_mm: float | None = None,
    width_mm: float | None = None,
    name: str | None = None,
) -> Rack:
    """Build a straight gear rack ``length_mm`` long for the given module."""
    height = height_mm if height_mm is not None else module_mm * 4
    width = width_mm if width_mm is not None else module_mm * 6
    teeth = int(length_mm / (math.pi * module_mm))
    rack = Rack(name or f"gear_rack_m{module_mm:g}_{int(length_mm)}mm")
    rack._build_body(
        cube(length_mm * MM, width * MM, height * MM),
        mass_kg=(length_mm * width * height) * MM**3 * STEEL_DENSITY,
        color=BODY_STEEL,
        notes=f"module {module_mm} gear rack, {int(length_mm)} mm ({teeth} teeth)",
    )
    rack.module_mm = module_mm
    rack.length_mm = length_mm
    rack.teeth = teeth
    return rack


# --------------------------------------------------------------------------
# Registered presets
# --------------------------------------------------------------------------

# (module, teeth) spur gears across the common tooth counts.
_SPUR = [
    (0.5, 20), (0.5, 40),
    (1.0, 10), (1.0, 12), (1.0, 15), (1.0, 20), (1.0, 24),
    (1.0, 30), (1.0, 40), (1.0, 60), (1.0, 80),
    (1.5, 15), (1.5, 30), (1.5, 45),
    (2.0, 12), (2.0, 15), (2.0, 20), (2.0, 30), (2.0, 40), (2.0, 60),
    (3.0, 15), (3.0, 20), (3.0, 40),
]
_HELICAL = [(1.0, 20), (2.0, 20), (2.0, 40)]
_BEVEL = [(1.0, 20), (1.5, 20), (2.0, 20), (2.0, 30)]
_WORM = [(1.0, 1), (1.5, 1), (2.0, 1), (2.0, 2)]
_RACKS = [(1.0, 200), (1.5, 300), (2.0, 500), (2.0, 1000)]


def _reg_spur(module, teeth, helix=0.0):
    kind = "helical" if helix else "spur"
    slug = f"{kind}_gear_m{module:g}_{teeth}t"

    def factory(m=module, t=teeth, h=helix, s=slug):
        return spur_gear(m, t, helix_deg=h, name=s)

    pd = module * teeth
    factory.__doc__ = (
        f"{kind.title()} gear, module {module}, {teeth} teeth: "
        f"{pd:g} mm pitch dia, {module * (teeth + 2):g} mm outer dia, 20deg PA."
    )
    return register(slug, "gear", factory, summary=f"module {module} x {teeth}T {kind} gear")


for _m, _t in _SPUR:
    globals()[f"get_spur_gear_m{_m:g}_{_t}t"] = _reg_spur(_m, _t)
for _m, _t in _HELICAL:
    globals()[f"get_helical_gear_m{_m:g}_{_t}t"] = _reg_spur(_m, _t, helix=15.0)


def _reg_bevel(module, teeth):
    slug = f"bevel_gear_m{module:g}_{teeth}t"

    def factory(m=module, t=teeth, s=slug):
        return bevel_gear(m, t, name=s)

    factory.__doc__ = (
        f"Bevel gear, module {module}, {teeth} teeth, 45deg pitch "
        f"(right-angle drive)."
    )
    return register(slug, "bevel_gear", factory,
                    summary=f"module {module} x {teeth}T bevel gear")


def _reg_worm(module, starts):
    slug = f"worm_m{module:g}_{starts}start"

    def factory(m=module, s=starts, name=slug):
        return worm(m, starts=s, name=name)

    factory.__doc__ = f"Worm, module {module}, {starts}-start (drives a worm wheel)."
    return register(slug, "worm", factory,
                    summary=f"module {module} {starts}-start worm")


def _reg_rack(module, length):
    slug = f"gear_rack_m{module:g}_{length}mm"

    def factory(m=module, l=length, name=slug):
        return gear_rack(m, length_mm=l, name=name)

    factory.__doc__ = f"Gear rack, module {module}, {length} mm long."
    return register(slug, "rack", factory,
                    summary=f"module {module} rack, {length} mm")


for _m, _t in _BEVEL:
    globals()[f"get_bevel_gear_m{_m:g}_{_t}t"] = _reg_bevel(_m, _t)
for _m, _s in _WORM:
    globals()[f"get_worm_m{_m:g}_{_s}start"] = _reg_worm(_m, _s)
for _m, _l in _RACKS:
    globals()[f"get_gear_rack_m{_m:g}_{_l}mm"] = _reg_rack(_m, _l)


__all__ = [
    "Gear", "BevelGear", "Worm", "Rack",
    "spur_gear", "bevel_gear", "worm", "gear_rack",
] + [n for n in list(globals()) if n.startswith("get_")]
