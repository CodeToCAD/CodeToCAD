"""A differential-drive TurtleBot simulated in MuJoCo, driven from a WebApp.

Everything a real robot would have, emulated in-process:

- **Parts** with real TurtleBot3 Burger dimensions: a 138 mm chassis,
  66 x 27 mm wheels with a 160 mm track, and a 1-inch steel caster ball.
  Each wheel is a custom Part3D that *is also* a DC motor
  (``DrivenWheel(Part3D, DCMotorMixin)``) with Dynamixel XL430-W250 specs
  (57 rpm no-load at 11.1 V, 1.4 N*m stall, 4096-tick encoder).
- **A microcontroller** (ESP32 definition with pin bindings for both
  motors and both quadrature encoders) run by ``EmulatedMicrocontroller``:
  motor commands drive MuJoCo velocity actuators and encoder telemetry is
  read back from the simulated joints, over the same JSON-lines wire
  protocol real firmware speaks.
- **A camera**: a housing part on the chassis front
  (``FrontCamera(Part3D, CameraMixin)``) with a matching MuJoCo camera
  mounted at its lens. Frames render offscreen, are PNG-encoded and
  streamed over the same telemetry channel as the encoders.
- **A WebApp** with sliders for the left/right motors, the live camera
  feed, encoder gauges/plots, and the robot's pose.
- **Terrain**: gentle rolling bumps (a MuJoCo heightfield) with a flat
  launch pad at the origin, so there is something to see and climb.

Run it (needs the mujoco and nicegui extras)::

    uv run python codetocad_integrations/robotics/turtlebot/turtlebot_diff_drive.py

then open http://localhost:8080 and drive. Equal slider values drive
straight; opposite values spin in place. By default the MuJoCo viewer
window opens so you can watch the robot — on macOS run the script with
``mjpython`` (MuJoCo's requirement for the viewer); without it the example
falls back to headless physics automatically. Pass ``--no-gui`` to skip
the viewer window entirely. Swapping the emulator for a
``SerialCommunication`` to a real board is the only change needed to drive
physical hardware from the same app.
"""

from __future__ import annotations

import base64
import math
import threading
import time

import numpy as np

from codetocad import (
    EmulatedMicrocontroller,
    Location,
    MaterialBase,
    Microcontroller,
    MicrocontrollerBoard,
    Part3D,
    Vec3,
    Vec4,
    WebApp,
    cylinder,
    encode_png,
    sphere,
    steel_material,
)
from codetocad.mixins import CameraMixin, DCMotorMixin, EncoderMixin
from codetocad.parts import _box_mesh, _cylinder_mesh

# TurtleBot3 Burger / Dynamixel XL430-W250 numbers.
WHEEL_RADIUS = 0.033  # 66 mm tire
WHEEL_WIDTH = 0.027
WHEEL_SEPARATION = 0.160
WHEEL_X = 0.030  # axle sits forward of the chassis center
CHASSIS_DIAMETER = 0.138
CHASSIS_HEIGHT = 0.140
CHASSIS_CLEARANCE = 0.020
CASTER_RADIUS = 0.0127  # 1" steel transfer ball
CASTER_X = -0.055
MOTOR_NO_LOAD_RPM = 57.0
ENCODER_CPR = 4096

# The camera module on the chassis front, just below the top plate.
CAMERA_SIZE = 0.025
CAMERA_X = 0.062
CAMERA_Z = 0.145
CAMERA_TILT_DEG = 15.0  # pitched down to see the terrain ahead
CAMERA_FPS = 8.0


class DrivenWheel(Part3D, DCMotorMixin):
    """A tire on a Dynamixel XL430-W250: the part is the wheel geometry
    *and* the motor actuator, so a UI slider can target it directly.

    The built-in cylinder primitive is Z-aligned; a wheel spins about Y,
    so this part generates its own Y-axis cylinder mesh."""

    nominal_voltage = 11.1
    no_load_speed_rpm = MOTOR_NO_LOAD_RPM
    stall_torque_nm = 1.4

    def __init__(self, name: str, center: tuple[float, float, float]):
        super().__init__(name)
        self.radius = WHEEL_RADIUS
        self.width = WHEEL_WIDTH
        self._origin = Vec3(*center)
        self.set_material(
            MaterialBase("tire", mass=0.030, color_rgba=Vec4(0.12, 0.12, 0.12, 1.0))
        )

    def get_bounding_box(self):
        origin = self._origin
        half = Vec3(self.radius, self.width / 2, self.radius)
        return (
            Vec3(origin.x - half.x, origin.y - half.y, origin.z - half.z),
            Vec3(origin.x + half.x, origin.y + half.y, origin.z + half.z),
        )

    def _generate_mesh(self):
        mesh = _cylinder_mesh(self.radius, self.width, Vec3(0.0, 0.0, 0.0))
        rotated = mesh.copy()  # rotate +90 deg about X: (x, y, z) -> (x, -z, y)
        rotated[..., 1] = -mesh[..., 2]
        rotated[..., 2] = mesh[..., 1]
        return rotated + np.array(self._origin.to_tuple())


class XL430Encoder(EncoderMixin):
    """The XL430's magnetic encoder: 4096 ticks per output revolution."""

    counts_per_revolution = ENCODER_CPR
    sample_rate_hz = 20.0


class FrontCamera(Part3D, CameraMixin):
    """A camera module on the chassis front: the part *is also* the camera
    sensor (like ``DrivenWheel`` is its motor). The housing is a small
    cube; ``capture_image()`` renders the MuJoCo camera mounted at its
    lens once the simulation wires it up."""

    resolution = (320, 240)
    field_of_view = "60 deg"
    sample_rate_hz = CAMERA_FPS

    def __init__(self, name: str, center: tuple[float, float, float]):
        super().__init__(name)
        self._origin = Vec3(*center)
        self._capture = None  # set by wire_emulation
        self.set_material(
            MaterialBase("camera_housing", mass=0.02, color_rgba=Vec4(0.06, 0.06, 0.06, 1.0))
        )

    def get_bounding_box(self):
        origin, half = self._origin, CAMERA_SIZE / 2
        return (
            Vec3(origin.x - half, origin.y - half, origin.z - half),
            Vec3(origin.x + half, origin.y + half, origin.z + half),
        )

    def _generate_mesh(self):
        return _box_mesh(*self.get_bounding_box())

    def capture_image(self):
        if self._capture is None:
            raise RuntimeError("Camera not wired to a simulation yet")
        return self._capture()


def build_turtlebot() -> tuple[Part3D, DrivenWheel, DrivenWheel, FrontCamera]:
    """The robot assembly, modeled in place: chassis at the origin, wheel
    axles at z = wheel radius, caster ball touching the floor (z=0), and
    the camera module on the chassis front."""
    chassis = cylinder(
        CHASSIS_DIAMETER / 2,
        CHASSIS_HEIGHT,
        start_location=Location(z=CHASSIS_CLEARANCE + CHASSIS_HEIGHT / 2),
    )
    chassis.name = "chassis"
    # ~0.82 kg: the 1 kg robot minus wheels/caster, motors included.
    chassis.set_material(
        MaterialBase("frame", mass=0.82, color_rgba=Vec4(0.15, 0.35, 0.75, 1.0))
    )

    axle_z = WHEEL_RADIUS
    left_wheel = DrivenWheel("left_wheel", (WHEEL_X, WHEEL_SEPARATION / 2, axle_z))
    right_wheel = DrivenWheel("right_wheel", (WHEEL_X, -WHEEL_SEPARATION / 2, axle_z))

    caster = sphere(CASTER_RADIUS, start_location=Location(x=CASTER_X, z=CASTER_RADIUS))
    caster.name = "caster"
    caster.set_material(steel_material())

    # Hinge axes point +Y (a location's joint axis is its rotated Z axis),
    # so positive wheel speed rolls the robot towards +X.
    left_axle = Location.from_euler(
        WHEEL_X, WHEEL_SEPARATION / 2, axle_z, x_deg=-90, name="left_axle"
    )
    right_axle = Location.from_euler(
        WHEEL_X, -WHEEL_SEPARATION / 2, axle_z, x_deg=-90, name="right_axle"
    )
    chassis.revolute(left_axle, left_wheel, left_axle)
    chassis.revolute(right_axle, right_wheel, right_axle)
    chassis.fixed(
        Location(x=CASTER_X, z=CASTER_RADIUS), caster, Location(x=CASTER_X, z=CASTER_RADIUS)
    )

    camera = FrontCamera("camera", (CAMERA_X, 0.0, CAMERA_Z))
    chassis.fixed(
        Location(x=CAMERA_X, z=CAMERA_Z), camera, Location(x=CAMERA_X, z=CAMERA_Z)
    )
    return chassis, left_wheel, right_wheel, camera


def make_terrain():
    """Gentle rolling bumps to drive over: a 6 x 6 m heightfield of
    crossed sine waves, faded to a flat launch pad around the origin so
    the robot starts level. 4 cm crests over a 1.2 m wavelength keep the
    slopes within what the XL430s can climb."""
    from codetocad_integrations.mujoco import TerrainSpec

    extent = 6.0
    coords = np.linspace(-extent / 2, extent / 2, 128)
    x, y = np.meshgrid(coords, coords)  # heightfield rows map to y, columns to x
    bumps = 0.5 * (1 + np.sin(2 * np.pi * x / 1.2) * np.sin(2 * np.pi * y / 1.2))
    ramp = np.clip((np.hypot(x, y) - 0.4) / 0.6, 0.0, 1.0)
    ramp = ramp * ramp * (3 - 2 * ramp)  # smoothstep: no kink at the pad edge
    return TerrainSpec(heights=0.04 * bumps * ramp, extent=(extent, extent))


def make_simulation(chassis: Part3D, output_dir=None):
    """MuJoCo with terrain, a free-floating base and velocity-controlled
    wheel joints. The caster ball is rigidly attached and nearly
    frictionless, which is how a transfer-ball caster behaves. The
    front camera is mounted at the housing's lens, pitched down to see
    the terrain ahead."""
    from codetocad_integrations.mujoco import CameraSpec, simulate

    tilt = math.radians(CAMERA_TILT_DEG)
    front_camera = CameraSpec(
        name="front_camera",
        link="camera",
        # The lens sits just outside the housing's front face; the camera
        # looks along +X (image up = +Z), pitched down by the tilt.
        position=(CAMERA_X + CAMERA_SIZE / 2 + 0.002, 0.0, CAMERA_Z),
        xyaxes=(0, -1, 0, math.sin(tilt), 0, math.cos(tilt)),
        fovy=60.0,
        resolution=FrontCamera.resolution,
    )
    return simulate(
        chassis,
        fixed_base=False,
        ground_plane=True,
        cameras=[front_camera],
        terrain=make_terrain(),
        actuator_types={"left_axle": "velocity", "right_axle": "velocity"},
        # XL430-W250 stall torque; keeps reaction torques on the 1 kg
        # chassis realistic so the robot cannot backflip off the line.
        actuator_forcerange={"left_axle": 1.4, "right_axle": 1.4},
        joint_damping={"left_axle": 0.005, "right_axle": 0.005},
        # Reflected rotor inertia of the XL430's 258:1 gearbox; this is
        # what makes a geared servo settle instead of oscillating.
        joint_armature={"left_axle": 0.005, "right_axle": 0.005},
        geom_friction={
            "left_wheel": (1.2, 0.005, 0.0001),
            "right_wheel": (1.2, 0.005, 0.0001),
            "caster": (0.02, 0.001, 0.0001),
        },
        time_step=1.0 / 240.0,
        output_dir=output_dir,
    )


def make_microcontroller(
    left_wheel: DrivenWheel, right_wheel: DrivenWheel
) -> tuple[Microcontroller, XL430Encoder, XL430Encoder]:
    """The same definition that would run on a physical robot: two H-bridge
    motor channels and two quadrature encoder channels on an ESP32."""
    mcu = Microcontroller("turtlebot", board=MicrocontrollerBoard.ESP32)
    mcu.bind_actuator(left_wheel, name="left_motor", pwm_pin=4, dir_pin=16)
    mcu.bind_actuator(right_wheel, name="right_motor", pwm_pin=5, dir_pin=17)
    left_encoder, right_encoder = XL430Encoder(), XL430Encoder()
    mcu.bind_sensor(left_encoder, name="left_encoder", a=34, b=35)
    mcu.bind_sensor(right_encoder, name="right_encoder", a=32, b=33)
    return mcu, left_encoder, right_encoder


def wire_emulation(
    sim, mcu: Microcontroller, camera: FrontCamera
) -> EmulatedMicrocontroller:
    """Connect the microcontroller's channels to the simulation: motor
    commands set wheel joint velocity targets, encoder telemetry reads the
    joint state back, and the chassis pose and camera frames are published
    for the app."""
    emulator = EmulatedMicrocontroller(mcu)
    camera._capture = lambda: sim.get_camera_image("front_camera")

    def motor_handler(joint_name):
        def handle(value):
            if not isinstance(value, dict):
                value = {"duty": float(value)}
            if value.get("stop"):
                rpm = 0.0
            elif "velocity_rpm" in value:
                rpm = float(value["velocity_rpm"])
            elif "duty" in value:
                rpm = float(value["duty"]) * MOTOR_NO_LOAD_RPM
            else:
                return
            rpm = max(-MOTOR_NO_LOAD_RPM, min(MOTOR_NO_LOAD_RPM, rpm))
            sim.set_joint_velocity_target(joint_name, rpm * 2 * math.pi / 60)

        return handle

    def encoder_reader(joint_name):
        def read():
            angle = sim.get_joint_value(joint_name)
            rate = sim.get_joint_velocity(joint_name)
            return {
                "count": int(angle / (2 * math.pi) * ENCODER_CPR),
                "rpm": rate * 60 / (2 * math.pi),
            }

        return read

    def read_pose():
        position, quat = sim.get_body_pose("chassis")
        w, x, y, z = quat
        yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
        return {
            "x": round(position[0], 4),
            "y": round(position[1], 4),
            "heading_deg": round(math.degrees(yaw), 2),
        }

    def read_frame():
        png = encode_png(camera.capture_image())
        return {"png": base64.b64encode(png).decode("ascii")}

    emulator.on_command("left_motor", motor_handler("left_axle"))
    emulator.on_command("right_motor", motor_handler("right_axle"))
    emulator.set_sensor("left_encoder", encoder_reader("left_axle"))
    emulator.set_sensor("right_encoder", encoder_reader("right_axle"))
    emulator.add_telemetry("pose", read_pose, sample_rate_hz=10.0)
    emulator.add_telemetry("camera", read_frame, sample_rate_hz=CAMERA_FPS)
    return emulator


def drive(sim, emulator: EmulatedMicrocontroller, duration_seconds: float,
          realtime: bool = False):
    """Step the simulation and the emulated firmware together."""
    start_wall = time.monotonic()
    start_sim = sim.data.time
    while sim.data.time - start_sim < duration_seconds:
        sim.step(4)
        emulator.step(sim.data.time)
        if realtime:
            lag = (sim.data.time - start_sim) - (time.monotonic() - start_wall)
            if lag > 0:
                time.sleep(lag)


def make_app(communication, left_wheel, right_wheel, left_encoder, right_encoder) -> WebApp:
    app = WebApp("TurtleBot diff drive").set_communication(communication)
    app.add_slider(
        "left motor (rpm)", target=left_wheel, command="velocity_rpm",
        minimum=-MOTOR_NO_LOAD_RPM, maximum=MOTOR_NO_LOAD_RPM,
    )
    app.add_slider(
        "right motor (rpm)", target=right_wheel, command="velocity_rpm",
        minimum=-MOTOR_NO_LOAD_RPM, maximum=MOTOR_NO_LOAD_RPM,
    )
    app.add_button("stop left", target=left_wheel, value={"stop": True})
    app.add_button("stop right", target=right_wheel, value={"stop": True})
    app.add_image("front camera", source="camera", key="png")
    app.add_plot("left wheel (rpm)", source=left_encoder, key="rpm")
    app.add_plot("right wheel (rpm)", source=right_encoder, key="rpm")
    app.add_gauge("left encoder", source=left_encoder, key="count", units="ticks")
    app.add_gauge("right encoder", source=right_encoder, key="count", units="ticks")
    app.add_gauge("pose x", source="pose", key="x", units="m")
    app.add_gauge("pose y", source="pose", key="y", units="m")
    app.add_gauge("heading", source="pose", key="heading_deg", units="deg")
    return app


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(
        description="Simulated diff-drive TurtleBot: MuJoCo viewer + control WebApp"
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="run headless: skip the MuJoCo viewer window (the WebApp still serves)",
    )
    parser.add_argument("--port", type=int, default=8080, help="WebApp port")
    args = parser.parse_args(argv)

    chassis, left_wheel, right_wheel, camera = build_turtlebot()
    sim = make_simulation(chassis)
    mcu, left_encoder, right_encoder = make_microcontroller(left_wheel, right_wheel)
    emulator = wire_emulation(sim, mcu, camera)
    emulator.communication.connect()
    app = make_app(
        emulator.communication, left_wheel, right_wheel, left_encoder, right_encoder
    )

    if args.no_gui:
        # Physics in a background thread; the WebApp owns the main thread.
        stop = threading.Event()

        def simulation_loop():
            while not stop.is_set():
                drive(sim, emulator, 0.25, realtime=True)

        thread = threading.Thread(target=simulation_loop, daemon=True)
        thread.start()
        try:
            app.run(port=args.port)
        finally:
            stop.set()
            thread.join(timeout=2)
        return

    # Default: the MuJoCo viewer owns the main thread (required by
    # launch_passive) and the WebApp serves from a background thread.
    web_thread = threading.Thread(
        target=lambda: app.run(port=args.port), daemon=True
    )
    web_thread.start()
    try:
        sim.launch_viewer(on_step=lambda: emulator.step(sim.data.time))
    except RuntimeError as error:
        print(
            f"codetocad: MuJoCo viewer unavailable ({error}).\n"
            "codetocad: on macOS run this script with mjpython to get the "
            "viewer window; continuing headless with just the WebApp."
        )
        while True:
            drive(sim, emulator, 0.25, realtime=True)


if __name__ == "__main__":
    main()
