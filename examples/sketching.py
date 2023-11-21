from codetocad import Sketch
from codetocad.enums.curve_types import CurveTypes

rectangle_points_sketch = Sketch(
    "rectangle_from_points", curve_type=CurveTypes.BEZIER
).create_from_vertices(["0,0,0", "1,0,0", "1,1,0", "0,1,0", "0,0,0"])

triangle_sketch = Sketch("triangle", curve_type=CurveTypes.NURBS)

line1 = triangle_sketch.create_line("0,0,0", "1,1,0")

line2 = triangle_sketch.create_line(line1.v2, "0,1,0")

line3 = triangle_sketch.create_line(line2.v2, line1.v1)


rectangle_lines_sketch = Sketch(
    name="rectangle_from_lines", curve_type=CurveTypes.BEZIER
)

line1 = rectangle_lines_sketch.create_line("0,0,0", "1,0,0")

line2 = rectangle_lines_sketch.create_line("0,1,0", "1,1,0")

line3 = rectangle_lines_sketch.create_line(line1.v1, line2.v1)

line4 = rectangle_lines_sketch.create_line(line1.v2, line2.v2)
