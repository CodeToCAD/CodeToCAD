from CodeToCAD import *

Part("Cube").createCube(2, 2, 2)
light = Light("Light").createSun(75)
light.setColor(73, 222, 190).translateXYZ(10, 10, 5)

camera = Camera("Camera").createPerspective()
camera.setFocalLength(20).translateXYZ(0, -5, 5).rotateXYZ(45, 0, 0)
