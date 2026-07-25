"""End effectors and pneumatics: grippers (with moving jaws), vacuum /
suction, air cylinders and solenoid valves.

Grippers are actuators -- a body with a jaw on a prismatic joint, so
``open()`` / ``close()`` / ``set_opening(mm)`` move it and a simulation can
drive ``gripper.jaw_joint``. Air cylinders reuse the
:class:`~._base.LinearActuator` rod. Suction cups and valves are passive
bodies with their ratings.
"""

from __future__ import annotations

from ._base import (
    MM,
    BODY_BLACK,
    BODY_STEEL,
    LinearActuator,
    LibraryPart3D,
    Location,
    MaterialBase,
    PassivePart,
    PowerSpec,
    ServoMixin,
    cube,
    cylinder,
    register,
)


class Gripper(LibraryPart3D, ServoMixin):
    """A gripper: a body with a jaw on a prismatic joint. ``set_opening(mm)``
    / ``open()`` / ``close()`` drive ``self.jaw_joint``."""

    category = "gripper"

    def __init__(
        self, name, *, body_l, body_w, body_h, jaw_travel_mm, mass_kg,
        power, drive="servo", grip_force_n=None, mfr=None, pn=None, notes=None,
    ):
        super().__init__(name)
        self.rotation_range_deg = None
        self.continuous = False
        self.jaw_travel_mm = jaw_travel_mm
        self.drive = drive
        self.grip_force_n = grip_force_n
        from ._base import _set_body
        _set_body(self, cube(body_l * MM, body_w * MM, body_h * MM))
        self._init_library(mass_kg=mass_kg, color=BODY_STEEL, power=power,
                           manufacturer=mfr, part_number=pn, notes=notes)
        # A single representative jaw sliding open along +Z.
        jaw = cylinder(radius=body_w * MM / 4,
                       height=body_h * MM * 0.6,
                       start_location=Location(z=body_h * MM / 2 + body_h * MM * 0.3))
        jaw.name = f"{name}_jaw"
        jaw.set_material(MaterialBase("jaw", mass=mass_kg * 0.2, color_rgba=BODY_BLACK))
        axis = Location(z=body_h * MM / 2, name=f"{name}_jaw_axis")
        self.jaw_joint = self.prismatic(axis, jaw, axis, min_limits=0.0,
                                        max_limits=jaw_travel_mm * MM)
        self.jaw = jaw

    def set_opening(self, millimetres: float):
        target = max(0.0, min(self.jaw_travel_mm, float(millimetres)))
        self._target_opening_mm = target
        return self.write({"opening_mm": target})

    def open(self):
        return self.set_opening(self.jaw_travel_mm)

    def close(self):
        return self.set_opening(0.0)


class EndEffector(PassivePart):
    category = "end_effector"


# --- grippers: slug, body(l,w,h), travel, mass, V, A, force_N, drive, mfr, pn, note
_GRIPPERS = [
    ("micro_gripper_sg90", (55, 22, 60), 25, 0.035, 5.0, 0.5, 5, "SG90 servo",
     "Generic", "micro gripper", "SG90-driven parallel gripper (light picking)"),
    ("parallel_gripper_servo", (75, 35, 70), 35, 0.120, 6.0, 1.5, 20, "servo",
     "Generic", "servo gripper", "metal parallel-jaw servo gripper"),
    ("robotiq_2f85", (114, 96, 152), 85, 0.900, 24.0, 0.5, 235, "brushless",
     "Robotiq", "2F-85", "industrial adaptive 2-finger gripper"),
]

# --- other end effectors: slug, category, shape, dims, mass, color, V, A, extra, mfr, pn, note
_EFFECTORS = [
    ("suction_cup_20mm", "suction", "cyl", (20, 18), 0.006, BODY_BLACK, 0, 0,
     {"cup_diameter_mm": 20}, "Generic", "20mm cup", "vacuum suction cup (bellows)"),
    ("suction_cup_30mm", "suction", "cyl", (30, 22), 0.010, BODY_BLACK, 0, 0,
     {"cup_diameter_mm": 30}, "Generic", "30mm cup", "vacuum suction cup"),
    ("vacuum_pump_12v", "suction", "box", (90, 40, 40), 0.200, BODY_STEEL, 12, 0.6,
     {"flow_lpm": 12, "vacuum_kpa": -75}, "Generic", "12V diaphragm",
     "12 V diaphragm vacuum pump"),
    ("solenoid_valve_pneumatic_12v", "valve", "box", (60, 30, 60), 0.150, BODY_STEEL,
     12, 0.3, {"ports": "5/2", "pressure_bar": 8}, "Generic", "4V210-08",
     "5/2 pneumatic solenoid valve"),
    ("solenoid_valve_water_12v", "valve", "box", (70, 40, 55), 0.120, BODY_BLACK,
     12, 0.5, {"ports": "2/2", "orifice_mm": 12}, "Generic", "1/2\" solenoid",
     "12 V normally-closed water valve"),
    ("electromagnet_25mm", "gripper_tool", "cyl", (25, 22), 0.060, BODY_STEEL,
     12, 0.4, {"holding_force_n": 25}, "Generic", "P25/20", "12 V holding electromagnet"),
]

# --- pneumatic air cylinders (reuse LinearActuator): slug, bore, stroke, mass, note
_AIR_CYLINDERS = [
    ("air_cylinder_16x50", 16, 50, 0.120, "SC/SDA 16 mm bore, 50 mm stroke"),
    ("air_cylinder_20x100", 20, 100, 0.220, "SC 20 mm bore, 100 mm stroke"),
    ("air_cylinder_32x200", 32, 200, 0.600, "SC 32 mm bore, 200 mm stroke"),
]


def _reg_gripper(row):
    slug, body, travel, mass, v, a, force, drive, mfr, pn, note = row

    def factory():
        return Gripper(
            slug, body_l=body[0], body_w=body[1], body_h=body[2],
            jaw_travel_mm=travel, mass_kg=mass,
            power=PowerSpec(nominal_voltage_v=v, current_a=a),
            drive=drive, grip_force_n=force, mfr=mfr, pn=pn, notes=note,
        )

    factory.__doc__ = (
        f"{note}. {travel} mm jaw travel, ~{force} N grip, {drive} at {v} V. "
        f"{mfr} {pn}."
    )
    return register(slug, "gripper", factory, manufacturer=mfr, part_number=pn,
                    summary=note)


def _reg_effector(row):
    slug, category, shape, dims, mass, color, v, a, extra, mfr, pn, note = row

    def factory():
        part = EndEffector(slug)
        power = PowerSpec(nominal_voltage_v=v or None, current_a=a or None)
        if shape == "cyl":
            part.build_cylinder(dims[0], dims[1], mass_kg=mass, color=color,
                                power=power, manufacturer=mfr, part_number=pn,
                                notes=note)
        else:
            part.build_box(dims[0], dims[1], dims[2], mass_kg=mass, color=color,
                           power=power, manufacturer=mfr, part_number=pn, notes=note)
        part.category = category
        for key, value in extra.items():
            setattr(part, key, value)
        return part

    factory.__doc__ = f"{note}. {mfr} {pn}."
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=note)


def _reg_air_cylinder(row):
    slug, bore, stroke, mass, note = row

    def factory():
        act = LinearActuator(
            slug, body_diameter_mm=bore * 1.5, body_length_mm=stroke * 0.6,
            rod_diameter_mm=bore * 0.4, stroke_mm=stroke, mass_kg=mass,
            speed_mm_s=300, driven_by="pneumatic",
            power=PowerSpec(),
            part_number=slug, manufacturer="Generic", notes=note,
        )
        act.category = "air_cylinder"
        act.bore_mm = bore
        return act

    factory.__doc__ = f"{note}. Air-driven; extend()/retract() the rod."
    return register(slug, "air_cylinder", factory, manufacturer="Generic",
                    part_number=slug, summary=note)


for _row in _GRIPPERS:
    globals()[f"get_{_row[0]}"] = _reg_gripper(_row)
for _row in _EFFECTORS:
    globals()[f"get_{_row[0]}"] = _reg_effector(_row)
for _row in _AIR_CYLINDERS:
    globals()[f"get_{_row[0]}"] = _reg_air_cylinder(_row)


__all__ = ["Gripper", "EndEffector"] + [
    n for n in list(globals()) if n.startswith("get_")
]
