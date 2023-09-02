from dataclasses import dataclass
from CodeToCAD import *


@dataclass
class DShaft:

    shaftLength: Dimension
    radius: Dimension
    dProfileRadius: Dimension
    dProfileLength: Dimension
    tolerance: Dimension = Dimension(0)

    def create(self, name, isDShaftBothSides=False) -> CodeToCADInterface.Part:
        shaftLength = self.shaftLength
        radius = self.radius - self.tolerance
        dProfileRadius = self.dProfileRadius - self.tolerance

        dProfileWidth = (radius - dProfileRadius) * 2

        shaft = Part(name).createCylinder(radius, shaftLength)

        dProfile = Part("dProfile").createCube(
            dProfileWidth, radius * 2, self.dProfileLength)

        shaftLeftSide = shaft.getLandmark(PresetLandmark.leftTop)
        dProfileLeftSide = dProfile.getLandmark(PresetLandmark.leftTop)

        Joint(shaftLeftSide, dProfileLeftSide).limitLocationXYZ(0, 0, 0)

        if isDShaftBothSides:
            dProfile.mirror(shaft, "z", None)

        shaft.subtract(dProfile)

        shaft.getLandmark(PresetLandmark.front).delete()

        return shaft


if __name__ == "__main__":
    shaftLength = Dimension.fromString("13.65mm")
    radius = Dimension.fromString("5.9/2mm")
    dProfileRadius = Dimension.fromString("5.3/2mm")
    dProfileLength = shaftLength/2
    tolerance = Dimension.fromString("0.15mm")

    dShaft = DShaft(shaftLength=shaftLength, radius=radius,
                    dProfileRadius=dProfileRadius, dProfileLength=dProfileLength, tolerance=tolerance).create("shaft")
