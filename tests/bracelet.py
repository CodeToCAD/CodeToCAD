print("Starting bracelet.py")

from CodeToCADBlenderProvider import Part, Scene, Analytics

Scene().setDefaultUnit("cm")
Scene().deleteGroup("Bracelet", True) \
    .createGroup("Bracelet")
Scene().deleteGroup("BraceletBooleanShapes", True) \
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
belt = {
    "outerDiameter": 162,
    "innerDiameter": 150,
    "thickness": 30
}

# TODO: translation calculations should be obsolete with the introduction of landmarks and joints
buttonTranslation = (bracelet["outerDiameter"] - button["depth"]) / 2

buttonInnerYTranslation = (bracelet["outerDiameter"] - buttonInner["depth"]) / 2

# Creating the shapes we will use

Part("bracelet") \
.createPrimitive("torus", [bracelet["innerDiameter"]/2,bracelet["outerDiameter"]/2, "cm"]) \
.scale("1,1,{}cm".format(bracelet["thickness"])) # Scale x,y by a scale factor of 1, so the number is unitless

Part("button") \
.createPrimitive("cylinder", [button["diameter"]/2,button["depth"], "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonTranslation,0,"cm"])

Part("buttonInner") \
.createPrimitive("cylinder", [buttonInner["diameter"]/2, buttonInner["depth"], "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonInnerYTranslation,0,"cm"])

Part("belt") \
.createPrimitive("cylinder", [belt["outerDiameter"]/2,belt["thickness"], "cm"])

Part("beltInner") \
.createPrimitive("cylinder", [belt["innerDiameter"]/2,belt["thickness"], "cm"])

Part("booleanButton")\
    .clone("button")

Part("booleanBracelet")\
    .clone("bracelet")

# Grouping

Scene().assignToGroup("bracelet", "Bracelet")
Scene().assignToGroup("button", "Bracelet")
Scene().assignToGroup("belt", "Bracelet")

Scene().assignToGroup("beltInner", "BraceletBooleanShapes").setVisibility("beltInner", False)
Scene().assignToGroup("buttonInner", "BraceletBooleanShapes").setVisibility("buttonInner", False)
Scene().assignToGroup("booleanBracelet", "BraceletBooleanShapes").setVisibility("booleanBracelet", False)
Scene().assignToGroup("booleanButton", "BraceletBooleanShapes").setVisibility("booleanButton", False)

# Modifying the shapes

Part("button") \
    .intersect("booleanBracelet")

Part("button") \
    .subtract("buttonInner")

Part("bracelet") \
    .subtract("booleanButton") 

Part("belt") \
    .subtract("beltInner")

## Save a copy of the belt to subtract from bracelet later
Part("booleanbelt")\
    .clone("belt")
    
Part("booleanBracelet2")\
    .clone("bracelet")

Scene().assignToGroup("booleanbelt", "BraceletBooleanShapes").setVisibility("booleanbelt", False)
    
Scene().assignToGroup("booleanBracelet2", "BraceletBooleanShapes").setVisibility("booleanBracelet2", False)
    
Part("belt") \
    .intersect("booleanBracelet2")

Part("bracelet") \
    .subtract("booleanbelt")

# Remesh final shapes
Part("belt").remesh()
Part("bracelet").remesh()
Part("button").remesh()