# Actuator & Sensor Library

A catalog of **real-world actuators, sensors and transmission parts** as
CodeToCAD `Part3D` objects. Call a `get_*` factory and you get a fully
specified part back — the idea is:

```python
from codetocad_integrations.library import get_nema_23

motor = get_nema_23()          # a Part3D you can drop into an assembly
print(motor.describe())
# nema_23  [stepper]  (StepperOnline 23HS22-2804S)
#   envelope: 57.0 x 57.0 x 56.0 mm
#   power: nominal_voltage_v=3.0, current_a=2.8, holding_torque_nm=1.26
#   note: the standard CNC / router NEMA 23

motor.set_velocity(120)        # drive it (the StepperMotorMixin API)
motor.export("nema23.stl")     # body + shaft, in assembled positions
```

Every part carries four things:

1. **Real geometry** built from primitives at datasheet millimetre
   dimensions — a square NEMA can, a round gimbal can, a servo case, a PCB.
2. **A moving element** where the real device has one: rotary actuators get
   an output **shaft** on a `RevoluteJoint`, linear actuators get a **rod**
   on a `PrismaticJoint`. That joint is what a simulation drives, so the
   shaft actually turns / the rod actually slides.
3. **The motor-control mixin** for its type (`StepperMotorMixin`,
   `BLDCMotorMixin`, `DCMotorMixin`, or the servo mixin) — the part *is* its
   own actuator, so it binds straight to a `Microcontroller` pin.
4. **Power requirements** — voltage, current, torque, speed — on
   `part.power` (a `PowerSpec`) and via `part.get_power_requirements()`.

## Families

| Module            | What                                             | Count |
|-------------------|--------------------------------------------------|-------|
| `steppers`        | NEMA 8/11/14/17/23/34/42 stepper motors          | 35    |
| `servos`          | hobby PWM + smart serial (Dynamixel/FeeTech/…)   | 27    |
| `bldc`            | gimbal, drone, RC, e-skate & hub brushless       | 22    |
| `dc_gearmotors`   | N20 / TT / metal-gearbox brushed DC gearmotors   | 12    |
| `linear`          | powered linear actuators                         | 10    |
| `end_effectors`   | grippers (moving jaws), suction, valves, air cylinders | 12 |
| `sensors`         | cameras, line, distance, switch/end-stop, IMU, encoder, current, temperature | 42 |
| `transmission`    | lead / ball / ACME screws, capstans, pulleys, belts | 18 |
| `gears`           | spur / helical / bevel / worm / rack (+ generators)          | 38 |
| `couplings`       | universal joints, shaft couplings, bearings (+ generators)   | 31 |
| `fasteners`       | bolts, nuts, washers, standoffs, inserts, threaded rod | 65 |
| `power`           | batteries, DC-DC converters, regulators, PSUs, protection | 24 |
| `drivers`         | stepper drivers, H-bridges, ESCs, servo & FOC controllers | 19 |
| `boards`          | microcontroller & single-board-computer outlines  | 21 |
| `structure`       | extrusion, brackets, rails, rods, plates (+ generators) | 28 |
| `wheels`          | wheels, tires, omni / mecanum, casters, tracks    | 12 |
| `hmi`             | displays, LEDs/pixels, buzzers, relays, pots      | 17 |

**~430 parts total.** See [`docs/`](docs/README.md) for per-family spec
tables and renderings (regenerate with
`python -m codetocad_integrations.library.generate_docs`).

### Fasteners note

The **core** `codetocad.CommonFasteners` enum stays where it is — it is part
of the public API and the Blender / build123d backends federate it into
exact models. This library *builds on* it: `fasteners.from_common(...)`
wraps an enum member as a catalog `Fastener`, and the `get_m*` factories add
a much larger set with head/drive/clearance-hole data.

## Parametric generators

Beyond the named presets, some families expose **generators** that build a
part to any spec:

```python
from codetocad_integrations.library.gears import spur_gear, bevel_gear, worm, gear_rack
from codetocad_integrations.library.couplings import (
    universal_joint, shaft_coupling, ball_bearing, linear_bearing,
)

pinion = spur_gear(module_mm=1.0, teeth=20)      # 20 mm pitch dia
wheel  = spur_gear(module_mm=1.0, teeth=60)
pinion.ratio_with(wheel)                          # 3.0
pinion.center_distance_to(wheel)                  # 40.0 mm

uj = universal_joint(bore_mm=8)                   # articulates via uj.bend_joint
cp = shaft_coupling(5, 8, "jaw")                  # 5 mm motor -> 8 mm screw
bg = ball_bearing(bore_mm=8, od_mm=22, width_mm=7)  # a 608
```

## Discovering the catalog

```python
import codetocad_integrations.library as lib

lib.categories()                 # {'stepper': 35, 'servo': 27, ...}
lib.list_parts("stepper")        # ['nema_11', 'nema_17', 'nema_23', ...]
lib.search("gimbal")             # ['gimbal_gm2804', 'gimbal_gm3506', ...]
lib.get("nema_23")               # same as lib.get_nema_23()
```

## Using parts together

Actuators, sensors and transmission parts are ordinary `Part3D`s, so they
join into assemblies and simulate like anything else:

```python
from codetocad import Location
from codetocad_integrations.library import get_nema_17, get_leadscrew_t8_8mm

motor = get_nema_17()
screw = get_leadscrew_t8_8mm()
# couple the screw to the motor shaft; 8 mm of travel per revolution
motor.fixed(Location(z="20mm"), screw, Location(z=0))
print(screw.linear_travel(motor.get_position() / 360))
```

Bind a sensor or actuator to a microcontroller pin exactly as with any
mixin-carrying part (see `../../.agents/integrations/controls.md`):

```python
from codetocad import Microcontroller, MicrocontrollerBoard, I2CBus
from codetocad_integrations.library import get_vl53l0x

mcu = Microcontroller(MicrocontrollerBoard.ESP32)
tof = get_vl53l0x()
mcu.bind_sensor(tof, bus=I2CBus(sda=21, scl=22))
```

## Notes

- Specs (torque, current, voltage, dimensions) are **nominal
  manufacturer-datasheet** values for planning and simulation — not
  certified figures. Check the real datasheet before committing hardware.
- Geometry is representative (a can + a shaft), not a mounting-accurate CAD
  model: bolt circles, connectors and flats are omitted. Bounding boxes,
  mass and joint axes are correct for layout and physics.
- Torque is stored in newton-metres. Servo datasheets quote kgf·cm; the
  factories convert (1 kgf·cm = 0.0981 N·m).
