from codetocad import Sketch
from codetocad.enums.curve_types import CurveTypes

rectangle_points_sketch = Sketch(
    "rectangle_from_points", curve_type=CurveTypes.BEZIER
).create_from_vertices(["0,0,0", "1,0,0", "1,1,0", "0,1,0", "0,0,0"])


triangle_sketch = Sketch("triangle", curve_type=CurveTypes.NURBS)
line1 = triangle_sketch.create_line("0,0,0", "1,1,0")
line2 = triangle_sketch.create_line(line1.v2, "0,1,0")
line3 = triangle_sketch.create_line(line2.v2, line1.v1)
triangle_sketch.translate_y(1)


rectangle_lines_sketch = Sketch(
    name="rectangle_from_lines", curve_type=CurveTypes.BEZIER
)
line1 = rectangle_lines_sketch.create_line("0,0,0", "1,0,0")
line2 = rectangle_lines_sketch.create_line("0,1,0", "1,1,0")
line3 = rectangle_lines_sketch.create_line(line1.v1, line2.v1)
line4 = rectangle_lines_sketch.create_line(line1.v2, line2.v2)
rectangle_lines_sketch.translate_y(2)


loft_sketch1 = Sketch("loft_sketch1", curve_type=CurveTypes.BEZIER)
w1 = loft_sketch1.create_rectangle(1, 1)
loft_sketch2 = Sketch("loft_sketch2", curve_type=CurveTypes.BEZIER)
w2 = loft_sketch2.create_rectangle(0.5, 0.5)
loft_sketch2.translate_z(1).rotate_x(45)
lofted = w1.loft(w2).set_name("loft")
lofted.translate_xyz(0.5, 3.5, 0)


circle_sketch = Sketch("circle", curve_type=CurveTypes.BEZIER)
circle_wire = circle_sketch.create_circle(0.5)
circle_sketch.translate_xyz(0.5, 4.5, 0)

arc_sketch = Sketch("arc", curve_type=CurveTypes.BEZIER)
arc_wire = arc_sketch.create_arc([-0.5, 0, 0], [1, 1, 0], 0.25)
arc_sketch.translate_xyz(0.5, 5.5, 0)


ellipse_sketch = Sketch("ellipse", curve_type=CurveTypes.BEZIER)
ellipse_wire = ellipse_sketch.create_ellipse(0.5, 0.25)
ellipse_sketch.translate_xyz(0.5, 6.5, 0)
