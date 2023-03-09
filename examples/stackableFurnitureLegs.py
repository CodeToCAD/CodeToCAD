from CodeToCAD import *

Scene().setDefaultUnit("mm")

ellipseLeg = Sketch("ellipseLeg") \
    .createEllipse("14mm", "27mm") \
    .extrude("5/2in")
ellipseLeg_top = ellipseLeg.createLandmark("top", center, center, max)
ellipseLeg_bottom = ellipseLeg.createLandmark("bottom", center, center, min)

ellipseLegOuterCutout = Sketch("ellipseLegOuterCutout").createEllipse("14mm", "27mm") \
    .extrude("1in")
ellipseLegOuterCutout.hollow("3mm", "3mm", 0)
ellipseLegOuterCutout_top = ellipseLegOuterCutout.createLandmark(
    "top", center, center, max)
ellipseLegOuterCutout.createLandmark("bottom", center, center, min)

Joint(ellipseLeg_top,
      ellipseLegOuterCutout_top).translateLandmarkOntoAnother()

ellipseLeg.hollow("5mm", "5mm", 0)
ellipseLeg.subtract(ellipseLegOuterCutout, isTransferLandmarks=True)

ellipseLeg2 = ellipseLeg.clone("Leg2")
Joint(ellipseLeg.getLandmark("ellipseLegOuterCutout_bottom"), ellipseLeg2.getLandmark("bottom")
      ).limitLocationXYZ(0, 0, 0).limitLocationZ(0, 10).limitRotationXYZ(0, 0, 0)


redMaterial = Material("red").setColor(0.709804, 0.109394, 0.245126, 0.9)
blueMaterial = Material("blue").setColor(0.0865257, 0.102776, 0.709804, 0.9)
ellipseLeg.setMaterial(redMaterial)
ellipseLeg2.setMaterial(blueMaterial)
