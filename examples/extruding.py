from codetocad import Sketch


rectangle = Sketch("cube")
r_wire = rectangle.create_rectangle(1, 1)
r_wire.extrude(1)


rectangle = Sketch("cube2")
rectangle.create_rectangle(1, 1)
rectangle.rotate_x(45)
print(rectangle)
r_wire1 = rectangle.get_wires()[0]
r_wire1.extrude(1)
