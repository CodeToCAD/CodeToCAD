# Open3D integration examples

Run with a normal Python interpreter (`codetocad <example>.py` or `python
<example>.py`). Requires the `open3d` extra (`uv sync --extra open3d`); this
example also models with Build123D (`uv sync --extra build123d`) since
booleans need a federated backend to produce real geometry.

- `embossed_text_logo.py` — a "CodeToCAD" logo plate: text extruded and
  unioned onto a plate with Build123D, rendered to a PNG with
  `codetocad_integrations.open3d.render()`.

  <img src="images/embossed_text_logo.png" width="400">

- `cube_locations.py` — navigate a shape with `CubeLocations` +
  `get_face` / `get_edge` / `get_vertex`, and `show(highlight=...)` each
  result. Renders the images for **[cube_locations.md](cube_locations.md)**, a
  visual dictionary of every face, edge and corner of a part's bounding cube.

  <img src="images/cube_face_top_center.png" width="300">

Use `show(part)` instead of `render(part, path=...)` to open an interactive
Open3D window rather than saving a screenshot.
