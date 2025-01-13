from codetocad import *

imported_cube = Part.create_from_file("./importableCube.stl")

Part.create_cube(1, 1, 1).export("./exportedCube.stl").export("./exportedCube.obj")
