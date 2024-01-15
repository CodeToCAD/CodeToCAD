from codetocad import Sketch


rectangle = Sketch("cube")
r_wire = rectangle.create_rectangle(1, 1)
rectangle.extrude(1)


rectangle = Sketch("cube2")
r_wire = rectangle.create_rectangle(1, 1)
rectangle.rotate_x(45)
rectangle.extrude(1)
