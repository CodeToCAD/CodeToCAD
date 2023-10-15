from codetocad import *

importedCube = Part("Imported Cube").createFromFile("./importableCube.stl")

Part("ExportedCube").createCube(1, 1, 1)\
    .export("./exportedCube.stl")\
    .export("./exportedCube.obj")
