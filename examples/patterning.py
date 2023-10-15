from codetocad import *

linearCube = Part("Linear Cube").createCube(
    "5cm", "5cm", "5cm").linearPattern(10, "7cm", "x")

Part("Circular spheres").createSphere(1).translateXYZ(0, 5, 0).circularPattern(
    4, "90d", linearCube, "z").circularPattern(6, f"{360/6}d", linearCube, "x")
