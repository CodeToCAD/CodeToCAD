# Robotics: putting it all together

[../../codetocad_integrations/robotics/](../../codetocad_integrations/robotics/)
holds end-to-end examples that combine every layer into one script:

- **MCAD** — the assembled parts and joint constraints ([geometry.md](geometry.md), [core-classes.md](../core-classes.md)).
- **ECAD** — the microcontroller as an `ElectricalComponent` with pin bindings.
- **MCU** — a `Microcontroller` definition, run by real firmware or, for
  simulation, an in-process `EmulatedMicrocontroller`.
- **Physics** — a pybullet/mujoco `Simulation` ([simulation.md](simulation.md)).
- **Control panel** — a `WebApp`/`PythonApp`/`RerunApp` ([controls.md](controls.md)).

All layers share one `Communication`, so swapping the emulator for a
`SerialCommunication` to a real board is the *only* change needed to drive
physical hardware from the same app.

## Examples

- **`arm_6dof/`** — a 6-DOF arm with a parallel-jaw gripper that picks up a cube.
  Good reference for multi-joint assemblies, gripper force/keyframe control, and
  `scene_parts` for the object being grasped.
- **`turtlebot/`** — a differential-drive TurtleBot3 Burger: real chassis/wheel/
  caster dimensions, Dynamixel XL430-W250 motor/encoder specs, an ESP32
  `Microcontroller`, MuJoCo physics with velocity-controlled wheels, and a
  `WebApp` with motor sliders and encoder/pose readouts. See its
  [README](../../codetocad_integrations/robotics/turtlebot/README.md) and
  `turtlebot_diff_drive.py`.

## Practical notes for agents

- Small wheeled robots need per-joint MuJoCo tuning (damping/armature/
  forcerange) or they flip/oscillate — see the turtlebot example's actuator setup.
- Grippers in pybullet: hold all joints, cap grip force (~10 N), ramp targets,
  keep fingertips off the floor — see the 6-DOF arm example.
- Use `collision_exclusions` for parts modeled overlapping at a joint, and
  `self_collision=True` for jointed pairs that must actually collide (a lid on
  its box). Details in [simulation.md](simulation.md).
- Drive wheels with `sim.set_joint_velocity(...)`; read pose/encoders back
  through the bound sensor mixins.
