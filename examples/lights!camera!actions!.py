from codetocad import *

Part("Cube").create_cube(2, 2, 2)
light = Light("Light").create_sun(75)
light.set_color(73, 222, 190).translate_xyz(10, 10, 5)

camera = Camera("Camera").createPerspective()
camera.setFocalLength(20).translate_xyz(0, -5, 5).rotate_xyz(45, 0, 0)
