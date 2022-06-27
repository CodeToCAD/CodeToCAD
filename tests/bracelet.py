print("Starting bracelet.py")

from CodeToCADBlenderProvider import shape, scene, BlenderLength, analytics

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
belt = {
    "outerDiameter": 162,
    "innerDiameter": 150,
    "thickness": 30
}

# TODO: translation calculations should be obsolete with the introduction of landmarks and joints
buttonTranslation = (bracelet["outerDiameter"] - button["depth"]) / 2

buttonInnerYTranslation = (bracelet["outerDiameter"] - buttonInner["depth"]) / 2

# Creating the shapes we will use

shape("bracelet") \
.createPrimitive("torus", [bracelet["innerDiameter"]/2,bracelet["outerDiameter"]/2, "cm"]) \
.scale("1,1,{}cm".format(bracelet["thickness"])) # Scale x,y by a scale factor of 1, so the number is unitless

shape("button") \
.createPrimitive("cylinder", [button["diameter"]/2,button["depth"], "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonTranslation,0,"cm"])

shape("buttonInner") \
.createPrimitive("cylinder", [buttonInner["diameter"]/2, buttonInner["depth"], "cm"]) \
.rotate("90deg,0,0") \
.translate([0,buttonInnerYTranslation,0,"cm"])

shape("belt") \
.createPrimitive("cylinder", [belt["outerDiameter"]/2,belt["thickness"], "cm"])

shape("beltInner") \
.createPrimitive("cylinder", [belt["innerDiameter"]/2,belt["thickness"], "cm"])

shape("booleanButton")\
    .cloneShape("button")

shape("booleanBracelet")\
    .cloneShape("bracelet")

# Grouping

scene().assignShapeToGroup("bracelet", "Bracelet")
scene().assignShapeToGroup("button", "Bracelet")
scene().assignShapeToGroup("belt", "Bracelet")

scene().assignShapeToGroup("beltInner", "BraceletBooleanShapes").setShapeVisibility("beltInner", False)
scene().assignShapeToGroup("buttonInner", "BraceletBooleanShapes").setShapeVisibility("buttonInner", False)
scene().assignShapeToGroup("booleanBracelet", "BraceletBooleanShapes").setShapeVisibility("booleanBracelet", False)
scene().assignShapeToGroup("booleanButton", "BraceletBooleanShapes").setShapeVisibility("booleanButton", False)

# Modifying the shapes

shape("button") \
    .intersect("booleanBracelet")

shape("button") \
    .subtract("buttonInner")

shape("bracelet") \
    .subtract("booleanButton") 

shape("belt") \
    .subtract("beltInner")

## Save a copy of the belt to subtract from bracelet later
shape("booleanbelt")\
    .cloneShape("belt")
    
shape("booleanBracelet2")\
    .cloneShape("bracelet")

scene().assignShapeToGroup("booleanbelt", "BraceletBooleanShapes").setShapeVisibility("booleanbelt", False)
    
scene().assignShapeToGroup("booleanBracelet2", "BraceletBooleanShapes").setShapeVisibility("booleanBracelet2", False)
    
shape("belt") \
    .intersect("booleanBracelet2")

shape("bracelet") \
    .subtract("booleanbelt")

# Remesh final shapes
shape("belt").remesh()
shape("bracelet").remesh()
shape("button").remesh()