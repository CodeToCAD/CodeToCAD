from codetocad import *

wall_thickness = Dimension.from_string(0.1)

hollow_cube = Part.create_cube(1, 1, 0.1)
hollow_cube.hollow(wall_thickness * 2, wall_thickness * 2, 0)

hollow_cube.translate_x(3)

c1 = Part.create_cube(1, 1, 1)
c1.translate_x(2)
c1.translate_y(2)
c1.translate_z(2)

hollow_cube_left = hollow_cube.get_landmark(PresetLandmark.left)
hollow_cube_left_inner = hollow_cube_left.clone("left_inner")
hollow_cube_left_inner = hollow_cube_left.clone(
    "left_inner_2", offset=[wall_thickness, 0, 0]
)

hollow_cube_left_inner = hollow_cube_left.clone("left_inner_3", new_parent=c1)
