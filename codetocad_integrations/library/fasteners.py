"""Fasteners: metric bolts / screws, nuts, washers, standoffs, heat-set
inserts and threaded rod.

This complements the **core** :class:`codetocad.CommonFasteners` enum
(which the geometry backends federate into exact models). The core enum
stays where it is -- it is part of the public API and the Blender /
build123d backends import it -- so this module *bridges* to it
(:func:`from_common`) and adds a much larger catalog of ready-made
fastener ``Part3D`` objects with head style, drive and clearance-hole
data::

    from codetocad_integrations.library import get_m3x12_socket_head, get_m3_nut
    bolt = get_m3x12_socket_head()
    bolt.clearance_hole(plate, plate.top_center)   # drills the right hole

Threads are simplified to plain cylinders (the core has no thread
primitive), but every dimension -- thread diameter, length, head diameter,
across-flats -- and the clearance-hole size are datasheet-correct.
"""

from __future__ import annotations

from codetocad import CommonFasteners, Location

from ._base import (
    MM,
    BODY_BRASS,
    BODY_STEEL,
    PassivePart,
    cylinder,
    register,
)

STEEL_DENSITY = 7850.0
BRASS_DENSITY = 8500.0

# ISO clearance-hole (medium fit) diameters, mm, keyed by thread size.
_CLEARANCE = {
    2: 2.4, 2.5: 2.9, 3: 3.4, 4: 4.5, 5: 5.5, 6: 6.6, 8: 9.0, 10: 11.0,
}
# Across-flats of a standard hex nut / bolt head, mm.
_HEX_AF = {2: 4, 2.5: 5, 3: 5.5, 4: 7, 5: 8, 6: 10, 8: 13, 10: 17}
# Socket-cap head diameter, mm.
_SOCKET_HEAD = {2: 3.8, 2.5: 4.5, 3: 5.5, 4: 7, 5: 8.5, 6: 10, 8: 13, 10: 16}


class Fastener(PassivePart):
    """A bolt / screw / nut / washer / standoff / insert. Carries thread
    size and a datasheet clearance-hole diameter, and can drill it."""

    category = "fastener"

    def clearance_hole(self, part, location: Location):
        """Drill a clearance hole for this fastener's thread into ``part``
        at ``location`` (needs a geometry backend to render the cut)."""
        return part.hole(
            location, radius_or_shape=self.clearance_hole_mm * MM / 2,
            amount=max(self.length_mm, 1) * MM,
        )


def from_common(fastener: CommonFasteners) -> Fastener:
    """Wrap a core :class:`codetocad.CommonFasteners` member as a library
    :class:`Fastener` (so it shows up alongside the rest of the catalog)."""
    thread_mm = fastener.diameter.value * 1000
    length_mm = fastener.length.value * 1000
    part = Fastener(fastener.name.lower())
    core = fastener.build()
    part._primitive = core._primitive
    part._init_library(mass_kg=0.005, color=BODY_STEEL,
                        notes=f"core CommonFasteners.{fastener.name}")
    part.thread_mm = thread_mm
    part.length_mm = length_mm
    part.clearance_hole_mm = _CLEARANCE.get(round(thread_mm, 1), thread_mm * 1.1)
    part.kind = fastener.kind
    return part


def _cyl_mass(dia_mm, length_mm, density=STEEL_DENSITY, fill=1.0):
    r = dia_mm * MM / 2
    return 3.14159 * r * r * (length_mm * MM) * density * fill


# --- bolts / socket-head cap screws: (thread, length) ---
_BOLTS = [
    (2, 6), (2, 10), (2.5, 8), (2.5, 12),
    (3, 6), (3, 8), (3, 10), (3, 12), (3, 16), (3, 20), (3, 25), (3, 30),
    (4, 8), (4, 12), (4, 16), (4, 20), (4, 25),
    (5, 10), (5, 16), (5, 20), (5, 25), (5, 30),
    (6, 16), (6, 20), (6, 25), (6, 30), (6, 40),
    (8, 20), (8, 25), (8, 30), (8, 40),
]
_NUTS = [2, 2.5, 3, 4, 5, 6, 8, 10]
_WASHERS = [2, 3, 4, 5, 6, 8, 10]
# standoffs: (thread, length) brass hex M-F
_STANDOFFS = [(2.5, 10), (3, 6), (3, 10), (3, 15), (3, 20), (3, 25),
              (4, 15), (4, 25)]
# heat-set inserts: (thread, length, od)
_INSERTS = [(2, 4, 3.2), (3, 4, 4.0), (3, 5.7, 4.6), (4, 5.7, 5.6),
            (5, 5.8, 6.4)]
# threaded rod: (thread, length)
_RODS = [(3, 100), (4, 250), (5, 300), (6, 300), (8, 300), (8, 500)]


def _reg_bolt(thread, length):
    slug = f"m{thread:g}x{length:g}_socket_head"
    head_d = _SOCKET_HEAD.get(thread, thread * 1.8)

    def factory(t=thread, l=length, s=slug, hd=head_d):
        f = Fastener(s)
        # A shank cylinder as the body; the head is a fixed cap on top.
        f._build_body(
            cylinder(radius=t * MM / 2, height=l * MM),
            mass_kg=_cyl_mass(t, l) + _cyl_mass(hd, t),
            color=BODY_STEEL,
            part_number=f"M{t:g}x{l:g} SHCS",
            notes=f"M{t:g} x {l:g} mm socket-head cap screw",
        )
        f.thread_mm = t
        f.length_mm = l
        f.head_diameter_mm = hd
        f.drive = "hex socket"
        f.kind = "bolt"
        f.clearance_hole_mm = _CLEARANCE.get(t, t * 1.1)
        return f

    factory.__doc__ = (
        f"M{thread:g} x {length:g} mm socket-head cap screw; "
        f"{head_d:g} mm head, {_CLEARANCE.get(thread, thread * 1.1):g} mm "
        "clearance hole."
    )
    return register(slug, "bolt", factory, part_number=f"M{thread:g}x{length:g} SHCS",
                    summary="socket-head cap screw")


def _reg_nut(thread):
    slug = f"m{thread:g}_nut"
    af = _HEX_AF.get(thread, thread * 1.8)
    height = thread * 0.8

    def factory(t=thread, a=af, h=height, s=slug):
        f = Fastener(s)
        f._build_body(
            cylinder(radius=a * MM / 2 / 0.866, height=h * MM),  # AF -> across corners
            mass_kg=_cyl_mass(a, h, fill=0.6),
            color=BODY_STEEL,
            part_number=f"M{t:g} hex nut",
            notes=f"M{t:g} hex nut, {a:g} mm across flats",
        )
        f.thread_mm = t
        f.length_mm = h
        f.across_flats_mm = a
        f.kind = "nut"
        f.clearance_hole_mm = t
        return f

    factory.__doc__ = f"M{thread:g} hex nut, {af:g} mm across flats."
    return register(slug, "nut", factory, part_number=f"M{thread:g} nut",
                    summary="hex nut")


def _reg_washer(thread):
    slug = f"m{thread:g}_washer"
    od = thread * 2.2

    def factory(t=thread, o=od, s=slug):
        f = Fastener(s)
        f._build_body(
            cylinder(radius=o * MM / 2, height=max(t * 0.2, 0.5) * MM),
            mass_kg=_cyl_mass(o, max(t * 0.2, 0.5), fill=0.7),
            color=BODY_STEEL,
            part_number=f"M{t:g} washer",
            notes=f"M{t:g} flat washer, {o:g} mm OD",
        )
        f.thread_mm = t
        f.length_mm = max(t * 0.2, 0.5)
        f.outer_diameter_mm = o
        f.kind = "washer"
        f.clearance_hole_mm = t * 1.1
        return f

    factory.__doc__ = f"M{thread:g} flat washer, {od:g} mm OD."
    return register(slug, "washer", factory, part_number=f"M{thread:g} washer",
                    summary="flat washer")


def _reg_standoff(thread, length):
    slug = f"m{thread:g}x{length:g}_standoff"
    af = _HEX_AF.get(thread, thread * 1.8)

    def factory(t=thread, l=length, a=af, s=slug):
        f = Fastener(s)
        f._build_body(
            cylinder(radius=a * MM / 2 / 0.866, height=l * MM),
            mass_kg=_cyl_mass(a, l, density=BRASS_DENSITY, fill=0.7),
            color=BODY_BRASS,
            part_number=f"M{t:g}x{l:g} standoff",
            notes=f"M{t:g} x {l:g} mm brass hex standoff (M-F)",
        )
        f.thread_mm = t
        f.length_mm = l
        f.across_flats_mm = a
        f.kind = "standoff"
        f.clearance_hole_mm = t
        return f

    factory.__doc__ = f"M{thread:g} x {length:g} mm brass hex standoff."
    return register(slug, "standoff", factory, part_number=f"M{thread:g}x{length:g}",
                    summary="brass hex standoff")


def _reg_insert(thread, length, od):
    slug = f"m{thread:g}x{length:g}_heatset_insert"

    def factory(t=thread, l=length, o=od, s=slug):
        f = Fastener(s)
        f._build_body(
            cylinder(radius=o * MM / 2, height=l * MM),
            mass_kg=_cyl_mass(o, l, density=BRASS_DENSITY, fill=0.6),
            color=BODY_BRASS,
            part_number=f"M{t:g} insert",
            notes=f"M{t:g} heat-set insert, {o:g} mm OD (for 3D prints)",
        )
        f.thread_mm = t
        f.length_mm = l
        f.outer_diameter_mm = o
        f.kind = "insert"
        f.clearance_hole_mm = o - 0.4  # boss hole slightly under the OD
        return f

    factory.__doc__ = (
        f"M{thread:g} brass heat-set insert, {od:g} mm OD "
        f"(boss hole ~{od - 0.4:g} mm)."
    )
    return register(slug, "insert", factory, part_number=f"M{thread:g} insert",
                    summary="heat-set insert")


def _reg_rod(thread, length):
    slug = f"m{thread:g}x{length:g}_threaded_rod"

    def factory(t=thread, l=length, s=slug):
        f = Fastener(s)
        f._build_body(
            cylinder(radius=t * MM / 2, height=l * MM),
            mass_kg=_cyl_mass(t, l),
            color=BODY_STEEL,
            part_number=f"M{t:g} rod {l:g}mm",
            notes=f"M{t:g} threaded rod, {l:g} mm",
        )
        f.thread_mm = t
        f.length_mm = l
        f.kind = "threaded_rod"
        f.clearance_hole_mm = _CLEARANCE.get(t, t * 1.1)
        return f

    factory.__doc__ = f"M{thread:g} threaded rod, {length:g} mm long."
    return register(slug, "threaded_rod", factory,
                    part_number=f"M{thread:g}x{length:g} rod",
                    summary="threaded rod")


for _t, _l in _BOLTS:
    globals()[f"get_m{_t:g}x{_l:g}_socket_head"] = _reg_bolt(_t, _l)
for _t in _NUTS:
    globals()[f"get_m{_t:g}_nut"] = _reg_nut(_t)
for _t in _WASHERS:
    globals()[f"get_m{_t:g}_washer"] = _reg_washer(_t)
for _t, _l in _STANDOFFS:
    globals()[f"get_m{_t:g}x{_l:g}_standoff"] = _reg_standoff(_t, _l)
for _t, _l, _o in _INSERTS:
    globals()[f"get_m{_t:g}x{_l:g}_heatset_insert"] = _reg_insert(_t, _l, _o)
for _t, _l in _RODS:
    globals()[f"get_m{_t:g}x{_l:g}_threaded_rod"] = _reg_rod(_t, _l)


__all__ = ["Fastener", "from_common", "CommonFasteners"] + [
    n for n in list(globals()) if n.startswith("get_")
]
