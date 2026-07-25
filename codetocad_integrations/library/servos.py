"""Hobby and robotics servos. PWM servos take a 1-2 ms RC pulse; smart
serial servos (Dynamixel, FeeTech, LX-16A, HerkuleX) take a bus packet --
either way each returns a :class:`~._base.ServoMotor` whose output spline
is a hinged shaft driven by ``set_angle()`` (or ``set_speed()`` for the
continuous-rotation ones).

Torque figures are stall torque at the quoted voltage, converted to N*m
(1 kgf*cm = 0.0980665 N*m).
"""

from __future__ import annotations

from ._base import PowerSpec, ServoMotor, register

KGFCM = 0.0980665  # kgf*cm -> N*m

# slug, case LxWxH mm, shaft_dia, shaft_len, stall_torque_kgfcm, voltage,
# current_A, mass_kg, range_deg, continuous, protocol, mfr, part_number, summary
_SERVOS = [
    # --- micro / mini PWM servos ---
    ("sg90", 23, 12.2, 29, 4.6, 6, 1.6, 0.25, 0.009, 180, False, "pwm",
     "TowerPro", "SG90", "9 g micro servo -- the ubiquitous blue one"),
    ("mg90s", 23, 12.2, 29, 4.6, 6, 2.2, 0.7, 0.013, 180, False, "pwm",
     "TowerPro", "MG90S", "9 g metal-gear micro servo"),
    ("sg92r", 23, 12.2, 30, 4.6, 6, 2.5, 0.7, 0.009, 180, False, "pwm",
     "TowerPro", "SG92R", "carbon-gear micro servo"),
    ("fs90r", 23, 12.2, 29, 4.6, 6, 1.5, 0.5, 0.009, None, True, "pwm",
     "FeeTech", "FS90R", "continuous-rotation micro servo (small wheels)"),
    ("es08ma", 25, 13, 30, 4.6, 6, 1.8, 0.6, 0.012, 180, False, "pwm",
     "Emax", "ES08MA", "metal-gear mini servo"),
    # --- standard PWM servos ---
    ("mg996r", 40.7, 19.7, 42.9, 5.5, 6, 11, 1.4, 0.055, 180, False, "pwm",
     "TowerPro", "MG996R", "the classic standard metal-gear servo"),
    ("mg995", 40.7, 19.7, 42.9, 5.5, 6, 10, 1.2, 0.055, 180, False, "pwm",
     "TowerPro", "MG995", "standard metal-gear servo"),
    ("hitec_hs311", 40, 20, 36.5, 5.5, 6, 3.7, 0.8, 0.043, 180, False, "pwm",
     "Hitec", "HS-311", "standard nylon-gear servo"),
    ("hitec_hs422", 40, 20, 37, 5.5, 6, 4.1, 0.9, 0.046, 180, False, "pwm",
     "Hitec", "HS-422", "standard servo, deluxe bearings"),
    ("hitec_hs645mg", 40.6, 19.8, 37.6, 6, 7.4, 9.6, 1.5, 0.055, 180, False,
     "pwm", "Hitec", "HS-645MG", "high-torque metal-gear standard servo"),
    ("futaba_s3003", 40, 20, 36, 5.5, 6, 3.2, 0.8, 0.037, 180, False, "pwm",
     "Futaba", "S3003", "standard servo (RC classic)"),
    ("powerhd_1501mg", 40.8, 20.2, 38, 5.8, 6, 15.5, 1.6, 0.060, 180, False,
     "pwm", "PowerHD", "HD-1501MG", "high-torque standard servo"),
    ("jx_pdi6221mg", 40.5, 20.2, 38, 5.5, 6, 20, 1.8, 0.062, 180, False, "pwm",
     "JX", "PDI-6221MG", "20 kg standard servo"),
    ("savox_sc1258tg", 40.3, 20.2, 36, 12, 6, 12, 1.5, 0.052, 180, False, "pwm",
     "Savox", "SC-1258TG", "thin-wing titanium-gear servo"),
    # --- high-torque digital PWM servos ---
    ("ds3218", 40, 20, 40.5, 20, 6.8, 21.5, 2.5, 0.060, 270, False, "pwm",
     "DSServo", "DS3218", "20 kg waterproof digital servo (robot arms)"),
    ("ds3225", 40, 20, 40.7, 25, 6.8, 25, 2.5, 0.062, 270, False, "pwm",
     "DSServo", "DS3225", "25 kg waterproof digital servo"),
    ("ds3235", 40, 20, 40.7, 35, 6.8, 35, 3.0, 0.065, 270, False, "pwm",
     "DSServo", "DS3235", "35 kg high-torque digital servo"),
    ("miuzei_ms24", 40, 20, 40, 24, 6.6, 24, 2.5, 0.060, 270, False, "pwm",
     "Miuzei", "MS24", "24 kg digital servo"),
    # --- FeeTech smart serial servos (bus) ---
    ("feetech_sts3215", 45.2, 24.7, 35, 19.5, 12, 30, 1.5, 0.060, 360, False,
     "serial", "FeeTech", "STS3215", "12 V magnetic-encoder bus servo (SO-ARM100)"),
    ("feetech_scs15", 40, 20, 38, 15, 7.4, 17, 1.5, 0.060, 300, False,
     "serial", "FeeTech", "SCS15", "TTL bus servo with feedback"),
    # --- Dynamixel smart servos ---
    ("dynamixel_ax12a", 32, 50, 40, 15.3, 12, 15, 0.9, 0.0535, 300, False,
     "serial", "Robotis", "AX-12A", "the classic TTL Dynamixel"),
    ("dynamixel_xl320", 24, 36, 27, 3.9, 7.4, 6, 0.4, 0.0166, 300, False,
     "serial", "Robotis", "XL-320", "tiny TTL Dynamixel (Ollo / small bots)"),
    ("dynamixel_xl430_w250", 28.5, 46.5, 34, 14, 11.1, 12, 1.4, 0.057, 360,
     False, "serial", "Robotis", "XL430-W250", "TurtleBot3 wheel servo, 4096-tick encoder"),
    ("dynamixel_mx28", 35.6, 50.6, 35.5, 25, 12, 14, 1.4, 0.077, 360, False,
     "serial", "Robotis", "MX-28", "RS-485/TTL Dynamixel, 12-bit encoder"),
    ("dynamixel_xm430_w350", 28.5, 46.5, 34, 47, 12, 24, 1.7, 0.082, 360,
     False, "serial", "Robotis", "XM430-W350", "high-torque X-series Dynamixel"),
    # --- other serial bus servos ---
    ("lx16a", 45.2, 24.6, 35, 17, 7.4, 20, 1.5, 0.060, 240, False, "serial",
     "LewanSoul", "LX-16A", "cheap TTL bus servo with position feedback"),
    ("herkulex_drs0101", 46, 24, 31, 12, 7.4, 12, 1.2, 0.060, 320, False,
     "serial", "Dongbu", "HerkuleX DRS-0101", "RS-485 smart servo"),
]


def _make(row):
    (slug, cl, cw, ch, shaft_d, torque_kgfcm, voltage, current, mass,
     range_deg, continuous, protocol, mfr, part_number, summary) = row
    stall_nm = torque_kgfcm * KGFCM

    def factory():
        return ServoMotor(
            slug,
            case_l_mm=cl,
            case_w_mm=cw,
            case_h_mm=ch,
            shaft_diameter_mm=shaft_d,
            shaft_length_mm=6,
            mass_kg=mass,
            power=PowerSpec(
                nominal_voltage_v=voltage,
                current_a=current,
                stall_torque_nm=round(stall_nm, 3),
            ),
            rotation_range_deg=range_deg,
            continuous=continuous,
            protocol=protocol,
            manufacturer=mfr,
            part_number=part_number,
            notes=summary,
        )

    kind = "continuous-rotation" if continuous else f"{range_deg}deg"
    factory.__doc__ = (
        f"{summary}. {cl}x{cw}x{ch} mm case, {kind} {protocol.upper()} servo; "
        f"stall torque {torque_kgfcm} kgf*cm ({stall_nm:.2f} N*m) at "
        f"{voltage} V. {mfr} {part_number}."
    )
    return register(
        slug, "servo", factory,
        manufacturer=mfr, part_number=part_number, summary=summary,
    )


for _row in _SERVOS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = [f"get_{_row[0]}" for _row in _SERVOS]
