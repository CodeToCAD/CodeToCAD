# Geometry backends: build123d, blender, open3d

These give the abstract core API a real kernel (build123d, blender) or a viewer
(open3d). Pick one modeling backend per script.

## build123d — `codetocad_integrations.build123d`

OpenCascade solids. Booleans/shells/fillets/chamfers/holes/transforms replay
natively; queries and STL/STEP export use the real topology. This is the default
"just give me real geometry" backend and needs no external program.

Install: `uv sync --extra build123d`.

Public: `Part2D`, `Part3D`, `ElectricalComponent`, `adapt`, and `make_*`
factories: `make_cube`, `make_box`, `make_cylinder`, `make_sphere`,
`make_import`, `make_rectangle`, `make_circle`, `make_text`, `make_led`,
`make_resistor`, `make_capacitor`, `make_fastener`.

```python
from codetocad_integrations.build123d import make_cube

if __name__ == "__main__":
    cube = make_cube("10cm", "10cm", "5cm")
    cube.hole(cube.top_center, radius="4cm", amount="5cm")
    print(cube.get_volume())          # real query
    cube.export("my_cube.stl")        # or .step
```

- **`adapt(part)`** converts any core part (`led()`, `resistor()`, a fastener,
  your custom `Part3D`) into a build123d-federated one — use it when you built
  with core factories but need real geometry.
- **Custom base shape:** subclass `codetocad_integrations.build123d.Part3D` and
  override `build_native()` to model with the Build123D API; all CodeToCAD
  operations still apply on top.

## blender — `codetocad_integrations.blender`

Same designs → Blender mesh objects (booleans, solidify shells, bevel
fillets/chamfers, modifier holes). Export `.stl/.obj/.glb/.fbx/.blend`.

Requires Blender on `PATH` or `CODETOCAD_BLENDER` pointing at the binary.
`ensure_blender()` **re-launches the current script** under `blender
--background`, so guard your code with `if __name__ == "__main__":`.

```python
from codetocad_integrations.blender import ensure_blender, make_cube

if __name__ == "__main__":
    ensure_blender()
    cube = make_cube("10cm", "10cm", "5cm")
    cube.hole(cube.top_center, radius="4cm", amount="5cm")
    cube.export("my_cube.blend")
```

Custom shapes: subclass `codetocad_integrations.blender.Part3D`, override
`build_native()` (bpy/bmesh). Note: keep bpy code Python-3.11 compatible.

## open3d — `codetocad_integrations.open3d`

A **viewer/renderer, not a kernel**. It exports the part (`part.export()`) to a
temp mesh and loads it, so it works with any modeling backend.

Install: `uv sync --extra open3d`. Public: `show`, `render`, `to_mesh`.

```python
from codetocad_integrations.build123d import make_cube
from codetocad_integrations.open3d import show, render

cube = make_cube("10cm", "10cm", "5cm")
show(cube)                       # interactive window
render(cube, path="cube.png")    # offscreen screenshot for docs/CI
```

## Choosing

- Need real geometry with zero setup → **build123d**.
- Need Blender-native output or modifiers/rendering → **blender**.
- Just want to look at / screenshot a part → **open3d** on top of either.
