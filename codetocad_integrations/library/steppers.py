"""NEMA stepper motors -- the workhorses of 3D printers, CNC and small
robots. Frame size names the NEMA standard (NEMA 17 == 42 mm square face);
each returns a :class:`~._base.StepperMotor` with a hinged output shaft.

Specs (holding torque, rated current per phase, voltage, mass) are nominal
datasheet figures for common StepperOnline (OMC) / LDO / Moons' parts.
"""

from __future__ import annotations

from ._base import PowerSpec, StepperMotor, register

# Each row: slug, frame_mm, body_mm, shaft_dia, shaft_len, holding_torque_Nm,
# current_A, voltage_V, mass_kg, steps, part_number, summary/notes.
_STEPPERS = [
    # --- NEMA 8 (20 mm) ---
    ("nema_8", 20, 30, 4, 12, 0.018, 0.6, 3.8, 0.06, 200,
     "8HS15-0604S", "20 mm micro stepper for tiny mechanisms"),
    ("nema_8_high_torque", 20, 38, 4, 12, 0.030, 0.6, 4.5, 0.08, 200,
     "8HS20-0604S", "long-body 20 mm stepper"),
    # --- NEMA 11 (28 mm) ---
    ("nema_11", 28, 32, 5, 20, 0.043, 0.67, 3.8, 0.12, 200,
     "11HS12-0674S", "28 mm stepper, pen plotters / small gantries"),
    ("nema_11_pancake", 28, 20, 5, 15, 0.020, 0.67, 2.8, 0.08, 200,
     "11HS10-0674S", "thin 28 mm pancake stepper"),
    ("nema_11_long", 28, 45, 5, 20, 0.090, 0.67, 4.5, 0.20, 200,
     "11HS20-0674S", "long 28 mm stepper"),
    ("nema_11_high_torque", 28, 51, 5, 20, 0.140, 1.0, 4.0, 0.24, 200,
     "11HS20-1004S", "high-torque 28 mm stepper"),
    # --- NEMA 14 (35 mm) ---
    ("nema_14", 35, 34, 5, 22, 0.140, 0.8, 3.4, 0.19, 200,
     "14HS13-0804S", "35 mm stepper"),
    ("nema_14_pancake", 35, 26, 5, 20, 0.080, 1.0, 2.7, 0.14, 200,
     "14HS11-1004S", "pancake 35 mm stepper"),
    ("nema_14_high_torque", 35, 52, 5, 22, 0.250, 1.5, 3.2, 0.28, 200,
     "14HS20-1504S", "long high-torque 35 mm stepper"),
    ("nema_14_0_9deg", 35, 34, 5, 22, 0.110, 0.8, 3.5, 0.20, 400,
     "14HM11-0404S", "0.9deg / 400-step 35 mm stepper"),
    # --- NEMA 17 (42 mm) -- the big family ---
    ("nema_17", 42, 40, 5, 24, 0.40, 1.7, 2.4, 0.28, 200,
     "17HS4401", "the default 3D-printer / CNC stepper"),
    ("nema_17_pancake", 42, 20, 5, 20, 0.16, 1.0, 2.8, 0.14, 200,
     "17HS08-1004S", "20 mm pancake NEMA 17 (extruders, deltas)"),
    ("nema_17_slim", 42, 16, 5, 18, 0.09, 1.0, 2.3, 0.11, 200,
     "17HS13-0616S", "ultra-thin 16 mm NEMA 17"),
    ("nema_17_creality", 42, 34, 5, 22, 0.28, 0.8, 3.4, 0.22, 200,
     "42-34 / 17HS15-0804S", "Creality Ender X/Y-axis stepper"),
    ("nema_17_high_torque", 42, 48, 5, 24, 0.59, 2.0, 2.8, 0.40, 200,
     "17HS19-2004S1", "E3D-class 48 mm high-torque NEMA 17"),
    ("nema_17_long", 42, 60, 5, 24, 0.65, 2.1, 3.1, 0.50, 200,
     "17HS24-2104S", "60 mm long-body NEMA 17"),
    ("nema_17_0_9deg", 42, 48, 5, 24, 0.44, 2.0, 2.8, 0.40, 400,
     "17HM19-2004S", "0.9deg / 400-step NEMA 17 (finer resolution)"),
    ("nema_17_ldo", 42, 48, 5, 24, 0.55, 2.5, 2.9, 0.39, 200,
     "LDO-42STH48-2504AC", "LDO high-torque NEMA 17 (Voron favourite)"),
    ("nema_17_moons", 42, 40, 5, 22, 0.44, 1.5, 3.1, 0.30, 200,
     "MS17HD2P4100", "Moons' premium NEMA 17"),
    ("nema_17_dual_shaft", 42, 40, 5, 24, 0.40, 1.7, 2.4, 0.29, 200,
     "17HS4401D", "dual-shaft NEMA 17 (rear encoder / hand-wheel)"),
    ("nema_17_low_current", 42, 34, 5, 22, 0.26, 1.2, 3.0, 0.23, 200,
     "17HS15-1204S", "1.2 A NEMA 17 for small drivers"),
    ("nema_17_planetary_5to1", 42, 74, 8, 24, 1.8, 1.68, 2.8, 0.52, 200,
     "17HS15-1684S-HG5", "NEMA 17 + 5.18:1 planetary gearbox"),
    # --- NEMA 23 (57 mm) ---
    ("nema_23", 57, 56, 6.35, 24, 1.26, 2.8, 3.0, 0.70, 200,
     "23HS22-2804S", "the standard CNC / router NEMA 23"),
    ("nema_23_short", 57, 41, 6.35, 21, 0.70, 2.0, 2.5, 0.55, 200,
     "23HS16-2004S", "short-body NEMA 23"),
    ("nema_23_30", 57, 76, 6.35, 24, 1.90, 2.8, 3.4, 1.10, 200,
     "23HS30-2804S", "76 mm NEMA 23 (higher torque)"),
    ("nema_23_high_torque", 57, 114, 8, 24, 3.00, 4.2, 3.6, 1.90, 200,
     "23HS45-4204S", "114 mm high-torque NEMA 23"),
    ("nema_23_low_inductance", 57, 100, 8, 24, 2.45, 1.8, 6.0, 1.50, 200,
     "23HS41-1804S", "low-inductance NEMA 23 for high-speed drives"),
    ("nema_23_dual_shaft", 57, 56, 6.35, 24, 1.26, 2.8, 3.0, 0.72, 200,
     "23HS22-2804D", "dual-shaft NEMA 23"),
    ("nema_23_geared_10to1", 57, 100, 8, 30, 12.0, 2.8, 3.0, 1.40, 200,
     "23HS22-2804S-PG10", "NEMA 23 + 10:1 planetary gearbox"),
    # --- NEMA 34 (86 mm) ---
    ("nema_34", 86, 78, 14, 37, 4.5, 5.0, 3.5, 2.20, 200,
     "34HS31-5004S", "NEMA 34 for large CNC / plasma tables"),
    ("nema_34_mid", 86, 118, 14, 37, 8.5, 5.0, 4.6, 3.20, 200,
     "34HS46-5064S", "118 mm NEMA 34"),
    ("nema_34_high_torque", 86, 151, 14, 40, 12.0, 5.5, 5.0, 4.20, 200,
     "34HS59-5504S", "151 mm high-torque NEMA 34"),
    ("nema_34_low_current", 86, 98, 14, 37, 6.5, 3.5, 6.4, 2.80, 200,
     "34HS38-3504S", "3.5 A NEMA 34 for smaller drivers"),
    # --- NEMA 42 (110 mm) ---
    ("nema_42", 110, 201, 19, 42, 20.0, 6.0, 4.0, 9.0, 200,
     "110BYGH201", "NEMA 42 for gantry cranes / big machines"),
    ("nema_42_high_torque", 110, 235, 19, 42, 30.0, 6.0, 4.6, 11.5, 200,
     "110HS28-6004S", "235 mm high-torque NEMA 42"),
]


def _make(row):
    (slug, frame, body, shaft_d, shaft_l, torque, current, voltage, mass,
     steps, part_number, summary) = row

    def factory():
        return StepperMotor(
            slug,
            frame_mm=frame,
            body_length_mm=body,
            shaft_diameter_mm=shaft_d,
            shaft_length_mm=shaft_l,
            steps_per_revolution=steps,
            mass_kg=mass,
            power=PowerSpec(
                nominal_voltage_v=voltage,
                current_a=current,
                holding_torque_nm=torque,
            ),
            part_number=part_number,
            manufacturer="StepperOnline",
            notes=summary,
        )

    factory.__doc__ = (
        f"{summary}. {frame} mm frame x {body} mm body, {shaft_d} mm shaft, "
        f"{360 / steps:.2g}deg/step; holding torque {torque} N*m at "
        f"{current} A / {voltage} V. Part {part_number}."
    )
    return register(
        slug, "stepper", factory,
        manufacturer="StepperOnline", part_number=part_number, summary=summary,
    )


for _row in _STEPPERS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = [f"get_{_row[0]}" for _row in _STEPPERS]
