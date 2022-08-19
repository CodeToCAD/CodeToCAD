from CodeToCADBlenderProvider import *

Part("Linear Cube").createCube("5cm","5cm","5cm").linearPattern(10, "x", "7cm")

Part("Circular spheres").createSphere(1).translate(0,5,0).circularPattern(4,"90d","z","Linear Cube").circularPattern(6,f"{360/6}d","x","Linear Cube")