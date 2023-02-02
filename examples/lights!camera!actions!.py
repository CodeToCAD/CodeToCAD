from CodeToCAD import *
from BlenderProvider import *

Part("Cube").createCube(2, 2, 2)
light = Light("Light").createSun(75)
light.setColor(73, 222, 190).translate(10, 10, 5)
