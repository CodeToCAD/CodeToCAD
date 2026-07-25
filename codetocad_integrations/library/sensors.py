"""Common robotics / maker sensors: cameras, line & reflectance sensors,
distance sensors, switches / end stops, rotary encoders, IMUs, and
current / temperature sensors.

Each returns a :class:`codetocad.Part3D` built at datasheet dimensions and
carrying the matching sensor mixin, so it can be bound to a
``Microcontroller`` pin and read like the real thing::

    from codetocad_integrations.library import get_vl53l0x, get_mpu6050
    tof = get_vl53l0x()          # ToF distance sensor Part3D
    imu = get_mpu6050()          # 6-axis IMU Part3D
    mcu.bind_sensor(tof, pin=..., bus=i2c)

Core mixins (``CameraMixin``, ``IMUMixin``, ``EncoderMixin``,
``CurrentSensorMixin``) come from :mod:`codetocad.mixins`; the switch /
distance / line / temperature mixins below are defined here.
"""

from __future__ import annotations

from codetocad import Location, MaterialBase
from codetocad.mixins import (
    CameraMixin,
    CurrentSensorMixin,
    EncoderMixin,
    IMUMixin,
    SensorMixin,
)

from ._base import (
    MM,
    LENS_DARK,
    PCB_GREEN,
    BODY_BLACK,
    BODY_STEEL,
    PassivePart,
    PowerSpec,
    cube,
    cylinder,
    register,
)


# --------------------------------------------------------------------------
# Sensor mixins not already in codetocad.mixins.
# --------------------------------------------------------------------------


class SwitchMixin(SensorMixin):
    """A switch / end stop: reads a boolean. ``normally_open`` describes the
    resting state; ``is_active()`` reports the current logical state."""

    normally_open: bool = True

    def is_active(self) -> bool:
        return bool(self.read())

    is_pressed = is_active
    is_triggered = is_active


class ProximityMixin(SwitchMixin):
    """A non-contact switch (inductive / capacitive / hall / optical) with a
    finite ``detection_range_m``."""

    detection_range_m: float = 0.004


class DistanceSensorMixin(SensorMixin):
    """A ranging sensor. ``read_distance_m()`` returns the latest range,
    clamped to ``[min_range_m, max_range_m]``."""

    min_range_m: float = 0.02
    max_range_m: float = 4.0

    def read_distance_m(self) -> float | None:
        value = self.read()
        return None if value is None else float(value)


class LineSensorMixin(SensorMixin):
    """A reflectance / line-follow sensor with ``channels`` analog outputs
    (1 for a single TCRT5000, 8 for a QTR array). ``read()`` yields the raw
    reflectance value(s)."""

    channels: int = 1


class TemperatureSensorMixin(SensorMixin):
    """A temperature sensor. ``read_temperature_c()`` returns degrees C."""

    def read_temperature_c(self) -> float | None:
        value = self.read()
        return None if value is None else float(value)


# --------------------------------------------------------------------------
# Sensor part classes: a PCB / body plus the mixin.
# --------------------------------------------------------------------------


def _attach_fixed(host, primitive, name, color=LENS_DARK, mass=0.001):
    """Rigidly attach a detail feature (camera lens, ultrasonic eye) to a
    sensor body so it shows up in the exported geometry."""
    primitive.name = name
    primitive.set_material(MaterialBase(name, mass=mass, color_rgba=color))
    top = Location(z=host.get_bounding_box()[1].z)
    host.fixed(top, primitive, Location(z=primitive.get_bounding_box()[0].z))
    return primitive


def _board(cls, name, l, w, h, *, mass, power, mfr, pn, notes, color=PCB_GREEN):
    part = cls(name)
    part._build_body(
        cube(l * MM, w * MM, h * MM),
        mass_kg=mass,
        color=color,
        power=power,
        manufacturer=mfr,
        part_number=pn,
        notes=notes,
    )
    return part


class CameraSensor(PassivePart, CameraMixin):
    category = "camera"


class ImuSensor(PassivePart, IMUMixin):
    category = "imu"


class EncoderSensor(PassivePart, EncoderMixin):
    category = "encoder"


class CurrentSensor(PassivePart, CurrentSensorMixin):
    category = "current_sensor"


class SwitchSensor(PassivePart, SwitchMixin):
    category = "switch"


class ProximitySensor(PassivePart, ProximityMixin):
    category = "proximity"


class DistanceSensor(PassivePart, DistanceSensorMixin):
    category = "distance_sensor"


class LineSensor(PassivePart, LineSensorMixin):
    category = "line_sensor"


class TemperatureSensor(PassivePart, TemperatureSensorMixin):
    category = "temperature_sensor"


# --------------------------------------------------------------------------
# Cameras
# --------------------------------------------------------------------------

# slug, board LxWxH, lens_dia, lens_h, resolution, fov_deg, voltage, current_A,
# interface, mass_kg, mfr, pn, notes
_CAMERAS = [
    ("rpi_camera_v2", 25, 23.86, 9, 7.5, 5.5, (3280, 2464), 62, 3.3, 0.25,
     "MIPI CSI-2", 0.003, "Raspberry Pi", "Camera Module v2 (IMX219)",
     "8 MP CSI camera"),
    ("rpi_camera_v3", 25, 24, 12.4, 7.5, 6, (4608, 2592), 66, 3.3, 0.25,
     "MIPI CSI-2", 0.004, "Raspberry Pi", "Camera Module v3 (IMX708)",
     "12 MP autofocus CSI camera"),
    ("rpi_hq_camera", 38, 38, 18.4, 25, 20, (4056, 3040), 60, 3.3, 0.30,
     "MIPI CSI-2", 0.030, "Raspberry Pi", "HQ Camera (IMX477)",
     "12.3 MP C/CS-mount camera"),
    ("esp32_cam", 27, 40.5, 4.5, 8, 6, (1600, 1200), 65, 5.0, 0.20,
     "WiFi", 0.010, "AI-Thinker", "ESP32-CAM (OV2640)",
     "WiFi camera board (streams JPEG)"),
    ("ov7670", 30, 30, 10, 8, 6, (640, 480), 60, 3.3, 0.10,
     "DVP parallel", 0.006, "OmniVision", "OV7670",
     "cheap VGA parallel camera module"),
    ("arducam_imx219", 25, 24, 9, 7.5, 5.5, (3280, 2464), 62, 3.3, 0.25,
     "MIPI CSI-2", 0.003, "Arducam", "IMX219", "8 MP CSI camera (v2 clone)"),
    ("logitech_c920", 94, 29, 24, 20, 8, (1920, 1080), 78, 5.0, 0.50,
     "USB 2.0", 0.090, "Logitech", "C920", "1080p USB webcam"),
    ("realsense_d435", 90, 25, 25, 0, 0, (1280, 720), 87, 5.0, 0.70,
     "USB 3.0", 0.072, "Intel", "RealSense D435",
     "stereo depth camera (no single lens)"),
    ("oak_d_lite", 91, 28, 17.5, 0, 0, (1920, 1080), 69, 5.0, 0.90,
     "USB 3.0", 0.061, "Luxonis", "OAK-D Lite",
     "depth + on-board AI camera"),
]


def _make_camera(row):
    (slug, l, w, h, lens_d, lens_h, res, fov, v, a, iface, mass, mfr, pn,
     notes) = row

    def factory():
        cam = CameraSensor(slug)
        cam._build_body(
            cube(l * MM, w * MM, h * MM),
            mass_kg=mass, color=PCB_GREEN,
            power=PowerSpec(nominal_voltage_v=v, current_a=a),
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        cam.resolution = res
        cam.field_of_view = f"{fov} deg"
        cam.interface = iface
        if lens_d:
            lens = cylinder(
                radius=lens_d * MM / 2, height=lens_h * MM,
                start_location=Location(z=h * MM / 2 + lens_h * MM / 2),
            )
            _attach_fixed(cam, lens, f"{slug}_lens")
        return cam

    factory.__doc__ = (
        f"{notes}. {l}x{w}x{h} mm, {res[0]}x{res[1]} px, {fov or '--'}deg FOV, "
        f"{iface} at {v} V ({a} A). {mfr} {pn}."
    )
    return register(slug, "camera", factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _CAMERAS:
    globals()[f"get_{_row[0]}"] = _make_camera(_row)


# --------------------------------------------------------------------------
# Simple breakout-style sensors, declared by a compact table each.
# --------------------------------------------------------------------------
# Each entry: (class, category, slug, L, W, H, extra-kwargs dict, power,
#              mfr, pn, notes)

_SIMPLE = [
    # --- line / reflectance ---
    (LineSensor, "line_sensor", "tcrt5000", 10.5, 8, 5, {"channels": 1},
     PowerSpec(nominal_voltage_v=5, current_a=0.02), "Vishay", "TCRT5000",
     "single reflective IR line sensor"),
    (LineSensor, "line_sensor", "qtr_8rc", 76, 9, 3, {"channels": 8},
     PowerSpec(nominal_voltage_v=5, current_a=0.1), "Pololu", "QTR-8RC",
     "8-channel reflectance array (line following)"),
    (LineSensor, "line_sensor", "qtr_1rc", 12, 9, 3, {"channels": 1},
     PowerSpec(nominal_voltage_v=5, current_a=0.02), "Pololu", "QTR-1RC",
     "single-channel reflectance sensor"),
    (SwitchSensor, "switch", "ir_obstacle_fc51", 32, 14, 7, {"normally_open": True},
     PowerSpec(nominal_voltage_v=5, current_a=0.02), "Generic", "FC-51",
     "IR obstacle-avoidance module (digital)"),
    # --- distance ---
    (DistanceSensor, "distance_sensor", "hc_sr04", 45, 20, 15,
     {"min_range_m": 0.02, "max_range_m": 4.0},
     PowerSpec(nominal_voltage_v=5, current_a=0.015), "Generic", "HC-SR04",
     "ultrasonic ranger, 2-400 cm"),
    (DistanceSensor, "distance_sensor", "vl53l0x", 25, 11, 3,
     {"min_range_m": 0.03, "max_range_m": 2.0},
     PowerSpec(nominal_voltage_v=2.8, current_a=0.02), "STMicro", "VL53L0X",
     "laser time-of-flight ranger, up to 2 m"),
    (DistanceSensor, "distance_sensor", "vl53l1x", 25, 11, 3,
     {"min_range_m": 0.04, "max_range_m": 4.0},
     PowerSpec(nominal_voltage_v=2.8, current_a=0.02), "STMicro", "VL53L1X",
     "laser time-of-flight ranger, up to 4 m"),
    (DistanceSensor, "distance_sensor", "sharp_gp2y0a21", 44, 18.9, 13.5,
     {"min_range_m": 0.10, "max_range_m": 0.80},
     PowerSpec(nominal_voltage_v=5, current_a=0.03), "Sharp", "GP2Y0A21YK0F",
     "analog IR distance sensor, 10-80 cm"),
    (DistanceSensor, "distance_sensor", "tf_luna", 35, 21, 16,
     {"min_range_m": 0.20, "max_range_m": 8.0},
     PowerSpec(nominal_voltage_v=5, current_a=0.07), "Benewake", "TF-Luna",
     "single-point LiDAR, up to 8 m"),
    # --- switches / end stops ---
    (SwitchSensor, "switch", "tactile_button", 6, 6, 5, {"normally_open": True},
     PowerSpec(), "Generic", "6x6 tactile", "momentary push button"),
    (SwitchSensor, "switch", "toggle_switch", 13, 8, 23, {"normally_open": True},
     PowerSpec(), "Generic", "MTS-101", "SPDT toggle switch"),
    (SwitchSensor, "switch", "microswitch_limit", 20, 6.4, 10,
     {"normally_open": True}, PowerSpec(), "Omron", "SS-5GL",
     "microswitch / limit switch with lever"),
    (SwitchSensor, "switch", "endstop_mechanical", 33, 16, 12,
     {"normally_open": True}, PowerSpec(nominal_voltage_v=5, current_a=0.001),
     "Makerbot", "mechanical endstop", "3D-printer mechanical endstop PCB"),
    (SwitchSensor, "switch", "endstop_optical", 33, 11, 15,
     {"normally_open": True}, PowerSpec(nominal_voltage_v=5, current_a=0.02),
     "Generic", "optical endstop", "slotted opto-interrupter endstop"),
    (SwitchSensor, "switch", "endstop_hall", 20, 13, 5,
     {"normally_open": True}, PowerSpec(nominal_voltage_v=5, current_a=0.005),
     "Generic", "hall endstop", "contactless hall-effect endstop"),
    (SwitchSensor, "switch", "reed_switch", 14, 2.5, 2.5,
     {"normally_open": True}, PowerSpec(), "Generic", "reed switch",
     "magnetic reed switch (glass ampoule)"),
    (ProximitySensor, "proximity", "inductive_lj12a3", 12, 12, 60,
     {"detection_range_m": 0.004, "normally_open": True},
     PowerSpec(nominal_voltage_v=12, current_a=0.2), "Generic", "LJ12A3-4-Z/BX",
     "M12 inductive proximity switch (metal, 4 mm)"),
    (ProximitySensor, "proximity", "capacitive_ldc1000", 30, 18, 3,
     {"detection_range_m": 0.01, "normally_open": True},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.02), "Generic", "capacitive prox",
     "capacitive proximity sensor breakout"),
    # --- IMUs ---
    (ImuSensor, "imu", "mpu6050", 21, 16, 3, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.004), "InvenSense", "MPU-6050",
     "6-axis accel + gyro (I2C)"),
    (ImuSensor, "imu", "mpu9250", 21, 16, 3, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.004), "InvenSense", "MPU-9250",
     "9-axis accel + gyro + magnetometer"),
    (ImuSensor, "imu", "icm20948", 24, 17, 3, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.003), "InvenSense", "ICM-20948",
     "low-power 9-axis IMU"),
    (ImuSensor, "imu", "bno055", 20, 27, 3, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.012), "Bosch", "BNO055",
     "9-axis IMU with on-chip sensor fusion (quaternions)"),
    # --- current / power ---
    (CurrentSensor, "current_sensor", "ina219", 26, 18, 3,
     {"amps_per_volt": 25.0}, PowerSpec(nominal_voltage_v=3.3, current_a=0.001),
     "TI", "INA219", "I2C high-side current / power monitor"),
    (CurrentSensor, "current_sensor", "ina260", 26, 18, 3,
     {"amps_per_volt": 25.0}, PowerSpec(nominal_voltage_v=3.3, current_a=0.001),
     "TI", "INA260", "I2C current/power monitor, integrated shunt"),
    (CurrentSensor, "current_sensor", "acs712_30a", 31, 13, 13,
     {"amps_per_volt": 15.15, "zero_offset_volts": 2.5},
     PowerSpec(nominal_voltage_v=5, current_a=0.01), "Allegro", "ACS712-30A",
     "hall-effect current sensor, +/-30 A"),
    # --- temperature ---
    (TemperatureSensor, "temperature_sensor", "ds18b20", 4, 4, 40, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.001), "Maxim", "DS18B20",
     "1-Wire digital temperature probe"),
    (TemperatureSensor, "temperature_sensor", "ntc_thermistor_10k", 3, 3, 6, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.0005), "Generic", "NTC 10k",
     "10 k NTC thermistor bead"),
    (TemperatureSensor, "temperature_sensor", "mlx90614", 17, 17, 8, {},
     PowerSpec(nominal_voltage_v=3.3, current_a=0.002), "Melexis", "MLX90614",
     "non-contact IR thermometer (I2C)"),
]


def _make_simple(row):
    cls, category, slug, l, w, h, extra, power, mfr, pn, notes = row

    def factory():
        part = _board(cls, slug, l, w, h, mass=0.01, power=power, mfr=mfr,
                      pn=pn, notes=notes)
        for key, value in extra.items():
            setattr(part, key, value)
        return part

    factory.__doc__ = f"{notes}. {l}x{w}x{h} mm. {mfr} {pn}."
    return register(slug, category, factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _SIMPLE:
    globals()[f"get_{_row[2]}"] = _make_simple(_row)


# --------------------------------------------------------------------------
# Rotary encoders -- some have a shaft you turn; model that shaft.
# --------------------------------------------------------------------------
# slug, body dims (dia or LxW), height, shaft_dia, shaft_len, CPR, voltage,
# interface, mass_kg, round?, mfr, pn, notes

_ENCODERS = [
    ("as5600", 20, 20, 3, 0, 0, 4096, 3.3, "I2C", 0.004, False,
     "AMS", "AS5600", "12-bit magnetic angle sensor (needs a diametric magnet)"),
    ("as5048a", 20, 20, 3, 0, 0, 16384, 3.3, "SPI", 0.004, False,
     "AMS", "AS5048A", "14-bit magnetic angle sensor"),
    ("ky040", 32, 19, 25, 6, 15, 20, 5.0, "quadrature", 0.010, False,
     "Generic", "KY-040", "detented rotary encoder module with push knob"),
    ("optical_wheel_600ppr", 38, 38, 20, 6, 15, 600, 5.0, "quadrature", 0.020,
     True, "Generic", "optical wheel", "slotted optical encoder disk + reader"),
    ("omron_e6b2_cwz6c", 40, 40, 30, 6, 15, 600, 12, "quadrature", 0.100, True,
     "Omron", "E6B2-CWZ6C", "industrial incremental rotary encoder, 600 P/R"),
]


def _make_encoder(row):
    (slug, l, w, h, shaft_d, shaft_l, cpr, v, iface, mass, round_body, mfr, pn,
     notes) = row

    def factory():
        enc = EncoderSensor(slug)
        body = (
            cylinder(radius=l * MM / 2, height=h * MM)
            if round_body
            else cube(l * MM, w * MM, h * MM)
        )
        enc._build_body(
            body, mass_kg=mass, color=BODY_BLACK if round_body else PCB_GREEN,
            power=PowerSpec(nominal_voltage_v=v, current_a=0.02),
            manufacturer=mfr, part_number=pn, notes=notes,
        )
        enc.counts_per_revolution = cpr
        enc.interface = iface
        if shaft_d:
            shaft = cylinder(
                radius=shaft_d * MM / 2, height=shaft_l * MM,
                start_location=Location(z=h * MM / 2 + shaft_l * MM / 2),
            )
            shaft.name = f"{slug}_shaft"
            shaft.set_material(MaterialBase("shaft", mass=0.002,
                                            color_rgba=BODY_STEEL))
            axis = Location(z=h * MM / 2, name=f"{slug}_axis")
            enc.shaft_joint = enc.revolute(axis, shaft, axis)
            enc.shaft = shaft
        return enc

    factory.__doc__ = (
        f"{notes}. {cpr} counts/rev, {iface} at {v} V. {mfr} {pn}."
    )
    return register(slug, "encoder", factory, manufacturer=mfr, part_number=pn,
                    summary=notes)


for _row in _ENCODERS:
    globals()[f"get_{_row[0]}"] = _make_encoder(_row)


__all__ = (
    [f"get_{r[0]}" for r in _CAMERAS]
    + [f"get_{r[2]}" for r in _SIMPLE]
    + [f"get_{r[0]}" for r in _ENCODERS]
    + [
        "SwitchMixin",
        "ProximityMixin",
        "DistanceSensorMixin",
        "LineSensorMixin",
        "TemperatureSensorMixin",
    ]
)
