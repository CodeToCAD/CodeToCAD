from BlenderProvider import Part, Scene, Analytics
print("Starting bracelet.py")


Scene().setDefaultUnit("cm")
Scene().createGroup("Bracelet")
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

buttonInnerYTranslation = (
    bracelet["outerDiameter"] - buttonInner["depth"]) / 2

# Creating the shapes we will use

Part("bracelet") \
    ._createPrimitive("torus", [bracelet["innerDiameter"]/2, bracelet["outerDiameter"]/2, "cm"]) \
    .scale(1, 1, f"{bracelet['thickness']}cm")  # Scale x,y by a scale factor of 1, so the number is unitless

Part("button") \
    ._createPrimitive("cylinder", [button["diameter"]/2, button["depth"], "cm"]) \
    .rotate(90, 0, 0) \
    .translate(0, f"{buttonTranslation}cm", 0)

Part("buttonInner") \
    ._createPrimitive("cylinder", [buttonInner["diameter"]/2, buttonInner["depth"], "cm"]) \
    .rotate(90, 0, 0) \
    .translate(0, f"{buttonInnerYTranslation}cm", 0)

Part("belt") \
    ._createPrimitive("cylinder", [belt["outerDiameter"]/2, belt["thickness"], "cm"])

Part("beltInner") \
    ._createPrimitive("cylinder", [belt["innerDiameter"]/2, belt["thickness"], "cm"])

Part("booleanButton")\
    .cloneFrom("button")

Part("booleanBracelet")\
    .cloneFrom("bracelet")

# Grouping

Scene().assignToGroup("bracelet", "Bracelet")
Scene().assignToGroup("button", "Bracelet")
Scene().assignToGroup("belt", "Bracelet")

# Modifying the shapes

Part("button") \
    .intersect("booleanBracelet")

Part("button") \
    .subtract("buttonInner")

Part("bracelet") \
    .subtract("booleanButton")

Part("belt") \
    .subtract("beltInner")

# Save a copy of the belt to subtract from bracelet later
Part("booleanbelt")\
    .cloneFrom("belt")

Part("booleanBracelet2")\
    .cloneFrom("bracelet")

Part("belt") \
    .intersect("booleanBracelet2")

Part("bracelet") \
    .subtract("booleanbelt")

# Remesh final shapes
Part("belt").remesh(strategy="edgesplit", amount=2)
Part("bracelet").remesh(strategy="edgesplit", amount=2)
Part("button").remesh(strategy="edgesplit", amount=2)
