# Cube locations — a visual dictionary

Every CodeToCAD `Part` exposes the **27 topological locations of its bounding
cube** — the geometric center, **6 face centers**, **12 edge midlines** and
**8 corners** — as attributes you can navigate a shape with, without ever
typing a coordinate:

```python
import codetocad
from codetocad_integrations.open3d import show

cube = codetocad.cube("60mm", "44mm", "32mm")

face   = cube.get_face(cube.top_center)         # the +z face
edge   = cube.get_edge(cube.top_right)          # the +z / +x edge midline
vertex = cube.get_vertex(cube.top_front_right)  # the +z / -y / +x corner

show(cube, highlight=[face])                    # opens a window, feature marked
show(cube, highlight=[face, edge, vertex])      # or several at once
```

`cube.top_center` is shorthand for `CubeLocations.TOP_CENTER.to_location(cube)`,
resolved against the part's bounding box. `get_face` / `get_edge` / `get_vertex`
snap that location to the nearest face, edge or vertex, and
`show(highlight=[...])` (or `render(..., highlight=[...])` for a PNG) overlays a
marker so you can see exactly where it landed.

Run the companion example to reproduce everything here:

```
codetocad cube_locations.py            # (re)render the images below
codetocad cube_locations.py --show     # open interactive windows instead
```

## Axis convention

`+x` is **right**, `+y` is **back**, `+z` is **top** — so `-x` is left, `-y` is
front and `-z` is bottom. The small triad in the corner of every image is the
same: <b>X = red, Y = green, Z = blue</b>. The cube below is intentionally
asymmetric (60 × 44 × 32 mm) so no two faces look alike.

> **Naming & aliases.** A location is named by the faces it touches. Order is
> free — `cube.top_front` and `cube.front_top` select the same edge — but the
> **first-named face becomes the marker's `+z`**, which matters when you place
> another part there. Every listing below uses the canonical order
> (top/bottom → front/back → left/right).

## Faces — `get_face(...)` — 6

The 6 face centers. Marker = the face outline plus a dot at its center.

<table>
<tr>
<td align="center"><img src="images/cube_face_top_center.png" width="240"><br><code>top_center</code><br><sub>+z</sub></td>
<td align="center"><img src="images/cube_face_bottom_center.png" width="240"><br><code>bottom_center</code><br><sub>−z</sub></td>
<td align="center"><img src="images/cube_face_front_center.png" width="240"><br><code>front_center</code><br><sub>−y</sub></td>
</tr>
<tr>
<td align="center"><img src="images/cube_face_back_center.png" width="240"><br><code>back_center</code><br><sub>+y</sub></td>
<td align="center"><img src="images/cube_face_left_center.png" width="240"><br><code>left_center</code><br><sub>−x</sub></td>
<td align="center"><img src="images/cube_face_right_center.png" width="240"><br><code>right_center</code><br><sub>+x</sub></td>
</tr>
</table>

## Edges — `get_edge(...)` — 12

The 12 edge midlines, one per pair of adjacent faces. Marker = a bold line
along the whole edge.

<table>
<tr>
<td align="center"><img src="images/cube_edge_top_front.png" width="240"><br><code>top_front</code></td>
<td align="center"><img src="images/cube_edge_top_back.png" width="240"><br><code>top_back</code></td>
<td align="center"><img src="images/cube_edge_top_left.png" width="240"><br><code>top_left</code></td>
<td align="center"><img src="images/cube_edge_top_right.png" width="240"><br><code>top_right</code></td>
</tr>
<tr>
<td align="center"><img src="images/cube_edge_bottom_front.png" width="240"><br><code>bottom_front</code></td>
<td align="center"><img src="images/cube_edge_bottom_back.png" width="240"><br><code>bottom_back</code></td>
<td align="center"><img src="images/cube_edge_bottom_left.png" width="240"><br><code>bottom_left</code></td>
<td align="center"><img src="images/cube_edge_bottom_right.png" width="240"><br><code>bottom_right</code></td>
</tr>
<tr>
<td align="center"><img src="images/cube_edge_front_left.png" width="240"><br><code>front_left</code></td>
<td align="center"><img src="images/cube_edge_front_right.png" width="240"><br><code>front_right</code></td>
<td align="center"><img src="images/cube_edge_back_left.png" width="240"><br><code>back_left</code></td>
<td align="center"><img src="images/cube_edge_back_right.png" width="240"><br><code>back_right</code></td>
</tr>
</table>

## Vertices — `get_vertex(...)` — 8

The 8 corners, one per triple of faces. Marker = a sphere at the corner.

<table>
<tr>
<td align="center"><img src="images/cube_vertex_top_front_left.png" width="240"><br><code>top_front_left</code></td>
<td align="center"><img src="images/cube_vertex_top_front_right.png" width="240"><br><code>top_front_right</code></td>
<td align="center"><img src="images/cube_vertex_top_back_left.png" width="240"><br><code>top_back_left</code></td>
<td align="center"><img src="images/cube_vertex_top_back_right.png" width="240"><br><code>top_back_right</code></td>
</tr>
<tr>
<td align="center"><img src="images/cube_vertex_bottom_front_left.png" width="240"><br><code>bottom_front_left</code></td>
<td align="center"><img src="images/cube_vertex_bottom_front_right.png" width="240"><br><code>bottom_front_right</code></td>
<td align="center"><img src="images/cube_vertex_bottom_back_left.png" width="240"><br><code>bottom_back_left</code></td>
<td align="center"><img src="images/cube_vertex_bottom_back_right.png" width="240"><br><code>bottom_back_right</code></td>
</tr>
</table>

## The center, plus offsets & rotations

- `cube.center` is the geometric center (`CubeLocations.CENTER`) — a marker
  there is a plain sphere with the identity `+z`.
- Nudge a location without leaving the cube frame with `.offset(...)` /
  `.translate(...)` and `.rotate(...)`, e.g.
  `codetocad.CubeLocations.top_center.offset(z="2mm").to_location(cube)` to sit
  2 mm above the top face.

These locations aren't cube-only: they resolve against **any** part's bounding
box, so `cylinder.top_center` or `imported_mesh.front_left` work the same way.
