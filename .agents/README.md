# Agent guide to CodeToCAD

This folder tells coding agents how to use CodeToCAD's classes and integrations.
It is a task-oriented companion to the human docs:

- [../README.md](../README.md) — the tour, with a runnable snippet per integration.
- [../CodeToCAD.md](../CodeToCAD.md) — the full design document (deepest reference).

Read this index first, then the topic file you need.

## The one idea: federation

You write **one** script against the core `codetocad` API. At run time it is
*federated* to a real backend — Build123D (OpenCascade), Blender, a physics
engine, a circuit simulator, etc. The core classes record operations into
*ledgers*; each integration replays those operations natively. So the same
`part.hole(...)` becomes an OpenCascade cut, a Blender boolean modifier, or a
mesh feature depending on which integration you imported.

Practical consequence: **import matters**. `import codetocad` gives you the
abstract API; `from codetocad_integrations.build123d import make_cube` gives you
a part backed by a real kernel. Geometry queries (volume, bounding box, export)
need a geometry backend — plain core parts can be modeled and constrained but
have no kernel behind them.

## Conventions that apply everywhere

- **Units.** A bare `float`/`int` is **meters** (or **radians** for angles). A
  string is parsed: `"2cm"`, `"10 deg"`, `"2in - 5mm"`. Prefer strings for
  human-scale dimensions; prefer floats in loops/math.
- **Locations.** `Location` is a 6-DOF pose (position + orientation). Build them
  with `Location(x=..., y=..., z=...)`, `Location.from_euler(...)`, or a shape's
  `CubeLocations` shortcuts (`part.top_center`, `part.left_center`, ... — the 23
  topological points of the bounding cube). The `@codetocad.location` decorator
  marks a named location method on a custom part class.
- **Constraints record joints.** Assembly constraints (`fixed`, `revolute`,
  `prismatic`, `coincide`, `parallel`, ...) are recorded on the part, not solved
  eagerly. Geometry backends ignore them; the simulation backends turn
  `fixed`/`revolute`/`prismatic` into physics joints. See
  [core-classes.md](core-classes.md) and [integrations/simulation.md](integrations/simulation.md).
- **Materials drive physics/FEA.** `set_material(...)` attaches density (→ mass &
  inertia in sim) and elastic properties (→ FEA). Color comes from the material too.
- **`export(path)`** writes geometry (`.stl`, `.step`, `.obj`, `.glb`, `.blend`,
  ... depending on backend). Many integrations round-trip through a temporary
  `export()` rather than reimplementing geometry.
- **Extras.** Integrations live behind optional dependencies. Install with
  `uv sync --extra <name>` (e.g. `build123d`, `skidl`, `spice`, `nicegui`,
  `rerun`). Blender/ngspice/netlistsvg/CalculiX are external programs discovered
  via `PATH` or `CODETOCAD_*` env vars.

## Topic map

| File | Covers |
|------|--------|
| [core-classes.md](core-classes.md) | Parts, assemblies, primitives, locations, materials, joints, mixins, ECAD components, fasteners, drawings |
| [integrations/geometry.md](integrations/geometry.md) | build123d, blender, open3d (modeling & rendering backends) |
| [integrations/simulation.md](integrations/simulation.md) | pybullet, mujoco — joints, keyframes, GIFs, **camera pose** |
| [integrations/fea.md](integrations/fea.md) | calculix — fixtures, loads, stress/displacement |
| [integrations/ecad.md](integrations/ecad.md) | skidl (schematics/netlists), spice (circuit simulation) |
| [integrations/controls.md](integrations/controls.md) | apps (nicegui/rerun/python), microcontroller + emulation, pyserial/mqtt/vesc/micropython transports |
| [integrations/robotics.md](integrations/robotics.md) | putting MCAD + ECAD + MCU + WebApp + physics together |

## Ground rules for agents

- Don't invent APIs. If a method isn't in these docs or the source, grep for it
  before using it. Public surfaces are the `__all__` of each integration package.
- Prefer core `codetocad` symbols; reach into an integration only for its entry
  point (`simulate`, `analyze`, `make_cube`, `serve`, ...).
- Scripts that federate to an external app usually need an
  `if __name__ == "__main__":` guard (Blender/simulation may re-launch the script).
