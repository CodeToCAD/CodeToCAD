"""Brushless DC (BLDC) motors: camera-gimbal motors, drone / FPV motors,
RC outrunners, e-skate / e-bike motors and a hub motor. Each returns a
:class:`~._base.BLDCMotor`; no-load speed is roughly ``kv * volts``.

Drive them with an ESC (servo-PWM / DShot) or a VESC / ODrive for
closed-loop field-oriented control (``codetocad_integrations.vesc``).
``kv`` is rpm per volt, ``pole_pairs`` is magnet pairs (poles / 2).
"""

from __future__ import annotations

from ._base import BLDCMotor, PowerSpec, register

# slug, can_diameter_mm, can_length_mm, shaft_dia, shaft_len, kv, pole_pairs,
# nominal_V, max_current_A, power_W, mass_kg, outrunner, mfr, pn, summary
_BLDC = [
    # --- camera gimbal motors (low kv, high pole count, smooth) ---
    ("gimbal_gbm2804", 34, 25, 4, 14, 100, 7, 12, 0.5, 5, 0.070, True,
     "iPower", "GBM2804-100T", "2804 gimbal motor for small camera gimbals"),
    ("gimbal_gm2804", 35, 30, 5, 14, 90, 7, 12, 0.6, 6, 0.078, True,
     "Feiyu", "GM2804", "2804 gimbal motor"),
    ("gimbal_gm3506", 41, 25, 5, 14, 130, 7, 12, 0.8, 8, 0.095, True,
     "iPower", "GM3506", "3506 gimbal motor (mirrorless gimbals)"),
    ("gimbal_gm4108", 46, 25, 5, 16, 160, 11, 16, 1.2, 15, 0.110, True,
     "iPower", "GM4108H", "4108 gimbal motor"),
    ("gimbal_gm5208", 60, 25, 8, 18, 24, 11, 24, 2.0, 40, 0.180, True,
     "iPower", "GM5208-24T", "5208 gimbal / direct-drive robot joint motor"),
    # --- FPV / drone motors (high kv, outrunners) ---
    ("drone_2205_2300kv", 27.9, 18, 5, 14, 2300, 7, 16, 30, 350, 0.030, True,
     "Generic", "2205-2300KV", "5-inch freestyle FPV motor"),
    ("drone_2207_1750kv", 27.9, 20, 5, 15, 1750, 7, 22, 35, 500, 0.033, True,
     "Generic", "2207-1750KV", "5-inch racing FPV motor"),
    ("drone_2306_1700kv", 27.9, 22, 5, 15, 1700, 7, 22, 38, 550, 0.035, True,
     "Emax", "ECO II 2306", "high-power 5-inch FPV motor"),
    ("drone_emax_rs2205", 27.9, 18, 5, 14, 2300, 7, 16, 28, 320, 0.029, True,
     "Emax", "RS2205", "the classic RaceSpec FPV motor"),
    ("drone_tmotor_f60", 27.9, 20, 5, 15, 1950, 7, 22, 33, 480, 0.034, True,
     "T-Motor", "F60 Pro IV", "premium 5-inch FPV motor"),
    ("drone_mn3110_780kv", 34, 27, 4, 14, 780, 7, 15, 15, 200, 0.086, True,
     "T-Motor", "MN3110", "efficient multirotor motor (larger props)"),
    ("drone_mn5208_340kv", 58, 26, 6, 16, 340, 14, 22, 20, 400, 0.180, True,
     "T-Motor", "MN5208", "aerial-photography multirotor motor"),
    ("drone_u8_135kv", 96, 33, 10, 20, 135, 21, 44, 24, 900, 0.240, True,
     "T-Motor", "U8", "heavy-lift multirotor / big prop motor"),
    # --- RC outrunners ---
    ("rc_a2212_1000kv", 27.9, 27, 3.17, 15, 1000, 7, 11.1, 12, 130, 0.052, True,
     "Generic", "A2212", "the classic hobby outrunner (small planes)"),
    ("rc_sunnysky_x2212", 27.9, 26, 3.17, 15, 980, 7, 11.1, 15, 160, 0.056, True,
     "SunnySky", "X2212", "quality 2212 outrunner"),
    ("rc_turnigy_sk3_3548", 42, 45, 5, 18, 900, 7, 14.8, 40, 570, 0.163, True,
     "Turnigy", "Aerodrive SK3 3548", "mid-size RC outrunner"),
    # --- e-skate / e-bike (sensored FOC-friendly outrunners) ---
    ("eskate_5065_270kv", 50, 65, 8, 22, 270, 7, 36, 40, 1200, 0.430, True,
     "Maytech", "5065-270KV", "e-skateboard belt-drive motor"),
    ("eskate_6354_190kv", 63, 54, 8, 24, 190, 7, 44, 60, 1800, 0.700, True,
     "Flipsky", "6354-190KV", "e-skate / small EV motor"),
    ("eskate_6374_170kv", 63, 74, 10, 24, 170, 7, 44, 80, 2500, 0.900, True,
     "Flipsky", "6374-170KV", "high-power e-skate motor"),
    # --- ODrive robotics motors ---
    ("odrive_d5065_270kv", 50, 65, 8, 22, 270, 7, 24, 40, 1000, 0.420, True,
     "ODrive", "D5065-270KV", "ODrive-matched robotics motor"),
    ("odrive_d6374_150kv", 63, 74, 10, 24, 150, 7, 44, 60, 2000, 0.890, True,
     "ODrive", "D6374-150KV", "high-torque ODrive robotics motor"),
    # --- hub motor ---
    ("hoverboard_hub_6_5in", 165, 55, 12, 30, 16, 15, 36, 8, 250, 2.80, True,
     "Generic", '6.5" hoverboard hub', "direct-drive hub motor (robot wheels)"),
]


def _make(row):
    (slug, dia, length, shaft_d, shaft_l, kv, poles, voltage, max_a, power_w,
     mass, outrunner, mfr, pn, summary) = row
    no_load_rpm = kv * voltage

    def factory():
        return BLDCMotor(
            slug,
            diameter_mm=dia,
            body_length_mm=length,
            shaft_diameter_mm=shaft_d,
            shaft_length_mm=shaft_l,
            mass_kg=mass,
            pole_pairs=poles,
            outrunner=outrunner,
            power=PowerSpec(
                nominal_voltage_v=voltage,
                current_a=max_a,
                power_w=power_w,
                kv_rpm_per_v=kv,
                no_load_speed_rpm=no_load_rpm,
            ),
            manufacturer=mfr,
            part_number=pn,
            notes=summary,
        )

    factory.__doc__ = (
        f"{summary}. {dia}x{length} mm can, {kv} kv ({poles} pole-pairs); "
        f"~{no_load_rpm:.0f} rpm no-load at {voltage} V, up to {max_a} A / "
        f"{power_w} W. {mfr} {pn}."
    )
    return register(
        slug, "bldc", factory, manufacturer=mfr, part_number=pn, summary=summary,
    )


for _row in _BLDC:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = [f"get_{_row[0]}" for _row in _BLDC]
