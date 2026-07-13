# What is CodeToCAD

CodeToCAD is a tool that accelerates mechanical and electrical CAD design, simulations and/or FEA analysis, controls software and MCU firmware by offering:
1. A cli interface to init a project, then interactively design parts.
1. A set of classes that define geometric topography such as a vertex, edge, face, or solid. These are used to interact with native topology in the federated application.
1. A set of classes to define Part2D, Part3D, Assembly2D, Assembly3D
1. Methods to generate primitive shapes in Part3D or Part 2D such as cubes, cylinders, circles, rectangles, e.g. `def cube(width,length,height) -> Part3D
1. Methods to generate common electrical components such as LEDs, resistors, capacitors that uses the ECAD Components mixin.
1. A mixin for each of sensors Camera, IMU, Microphone that a custom Part3D class can inherit and override the relevant methods
1. A mixin for actuators DC motor, BLDC motor  that a custom Part3D class can inherit and override the relevant methods
1. A mixin for ECAD components and electrical properties such as voltage, current limits, capacitance, resistance, etc.. that can be used in a custom Part3D class can inherit and override the relevant methods
1. An enum for common fasteners that can be used to build() their Part3D or apply their features in the federated application
The intent is that the user has one language to define their design, and when you run codetocad, their script is federated to the modeling or design application automatically.

## CLI interface

The CLI interface is the flagship product of CodeToCAD.

Install it with `pip install codetocad`.

Start a project with `codetocad init cup`, which will create a cup folder with a `cup.py` file.

The cli then displays an interactive menu:
```
You've started the project cup!

Selected Geometry: None

What do you want to do?
1. Part
2. Sketch
3. Select geometry
4. Export selected geometry

Enter a command using the numbers: 1
```

```
On project cup.

Selected Geometry: None

What do you want to do?
1. Create a part
2. Define a location on selected part  (greyed out since no selected geometry)
3. Transform selected part (greyed out since no selected geometry)
4. Boolean selected part (greyed out since no selected geometry)
5. Shell selected part  (greyed out since no selected geometry)
6. Add a constraint with another part  (greyed out since no selected geometry)

Enter a command using the numbers: 1
```

```
You are creating a new part.

Enter name, description? Leave blank for none. cup_cylinder
```

```
You are creating a part "cup_cylinder".

What do you want to create?
1. Blank Part (creates a blank part.py)
2. Import STL or other file
3. Cube
4. Cylinder
... other primitives.

Enter a command using the numbers: 4
```

```
You are creating a part "cup_cylinder".

Enter radius, height of the cylinder: 2cm, 5cm
```

```
On project cup.

Selected Geometry: cup_clinder

What do you want to do?
1. Part
2. Sketch
3. Select geometry
4. Export selected geometry

Enter a command using the numbers: 1
```

```
On project cup.

Selected Geometry: cup_clinder

What do you want to do?
1. Create a part
2. Define a location on selected part 
3. Transform selected part
4. Boolean selected part
5. Shell selected part 
6. Add a constraint with another part 

Enter a command using the numbers: 5
```


```
On project cup.

Enter a shell thickness: 5mm
```

All this will be updating a cup_cylinder.py part, and the cli will extend to all the functionality of the classes to allow the user the full functionality of CodeToCAD through the CLI.

## Units

You can enter floats, which will be interpreted as meters or radians, or standard SI unit.
You can enter strings, such as "2in", which will be converted to meters or "10 deg", which will be converted to radians.
You can enter expressions, such as "2in - 5mm", which will be evaluated and converted to meters. Same for angles.
All will be converted to an instance of SomeUnit, so you could also do "2mm" + SomeUnit or SomeUnit * 0.5, and it will be evaluated correctly. If an expression cannot be evaluated, you will get a ValueError.
The transient datatype between float or strings to SomeUnit will be denoted with a "WithUnit" suffix, such as LengthWithUnit or AngleWithUnit.

```
class SomeUnit:
    def __init__(value:float):
        self.value = value

    def __add__(self, other):...
    def __sub__(self, other):...
    def __mul__(self, other):...
    def __div__(self, other):...

class LengthMeters(SomeUnit):
    def __init__(value:str|float|LengthMeters):
        super(self.value_to_meters(value))
    
    @static_method
    def value_to_meters(value):
        return ...

LengthWithUnit:TypeDef = str|float|LengthMeters

class AngleRadians(SomeUnit):
    def __init__(value:str|float|AngleRadians):
        super(self.value_to_radians(value))
    
    @static_method
    def value_to_radians(value):
        return ...

AngleWithUnit:TypeDef = str|float|AngleRadians
```

## Locations

Locations are 6-dof translational position and rotational orientation that are used to query geometry (find edges or faces), transform solids, select the location of assembly operations, among other functions that require pointing out a location in 2D or 3D space.
You can construct them by using the string expression, float or SomeUnit values as discussed in the Units section above.
CubeLocations are shortcuts to the 23 topological locations and geometric centers of a cube. They can be used to quickly navigate any shape.
The Location class can be used as a decorator `@Location` on an Assembly or Part2D class

```
class CubeLocations(Enum):
    TOP_CENTER = auto()
    ... the 8 corners, 6 face centers, 8 midlines and geometric center


    def to_location(self, part:AssemblyCommon):
        return Location() # calculate based on part dimensions
```

```
@dataclass
class Location
    x:LengthWithUnit = 0
    y:LengthWithUnit = 0
    z:LengthWithUnit = 0
    quat_x:AngleWithUnit = 0
    quat_y:AngleWithUnit = 0
    quat_z:AngleWithUnit = 0
    quat_w:AngleWithUnit = 1
    inverted:bool = False
    """If inverted is true, the unit normal will point in the negative direction."""
    snap_to_geometry = False
    """If snap_to_geometry is true, the Location will be evaluated to the closest euclidean location on the geometry."""
    name:str|None = None
    """A descriptive name of this location"""

    @classmethod
    def from_euler(cls, x,y,z,x_deg,y_deg,z_deg, inverted:bool=False, snap_to_geometry:bool=False):
        quat = euler_to_quat(x_deg,y_deg,z_deg,inverted, snap_to_geometry)
        return cls(x, y, z, *quat)

    def rotate(self, x_deg, y_deg, z_deg): ...
    def translate(self, x_deg, y_deg, z_deg): ...

```

```
class LocationMixin:

    def __init__():
        self.loc = BoxLocations # quick access to box locations

    def get_locations(self) -> list[Locations]:
        """Retrieves user-defined locations in the Part class marked with the @location decorator"""
```

## Ledgers

Most operations done are saved in ledgers to be able to build geometry easily

```
@dataclass
class BooleanLedger:
    """Stores information about CSG operations"""
    self.ledger.intersected_parts
    self.ledger.unioned_parts
    self.ledger.subtracted_parts

    @property
    def all_parts(self):
        return list(set(self.intersected_parts, self.unioned_parts, self.subtracted_parts))

@dataclass
class AssemblyLedger:
    coincide_constraints: list[Part2D] = field(default_factory=list)
    ... other Assembly2D constraints

    fixed_constraints: list[Part3D] = field(default_factory=list)
    revolute_constraints: list[Part3D] = field(default_factory=list)
    ... other Assembly3D constraints

    self.transformations:list[Location] = field(default_factory=list)

    @property
    def all_parts(self):
        return list(set(self.fixed_constraints, self.revolute_constraints, ...))
```

## Mixins

Mixins extend the functionality of Part2D and Part3D

```
class BooleanMixin:
    def __init__():
        self.ledger = BooleanLedger()
    def subtract(self, location:Location, other_part:Part3D, other_location:Location) -> Part3D:
        # Do boolean subtract logic
        self.ledger.subtracted_parts += [other_part]
        return new_part

    def union(self, location:Location, other_part:Part3D, other_location:Location) -> Part3D:
        # Do boolean union logic
        self.ledger.unioned_parts += [other_part]
        return new_part

    def intersect(self, location:Location, other_part:Part3D, other_location:Location) -> Part3D:
        # Do boolean intersect logic
        self.ledger.intersected_parts += [other_part]
        return new_part
```

```
class GeometryQueryMixin:
    deg get_face(self, location:Location, tolerance:float = 1e-2): ...
    deg get_edge(self, location:Location, tolerance:float = 1e-2): ...
    deg get_vertex(self, location:Location, tolerance:float = 1e-2): ...
    deg get_faces(self, location1:Location, location2:Location, location3:Location|None = None, location4:Location|None = None):
        """Get faces bounded by locations"""
    deg get_edges(self, location:Location, location2:Location, location3:Location|None = None, location4:Location|None = None):
        """Get edges bounded by locations"""
    deg get_vertices(self, location:Location, location2:Location, location3:Location|None = None, location4:Location|None = None):
        """Get vertices bounded by locations"""

```

```
class GeometryAnalysisMixin:
    def get_area(self): ...
    def get_volume(self): ...
```

```
class MaterialBase:

    def __init__(name:str, mass: WeightWithUnit, density: DensityWithUnit, color_rgba:Vec4|None = None):
        self.mass = mass
        self.density = density
        self.color_rgba = color_rgba

class MaterialMixin:

    def __init__():
        self.material:MaterialMixin|None = None
    
    def set_material(self, material:MaterialBase):
        self.material = material

    def get_mass(self): ...
    def get_density(self): ...

```

## Assembly

The Assembly2D and Assembly3D are the base of Part3D and Part2D respectively.

```
class AssemblyCommon:
    def __init__(name:str|None = None, description:str|None):
        self.name = name
        self.description = description
        self.ledger = AssemblyLedger()

    def build(self):
        """This method must be implemented to create the shape in your target modeling application."""

    def export(self, location: str):
        """This method must be implemented to export the shape from your target modeling application."""


    def transform(self, *, absolute:Location|None=None, relative:Location|None=None):
        # translate and/or rotate by the given location, one of absolute or relative must be supplied, ValueError if both or neither.
        self.ledger.transformations += [absolute or relative]

class Assembly2D(AssemblyCommon):

    def coincide(self, location:Location, other_part:Part2D, other_location:Location) -> Part2D:
        # Do coincident constraint logic
        self.ledger.coincide_constraint += [other_part]
        return new_part

    ... other 2D constraints such as parallel, perpendicular, tangent


class Assembly3D(AssemblyCommon):

    def fixed(self, location:Location, other_part:Part3D, other_location:Location) -> Part3D:
        # Do fixed constraint logic
        self.ledger.fixed_constraints += [other_part]
        return new_part

    def revolute(self, location:Location, other_part:Part3D, other_location:Location, min_limits:Vec3|None = None, max_limits: Vec3|None = None) -> Part3D:
        # Do revolute constraint logic
        self.ledger.revolute_constraints += [other_part]
        return new_part

    def prismatic(self, location:Location, other_part:Part3D, other_location:Location, min_limits:Vec3|None = None, max_limits: Vec3|None = None) -> Part3D:
        # Do prismatic constraint logic
        self.ledger.prismatic_constraints += [other_part]
        return new_part
```

## Parts

```
class Part2D(Assembly2D, LocationMixin, GeometryQueryMixin): 

    def extrude(self, height: LengthWithUnit):
        return Part3D

class Part3D(Assembly3D, LocationMixin, GeometryQueryMixin, BooleanMixin, MaterialMixin): 

    def shell(self, thickness: LengthWithUnit, start_at_location: Location|None = None):
        # Do shell operation

    def fillet(self, edges:list[Edge]|None = None, faces:list[Face]|None = None, amount: LengthWithUnit)
    def chamfer(self, edges:list[Edge]|None = None, faces:list[Face]|None = None, amount: LengthWithUnit)
    def hole(self, start_location:Location, radius: LengthWithUnit, *, amount: LengthWithUnit|None = None, end_location: Location|None=None)

    def duplicate(self, name:str|None = None) -> Part3D
        # An independent copy of the part: same primitive, recorded
        # operations, placement and material.

    # Instancing. count includes the original instance; patterns are baked
    # into core meshes/bounding boxes (they need no CAD kernel) and replayed
    # natively by the Build123D/Blender adapters.
    def linear_pattern(self, count:int, offset:Location) -> Part3D
    def circular_pattern(self, count:int, separation_angle:AngleWithUnit, center:Location|None = None, axis:str|tuple = "z") -> Part3D
        # separation_angle: bare numbers are degrees; strings may carry units

```

## Primitives

Preset primitive functions are available to quickly generate Part2D or Part3D objects.

2D presets:
```
def rectangle(width:LengthWithUnit, height:LengthWithUnit, start_location: Location|None = None) -> Part2D: ...
def cicle(radius:LengthWithUnit, start_location: Location|None = None) -> Part2D: ...
def text(text:str, font:str, size:LengthWithUnit, start_location: Location|None = None) -> Part2D: ...
```

3D presets
```
def cube(length:LengthWithUnit, width:LengthWithUnit, height:LengthWithUnit, start_location: Location|None = None) -> Part3D: ...
def cylinder(radius:LengthWithUnit, height:LengthWithUnit, start_location: Location|None = None) -> Part3D: ...
```

Materials:
```
def white_material() -> MaterialBase
def red_material() -> MaterialBase
def green_material() -> MaterialBase
def aluminum_material() -> MaterialBase
```

## User defined Parts

A user can define a part in the API of their choice. This will run against whatever software they choose.

Usually if using the CLI interface, the user will choose a Blank Part, and populate the python file themselves.

For example, a user may choose to use [Build123D](https://build123d.readthedocs.io/en/latest/introductory_examples.html) to create a box. Their parts file may look like this: 

```
import build123d
import codetocad

class Box(codetocad.Part3D):
    def build(self):
        """User defined script to generate a shape here"""
        length, width, thickness = 80.0, 60.0, 10.0

        with build123d.BuildPart() as ex1:
            build123d.Box(length, width, thickness)

    @codetocad.location
    def example_location(self):
        return codetocad.CubeLocations.top_center.translate(x="2cm, y="2mm") # A location on the top center of the shape, offset by 2cm in the x direction and 2mm in the y direction.
```

In some cases, CodeToCAD may have integrations already available and the user does not need to define a custom shape.

## Running a script

A user can run `codetocad path/to/script`, the script will usually have all the necessary information to connect with the intended software and call the `build()` method in Parts.

Example my_script.py:

```
from my_project.my_assembly import MyAssembly

if __name__ == "__main__":
    MyAssembly().build()
```

# Microcontroller, Sensors/Actuators definition, and communication to local or remote mediums

- A microcontroller class should be made available to enable defining a microcontroller. Sensor and Actuator mixin classes could be added to the microcontroller class to define the data being read or transmitted. A communication mixin can be added to the microcontroller class to define data transfer to a remote computer or a local storage device.
- Common methods for microcontroller routines like motor position and velocity control for DC/BLDC/Stepper motors, current measurement, encoder readings, signal filtering, VESC control, in python should be made available either using libraries or implemented; the components or protocols should be documented for such methods. The idea is to facilitate using the Part3D and mixins such as MotorMixin and SensorMixin interface to common components for quick prototyping.
- Microcontroller integration should be made available for common boards using PySerial, Micropython and VESC with python. The idea is to be able to define the microcontroller type (for example esp32, esp 8266, raspberry pi running python with serial), and the user would be able to run the script to upload to the microcontroller and establish communication with it with their PythonApp or WebApp instances.
- Common wireless communication protocols to the microcontrollers should also be made available via Mixins like Bluetooth and Wifi connection enablement, MQTT messaging, Reactive (Rx) eventing should be available so that the user can subscribe to and transform sensor streams.
- A quick python or web gui using NiceGUI or Rerun integration should be made available to establish communication between a computer and a microcontroller. This should be a PythonApp or WebApp or RerunApp class and it would take the same Communication mixin as the microcontroller to be able to connect, and display controls to control actuators or display sensor values.

## Microcontroller

`Microcontroller` is an `ElectricalComponent` (so it has a footprint and can be placed on board assemblies) that declares which sensor/actuator parts hang off which GPIO pins, plus a `Communication` channel to the computer. `MicrocontrollerBoard` selects the board and runtime: `ESP32`, `ESP8266` and `RASPBERRY_PI_PICO` run MicroPython; `RASPBERRY_PI` runs plain Python (gpiozero).

```python
from codetocad import Microcontroller, MicrocontrollerBoard, SerialCommunication
from codetocad.mixins import DCMotorMixin, EncoderMixin, SensorMixin

class GearMotor(DCMotorMixin):
    no_load_speed_rpm = 200

motor, encoder, throttle = GearMotor(), EncoderMixin(), SensorMixin()

mcu = Microcontroller("motor-lab", board=MicrocontrollerBoard.ESP32)
mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)   # H-bridge PWM+DIR
mcu.bind_sensor(encoder, name="enc", a=32, b=33)                # quadrature encoder
mcu.bind_sensor(throttle, name="throttle", pin=34)              # ADC input
mcu.set_communication(SerialCommunication("/dev/ttyUSB0"))

mcu.upload()          # generate main.py from the bindings and flash it (mpremote)
mcu.connect()
motor.set_velocity(120)          # -> {"type": "command", "name": "wheel", ...}
mcu.poll()                       # pump telemetry into the bound sensors
print(encoder.read_velocity_rpm(), throttle.read())
```

Bindings infer a firmware *driver* from the mixin type (`dc_motor`, `stepper`, `encoder`, `current`, `imu_mpu6050`, `analog`, `pwm`, ...); the wiring each driver expects (L298N/DRV8871 H-bridges, A4988/TMC2209 step-dir drivers, ACS712/INA219 current sensing, MPU6050 over I2C) is documented in `codetocad_integrations.micropython`. Both ends speak a JSON-lines wire protocol: telemetry `{"type": "telemetry", "name": <channel>, "value": ..., "t": ...}` and commands `{"type": "command", "name": <channel>, "value": ...}`.

### I2C, SPI and UART devices

Sensors, motors and motor controllers that sit on a bus instead of raw GPIO are bound through a shared bus declaration: `I2CBus(sda, scl)` plus a per-device `address=`, `SPIBus(sck, mosi, miso)` plus a per-device `cs=` chip select, or `UARTBus(tx, rx)` for serial peripherals. The driver is again inferred from the mixin type — an `IMUMixin` on I2C becomes an MPU6050, a `CurrentSensorMixin` an INA219 (telemetry directly in amps), a `MotorMixin` a DRV8830 I2C motor driver, a plain actuator a PCA9685 PWM channel, a `MotorMixin` on UART a VESC — or can be set explicitly with `driver=` (e.g. the generic `i2c_register` sensor for any register-mapped chip):

```python
i2c = I2CBus(sda=21, scl=22)
spi = SPIBus(sck=14, mosi=13, miso=12)

mcu.bind_sensor(imu, bus=i2c, address=0x68)                      # MPU6050
mcu.bind_sensor(current, bus=i2c, address=0x40)                  # INA219
mcu.bind_sensor(temperature, bus=i2c, address=0x48,              # any register chip
                params={"register": 0x00, "scale": 0.0078125, "signed": True})
mcu.bind_sensor(joystick, bus=spi, cs=5, params={"channel": 2})  # MCP3008 ADC
mcu.bind_actuator(pan_servo, bus=i2c, address=0x40, driver="servo_pca9685",
                  params={"channel": 0})                         # PCA9685
mcu.bind_actuator(gear_motor, bus=i2c, address=0x60)             # DRV8830
mcu.bind_actuator(bldc, bus=UARTBus(tx=17, rx=16))               # VESC over UART
```

The generated firmware sets each bus up once and shares it between devices. On MicroPython boards this uses `machine.I2C/SPI/UART`; on a Raspberry Pi the same bindings generate `smbus2` (I2C), gpiozero `MCP3008` (SPI) and pyserial (UART) code. VESC commands are framed on-device (CRC16 short packets: `COMM_SET_DUTY`/`COMM_SET_CURRENT`/`COMM_SET_RPM`), so `bldc.set_velocity(rpm)` works the same whether the VESC hangs off the microcontroller's UART or is driven directly from the computer with `codetocad_integrations.vesc.VESCMotor`.

## Sensor, Actuator and Motor mixins

`SensorMixin` (values in via `read()`/`events`) and `ActuatorMixin` (commands out via `write()`) are the bases; on top of them sit `EncoderMixin`, `CurrentSensorMixin`, `IMUMixin`, `CameraMixin`, `MicrophoneMixin`, and `MotorMixin` with `DCMotorMixin`, `BLDCMotorMixin` and `StepperMotorMixin`. Motors expose `set_velocity(rpm)`, `set_position(degrees)`, `set_current(amps)`, `set_duty(-1..1)` and `stop()`. Any Part3D class can inherit these, so the same object is both geometry and device. VESC controllers are driven directly with `codetocad_integrations.vesc.VESCMotor` (pyvesc over serial), which implements the same MotorMixin API.

## Communication and reactive streams

`SerialCommunication`, `WifiCommunication`, `BluetoothCommunication` (SPP serial port) and `MqttCommunication` describe the medium; the same instance is shared by the microcontroller and the app so both ends agree. Transports are federated: pyserial (`codetocad_integrations.pyserial`), stdlib TCP for wifi, paho-mqtt (`codetocad_integrations.mqtt`). Incoming messages are exposed as Rx-style `EventStream`s (`subscribe`/`map`/`filter`/`throttle`), and `codetocad.signals` provides streaming `LowPassFilter`, `MovingAverageFilter` and `MedianFilter` that can be mapped over them:

```python
smooth_rpm = encoder.events.map(lambda v: v["rpm"]).map(LowPassFilter(alpha=0.2))
smooth_rpm.subscribe(print)
```

## PythonApp, WebApp and RerunApp

Control-panel apps declare sliders/buttons/toggles that command actuators and gauges/plots that display sensor telemetry, then federate to NiceGUI (`PythonApp` = native window, `WebApp` = browser, via `codetocad_integrations.nicegui`) or the Rerun viewer (`RerunApp`, via `codetocad_integrations.rerun`):

```python
app = WebApp("Motor lab").set_communication(mcu.communication)
app.add_slider("speed (rpm)", target=motor, command="velocity_rpm", maximum=200)
app.add_button("stop", target=motor, value={"stop": True})
app.add_gauge("throttle (V)", source=throttle, maximum=3.3, units="V")
app.add_plot("measured rpm", source=encoder)
app.run()
```

Extras: `uv sync --extra micropython --extra pyserial --extra mqtt --extra vesc --extra nicegui --extra rerun`. A complete example lives at `codetocad_integrations/micropython/examples/motor_lab.py`.

## Emulating a microcontroller (simulation in the loop)

`EmulatedMicrocontroller` runs the device side of a `Microcontroller` definition in-process — command dispatch and periodic telemetry over an in-memory loopback, speaking the same JSON-lines wire protocol as real firmware. Wire its handlers to a physics simulation and the unchanged `WebApp` drives the simulated robot; swap the emulator's communication for a `SerialCommunication` and the same app drives hardware:

```python
emulator = EmulatedMicrocontroller(mcu)   # also becomes mcu.communication
emulator.on_command("left_motor", lambda v: sim.set_joint_velocity_target("left_axle", ...))
emulator.set_sensor("left_encoder", lambda: {"count": ..., "rpm": ...})
emulator.add_telemetry("pose", read_pose, sample_rate_hz=10)
emulator.step(sim.data.time)              # call from the simulation loop

app = WebApp("robot lab").set_communication(emulator.communication)
```

A complete simulated differential-drive TurtleBot (TurtleBot3 Burger dimensions, Dynamixel XL430-W250 motor/encoder specs, MuJoCo physics with a ground plane and velocity-controlled wheels, WebApp with motor sliders and encoder/pose readouts) lives at `codetocad_integrations/robotics/turtlebot/turtlebot_diff_drive.py`. For mobile robots the mujoco integration's `simulate()` accepts `ground_plane=True`, `fixed_base=False`, per-joint `actuator_types` ("position"/"velocity"), `actuator_forcerange` (stall torque), `joint_damping` and `joint_armature` (a geared servo's reflected rotor inertia), plus per-link `geom_friction`.