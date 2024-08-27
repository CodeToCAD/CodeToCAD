from codetocad import *

imported_cube = Part("Imported Cube").create_from_file("./importableCube.stl")

Part("ExportedCube").create_cube(1, 1, 1).export("./importableCube.stl").export("./exportedCube.obj")
