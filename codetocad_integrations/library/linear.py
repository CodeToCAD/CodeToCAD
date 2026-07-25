"""Powered linear actuators: micro Actuonix rods, generic 12 V industrial
tube actuators, and motion-controlled screw actuators. Each returns a
:class:`~._base.LinearActuator` with a rod on a prismatic joint --
``extend()`` / ``retract()`` / ``set_stroke(mm)`` slide it, and a
simulation drives the same joint.

For the passive lead screws, ball screws and capstans that turn a motor's
rotation into travel, see ``codetocad_integrations.library.transmission``.
"""

from __future__ import annotations

from ._base import LinearActuator, PowerSpec, register

# slug, body_dia_mm, body_len_mm (retracted, minus rod), rod_dia, stroke_mm,
# force_N, speed_mm_s, voltage, current_A, mass_kg, driven_by, mfr, pn, summary
_LINEAR = [
    ("actuonix_l12_100", 12, 99, 4, 100, 42, 23, 6, 0.5, 0.028, "brushed DC",
     "Actuonix", "L12-100-100-6-P", "L12 micro linear actuator, 100 mm stroke"),
    ("actuonix_l16_100", 20, 128, 5, 100, 200, 32, 12, 0.65, 0.056, "brushed DC",
     "Actuonix", "L16-100-63-12-P", "L16 linear actuator, 100 mm stroke"),
    ("actuonix_pq12", 15, 46, 4, 20, 45, 15, 6, 0.55, 0.015, "brushed DC",
     "Actuonix", "PQ12-100-6-P", "PQ12 tiny linear servo actuator"),
    ("linear_12v_50mm", 35, 138, 10, 50, 750, 12, 12, 1.2, 0.28, "brushed DC",
     "Generic", "12V-50mm-750N", "industrial tube actuator, 50 mm stroke"),
    ("linear_12v_100mm", 35, 188, 10, 100, 750, 12, 12, 1.2, 0.34, "brushed DC",
     "Generic", "12V-100mm-750N", "industrial tube actuator, 100 mm stroke"),
    ("linear_12v_150mm", 35, 238, 10, 150, 750, 12, 12, 1.2, 0.40, "brushed DC",
     "Generic", "12V-150mm-750N", "industrial tube actuator, 150 mm stroke"),
    ("linear_12v_200mm", 35, 288, 10, 200, 900, 10, 12, 1.5, 0.46, "brushed DC",
     "Generic", "12V-200mm-900N", "heavy industrial tube actuator, 200 mm"),
    ("progressive_pa04", 45, 250, 12, 152, 2200, 8, 12, 5.0, 1.10, "brushed DC",
     "Progressive Automations", "PA-04", "2200 N heavy-duty actuator"),
    ("nema17_t8_actuator", 42, 150, 8, 100, 300, 30, 12, 1.68, 0.35, "stepper",
     "Generic", "NEMA17 + T8", "NEMA 17 with external T8 lead-screw carriage"),
    ("nema23_ballscrew_actuator", 57, 300, 16, 200, 2000, 25, 24, 2.8, 2.5,
     "stepper", "Generic", "NEMA23 + 1605 ballscrew", "ballscrew linear stage"),
]


def _make(row):
    (slug, dia, length, rod_d, stroke, force, speed, voltage, current, mass,
     driven, mfr, pn, summary) = row

    def factory():
        act = LinearActuator(
            slug,
            body_diameter_mm=dia,
            body_length_mm=length,
            rod_diameter_mm=rod_d,
            stroke_mm=stroke,
            mass_kg=mass,
            speed_mm_s=speed,
            driven_by=driven,
            power=PowerSpec(
                nominal_voltage_v=voltage,
                current_a=current,
                rated_torque_nm=None,
            ),
            manufacturer=mfr,
            part_number=pn,
            notes=summary,
        )
        act.rated_force_n = force
        return act

    factory.__doc__ = (
        f"{summary}. {stroke} mm stroke, {force} N push, {speed} mm/s at "
        f"{voltage} V ({current} A), {driven}. {mfr} {pn}."
    )
    return register(
        slug, "linear_actuator", factory,
        manufacturer=mfr, part_number=pn, summary=summary,
    )


for _row in _LINEAR:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = [f"get_{_row[0]}" for _row in _LINEAR]
