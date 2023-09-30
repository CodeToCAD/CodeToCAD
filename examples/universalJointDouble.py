from CodeToCAD import *
from universalJoint import Yoke, Cross


def createDoubleUniversalJoint():

    shaftRadius = Dimension.fromString("5mm")
    wallThickness = Dimension.fromString("3mm")
    shaftLength = Dimension.fromString("15mm")
    centerYolkLength = Dimension.fromString("5mm")
    pinArmLength = Dimension.fromString("13mm")
    pinHoleRadius = Dimension.fromString("2mm")
    setScrewRadius = Dimension.fromString("3mm")

    yokeCenter = Yoke(
        shaftRadius=shaftRadius,
        wallThickness=wallThickness,
        shaftLength=centerYolkLength,
        pinArmLength=pinArmLength,
        pinHoleRadius=pinHoleRadius,
        setScrewRadius=setScrewRadius,
        isHollowed=False
    ).create("yokeCenter")
    yokeCenterPinTop = yokeCenter.getLandmark("pinArm_pin")
    yokeCenterPinTopLocation = yokeCenterPinTop.getLocationLocal()
    yokeCenterBottomZ = yokeCenter.getLandmark(
        PresetLandmark.bottom).getLocationLocal().z
    yokeCenter.mirror(yokeCenter.getLandmark(
        PresetLandmark.bottom), "z", None)
    yokeCenterPinBottom = yokeCenter.createLandmark(
        "pinBottom", yokeCenterPinTopLocation.x, yokeCenterPinTopLocation.y, yokeCenterPinTopLocation.z * -1 + yokeCenterBottomZ*2)

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

    yokeBottom = Yoke(
        shaftRadius=shaftRadius,
        wallThickness=wallThickness,
        shaftLength=shaftLength,
        pinArmLength=pinArmLength,
        pinHoleRadius=pinHoleRadius,
        setScrewRadius=setScrewRadius
    ).create("yokeBottom")
    yokeBottom.rotateZ(90)

    cross1 = Cross(
        width=shaftRadius,
        pinRadius=pinHoleRadius,
        pinLength=shaftRadius/2 + wallThickness
    ).create("cross1")

    cross2 = Cross(
        width=shaftRadius,
        pinRadius=pinHoleRadius,
        pinLength=shaftRadius/2 + wallThickness
    ).create("cross2")

    Joint(
        cross1.getLandmark(PresetLandmark.right),
        yokeTop.getLandmark("pinArm_pin"),
    ).limitRotationXYZ(None, 0, 0).limitRotationX(-45, 45).limitLocationXYZ(0, 0, 0)

    Joint(
        cross1.getLandmark(PresetLandmark.front), yokeCenterPinTop
    ).limitRotationXYZ(0, None, 0).limitRotationY(-45, 45).limitLocationXYZ(0, 0, 0)

    Joint(yokeCenterPinBottom,
          cross2.getLandmark(PresetLandmark.front),
          ).limitRotationXYZ(None, 0, 0).limitRotationX(-45, 45).limitLocationXYZ(0, 0, 0)

    Joint(
        cross2.getLandmark(
            PresetLandmark.right), yokeBottom.getLandmark("pinArm_pin")
    ).limitRotationXYZ(None, 0, 0).limitRotationX(-45, 45).limitLocationXYZ(0, 0, 0)


if __name__ == "__main__":

    createDoubleUniversalJoint()
