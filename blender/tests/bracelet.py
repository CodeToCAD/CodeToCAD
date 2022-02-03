import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))


import bpy
from textToBlender import shape, scene, BlenderLength

scene().setDefaultUnit(BlenderLength.CENTIMETERS) \
    .deleteGroup("Bracelet", True) \
    .createGroup("Bracelet")


# in mm
bracelet = {
    "outerDiameter": 161,
    "innerDiameter": 81,
    "thickness": 83
}
button = {
    "diameter": 60,
    "depth": 13.6
}
buttonInner = {
    "diameter": 40,
    "depth": 5
}

shape("bracelet").primitive("torus", "{}/2,{}/2,cm".format(bracelet["innerDiameter"],bracelet["outerDiameter"])).scale("1,1,{}cm".format(bracelet["thickness"]))