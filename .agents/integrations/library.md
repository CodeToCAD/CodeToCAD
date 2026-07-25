# Hardware library: ready-made actuators, sensors & mechanical parts

[../../codetocad_integrations/library/](../../codetocad_integrations/library/)
is a catalog of **~430 real-world parts** as `Part3D` objects — motors
(stepper / servo / BLDC / DC gearmotor / linear), sensors, gears, couplings,
bearings, **fasteners, power, motor drivers, compute boards, structure /
extrusion, wheels, HMI and end effectors**. Reach for it before
hand-modeling any hobby / robotics hardware: `get_nema_23()` returns a
fully-specified part in one call.

Pure-core: needs **no extra install** (parts are built from `codetocad`
primitives), so it works with any backend or none.

## The one call

```python
from codetocad_integrations.library import get_nema_23
motor = get_nema_23()          # a Part3D you can assemble/simulate/export
print(motor.describe())         # identity + envelope + power requirements
motor.set_velocity(120)         # it IS its own actuator (StepperMotorMixin)
motor.export("nema23.stl")      # body + shaft, in assembled positions
```

Every part carries four things:

1. **Real geometry** at datasheet mm (a `get_nema_23()` is a 57×57×56 mm can).
2. **A moving element** where the device has one — rotary actuators expose
   `part.shaft` on a `RevoluteJoint` (`part.shaft_joint`); linear actuators
   expose `part.rod` on a `PrismaticJoint` (`part.rod_joint`); universal
   joints expose `part.bend_joint`. That joint is what a `Simulation` drives.
3. **The control mixin** for its type, so `motor.set_velocity()/move_steps()`,
   `servo.set_angle()`, `actuator.extend()` work and it binds to a
   `Microcontroller` pin (see [controls.md](controls.md)).
4. **Power requirements** via `part.power` (a `PowerSpec`) and
   `part.get_power_requirements()` → `{voltage, current, torque, speed, ...}`.

## Discovery (don't guess slugs — look them up)

```python
import codetocad_integrations.library as lib
lib.categories()               # {'stepper': 35, 'servo': 27, 'bldc': 22, ...}
lib.list_parts("stepper")      # ['nema_11', 'nema_17', 'nema_23', ...]
lib.search("gimbal")           # slugs matching name/part#/mfr/summary
lib.get("nema_23")             # == lib.get_nema_23()
lib.catalog()                  # {slug: CatalogEntry} metadata, no instantiation
```

Full spec tables + renderings per family:
[../../codetocad_integrations/library/docs/](../../codetocad_integrations/library/docs/README.md).

## Families and their factories

| Module | Category slugs | Example factories |
|--------|----------------|-------------------|
| `steppers` | `stepper` | `get_nema_8/11/14/17/23/34/42(...)` and variants |
| `servos` | `servo` | `get_sg90`, `get_mg996r`, `get_ds3218`, `get_dynamixel_ax12a` |
| `bldc` | `bldc` | `get_gimbal_gm4108`, `get_drone_2205_2300kv`, `get_odrive_d5065_270kv` |
| `dc_gearmotors` | `dc_gearmotor` | `get_n20_100rpm`, `get_tt_gearmotor`, `get_pololu_37d_50_1` |
| `linear` | `linear_actuator` | `get_actuonix_l16_100`, `get_linear_12v_100mm` |
| `sensors` | `camera`, `line_sensor`, `distance_sensor`, `switch`, `proximity`, `imu`, `encoder`, `current_sensor`, `temperature_sensor` | `get_rpi_camera_v2`, `get_vl53l0x`, `get_hc_sr04`, `get_mpu6050`, `get_as5600`, `get_ina219`, `get_microswitch_limit` |
| `transmission` | `transmission` | `get_leadscrew_t8_8mm`, `get_ballscrew_1605`, `get_capstan_drum_40mm`, `get_gt2_pulley_20t`, `get_gt2_belt_200mm` |
| `gears` | `gear`, `bevel_gear`, `worm`, `rack` | `get_spur_gear_m1_20t`, `get_bevel_gear_m2_20t`, `get_worm_m2_1start` |
| `couplings` | `universal_joint`, `coupling`, `bearing` | `get_universal_joint_8mm`, `get_coupling_5x8_jaw`, `get_bearing_608`, `get_lm8uu` |
| `fasteners` | `bolt`, `nut`, `washer`, `standoff`, `insert`, `threaded_rod` | `get_m3x12_socket_head`, `get_m3_nut`, `get_m3x10_standoff`, `get_m3x5.7_heatset_insert` |
| `power` | `battery`, `converter`, `regulator`, `supply`, `protection` | `get_lipo_3s_2200`, `get_li18650_cell`, `get_buck_lm2596`, `get_psu_meanwell_lrs350_24` |
| `drivers` | `stepper_driver`, `h_bridge`, `esc`, `servo_driver`, `motion_controller` | `get_a4988`, `get_tmc2209`, `get_l298n_module`, `get_esc_30a_bldc`, `get_odrive_v36`, `get_pca9685` |
| `boards` | `microcontroller_board`, `sbc` | `get_arduino_uno`, `get_rpi_pico`, `get_esp32_devkit`, `get_teensy_40`, `get_rpi_4b`, `get_jetson_orin_nano` |
| `structure` | `extrusion`, `bracket`, `linear_rail`, `rod`, `plate`, `mount` | `get_extrusion_2020_500mm`, `get_smooth_rod_8mm_500mm`, `get_linear_rail_mgn12_400mm` |
| `wheels` | `wheel`, `omni_wheel`, `mecanum_wheel`, `caster`, `track` | `get_tt_wheel_65mm`, `get_mecanum_wheel_80mm`, `get_caster_wheel_swivel_50mm` |
| `hmi` | `display`, `indicator`, `audio`, `control` | `get_oled_ssd1306_096`, `get_ws2812b_pixel`, `get_relay_module_4ch`, `get_potentiometer_10k` |
| `end_effectors` | `gripper`, `suction`, `valve`, `air_cylinder` | `get_parallel_gripper_servo`, `get_suction_cup_30mm`, `get_air_cylinder_20x100` |

## Parametric generators (when no preset fits)

```python
from codetocad_integrations.library.gears import spur_gear, bevel_gear, worm, gear_rack
from codetocad_integrations.library.couplings import (
    universal_joint, shaft_coupling, ball_bearing, linear_bearing)
from codetocad_integrations.library.structure import extrusion, smooth_rod

pinion = spur_gear(module_mm=1.0, teeth=20)   # any module/teeth
pinion.ratio_with(spur_gear(1.0, 60))          # 3.0 ; also .center_distance_to()
uj = universal_joint(bore_mm=8)                # articulates via uj.bend_joint
cp = shaft_coupling(5, 8, "jaw")               # rigid/jaw/oldham/helical/setscrew
bg = ball_bearing(bore_mm=8, od_mm=22, width_mm=7)
rail = extrusion(20, 500, width_mm=40)         # a 2040 x 500 mm; smooth_rod(8, 300)
```

## Fasteners bridge (the core enum was NOT moved)

`codetocad.CommonFasteners` stays in core — the Blender / build123d backends
federate it into exact models. The library *builds on* it:
`fasteners.from_common(CommonFasteners.M3_BOLT)` wraps a member as a catalog
`Fastener`, and `get_m3x12_socket_head()` etc. add a bigger set with
head/drive/clearance data. `bolt.clearance_hole(plate, plate.top_center)`
drills the right hole.

## Putting parts together

They are ordinary `Part3D`s, so they assemble and simulate like anything
else — join a screw to a motor shaft, bind a sensor to an MCU pin:

```python
from codetocad import Location, Microcontroller, MicrocontrollerBoard, I2CBus
from codetocad_integrations.library import get_nema_17, get_leadscrew_t8_8mm, get_vl53l0x

motor, screw = get_nema_17(), get_leadscrew_t8_8mm()
motor.fixed(Location(z="20mm"), screw, Location(z=0))   # Z-axis: 8 mm/rev
mcu = Microcontroller(MicrocontrollerBoard.ESP32)
mcu.bind_sensor(get_vl53l0x(), bus=I2CBus(sda=21, scl=22))
```

## Notes for agents

- **Specs are nominal datasheet values** for layout/simulation, not
  certified figures. Geometry is a representative can/PCB + shaft — no bolt
  circles, connectors or cut gear teeth (the core has no arbitrary-polygon
  primitive). Bounding boxes, mass, joint axes and the meshing math are
  correct.
- Torque is stored in **N·m** (servo kgf·cm is converted on the way in).
- Drive a part's joint in a `Simulation` via `sim.get_joint(part.shaft_joint)`
  / `set_joint_velocity(...)`; read encoders/sensors back through the bound
  mixins ([simulation.md](simulation.md), [controls.md](controls.md)).
- Regenerate `docs/` after editing parts:
  `python -m codetocad_integrations.library.generate_docs`.
