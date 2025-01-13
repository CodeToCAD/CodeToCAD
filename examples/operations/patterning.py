from codetocad import *

linear_cube = Part.create_cube("5cm", "5cm", "5cm").linear_pattern(10, "7cm", "x")

Part.create_sphere(1).translate_xyz(0, 5, 0).circular_pattern(
    4, "90d", linear_cube, "z"
).circular_pattern(6, f"{360/6}d", linear_cube, "x")
