from dataclasses import dataclass
from codetocad import *

blueMetallicMaterial = Material("blue").setColor(
    0.0865257, 0.102776, 0.709804, 0.8).setReflectivity(1.0)
redMetallicMaterial = Material("red").setColor(
    0.709804, 0.109394, 0.245126, 0.8).setReflectivity(1.0)


@dataclass
class Yoke:
    '''
    A class that creates the arm of a universal joint:
    ___  ____________  __
   ( )                   )  < hollow rod
    ⁻⁻⁻  ⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻⁻  ⁻⁻
        ^             ^
     setScrew       pinHole
    '''
    shaftRadius: Dimension
    wallThickness: Dimension
    shaftLength: Dimension

    pinArmLength: Dimension
    pinHoleRadius: Dimension
    setScrewRadius: Dimension

    isHollowed: bool = True

    def _createHollowRod(self, name: str, length: Dimension) -> Part:
        outerRadius = self.shaftRadius + self.wallThickness

        rod = Part(name).createCylinder(
            outerRadius, length)

        if self.isHollowed:
            rod.hollow(self.wallThickness, self.wallThickness,
                       self.wallThickness/2, flipAxis=True)

        _ = rod.createLandmark(
            "wallFront", center, f"min + {self.wallThickness/4}", max)

        return rod

    def _createShaftCoupling(self) -> Part:

        shaftCoupling = self._createHollowRod(
            "shaftCoupling", self.shaftLength)

        if self.isHollowed:
            shaftCoupling.hole(shaftCoupling.getLandmark(PresetLandmark.back),
                               self.setScrewRadius, shaftCoupling.getDimensions().y, normalAxis="y")

        return shaftCoupling

    def _createPinArm(self) -> Part:

        pinArm = self._createHollowRod("pinArm", self.pinArmLength)

        pinArmSize = pinArm.getDimensions()

        pinArmDiscardAmount = 1/15

        pinArm.subtract(
            Part("pinArmDiscard").createCube(
                pinArmSize.x,
                pinArmSize.y * (
                    1-pinArmDiscardAmount),
                pinArmSize.z + "1mm"
            ).translateY(pinArmSize.y * pinArmDiscardAmount)
        )

        pinArm.rotateY(180)

        pinLocation = pinArm.createLandmark(
            "pin", center, min, "max -  (max-min) * 1/4")

        pinArm.hole(pinLocation,
                    self.pinHoleRadius, pinArmSize.y, normalAxis="y", flipAxis=True)

        # pinArm.filletFaces(
        #     "25mm",
        #     [pinArm.getLandmark(PresetLandmark.top)]
        # )

        return pinArm

    def create(self, name: str) -> Part:

        shaftCoupling = self._createShaftCoupling()

        pinArm = self._createPinArm()

        Joint(
            shaftCoupling.getLandmark("wallFront"),
            pinArm.getLandmark(
                "wallFront")
        ).limitLocationXYZ(0, 0, 0)

        pinArm.mirror(shaftCoupling, "y", None)

        shaftCoupling.getLandmark(PresetLandmark.top)

        yoke = shaftCoupling.union(
            pinArm,
            isTransferLandmarks=True
        )

        # shaftCoupling.filletFaces(
        #     "25mm", [shaftCoupling.getLandmark(PresetLandmark.top)])

        yoke.rename(name)

        yoke.setMaterial(blueMetallicMaterial)

        return yoke


@dataclass
class Cross:

    width: Dimension
    pinRadius: Dimension
    pinLength: Dimension

    def create(self, name: str) -> Part:

        core = Part(name).createCube(self.width, self.width, self.width)

        pin = Part("pin").createCylinder(self.pinRadius, self.pinLength)

        Joint(
            core.getLandmark(PresetLandmark.top),
            pin.getLandmark(
                PresetLandmark.bottom)
        ).limitLocationXYZ(0, 0, 0)

        pin.circularPattern(4, 90, core, normalDirectionAxis="y")

        core = core.union(pin)

        core.rotateX(90)

        core.setMaterial(redMetallicMaterial)

        return core


def createUniversalJoint():

    shaftRadius = Dimension.fromString("5mm")
    wallThickness = Dimension.fromString("3mm")
    shaftLength = Dimension.fromString("15mm")
    pinArmLength = Dimension.fromString("13mm")
    pinHoleRadius = Dimension.fromString("2mm")
    setScrewRadius = Dimension.fromString("3mm")

    yokeBottom = Yoke(
        shaftRadius=shaftRadius,
        wallThickness=wallThickness,
        shaftLength=shaftLength,
        pinArmLength=pinArmLength,
        pinHoleRadius=pinHoleRadius,
        setScrewRadius=setScrewRadius
    ).create("yokeBottom")

    yokeTop = Yoke(
        shaftRadius=shaftRadius,
        wallThickness=wallThickness,
        shaftLength=shaftLength,
        pinArmLength=pinArmLength,
        pinHoleRadius=pinHoleRadius,
        setScrewRadius=setScrewRadius
    ).create("yokeTop")
    yokeTop.rotateY(180)
    yokeTop.rotateZ(90)

    cross = Cross(
        width=shaftRadius,
        pinRadius=pinHoleRadius,
        pinLength=shaftRadius/2 + wallThickness
    ).create("cross")

    Joint(
        cross.getLandmark(PresetLandmark.front),
        yokeBottom.getLandmark("pinArm_pin")
    ).limitLocationXYZ(0, 0, 0).limitRotationXYZ(0, None, 0).limitRotationY(-45, 45)

    Joint(
        cross.getLandmark(PresetLandmark.right),
        yokeTop.getLandmark("pinArm_pin")
    ).limitLocationXYZ(0, 0, 0).limitRotationXYZ(None, 0, 0).limitRotationX(-45, 45)


if __name__ == "__main__":

    createUniversalJoint()
