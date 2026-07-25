"""Motor drivers and controllers: STEP/DIR stepper drivers, brushed-DC
H-bridges, brushless ESCs, servo drivers and FOC motion controllers -- the
electronics between a microcontroller and the actuators in this library.

Each returns a ``Part3D`` at the real module size, with input voltage /
current rating on ``part.power`` and ``channels`` / ``interface`` /
``drives`` attributes describing what it controls.
"""

from __future__ import annotations

from ._base import (
    BODY_BLACK,
    BODY_RED,
    PCB_GREEN,
    PassivePart,
    PowerSpec,
    register,
)


class MotorDriver(PassivePart):
    category = "driver"


# slug, category, (l,w,h), mass, color, in_voltage, current_A, channels,
# interface, drives, mfr, pn, notes
_ITEMS = [
    # --- stepper drivers (STEP/DIR) ---
    ("a4988", "stepper_driver", (20, 15, 11), 0.003, PCB_GREEN, 35, 2.0, 1,
     "STEP/DIR", "stepper", "Allegro", "A4988", "the classic stepper driver, 1/16"),
    ("drv8825", "stepper_driver", (20, 15, 11), 0.003, PCB_GREEN, 45, 2.2, 1,
     "STEP/DIR", "stepper", "TI", "DRV8825", "stepper driver, 1/32 microstep"),
    ("tmc2209", "stepper_driver", (20, 15, 10), 0.003, PCB_GREEN, 28, 2.0, 1,
     "STEP/DIR + UART", "stepper", "Trinamic", "TMC2209", "silent StealthChop driver, UART"),
    ("tmc2208", "stepper_driver", (20, 15, 10), 0.003, PCB_GREEN, 36, 1.4, 1,
     "STEP/DIR + UART", "stepper", "Trinamic", "TMC2208", "silent stepper driver"),
    ("tmc5160", "stepper_driver", (26, 20, 11), 0.005, PCB_GREEN, 46, 3.0, 1,
     "STEP/DIR + SPI", "stepper", "Trinamic", "TMC5160", "high-current SPI stepper driver"),
    # --- brushed DC H-bridges ---
    ("l298n_module", "h_bridge", (43, 43, 27), 0.030, PCB_GREEN, 46, 2.0, 2,
     "PWM + DIR", "brushed DC", "ST", "L298N", "dual H-bridge module (classic)"),
    ("tb6612fng", "h_bridge", (20, 20, 3), 0.003, PCB_GREEN, 13.5, 1.2, 2,
     "PWM + DIR", "brushed DC", "Toshiba", "TB6612FNG", "efficient dual H-bridge"),
    ("drv8871", "h_bridge", (20, 18, 3), 0.003, PCB_GREEN, 45, 3.6, 1,
     "PWM", "brushed DC", "TI", "DRV8871", "single 3.6 A H-bridge"),
    ("bts7960", "h_bridge", (50, 50, 15), 0.040, PCB_GREEN, 27, 43, 1,
     "PWM + DIR", "brushed DC", "Infineon", "BTS7960", "43 A high-current H-bridge"),
    ("cytron_md13s", "h_bridge", (43, 43, 15), 0.030, PCB_GREEN, 30, 13, 1,
     "PWM + DIR", "brushed DC", "Cytron", "MD13S", "13 A brushed DC driver"),
    # --- brushless ESCs ---
    ("esc_30a_bldc", "esc", (48, 24, 10), 0.028, BODY_BLACK, 16.8, 30, 1,
     "servo PWM / DShot", "BLDC", "Generic", "30A BLHeli", "brushless ESC (drones / RC)"),
    ("esc_4in1_45a", "esc", (38, 38, 8), 0.012, BODY_BLACK, 25.2, 45, 4,
     "DShot600", "BLDC", "Generic", "4-in-1 45A", "4-in-1 FPV ESC stack"),
    ("esc_car_60a", "esc", (55, 32, 25), 0.070, BODY_BLACK, 16.8, 60, 1,
     "servo PWM", "BLDC (sensored)", "Generic", "60A car ESC", "sensored brushless car ESC"),
    # --- servo driver ---
    ("pca9685", "servo_driver", (62, 26, 4), 0.010, PCB_GREEN, 6, 25, 16,
     "I2C", "servos", "NXP", "PCA9685", "16-channel PWM servo driver (I2C)"),
    # --- FOC motion controllers ---
    ("odrive_v36", "motion_controller", (85, 55, 15), 0.070, PCB_GREEN, 56, 60, 2,
     "UART / CAN / STEP-DIR", "BLDC (FOC)", "ODrive", "ODrive v3.6", "dual-axis BLDC FOC controller"),
    ("odrive_s1", "motion_controller", (50, 50, 15), 0.040, PCB_GREEN, 48, 40, 1,
     "CAN / UART", "BLDC (FOC)", "ODrive", "ODrive S1", "single-axis FOC controller"),
    ("moteus_r4", "motion_controller", (46, 53, 14), 0.030, PCB_GREEN, 44, 40, 1,
     "CAN-FD", "BLDC (FOC)", "mjbots", "moteus r4.11", "compact FOC servo controller"),
    ("simplefoc_shield", "motion_controller", (69, 53, 15), 0.035, BODY_RED, 24, 5, 1,
     "PWM (Arduino)", "BLDC / stepper (FOC)", "SimpleFOC", "SimpleFOCShield", "Arduino FOC shield"),
    ("grbl_cnc_shield", "motion_controller", (69, 53, 20), 0.030, BODY_BLACK, 36, 2, 4,
     "STEP/DIR (GRBL)", "steppers", "Protoneer", "CNC Shield v3", "4-axis GRBL stepper shield"),
]


def _make(row):
    (slug, category, dims, mass, color, voltage, current, channels, interface,
     drives, mfr, pn, notes) = row

    def factory():
        part = MotorDriver(slug)
        part.build_box(
            dims[0], dims[1], dims[2], mass_kg=mass, color=color,
            power=PowerSpec(nominal_voltage_v=voltage, current_a=current),
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        part.category = category
        part.channels = channels
        part.interface = interface
        part.drives = drives
        part.max_current_a = current
        return part

    factory.__doc__ = (
        f"{notes}. {channels}-channel, up to {current} A at {voltage} V; "
        f"{interface}; drives {drives}. {mfr} {pn}."
    )
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _ITEMS:
    globals()[f"get_{_row[0]}"] = _make(_row)

__all__ = ["MotorDriver"] + [f"get_{r[0]}" for r in _ITEMS]
