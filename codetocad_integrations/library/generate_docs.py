"""Regenerate the catalog documentation under ``docs/``.

Run it after adding or changing parts::

    uv run python -m codetocad_integrations.library.generate_docs

For every family it writes a markdown page with a spec table (grouped by
category) of *all* its parts, plus isometric SVG renderings of a
representative few. Tables and renderings are derived straight from the
registered parts, so the docs never drift from the code.
"""

from __future__ import annotations

from pathlib import Path

from . import catalog, get

DOCS = Path(__file__).parent / "docs"
IMAGES = DOCS / "images"

MM = 1000.0

# Families -> the categories they bundle, the page title, and a lead-in.
FAMILIES: dict[str, dict] = {
    "steppers": {
        "title": "Stepper Motors",
        "categories": ["stepper"],
        "intro": "NEMA-frame stepper motors. Frame size names the NEMA "
        "standard (NEMA 17 == 42 mm square face). Each is a "
        "`StepperMotor` with a hinged output shaft; drive it open-loop "
        "with `move_steps()` / `set_position(deg)`.",
    },
    "servos": {
        "title": "Servos",
        "categories": ["servo"],
        "intro": "Hobby PWM and smart serial (Dynamixel / FeeTech / LX-16A) "
        "servos. `set_angle(deg)` commands position; continuous-rotation "
        "servos take `set_speed(-1..1)`.",
    },
    "brushless": {
        "title": "Brushless (BLDC) Motors",
        "categories": ["bldc"],
        "intro": "Gimbal, drone / FPV, RC, e-skate and hub brushless motors. "
        "No-load speed ~= kv x volts; drive with an ESC or a VESC / ODrive.",
    },
    "dc_gearmotors": {
        "title": "DC Gearmotors",
        "categories": ["dc_gearmotor"],
        "intro": "Brushed DC motors and gearmotors (N20, TT, metal gearboxes, "
        "RC cans). Output rpm / torque are after the gear ratio; drive from "
        "an H-bridge.",
    },
    "linear_actuators": {
        "title": "Linear Actuators",
        "categories": ["linear_actuator"],
        "intro": "Powered linear actuators with a rod on a prismatic joint. "
        "`extend()` / `retract()` / `set_stroke(mm)` drive it.",
    },
    "cameras": {
        "title": "Cameras",
        "categories": ["camera"],
        "intro": "CSI / USB / depth cameras carrying `CameraMixin`.",
    },
    "sensors": {
        "title": "Sensors",
        "categories": [
            "line_sensor", "distance_sensor", "switch", "proximity",
            "imu", "encoder", "current_sensor", "temperature_sensor",
        ],
        "intro": "Line / reflectance, distance, switch & end-stop, proximity, "
        "IMU, encoder, current and temperature sensors. Each carries its "
        "matching sensor mixin and binds to a `Microcontroller` pin.",
    },
    "screws_and_pulleys": {
        "title": "Lead Screws, Ball Screws, Capstans & Pulleys",
        "categories": ["transmission"],
        "intro": "Passive linear-motion transmission. `linear_travel(revs)` "
        "and `travel_per_rev_mm` convert turns to millimetres.",
    },
    "gears": {
        "title": "Gears",
        "categories": ["gear", "bevel_gear", "worm", "rack"],
        "intro": "Spur, helical, bevel, worm and rack gears -- from the "
        "`spur_gear()` / `bevel_gear()` / `worm()` / `gear_rack()` "
        "generators. Blanks at the outer diameter; `ratio_with()` and "
        "`center_distance_to()` give exact meshing math.",
    },
    "couplings_and_bearings": {
        "title": "Universal Joints, Couplings & Bearings",
        "categories": ["universal_joint", "coupling", "bearing"],
        "intro": "Universal joints (which articulate via `bend_joint`), shaft "
        "couplings and bearings -- from `universal_joint()`, "
        "`shaft_coupling()` and `ball_bearing()`.",
    },
    "fasteners": {
        "title": "Fasteners",
        "categories": ["bolt", "nut", "washer", "standoff", "insert",
                       "threaded_rod"],
        "intro": "Metric bolts, nuts, washers, brass standoffs, heat-set "
        "inserts and threaded rod. Complements the core "
        "`codetocad.CommonFasteners` enum (bridged via `from_common`); each "
        "carries a datasheet clearance-hole size and can `clearance_hole()` "
        "a part.",
    },
    "power": {
        "title": "Power",
        "categories": ["battery", "converter", "regulator", "supply",
                       "protection"],
        "intro": "Batteries, DC-DC converters / regulators, bench supplies "
        "and protection. Electrical ratings are on `part.power`.",
    },
    "drivers": {
        "title": "Motor Drivers & Controllers",
        "categories": ["stepper_driver", "h_bridge", "esc", "servo_driver",
                       "motion_controller"],
        "intro": "The electronics between a microcontroller and the "
        "actuators: STEP/DIR stepper drivers, brushed-DC H-bridges, "
        "brushless ESCs, servo drivers and FOC motion controllers.",
    },
    "boards": {
        "title": "Compute Boards",
        "categories": ["microcontroller_board", "sbc"],
        "intro": "Physical microcontroller and single-board-computer "
        "outlines. For the logical pin-binding API use "
        "`codetocad.Microcontroller`.",
    },
    "structure": {
        "title": "Structure & Motion Hardware",
        "categories": ["extrusion", "bracket", "linear_rail", "rod", "plate",
                       "mount"],
        "intro": "Aluminum extrusion, brackets, linear rails, smooth rods "
        "and plates. `extrusion()` and `smooth_rod()` generate any size.",
    },
    "wheels": {
        "title": "Wheels, Casters & Tracks",
        "categories": ["wheel", "omni_wheel", "mecanum_wheel", "caster",
                       "track"],
        "intro": "What a mobile robot rolls on. `distance_per_rev_mm()` gives "
        "the odometry step per wheel revolution.",
    },
    "hmi": {
        "title": "Displays, Indicators & Controls",
        "categories": ["display", "indicator", "audio", "control"],
        "intro": "Human-machine interface parts: OLED/TFT displays, LEDs and "
        "addressable pixels, buzzers/speakers, relays, MOSFET switches and "
        "potentiometers.",
    },
    "end_effectors": {
        "title": "End Effectors & Pneumatics",
        "categories": ["gripper", "gripper_tool", "suction", "valve",
                       "air_cylinder"],
        "intro": "Grippers (with a jaw on a prismatic joint -- `open()` / "
        "`close()`), vacuum / suction, solenoid valves and air cylinders.",
    },
}

# A representative few per family to render (kept small; tables list them all).
RENDER: dict[str, list[str]] = {
    "steppers": ["nema_8", "nema_17", "nema_23", "nema_34"],
    "servos": ["sg90", "mg996r", "ds3218", "dynamixel_ax12a"],
    "brushless": ["gimbal_gm4108", "drone_2205_2300kv", "eskate_6374_170kv"],
    "dc_gearmotors": ["n20_100rpm", "tt_gearmotor", "pololu_37d_50_1"],
    "linear_actuators": ["actuonix_l16_100", "linear_12v_100mm"],
    "cameras": ["rpi_camera_v2", "esp32_cam", "realsense_d435"],
    "sensors": ["hc_sr04", "qtr_8rc", "mpu6050", "omron_e6b2_cwz6c"],
    "screws_and_pulleys": ["leadscrew_t8_8mm", "ballscrew_1605", "capstan_drum_40mm"],
    "gears": ["spur_gear_m2_20t", "bevel_gear_m2_20t", "worm_m2_1start"],
    "couplings_and_bearings": [
        "universal_joint_8mm", "coupling_5x8_jaw", "bearing_608",
    ],
    "fasteners": ["m3x12_socket_head", "m5_nut", "m3x10_standoff"],
    "power": ["lipo_3s_2200", "buck_lm2596", "psu_meanwell_lrs350_24"],
    "drivers": ["a4988", "l298n_module", "odrive_v36"],
    "boards": ["arduino_uno", "rpi_pico", "rpi_4b"],
    "structure": ["extrusion_2020_500mm", "smooth_rod_8mm_500mm"],
    "wheels": ["tt_wheel_65mm", "mecanum_wheel_80mm", "caster_wheel_swivel_50mm"],
    "hmi": ["oled_ssd1306_096", "relay_module_4ch", "potentiometer_10k"],
    "end_effectors": ["parallel_gripper_servo", "air_cylinder_20x100"],
}


def _dims_mm(part) -> tuple[float, float, float]:
    lo, hi = part.get_bounding_box()
    return tuple(round((h - l) * MM, 1) for l, h in zip(lo.to_tuple(), hi.to_tuple()))


def _g(part, attr, default="-"):
    value = getattr(part, attr, None)
    return default if value is None else value


def _power(part, key, default="-"):
    return part.get_power_requirements().get(key, default)


# Per-category table columns: (header, cell(part) -> str).
def _common_size(part):
    l, w, h = _dims_mm(part)
    return f"{l} x {w} x {h}"


def _mass_g(part):
    try:
        return f"{part.get_mass().value * 1000:.1f}"
    except Exception:
        return "-"


_COLUMNS: dict[str, list[tuple[str, callable]]] = {
    "stepper": [
        ("Frame", lambda p: f"{p.frame_mm:g} mm"),
        ("Holding torque", lambda p: f"{_power(p, 'holding_torque_nm')} N*m"),
        ("Current", lambda p: f"{_power(p, 'current_a')} A"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Step", lambda p: f"{p.step_angle_deg:g}deg"),
    ],
    "servo": [
        ("Stall torque", lambda p: f"{_power(p, 'stall_torque_nm')} N*m"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Travel", lambda p: "continuous" if p.continuous else f"{p.rotation_range_deg}deg"),
        ("Bus", lambda p: p.protocol),
    ],
    "bldc": [
        ("kv", lambda p: f"{_power(p, 'kv_rpm_per_v')}"),
        ("Poles", lambda p: f"{p.pole_pairs * 2}"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Max current", lambda p: f"{_power(p, 'current_a')} A"),
        ("Power", lambda p: f"{_power(p, 'power_w')} W"),
    ],
    "dc_gearmotor": [
        ("Gear ratio", lambda p: f"{p.gear_ratio:g}:1"),
        ("No-load", lambda p: f"{_power(p, 'no_load_speed_rpm')} rpm"),
        ("Stall torque", lambda p: f"{_power(p, 'stall_torque_nm')} N*m"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Encoder", lambda p: "yes" if p.has_encoder else "-"),
    ],
    "linear_actuator": [
        ("Stroke", lambda p: f"{p.stroke_mm:g} mm"),
        ("Force", lambda p: f"{getattr(p, 'rated_force_n', '-')} N"),
        ("Speed", lambda p: f"{p.speed_mm_s:g} mm/s"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Driven by", lambda p: p.driven_by),
    ],
    "camera": [
        ("Resolution", lambda p: f"{p.resolution[0]}x{p.resolution[1]}"),
        ("FOV", lambda p: f"{p.field_of_view}"),
        ("Interface", lambda p: getattr(p, "interface", "-")),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "line_sensor": [
        ("Channels", lambda p: f"{p.channels}"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "distance_sensor": [
        ("Range", lambda p: f"{p.min_range_m * 100:g}-{p.max_range_m * 100:g} cm"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "switch": [
        ("Normally", lambda p: "open" if p.normally_open else "closed"),
    ],
    "proximity": [
        ("Range", lambda p: f"{p.detection_range_m * 1000:g} mm"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "imu": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "encoder": [
        ("Counts/rev", lambda p: f"{p.counts_per_revolution}"),
        ("Interface", lambda p: getattr(p, "interface", "-")),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "current_sensor": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "temperature_sensor": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "transmission": [
        ("Travel/rev", lambda p: f"{p.travel_per_rev_mm:g} mm"),
        ("Lead", lambda p: f"{p.lead_mm:g} mm" if p.lead_mm else "-"),
        ("Type", lambda p: getattr(p, "subtype", "-")),
    ],
    "gear": [
        ("Module", lambda p: f"{p.module_mm:g}"),
        ("Teeth", lambda p: f"{p.teeth}"),
        ("Pitch dia", lambda p: f"{p.pitch_diameter_mm:g} mm"),
        ("Outer dia", lambda p: f"{p.outer_diameter_mm:g} mm"),
    ],
    "bevel_gear": [
        ("Module", lambda p: f"{p.module_mm:g}"),
        ("Teeth", lambda p: f"{p.teeth}"),
        ("Pitch angle", lambda p: f"{p.pitch_angle_deg:g}deg"),
    ],
    "worm": [
        ("Module", lambda p: f"{p.module_mm:g}"),
        ("Starts", lambda p: f"{p.starts}"),
        ("Lead", lambda p: f"{p.lead_mm:.2f} mm"),
    ],
    "rack": [
        ("Module", lambda p: f"{p.module_mm:g}"),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
        ("Teeth", lambda p: f"{p.teeth}"),
    ],
    "universal_joint": [
        ("Bore", lambda p: f"{p.bore_mm:g} mm"),
        ("Outer dia", lambda p: f"{p.outer_diameter_mm:g} mm"),
        ("Max bend", lambda p: f"+/-{p.max_angle_deg:g}deg"),
    ],
    "coupling": [
        ("Bore A", lambda p: f"{p.bore_a_mm:g} mm"),
        ("Bore B", lambda p: f"{p.bore_b_mm:g} mm"),
        ("Type", lambda p: p.coupling_type),
    ],
    "bearing": [
        ("Bore", lambda p: f"{p.bore_mm:g} mm"),
        ("Outer dia", lambda p: f"{p.outer_diameter_mm:g} mm"),
        ("Width", lambda p: f"{p.width_mm:g} mm"),
    ],
    # --- fasteners ---
    "bolt": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
        ("Head", lambda p: f"{p.head_diameter_mm:g} mm"),
        ("Drive", lambda p: p.drive),
        ("Clearance", lambda p: f"{p.clearance_hole_mm:g} mm"),
    ],
    "nut": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Across flats", lambda p: f"{p.across_flats_mm:g} mm"),
    ],
    "washer": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Outer dia", lambda p: f"{p.outer_diameter_mm:g} mm"),
    ],
    "standoff": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
        ("Across flats", lambda p: f"{p.across_flats_mm:g} mm"),
    ],
    "insert": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Outer dia", lambda p: f"{p.outer_diameter_mm:g} mm"),
    ],
    "threaded_rod": [
        ("Thread", lambda p: f"M{p.thread_mm:g}"),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
    ],
    # --- power ---
    "battery": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Capacity", lambda p: f"{_g(p, 'capacity_mah')} mAh"),
        ("Chemistry", lambda p: _g(p, "chemistry")),
    ],
    "converter": [
        ("Input", lambda p: _g(p, "input_range")),
        ("Output", lambda p: _g(p, "output_v")),
        ("Current", lambda p: f"{_power(p, 'current_a')} A"),
    ],
    "regulator": [
        ("Input", lambda p: _g(p, "input_range")),
        ("Output", lambda p: _g(p, "output_v")),
    ],
    "supply": [
        ("Output", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Current", lambda p: f"{_power(p, 'current_a')} A"),
        ("Power", lambda p: f"{_power(p, 'power_w')} W"),
    ],
    "protection": [
        ("Rating", lambda p: f"{_power(p, 'current_a')} A"),
    ],
    # --- drivers ---
    **{cat: [
        ("Channels", lambda p: f"{p.channels}"),
        ("Max current", lambda p: f"{p.max_current_a} A"),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
        ("Interface", lambda p: p.interface),
        ("Drives", lambda p: p.drives),
    ] for cat in ("stepper_driver", "h_bridge", "esc", "servo_driver",
                  "motion_controller")},
    # --- boards ---
    **{cat: [
        ("Chip", lambda p: p.chip),
        ("Logic", lambda p: f"{p.logic_voltage} V"),
        ("GPIO", lambda p: f"{p.gpio}"),
        ("Connectivity", lambda p: p.connectivity),
    ] for cat in ("microcontroller_board", "sbc")},
    # --- structure ---
    "extrusion": [
        ("Profile", lambda p: p.profile),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
    ],
    "linear_rail": [
        ("Rail", lambda p: getattr(p, "rail_size", "-")),
        ("Length", lambda p: f"{getattr(p, 'length_mm', 0):g} mm"),
    ],
    "rod": [
        ("Diameter", lambda p: f"{p.diameter_mm:g} mm"),
        ("Length", lambda p: f"{p.length_mm:g} mm"),
    ],
    # --- wheels ---
    **{cat: [
        ("Diameter", lambda p: f"{p.diameter_mm:g} mm"),
        ("Width", lambda p: f"{p.width_mm:g} mm"),
        ("Bore", lambda p: f"{p.bore_mm:g} mm" if p.bore_mm else "-"),
        ("Hub", lambda p: _g(p, "hub")),
    ] for cat in ("wheel", "omni_wheel", "mecanum_wheel", "caster", "track")},
    # --- hmi ---
    "display": [
        ("Resolution", lambda p: f"{p.resolution[0]}x{p.resolution[1]}"),
        ("Interface", lambda p: _g(p, "interface")),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "indicator": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "audio": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "control": [
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    # --- end effectors ---
    "gripper": [
        ("Jaw travel", lambda p: f"{p.jaw_travel_mm:g} mm"),
        ("Grip force", lambda p: f"{_g(p, 'grip_force_n')} N"),
        ("Drive", lambda p: p.drive),
        ("Voltage", lambda p: f"{_power(p, 'nominal_voltage_v')} V"),
    ],
    "air_cylinder": [
        ("Bore", lambda p: f"{getattr(p, 'bore_mm', '-')} mm"),
        ("Stroke", lambda p: f"{p.stroke_mm:g} mm"),
    ],
}


def _category_title(category: str) -> str:
    return category.replace("_", " ").title()


def _table(entries: list) -> str:
    """A markdown table for one category's entries (all share columns)."""
    category = entries[0].category
    extra = _COLUMNS.get(category, [])
    header = ["Factory", "Part", *[h for h, _ in extra], "Size (mm)", "Mass (g)"]
    rows = ["| " + " | ".join(header) + " |",
            "|" + "|".join(["---"] * len(header)) + "|"]
    for entry in sorted(entries, key=lambda e: e.slug):
        part = entry.factory()
        cells = [
            f"`{entry.getter}()`",
            entry.part_number or "-",
            *[str(fn(part)) for _, fn in extra],
            _common_size(part),
            _mass_g(part),
        ]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def _render(slug: str) -> str | None:
    """Render an isometric SVG for ``slug``; return the relative image path."""
    IMAGES.mkdir(parents=True, exist_ok=True)
    part = get(slug)
    out = IMAGES / f"{slug}.svg"
    try:
        part.generate_drawing(str(out), views=("iso",))
    except Exception:
        return None
    return f"images/{out.name}"


def build_docs() -> list[Path]:
    DOCS.mkdir(parents=True, exist_ok=True)
    registry = catalog()
    written: list[Path] = []
    index_rows = ["| Page | Families | Parts |", "|---|---|---|"]

    for family, meta in FAMILIES.items():
        cats = meta["categories"]
        entries_by_cat = {
            cat: [e for e in registry.values() if e.category == cat]
            for cat in cats
        }
        total = sum(len(v) for v in entries_by_cat.values())
        lines = [f"# {meta['title']}", "", meta["intro"], ""]

        # Renderings row.
        shots = [s for s in RENDER.get(family, []) if s in registry]
        if shots:
            lines.append("## Renderings")
            lines.append("")
            for slug in shots:
                path = _render(slug)
                if path:
                    lines.append(f'<img src="{path}" alt="{slug}" width="320">')
            lines.append("")
            lines.append(f"*Isometric projections of `{shots[0]}` and others "
                         "(generated from the parts themselves).*")
            lines.append("")

        # One table per category.
        for cat in cats:
            entries = entries_by_cat[cat]
            if not entries:
                continue
            if len(cats) > 1:
                lines.append(f"## {_category_title(cat)}  ({len(entries)})")
                lines.append("")
            lines.append(_table(entries))
            lines.append("")

        page = DOCS / f"{family}.md"
        page.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        written.append(page)
        index_rows.append(
            f"| [{meta['title']}]({family}.md) | "
            f"{', '.join(_category_title(c) for c in cats)} | {total} |"
        )

    # Index page.
    counts = {}
    for e in registry.values():
        counts[e.category] = counts.get(e.category, 0) + 1
    index = [
        "# Catalog",
        "",
        f"{len(registry)} parts across {len(counts)} categories. Every row's "
        "`get_*()` factory returns a ready-to-use `Part3D`. Regenerate this "
        "folder with `python -m codetocad_integrations.library.generate_docs`.",
        "",
        *index_rows,
        "",
        "See the top-level [README](../README.md) for usage.",
    ]
    index_path = DOCS / "README.md"
    index_path.write_text("\n".join(index) + "\n", encoding="utf-8")
    written.insert(0, index_path)
    return written


if __name__ == "__main__":
    for path in build_docs():
        print("wrote", path)
