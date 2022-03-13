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
scene().deleteGroup("BraceletBooleanShapes", True) \
    .createGroup("BraceletBooleanShapes")

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
.scale("1,1,{}cm".format(bracelet["thickness"]))  # Scale x,y by a scale factor of 1, so the number is unitless

shape("button")\
.primitive("cylinder", [button["diameter"]/2,button["depth"]/2, "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonTranslation,0,"cm"])

shape("buttonInner") \
.primitive("cylinder", [buttonInner["diameter"]/2, buttonInner["depth"]/2, "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonInnerYTranslation,0,"cm"])\
    .visibility(False)

shape("booleanButtonAndButtonInner")\
    .cloneShape("button")\
        .union("buttonInner")\
            .visibility(False)
shape("booleanBracelet")\
    .cloneShape("bracelet")\
            .visibility(False)

# Grouping

scene().assignShapeToGroup("bracelet", "Bracelet")
scene().assignShapeToGroup("button", "Bracelet")

scene().assignShapeToGroup("buttonInner", "BraceletBooleanShapes")
scene().assignShapeToGroup("booleanBracelet", "BraceletBooleanShapes")
scene().assignShapeToGroup("buttonAndButtonInner", "BraceletBooleanShapes")

# Modifying the shapes

shape("button")\
.intersect("booleanBracelet")

shape("button") \
.subtract("buttonInner")

shape("bracelet") \
.subtract("buttonAndButtonInner")