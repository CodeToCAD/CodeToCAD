# Build123D integration examples

Translations of examples from the Build123D documentation into CodeToCAD.
Run any of them with `codetocad <example>.py` (requires the `build123d`
extra: `uv sync --extra build123d`). Each exports an STL next to where it is
run.

From the [introductory examples](https://build123d.readthedocs.io/en/latest/introductory_examples.html),
using CodeToCAD primitives and operations:

- `intro_02_plate_with_hole.py` — Box + `hole()`

  <img src="images/intro_02_plate_with_hole.png" width="400">

- `intro_03_prismatic_solid.py` — extruded sketches + boolean `subtract()`

  <img src="images/intro_03_prismatic_solid.png" width="400">

- `intro_09_fillet_chamfer.py` — edge selection with bounded geometry
  queries + `fillet()`/`chamfer()`

  <img src="images/intro_09_fillet_chamfer.png" width="400">

- `intro_26_shelled_box.py` — `shell()` with an opening face

  <img src="images/intro_26_shelled_box.png" width="400">

- `intro_34_embossed_text.py` — text sketches extruded, then unioned/
  subtracted using anchor locations

  <img src="images/intro_34_embossed_text.png" width="400">

From the [examples gallery](https://build123d.readthedocs.io/en/stable/examples_1.html),
as custom user parts overriding `build_native()` with the Build123D API
(CodeToCAD operations, queries, analysis and export still apply on top):

- `gallery_circuit_board.py` — Circuit Board With Holes (pure CodeToCAD
  primitives: extruded rectangle + 56 `hole()` operations)

  <img src="images/gallery_circuit_board.png" width="400">

- `gallery_key_cap.py` — Key Cap (taper extrude, dish, ribs, socket)

  <img src="images/gallery_key_cap.png" width="400">

- `gallery_handle.py` — Handle (multi-section sweep + a
  `@codetocad.location` named location)

  <img src="images/gallery_handle.png" width="400">

- `gallery_multi_sketch_loft.py` — Multi-Sketch Loft (loft + shell)

  <img src="images/gallery_multi_sketch_loft.png" width="400">

- `gallery_vase.py` — Vase (revolved profile + shell + fillets)

  <img src="images/gallery_vase.png" width="400">

Output:

- `technical_drawing.py` — `generate_drawing()` projects the native solid
  (so the hole shows up) into a third-angle SVG sheet; the returned drawing is
  an editable `Part2D` you rename, transform and `export("...svg")`.

  <img src="images/technical_drawing.png" width="400">

Note: CodeToCAD's base unit is meters, so the original (millimeter) values
appear as `"80mm"` strings or are scaled by `MM = 0.001` in custom parts.
