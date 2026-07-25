"""Structural hardware: aluminum V-slot / T-slot extrusion, brackets and
gussets, linear rails, smooth rods and mounting plates -- the frame a
machine is built on.

Includes generators -- ``extrusion(profile_mm, length_mm)`` and
``smooth_rod(diameter_mm, length_mm)`` build any size -- plus common
presets. Extrusions are modeled as solid bars at the profile envelope (the
V-slots are not cut, but the outer dimensions and mass are right).
"""

from __future__ import annotations

from ._base import (
    MM,
    BODY_ALU,
    BODY_STEEL,
    PassivePart,
    register,
)

ALU_DENSITY = 2700.0
STEEL_DENSITY = 7850.0


class StructuralPart(PassivePart):
    category = "structure"


def extrusion(
    profile_mm: float = 20,
    length_mm: float = 250,
    *,
    width_mm: float | None = None,
    name: str | None = None,
) -> StructuralPart:
    """A length of aluminum extrusion. ``profile_mm`` x (``width_mm`` or
    ``profile_mm``) cross-section, e.g. ``extrusion(20, 500)`` is a 2020 x
    500 mm; ``extrusion(20, 500, width_mm=40)`` is a 2040."""
    width = width_mm if width_mm is not None else profile_mm
    tag = f"{int(profile_mm)}{int(width)}"
    part = StructuralPart(name or f"extrusion_{tag}_{int(length_mm)}mm")
    # ~35% fill accounts for the hollow V-slot cross-section.
    mass = (profile_mm * width * length_mm) * MM**3 * ALU_DENSITY * 0.35
    part.build_box(length_mm, width, profile_mm, mass_kg=mass, color=BODY_ALU,
                   part_number=f"{tag} x {int(length_mm)}mm",
                   notes=f"{tag} aluminum extrusion, {int(length_mm)} mm")
    part.category = "extrusion"
    part.profile = tag
    part.length_mm = length_mm
    return part


def smooth_rod(
    diameter_mm: float, length_mm: float, *, chrome: bool = True,
    name: str | None = None,
) -> StructuralPart:
    """A hardened / chromed smooth rod (for LMxUU linear bushings)."""
    part = StructuralPart(name or f"smooth_rod_{diameter_mm:g}mm_{int(length_mm)}mm")
    mass = 3.14159 * (diameter_mm * MM / 2) ** 2 * (length_mm * MM) * STEEL_DENSITY
    part.build_cylinder(diameter_mm, length_mm, mass_kg=mass, color=BODY_STEEL,
                        part_number=f"rod {diameter_mm:g}x{int(length_mm)}",
                        notes=f"{diameter_mm:g} mm smooth rod, {int(length_mm)} mm")
    part.category = "rod"
    part.diameter_mm = diameter_mm
    part.length_mm = length_mm
    return part


# Extrusion presets: (profile, width, length)
_EXTRUSIONS = [
    (20, 20, 100), (20, 20, 250), (20, 20, 500), (20, 20, 1000),
    (20, 40, 250), (20, 40, 500), (30, 30, 500), (40, 40, 500), (40, 40, 1000),
]
# Rods: (diameter, length)
_RODS = [(8, 300), (8, 500), (10, 400), (12, 500)]

# Brackets / plates: (slug, category, (l,w,h), mass, color, pn, notes)
_PARTS = [
    ("corner_bracket_2020", "bracket", (20, 20, 20), 0.010, BODY_ALU,
     "2020 inside corner", "inside corner bracket for 2020 extrusion"),
    ("l_bracket_steel", "bracket", (38, 38, 20), 0.030, BODY_STEEL,
     "steel L-bracket", "zinc steel L / angle bracket"),
    ("gusset_2020", "bracket", (28, 28, 20), 0.020, BODY_ALU,
     "2020 gusset", "diagonal gusset bracket for rigidity"),
    ("corner_cube_3way", "bracket", (20, 20, 20), 0.015, BODY_ALU,
     "3-way corner", "3-way corner connector for extrusion frames"),
    ("t_nut_2020", "bracket", (6, 10, 6), 0.002, BODY_STEEL,
     "M5 T-nut", "drop-in M5 T-nut for 2020 slot"),
    ("angle_bracket_2040", "bracket", (40, 20, 40), 0.035, BODY_ALU,
     "2040 angle", "90deg angle bracket for 2040"),
    ("rubber_foot_m6", "mount", (25, 25, 15), 0.010, BODY_STEEL,
     "M6 foot", "rubber leveling foot with M6 stud"),
    ("perfboard_70x90", "plate", (90, 70, 1.6), 0.030, BODY_ALU,
     "perfboard", "70x90 mm prototyping perfboard"),
    ("breadboard_830", "plate", (165, 55, 10), 0.060, BODY_ALU,
     "MB-102", "830-point solderless breadboard"),
    ("alu_plate_100x100", "plate", (100, 100, 3), 0.081, BODY_ALU,
     "alu plate", "100x100x3 mm aluminum mounting plate"),
    ("mgn12_carriage", "linear_rail", (44, 27, 13), 0.055, BODY_STEEL,
     "MGN12H block", "MGN12 linear-rail carriage block"),
]

# Linear rails (rail only, by length): (size, length)
_RAILS = [("mgn9", 250), ("mgn12", 250), ("mgn12", 400), ("sbr16", 500)]


def _reg_extrusion(profile, width, length):
    slug = f"extrusion_{profile}{width}_{length}mm"

    def factory(p=profile, w=width, l=length, name=slug):
        return extrusion(p, l, width_mm=w, name=name)

    factory.__doc__ = f"{profile}{width} aluminum extrusion, {length} mm."
    return register(slug, "extrusion", factory,
                    part_number=f"{profile}{width}x{length}",
                    summary="aluminum extrusion")


def _reg_rod(dia, length):
    slug = f"smooth_rod_{dia:g}mm_{length}mm"

    def factory(d=dia, l=length, name=slug):
        return smooth_rod(d, l, name=name)

    factory.__doc__ = f"{dia:g} mm chromed smooth rod, {length} mm."
    return register(slug, "rod", factory, part_number=f"rod {dia:g}x{length}",
                    summary="smooth rod")


def _reg_rail(size, length):
    slug = f"linear_rail_{size}_{length}mm"
    # MGN9 ~9 mm wide, MGN12 ~12 mm, SBR16 ~40 mm base.
    width = {"mgn9": 9, "mgn12": 12, "sbr16": 40}.get(size, 12)
    height = {"mgn9": 8, "mgn12": 8, "sbr16": 40}.get(size, 8)

    def factory(s=size, l=length, w=width, h=height, name=slug):
        part = StructuralPart(name)
        mass = (l * w * h) * MM**3 * STEEL_DENSITY * 0.7
        part.build_box(l, w, h, mass_kg=mass, color=BODY_STEEL,
                       part_number=f"{s.upper()} {l}mm",
                       notes=f"{s.upper()} linear rail, {l} mm")
        part.category = "linear_rail"
        part.rail_size = s
        part.length_mm = l
        return part

    factory.__doc__ = f"{size.upper()} linear rail, {length} mm."
    return register(slug, "linear_rail", factory,
                    part_number=f"{size.upper()} {length}mm", summary="linear rail")


def _reg_part(row):
    slug, category, dims, mass, color, pn, notes = row

    def factory(s=slug, c=category, d=dims, m=mass, col=color, p=pn, n=notes):
        part = StructuralPart(s)
        part.build_box(d[0], d[1], d[2], mass_kg=m, color=col,
                       part_number=p, notes=n)
        part.category = c
        return part

    factory.__doc__ = f"{notes}."
    return register(slug, category, factory, part_number=pn, summary=notes)


for _p, _w, _l in _EXTRUSIONS:
    globals()[f"get_extrusion_{_p}{_w}_{_l}mm"] = _reg_extrusion(_p, _w, _l)
for _d, _l in _RODS:
    globals()[f"get_smooth_rod_{_d:g}mm_{_l}mm"] = _reg_rod(_d, _l)
for _s, _l in _RAILS:
    globals()[f"get_linear_rail_{_s}_{_l}mm"] = _reg_rail(_s, _l)
for _row in _PARTS:
    globals()[f"get_{_row[0]}"] = _reg_part(_row)


__all__ = [
    "StructuralPart", "extrusion", "smooth_rod",
] + [n for n in list(globals()) if n.startswith("get_")]
