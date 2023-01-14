from BlenderProvider import *

Part("Cube").createCube(1,1,1)\
    .export("./exportedCube.stl")\
        .export("./exportedCube.obj")