from CodeToCAD import *
from dShaft import DShaft


def createDShaftSleeve(dShaft: CodeToCADInterface.Part, sleeveThickness):
    dShaftDiameter = dShaft.getDimensions().y

    sleeve = Part("sleeve").createCylinder(
        dShaftDiameter/2 + sleeveThickness, dShaft.getDimensions().z)

    sleeve.subtract(dShaft, isTransferLandmarks=True)

    return sleeve


def createKnob(radius):
    knob = Sketch("knob").createPolygon(7, radius, radius).extrude(radius*0.2)

    return knob


if __name__ == "__main__":

    Scene.default().setDefaultUnit("mm")

    shaftLength = Dimension.fromString("13.65mm")
    radius = Dimension.fromString("5.9/2mm")
    dProfileRadius = Dimension.fromString("5.3/2mm")
    dProfileLength = shaftLength
    tolerance = Dimension.fromString("0.15mm")

    dShaft = DShaft(shaftLength=shaftLength, radius=radius,
                    dProfileRadius=dProfileRadius, dProfileLength=dProfileLength, tolerance=tolerance).create("shaft")

    sleeve = createDShaftSleeve(dShaft, "1.5mm")

    knob = createKnob(sleeve.getDimensions().x)

    Joint(sleeve.createLandmark("top", center, center, max), knob.createLandmark(
        "bottom", center, center, min)).limitLocationXYZ(0, 0, 0)

    sleeve.union(knob)
    # sleeve.export("./appliance_knob.stl", scale=1000)
