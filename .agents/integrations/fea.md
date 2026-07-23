# FEA: calculix — `codetocad_integrations.calculix`

Finite-element stress/displacement on the same parts. `analyze(part)` meshes the
exported geometry with gmsh, applies fixtures/loads described with `Location`s,
solves with CalculiX via [pygccx](https://github.com/calculix/pygccx), and
returns fields with visualization.

Install: `uv sync --extra calculix`. The `ccx` solver is auto-discovered from
`CODETOCAD_CCX`, the `PATH`, or `~/.codetocad/ccx/bin/ccx`.

Public: `analyze` → `CalculixFEA`, plus `find_ccx`.

```python
from codetocad import steel_material
from codetocad_integrations.build123d import make_cube
from codetocad_integrations.calculix import analyze

beam = make_cube("200mm", "20mm", "10mm")
beam.set_material(steel_material())          # elastic props come from material

fea = analyze(beam)
fea.fix(beam.left_center)                     # clamp a face
fea.add_force(beam.right_center, force=(0, 0, -100))   # newtons
results = fea.solve()
print(results.max_displacement, results.max_von_mises)
results.visualize("beam_fea.png")
```

## Essentials

- **Material required for stiffness.** `steel_material()`, `aluminum_material()`,
  or set `youngs_modulus`/`poissons_ratio` on any `MaterialBase`.
- **Fixtures & loads are located** with the same `Location`/`CubeLocations`
  shortcuts used for modeling (`beam.left_center`, etc.).
- `fea.fix(location)` clamps; `fea.add_force(location, force=(fx, fy, fz))` loads.
- `results` (`FEAResults`) exposes `max_displacement`, `max_von_mises`, and
  `visualize(path)` for a rendered field plot.

See [../../codetocad_integrations/calculix/examples/](../../codetocad_integrations/calculix/examples/).
