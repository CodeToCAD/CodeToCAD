# Core classes (`import codetocad`)

Everything here is importable from the top-level `codetocad` package. These are
the abstract, backend-agnostic building blocks. To get real geometry, model with
a geometry integration (see [integrations/geometry.md](integrations/geometry.md)),
but the *shape of the API* is identical.

## Primitives (functions → `Part3D`/`Part2D`)

```python
import codetocad
body = codetocad.cube("10cm", "10cm", "5cm")       # width, length, height
rod  = codetocad.cylinder(radius="2cm", height="5cm")
ball = codetocad.sphere(radius="3cm")
sk   = codetocad.rectangle("4cm", "2cm")           # Part2D
c    = codetocad.circle(radius="1cm")              # Part2D
t    = codetocad.text("hi", font_size="1cm")       # Part2D
imp  = codetocad.import_file("part.step")
```

All accept `start_location=Location(...)` to place them.

## Part3D — the workhorse

A `Part3D` records operations you can chain:

- **Features:** `extrude`, `revolve`, `loft`, `sweep`, `shell(thickness=...)`,
  `hole(location, radius=, amount=)`, fillet/chamfer edges.
- **Booleans:** union / subtract / intersect another part.
- **Transforms:** translate / rotate / scale (accept unit strings).
- **Material:** `set_material(codetocad.aluminum_material())` — presets:
  `steel_material`, `aluminum_material`, plus `red/green/white_material` and
  `MaterialBase(...)` for custom density/`youngs_modulus`/`poissons_ratio`/color.
- **Queries** (need a geometry backend): `get_volume()`, `get_mass()`,
  `get_bounding_box()`.
- **Locations:** `part.top_center`, `.left_center`, ... (`CubeLocations`), or a
  `@codetocad.location`-decorated method for named custom locations.
- **Export:** `part.export("cup.stl")`.
- **Drawings:** `part.generate_drawing()` → a `Drawing`/`Part2D` third-angle
  sheet (front/top/right/iso, dimensioned); `drawing.export("part.svg")`.

Custom parts: subclass `codetocad.Part3D` and implement `build(self)` with the
API of your choice (Build123D, bpy, ...). See "User-defined parts" in
[../README.md](../README.md).

## Locations

```python
from codetocad import Location
Location(x="2cm", y=0, z="5cm")
Location.from_euler(0, 0, "50cm", x_deg=-90, name="pivot")   # position + orientation
part.top_center.translate(x="2cm")                            # from CubeLocations
```

Floats are meters/radians; strings are parsed. `Location.name` labels a joint.

## Assemblies & joints

Constraints are recorded on the parent part; the child is passed in. The
movable ones return a `Joint` object you can later drive in simulation.

```python
mount.fixed(location, other_part, other_location)
joint = mount.revolute(pivot, rod, pivot, min_limits="-90deg", max_limits="90deg")
joint = mount.prismatic(track, slider, track, min_limits=0, max_limits="10cm")
# also: coincide, parallel, perpendicular, tangent (assembly only, no joint)
```

`Joint` subtypes: `RevoluteJoint`, `PrismaticJoint`, `FixedJoint`. Optional
`starting_angle`/`starting_pos` set the assembled/initial pose. In a simulation,
`sim.get_joint(name_or_part).move_to(...)`/`move_by(...)` drives them.

## Mixins (for custom parts)

Inherit these on a `Part3D` subclass and override the relevant methods:

- **Sensors:** `CameraMixin`, `IMUMixin`, `MicrophoneMixin`, `EncoderMixin`,
  `CurrentSensorMixin`.
- **Actuators:** `DCMotorMixin`, `BLDCMotorMixin`, `StepperMotorMixin`
  (set class attrs like `no_load_speed_rpm`).
- **ECAD:** `ECADMixin` / `ElectricalComponent` (voltage/current limits,
  resistance, capacitance, a `Footprint`).

Mixins are what let a part double as a sensor/actuator bound to a
`Microcontroller` pin — see [integrations/controls.md](integrations/controls.md).

## ECAD components & circuits

Component factories (each a `Part3D` with pins + `Footprint`): `led`, `diode`,
`resistor`, `capacitor`, `inductor`, `voltage_source`, `current_source`.

```python
from codetocad import Circuit, resistor, voltage_source
circuit = Circuit("divider")
v1 = circuit.add(voltage_source(dc=9))
r1, r2 = circuit.add(resistor("10k"), resistor("20k"))
circuit.connect(v1["+"], r1[1], name="VIN")
circuit.connect(r1[2], r2[1], name="VOUT")
circuit.connect(r2[2], v1["-"], circuit.gnd)
```

Federate the `Circuit` with skidl / spice — see [integrations/ecad.md](integrations/ecad.md).

## Fasteners

`CommonFasteners` is an enum; each member can `build()` its `Part3D` or apply
its features (e.g. clearance holes) to another part.

## Microcontroller & communication

`Microcontroller` (with `MicrocontrollerBoard`) binds sensor/actuator parts to
pins and talks over a `Communication` (`SerialCommunication`,
`MqttCommunication`, `WifiCommunication`, `BluetoothCommunication`, or
`EmulatedCommunication`). Buses: `I2CBus`, `SPIBus`, `UARTBus`. Signal filters:
`LowPassFilter`, `MovingAverageFilter`, `MedianFilter` (`apply_filter`).
`EmulatedMicrocontroller` runs firmware logic in-process to drive a simulation.
Details in [integrations/controls.md](integrations/controls.md).

## Apps (control panels)

`WebApp`, `PythonApp`, `RerunApp` (all `AppBase`) render sliders/buttons/gauges/
plots bound to a `Communication`. Backed by the nicegui/rerun integrations.
