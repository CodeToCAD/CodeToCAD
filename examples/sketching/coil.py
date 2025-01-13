from codetocad import *


drum_radius = Dimension.from_string("5mm")
drum_length = Dimension.from_string("15.0 mm")

wire_thickness = Dimension.from_string("1mm")
number_of_windings = 10

groove_spiral = Sketch.create_spiral(number_of_windings, drum_length, drum_radius)

groove = Sketch.create_circle(wire_thickness / 2)

groove_spiral.sweep(groove)
