"""Brushed DC motors and gearmotors: N20 micro gearmotors, TT (yellow)
gearboxes, metal 25GA / 37D gearmotors, and bare RC-can motors. Each
returns a :class:`~._base.DCGearmotor` with a hinged output shaft; drive it
from an H-bridge (L298N / TB6612 / DRV8871). Add an encoder from
``codetocad_integrations.library.sensors`` for closed loop.

``no_load_speed_rpm`` and ``stall_torque_nm`` are the *output* figures
after the ``gear_ratio``.
"""

from __future__ import annotations

from ._base import DCGearmotor, PowerSpec, register

KGFCM = 0.0980665

# slug, body_dia_mm, body_len_mm (incl gearbox), shaft_dia, shaft_len,
# gear_ratio, no_load_rpm, stall_torque_kgfcm, voltage, stall_current_A,
# mass_kg, shape, has_encoder, mfr, pn, summary
_DC = [
    ("n20_100rpm", 12, 34, 3, 10, 100, 100, 2.2, 6, 1.1, 0.010, "box", False,
     "Generic", "N20-100", "6 V N20 micro gearmotor (small robots)"),
    ("n20_200rpm", 12, 30, 3, 10, 50, 200, 1.2, 6, 1.1, 0.010, "box", False,
     "Generic", "N20-200", "faster N20 micro gearmotor"),
    ("n20_encoder_100rpm", 12, 43, 3, 10, 100, 100, 2.2, 6, 1.1, 0.013, "box",
     True, "Generic", "N20-100-Enc", "N20 gearmotor with magnetic encoder"),
    ("tt_gearmotor", 22.6, 37, 5.5, 10, 48, 200, 0.8, 6, 1.0, 0.030, "box",
     False, "Generic", "TT / BO-1", "the yellow twin-shaft hobby gearmotor"),
    ("25ga_370_130rpm", 25, 68, 4, 11, 34, 130, 3.5, 12, 1.5, 0.096, "box",
     False, "Generic", "25GA-370", "25 mm metal gearmotor"),
    ("pololu_25d_hp_75_1", 25, 71, 4, 12.5, 75, 130, 5.1, 12, 3.3, 0.108, "box",
     True, "Pololu", "25D-HP 75:1", "25D metal gearmotor + encoder"),
    ("pololu_37d_50_1", 37, 70, 6, 12.5, 50, 200, 11, 12, 5.5, 0.215, "box",
     True, "Pololu", "37Dx70L 50:1", "37D metal gearmotor + 64 CPR encoder"),
    ("pololu_micro_hp_100_1", 12, 26, 3, 9, 100, 120, 2.4, 6, 1.6, 0.0095,
     "box", False, "Pololu", "micro metal HP 100:1", "high-power micro metal gearmotor"),
    ("jgb37_520_178rpm", 37, 74, 6, 14, 56, 178, 15, 12, 3.2, 0.210, "box",
     True, "Generic", "JGB37-520", "37 mm worm-ready gearmotor + encoder"),
    ("rs775_12v", 42, 66, 5, 20, 1, 18000, 0.6, 12, 30, 0.320, "round", False,
     "Mabuchi", "RS-775", "high-speed brushed can motor (power tools)"),
    ("rs540_12v", 36, 57, 3.17, 12, 1, 15000, 0.3, 7.2, 25, 0.180, "round",
     False, "Mabuchi", "RS-540", "RC brushed can motor"),
    ("my1016_250w", 82, 98, 11, 20, 9.78, 2650, 60, 24, 13.4, 2.30, "round",
     False, "Generic", "MY1016", "250 W scooter / e-bike brushed motor"),
]


def _make(row):
    (slug, dia, length, shaft_d, shaft_l, ratio, rpm, torque_kgfcm, voltage,
     stall_a, mass, shape, has_enc, mfr, pn, summary) = row
    stall_nm = torque_kgfcm * KGFCM

    def factory():
        return DCGearmotor(
            slug,
            diameter_mm=dia,
            body_length_mm=length,
            shaft_diameter_mm=shaft_d,
            shaft_length_mm=shaft_l,
            mass_kg=mass,
            gear_ratio=ratio,
            has_encoder=has_enc,
            gearbox_shape=shape,
            power=PowerSpec(
                nominal_voltage_v=voltage,
                current_a=round(stall_a / 4, 2),
                peak_current_a=stall_a,
                no_load_speed_rpm=rpm,
                stall_torque_nm=round(stall_nm, 3),
            ),
            manufacturer=mfr,
            part_number=pn,
            notes=summary,
        )

    factory.__doc__ = (
        f"{summary}. {dia}x{length} mm, {ratio}:1 gearbox -> {rpm} rpm no-load, "
        f"stall torque {torque_kgfcm} kgf*cm ({stall_nm:.2f} N*m) at {voltage} V "
        f"(stall {stall_a} A). {mfr} {pn}."
        + ("  Includes a quadrature encoder." if has_enc else "")
    )
    return register(
        slug, "dc_gearmotor", factory,
        manufacturer=mfr, part_number=pn, summary=summary,
    )


for _row in _DC:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = [f"get_{_row[0]}" for _row in _DC]
