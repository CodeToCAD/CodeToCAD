from codetocad import *

Wire("a", native_instance="b")

red_material = Material("red").set_color(0.709804, 0.109394, 0.245126, 0.8)
blue_material = Material("blue").set_color(0.0865257, 0.102776, 0.709804, 0.8)
green_material = Material("green").set_color(0.118213, 0.709804, 0.109477, 0.8)


a = Part("a").create_cube(1, 1, 1).set_material(blue_material)
a_top = a.create_landmark("top", "center", "center", "max")
a_bottom = a.create_landmark("bottom", "center", "center", "min")

b = Part("b").create_cube(1, 1, 1).set_material(red_material)
b_bottom = b.create_landmark("bottom", "center", "center", "min")

c = Part("c").create_cube(1, 1, 1).set_material(green_material)
c_top = c.create_landmark("top", "center", "center", "max")

# Joint("a","b","top","bottom").translate_landmark_onto_another()

Joint(a_top, b_bottom).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, 0, 0)

Joint(a_bottom, c_top).limit_location_xyz(0, 0, 0).limit_rotation_xyz(0, 0, 0)
