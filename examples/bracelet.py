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
    .createTorus(f"{bracelet['innerDiameter']/2}cm", f"{bracelet['outerDiameter']/2}cm") \
    .scaleZ(f"{bracelet['thickness']}cm").apply()  # Scale x,y by a scale factor of 1, so the number is unitless

Part("button") \
    .createCylinder(f"{button['diameter']/2}cm", f"{button['depth']}cm") \
    .rotateXYZ(90, 0, 0) \
    .translateXYZ(0, f"{buttonTranslation}cm", 0).apply()

Part("buttonInner") \
    .createCylinder(f"{buttonInner['diameter']/2}cm", f"{buttonInner['depth']}cm") \
    .rotateXYZ(90, 0, 0) \
    .translateXYZ(0, f"{buttonInnerYTranslation}cm", 0).apply()

Part("belt") \
    .createCylinder(f"{belt['outerDiameter']/2}cm", f"{belt['thickness']}cm").apply()

Part("beltInner") \
    .createCylinder(f"{belt['innerDiameter']/2}cm", f"{belt['thickness']}cm").apply()


Part("button")\
    .clone("booleanButton")

Part("bracelet")\
    .clone("booleanBracelet")

# Grouping

Scene().assignToGroup(["bracelet", "button", "belt"], "Bracelet")

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
Part("belt")\
    .clone("booleanbelt")

Part("bracelet")\
    .clone("booleanBracelet2")

Part("belt") \
    .intersect("booleanBracelet2")

Part("bracelet") \
    .subtract("booleanbelt")

# Remesh final shapes
Part("belt").remesh(strategy="edgesplit", amount=2)
Part("bracelet").remesh(strategy="edgesplit", amount=2)
Part("button").remesh(strategy="edgesplit", amount=2)
