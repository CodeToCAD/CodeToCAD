# Physics simulation: pybullet & mujoco

Model + assemble with joint constraints, then `simulate(part)` walks the
assembly, exports meshes, and generates a URDF (pybullet) or MJCF (mujoco).

- pybullet: `from codetocad_integrations.pybullet import simulate` → `PyBulletSimulation`
- mujoco:  `from codetocad_integrations.mujoco import simulate` → `MujocoSimulation`

Both return a `Simulation` (base class in [../../codetocad/simulation.py](../../codetocad/simulation.py)).

```python
from codetocad import Location
from codetocad_integrations.build123d import make_cube, make_cylinder
from codetocad_integrations.pybullet import simulate     # or ...mujoco

mount = make_cube("6cm", "6cm", "4cm", start_location=Location(z="52cm"))
rod   = make_cylinder("1cm", "40cm", start_location=Location(z="30cm"))
pivot = Location.from_euler(0, 0, "50cm", x_deg=-90, name="pivot")
mount.revolute(pivot, rod, pivot)          # hinge about Y

sim = simulate(mount, gui=True)
sim.set_joint_value("pivot", 1.0)          # teleport, no dynamics
sim.run(10.0, realtime=True)
```

## Common `simulate(...)` parameters (both backends)

From the base `Simulation.__init__` — every backend forwards these:

- `lighting: list[Lighting]` — scene lights (`codetocad.Lighting`).
- `camera: Camera` — the overview camera (`codetocad.Camera`); see below.
- `gravity=(0,0,-9.81)`, `time_step=1/240`.
- `fixed_base=True` — weld the root to the world (False = free-floating robot).
- `actuated=True` — add motors to movable joints.
- `scene_parts=[...]` — free-floating bodies the robot can push/pick up.
- `ground_plane=False` — add a floor.
- `self_collision=True` — collide assembly parts against each other, **except**
  parts welded by `fixed` joints (they move as one body).
- `collision_exclusions=[(a, b), ...]` — opt specific pairs out of contact;
  each entry is a link name **or the `Part3D`** that was joined. Use for parts
  that overlap by construction (a rod modeled into its base at a joint).
- `output_dir=...` — where meshes/URDF/MJCF are written (temp dir by default).

Backend-specific extras: **pybullet** adds `gui: bool`. **mujoco** adds
`cameras: list[CameraSpec]`, `terrain: TerrainSpec`, and actuator tuning
(per-joint damping/armature/forcerange — small wheeled robots need these or they
flip/oscillate).

## Driving joints

- `sim.set_joint_value(joint, value)` — instant teleport (no dynamics).
- `sim.get_joint(joint).move_to(value)` / `.move_by(delta)` — position control
  through the actuator (the intended way to drive).
- `sim.set_joint_velocity(joint, value)` — velocity control (rad/s or m/s).
- `sim.get_joint_value(joint)` — read current value.
- `joint` is a joint **name** or the child **`Part3D`** that was joined.
- `sim.joint_names`, `sim.joints` list what's drivable.

## Stepping & running

- `sim.step(count=1)` — advance N physics steps.
- `sim.run(duration, realtime=False)` — step for `duration` seconds.

## Keyframes → animation

```python
sim.get_joint("pivot").move_to(0.0);  sim.set_keyframe(0.0)
sim.get_joint("pivot").move_to(1.5);  sim.set_keyframe(2.0)   # t defaults to prev+1s
sim.play_keyframes(fps=30, realtime=True)
sim.record_gif("swing.gif", keyframes=True, fps=30)
```

`set_keyframe(t)` snapshots the currently *commanded* targets, so command joints
first, then pin. `record_gif(path, duration=..., fps=..., loop=...)` also records
a plain time span when `keyframes=False`.

## The overview camera & lighting (unified across all backends)

`capture_image(width, height)` returns an `(H, W, 3)` uint8 RGB array from the
simulation's **overview camera**. Encode with `codetocad.encode_png` /
`encode_gif` for telemetry. Camera and lighting are set the *same way* on every
backend (pybullet, mujoco, blender):

```python
from codetocad import Camera, Lighting

# at construction:
sim = simulate(part, camera=Camera(yaw=90, pitch=-20, distance=3.0),
               lighting=[Lighting(position=(2, 2, 4))])

# or live, any time:
sim.set_camera(yaw=120, pitch=-15)          # merge fields onto current camera
sim.set_camera(Camera(position=(2, -2, 1.5), target=(0, 0, 0.3)))  # explicit eye
sim.set_lighting([Lighting(position=(0, 0, 5), color=(1, 0.9, 0.8))])
```

### `Camera` (`codetocad.Camera`)

An **orbit** camera by default — looks at `target` from `distance` away, swung
`yaw`° around the up axis and tilted `pitch`° (negative looks down):

| field | meaning | default |
|-------|---------|---------|
| `target` | look-at point | assembly center |
| `distance` | orbit radius (m) | auto-fit to assembly |
| `yaw` | azimuth degrees | 45 |
| `pitch` | elevation degrees (negative = look down) | −35 |
| `position` | explicit eye point (**overrides** distance/yaw/pitch) | None |
| `up` | up vector | (0,0,1) |
| `fov` | vertical field of view degrees | 60 |

Any field left `None` is auto-derived, so `Camera(pitch=-10)` still frames the
scene. `set_camera(**fields)` merges fields onto the current camera;
`set_camera(Camera(...))` replaces it. Both return the active `Camera`.

- **pybullet** applies the camera to `capture_image` **and** the live GUI window
  (via `resetDebugVisualizerCamera`). `capture_image` also still takes per-call
  overrides: `sim.capture_image(yaw=200, distance=2)` and these flow through
  `record_gif(...)` too.
- **mujoco** applies it to the free camera in `capture_image` and to
  `launch_viewer()`.
- **blender** builds/positions the render camera from it (else auto-frames).

### Lighting

`set_lighting([...])` / the `lighting=` arg take `codetocad.Lighting` (`position`,
`direction`, `color`, `intensity`, `light_type` = "directional"/"point"/"spot").
mujoco updates its live scene lights **by name** (lights are declared at build
time — new *names* need a fresh `simulate`); blender realizes them as scene
lights the Workbench render uses; pybullet applies the first light to the GUI.

### mujoco: also mounted (on-robot) cameras
Separate from the overview camera, mujoco can mount fixed `CameraSpec` cameras on
links — "what the robot sees" — rendered by name:

```python
from codetocad_integrations.mujoco import CameraSpec, simulate
sim = simulate(part, cameras=[CameraSpec(name="eye", link="head",
               position=(0.1, 0, 0.2), fovy=60, resolution=(640, 480))])
img = sim.get_camera_image("eye")          # or capture_image(camera="eye")
```
`position` is world coords in the modeled pose; `xyaxes` = image-right/up axes
(camera looks along −Z).

## MuJoCo extras

- `CameraSpec` — fixed camera on a link (above).
- `TerrainSpec(heights=..., extent=..., checker_rgba=...)` — heightfield floor.
- `sim.get_camera_image(name)` — render a mounted camera (what the robot sees).

## Notes

- pybullet/mujoco need Python 3.12 in this repo (`.venv-sim`); mujoco lives
  there too. See repo memory on sim env setup.
- `sim.close()` / `with simulate(...) as sim:` releases the engine/renderers.
