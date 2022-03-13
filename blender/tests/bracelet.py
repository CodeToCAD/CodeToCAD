print("Starting bracelet.py")

import sys
from pathlib import Path
scriptDir = Path(__file__).parent.parent.absolute()
if scriptDir in sys.path:
    sys.path.remove(scriptDir)
sys.path.insert(0, str(scriptDir))


from textToBlender import shape, scene, BlenderLength, analytics

scene().setDefaultUnit(BlenderLength.CENTIMETERS)
scene().deleteGroup("Bracelet", True) \
    .createGroup("Bracelet")
scene().createGroup("BraceletBooleanShapes")

# Defining dimensions and calculated properties

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

# Creating the shapes we will use

shape("bracelet") \
.primitive("torus", [bracelet["innerDiameter"]/2,bracelet["outerDiameter"]/2, "cm"]) \
.scale("1,1,{}cm".format(bracelet["thickness"]))

shape("button")\
.primitive("cylinder", "{}/2,{}/2,cm".format(button["diameter"],button["depth"])) \
.rotate("90deg,0,0") \
.translate("0,{}cm,0".format(buttonTranslation))

shape("buttonInner") \
.primitive("cylinder", "{}/2,{}/2,cm".format(buttonInner["diameter"],buttonInner["depth"])) \
.rotate("90deg,0,0") \
.translate("0,{}cm,0".format(buttonInnerYTranslation))

shape("buttonCylinderForBoolean").cloneShape("button")

# Grouping

scene().assignShapeToGroup("bracelet", "Bracelet")
scene().assignShapeToGroup("button", "Bracelet")
scene().assignShapeToGroup("buttonInner", "Bracelet")

scene().assignShapeToGroup("buttonCylinderForBoolean", "BraceletBooleanShapes")

# Modifying the shapes

shape("bracelet") \
.subtract("buttonCylinderForBoolean")

shape("button")\
.intersect("bracelet")

shape("button") \
.subtract("buttonInner")