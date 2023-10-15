from codetocad import *

Scene.default().setDefaultUnit("cm")
Scene.default().createGroup("Bracelet")


class Bracelet:
    outerDiameter = "161cm"
    innerDiameter = "81cm"
    thickness = "83cm"

    def create(self):
        bracelet = Part("bracelet") \
            .createTorus(Dimension.fromString(self.innerDiameter)/2, Dimension.fromString(self.outerDiameter)/2)
        bracelet.scaleZ(self.thickness)

        return bracelet


class Button:
    radius = "60/2cm"
    depth = "13.6cm"
    insetRadius = "20cm"
    insetDepth = "3cm"

    def create(self):
        button = Part("button") \
            .createCylinder(self.radius, self.depth)
        button_top = button.getLandmark("top")
        button.filletFaces("5cm", [button_top])
        button.hole(
            button_top, self.insetRadius, self.insetDepth)
        return button


class Belt:
    outerRadius = "162/2cm"
    innerRadius = "150/2cm"
    thickness = "30cm"

    def create(self):
        belt = Part("belt").createCylinder(
            self.outerRadius, self.thickness)
        belt.hole(belt.getLandmark("top"),
                  self.innerRadius, self.thickness)
        return belt


# MARK: Create components
bracelet = Bracelet().create()
button = Button().create()
belt = Belt().create()

# Mark: Joint the button to the front of the bracelet
Joint(bracelet.getLandmark("front"), button.getLandmark(
    "top")).limitLocationXYZ(0, 0, 0).limitRotationXYZ(90, 0, 0)
Joint(bracelet.getLandmark("center"), belt.getLandmark(
    "center")).limitLocationXYZ(0, 0, 0).limitRotationXYZ(0, 0, 0)

# Mark: subtract the button and belt from the bracelet:
bracelet.subtract(belt, deleteAfterSubtract=False)

bracelet.hole(belt.getLandmark("front"),
              button.getDimensions().x / 2, button.getDimensions().z, normalAxis="y", flipAxis=True)
belt.hole(belt.getLandmark("front"),
          button.getDimensions().x / 2, belt.getDimensions().z, normalAxis="y", flipAxis=True)

# Mark: Assign to a group:

Scene().assignToGroup([bracelet, button, belt], "Bracelet")

# Mark apply materials:
redMaterial = Material("red").setColor(181, 16, 4)
blueMaterial = Material("blue").setColor(19, 107, 181)

bracelet.setMaterial(redMaterial)
button.setMaterial(blueMaterial)
belt.setMaterial(blueMaterial)
