from CodeToCADBlenderProvider import *

Scene().setDefaultUnit("mm")

ellipseLeg = Sketch("ellipseLeg") \
    .createEllipse("14mm", "27mm") \
    .extrude("5/2in")
ellipseLeg_top = ellipseLeg.createLandmark("top", center, center, max)
ellipseLeg_bottom = ellipseLeg.createLandmark("bottom", center, center, min)

ellipseLegOuterCutout = Sketch("ellipseLegOuterCutout").createEllipse("14mm", "27mm") \
    .extrude("1in")
ellipseLegOuterCutout.hollow("3mm","3mm",0)
ellipseLegOuterCutout_top = ellipseLegOuterCutout.createLandmark("top", center, center, max)
ellipseLegOuterCutout.createLandmark("bottom", center, center, min)

Joint(ellipseLeg, ellipseLegOuterCutout, ellipseLeg_top, ellipseLegOuterCutout_top).translateLandmarkOntoAnother()

ellipseLeg.hollow("5mm","5mm",0)
ellipseLeg.subtract(ellipseLegOuterCutout)

leg2 = ellipseLeg.clone("Leg2")
Joint(ellipseLeg, leg2, "ellipseLegOuterCutout_bottom", "bottom").limitLocation(0,0,0,0,0,10).limitRotation(0,0,0)