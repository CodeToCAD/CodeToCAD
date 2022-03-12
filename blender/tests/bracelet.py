import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()

if scriptDir not in sys.path:
    sys.path.insert(0, str(scriptDir))

from textToBlender import shape, scene, BlenderLength, analytics

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

# TODO: translation calculations should be obsolete with the introduction of landmarks and joints
buttonTranslation = (bracelet["outerDiameter"]/2) - (button["depth"]/2)

buttonInnerYTranslation = (bracelet["outerDiameter"]/2 - buttonInner["depth"]/2)

shape("bracelet") \
.primitive("torus", "{}/2,{}/2,cm".format(bracelet["innerDiameter"],bracelet["outerDiameter"])) \
.scale("1,1,{}cm".format(bracelet["thickness"]))

shape("button")\
.primitive("cylinder", "{}/2,{}/2,cm".format(button["diameter"],button["depth"])) \
.rotate("90deg,0,0") \
.translate("0,{}cm,0".format(buttonTranslation))

shape("buttonInner") \
.primitive("cylinder", "{}/2,{}/2,cm".format(buttonInner["diameter"],buttonInner["depth"])) \
.rotate("90deg,0,0") \
.translate("0,{}cm,0".format(buttonInnerYTranslation))

shape("bracelet") \
.subtract("button")

shape("button")\
.intersect("bracelet")

shape("button") \
.subtract("buttonInner")