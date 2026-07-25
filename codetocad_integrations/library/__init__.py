"""A catalog of real-world actuators, sensors and transmission parts as
CodeToCAD ``Part3D`` objects.

Call a ``get_*`` factory to get a fully-specified part -- real millimetre
dimensions, the right control mixin, a moving shaft / rod where the device
has one, and its power requirements (voltage, current, torque, speed)::

    from codetocad_integrations.library import get_nema_23
    motor = get_nema_23()
    print(motor.describe())
    motor.set_velocity(120)          # drive it (StepperMotorMixin API)
    motor.export("nema23.stl")       # body + shaft, assembled

    from codetocad_integrations.library import get_sg90, get_vl53l0x
    servo = get_sg90();  servo.set_angle(90)
    tof   = get_vl53l0x()

Families:

- :mod:`.steppers`      -- NEMA 8 / 11 / 14 / 17 / 23 / 34 / 42 stepper motors
- :mod:`.servos`        -- hobby PWM + smart serial (Dynamixel/FeeTech/...) servos
- :mod:`.bldc`          -- gimbal, drone, RC, e-skate, hub brushless motors
- :mod:`.dc_gearmotors` -- N20 / TT / metal-gearbox brushed DC gearmotors
- :mod:`.linear`        -- powered linear actuators
- :mod:`.sensors`       -- cameras, line, distance, switch/end-stop, IMU,
                           encoder, current and temperature sensors
- :mod:`.transmission`  -- lead / ball / ACME screws, capstans, timing pulleys
- :mod:`.gears`         -- spur / helical / bevel / worm / rack gears, plus
                           the ``spur_gear()`` / ``bevel_gear()`` / ``worm()``
                           / ``gear_rack()`` generators
- :mod:`.couplings`     -- universal joints, shaft couplings and bearings,
                           plus the ``universal_joint()`` / ``shaft_coupling()``
                           / ``ball_bearing()`` generators
- :mod:`.fasteners`     -- bolts, nuts, washers, standoffs, heat-set inserts,
                           threaded rod (bridges core ``CommonFasteners``)
- :mod:`.power`         -- batteries, DC-DC converters, regulators, PSUs
- :mod:`.drivers`       -- stepper drivers, H-bridges, ESCs, FOC controllers
- :mod:`.boards`        -- microcontroller & single-board-computer outlines
- :mod:`.structure`     -- extrusion, brackets, linear rails, rods, plates
                           (``extrusion()`` / ``smooth_rod()`` generators)
- :mod:`.wheels`        -- wheels, tires, omni / mecanum, casters, tracks
- :mod:`.hmi`           -- displays, LEDs, buzzers, relays, potentiometers
- :mod:`.end_effectors` -- grippers (moving jaws), suction, valves, air
                           cylinders

Discover the catalog without instantiating anything::

    import codetocad_integrations.library as lib
    lib.list_parts(category="stepper")          # -> ["nema_8", "nema_11", ...]
    lib.search("gimbal")                        # -> matching slugs
    lib.get("nema_23")                           # same as lib.get_nema_23()
    lib.categories()                             # counts per category

Specs are nominal manufacturer-datasheet values for planning and
simulation, not certified figures.
"""

from __future__ import annotations

from ._base import (
    CATALOG,
    BLDCMotor,
    CatalogEntry,
    DCGearmotor,
    LibraryPart3D,
    LinearActuator,
    PassivePart,
    PowerSpec,
    ServoMixin,
    ServoMotor,
    StepperMotor,
)
from . import (
    bldc,
    boards,
    couplings,
    dc_gearmotors,
    drivers,
    end_effectors,
    fasteners,
    gears,
    hmi,
    linear,
    power,
    sensors,
    servos,
    steppers,
    structure,
    transmission,
    wheels,
)

_MODULES = (
    steppers, servos, bldc, dc_gearmotors, linear, sensors, transmission,
    gears, couplings, fasteners, power, drivers, boards, structure, wheels,
    hmi, end_effectors,
)


def _install_getters() -> list[str]:
    """Re-export every ``get_*`` factory at the package top level."""
    names: list[str] = []
    for module in _MODULES:
        for name in getattr(module, "__all__", ()):
            if name.startswith("get_"):
                globals()[name] = getattr(module, name)
                names.append(name)
    return names


_GETTER_NAMES = _install_getters()


def list_parts(category: str | None = None) -> list[str]:
    """Slugs of every catalog part, optionally filtered by ``category``
    (e.g. ``"stepper"``, ``"servo"``, ``"camera"``). Sorted."""
    return sorted(
        slug
        for slug, entry in CATALOG.items()
        if category is None or entry.category == category
    )


def categories() -> dict[str, int]:
    """A ``{category: count}`` map over the whole catalog."""
    counts: dict[str, int] = {}
    for entry in CATALOG.values():
        counts[entry.category] = counts.get(entry.category, 0) + 1
    return dict(sorted(counts.items()))


def search(query: str) -> list[str]:
    """Slugs whose name, part number, manufacturer or summary contain
    ``query`` (case-insensitive)."""
    q = query.lower()
    hits = []
    for slug, entry in CATALOG.items():
        haystack = " ".join(
            str(field)
            for field in (
                slug, entry.summary, entry.manufacturer, entry.part_number,
            )
            if field
        ).lower()
        if q in haystack:
            hits.append(slug)
    return sorted(hits)


def get(slug: str) -> LibraryPart3D:
    """Instantiate a catalog part by slug: ``get("nema_23")`` ==
    ``get_nema_23()``. Raises ``KeyError`` with near-matches on a miss."""
    entry = CATALOG.get(slug)
    if entry is None:
        hints = search(slug)[:8]
        raise KeyError(
            f"No catalog part {slug!r}."
            + (f" Did you mean: {', '.join(hints)}?" if hints else "")
        )
    return entry.factory()


def catalog() -> dict[str, CatalogEntry]:
    """The full registry, keyed by slug (metadata only; call
    ``entry.factory()`` to build)."""
    return dict(CATALOG)


__all__ = [
    "PowerSpec",
    "LibraryPart3D",
    "PassivePart",
    "StepperMotor",
    "ServoMotor",
    "ServoMixin",
    "BLDCMotor",
    "DCGearmotor",
    "LinearActuator",
    "CatalogEntry",
    "list_parts",
    "categories",
    "search",
    "get",
    "catalog",
    *_GETTER_NAMES,
]
