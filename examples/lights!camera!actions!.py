from codetocad import *

Part("Cube").create_cube(2, 2, 2)
light = Light("Light").create_sun(75)
light.set_color(73, 222, 190).translate_xyz(10, 10, 5)

camera = Camera("Camera").create_perspective()
camera.set_focal_length(20).translate_xyz(0, -5, 5).rotate_xyz(45, 0, 0)
