from CodeToCAD import Analytics, Part, Sketch, Scene, Dimension, min, center, max as part_max, Joint, CodeToCADInterface

Scene.default().setDefaultUnit("mm")

tolerance = "0.15mm"


def createDShaft(shaftLength, radius, dProfileRadius):
    shaftLength = Dimension.fromString(shaftLength) + tolerance
    radius = Dimension.fromString(radius) + tolerance
    dProfileRadius = Dimension.fromString(dProfileRadius) + tolerance

    dProfileWidth = (radius - dProfileRadius) * 2

    shaft = Part("shaft").createCylinder(radius, shaftLength)

    dProfile = Part("dProfile").createCube(
        dProfileWidth, radius * 2, shaftLength)

    shaftLeftSide = shaft.createLandmark("left", min, center, center)
    dProfileLeftSide = dProfile.createLandmark("left", min, center, center)

    Joint(shaftLeftSide, dProfileLeftSide).limitLocationXYZ(0, 0, 0)

    shaft.subtract(dProfile)

    return shaft


def createDShaftSleeve(dShaft: CodeToCADInterface.Part, sleeveThickness):
    dShaftDiameter = dShaft.getDimensions().y

    sleeve = Part("sleeve").createCylinder(
        dShaftDiameter/2 + sleeveThickness, dShaft.getDimensions().z)

    sleeve.subtract(dShaft, isTransferLandmarks=True)

    return sleeve


def createKnob(radius):
    knob = Sketch("knob").createPolygon(7, radius, radius).extrude(radius*0.2)

    return knob


dShaft = createDShaft("13.65mm",  "5.9/2mm", "5.3/2mm")

sleeve = createDShaftSleeve(dShaft, "1.5mm")

knob = createKnob(sleeve.getDimensions().x)

Joint(sleeve.createLandmark("top", center, center, part_max), knob.createLandmark(
    "bottom", center, center, min)).limitLocationXYZ(0, 0, 0)

sleeve.union(knob).export("./appliance_knob.stl", scale=1000)
