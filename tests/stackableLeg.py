from CodeToCADBlenderProvider import *

Scene().setDefaultUnit("mm")

legExtrudePath = Sketch("legExtrudePath").createLine("5in").rotate(0,0,90)
stackingCutoutExtrudePath = Sketch("stackingCutoutExtrudePath").createLine("1in").rotate(0,0,90)

ellipseLeg = Sketch("ellipseLeg").createEllipse("14mm", "27mm") \
    .sweep("legExtrudePath", False) \
    .thicken("5mm")
ellipseLeg_top = ellipseLeg.createLandmark("top", center, center, max)
ellipseLeg_bottom = ellipseLeg.createLandmark("bottom", center, center, min)

ellipseLegOuterCutout = Sketch("ellipseLegOuterCutout").createEllipse("14+3mm", "27+3mm") \
    .sweep("stackingCutoutExtrudePath", False) \
    .thicken("5mm")
ellipseLegOuterCutout_top = ellipseLegOuterCutout.createLandmark("top", center, center, max)

Joint(ellipseLeg, ellipseLegOuterCutout, ellipseLeg_top, ellipseLegOuterCutout_top).translateLandmarkOntoAnother()

# Sketch("ellipseLeg").subtract("ellipseLegOuterCutout")

# shape("ellipseLeg").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLeg").scale("20+3mm,34+3mm,5in")
# shape("ellipseLegInner").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLegInner").scale("20mm,34mm,6in")

# shape("ellipseLeg").subtract("ellipseLegInner")
# shape("ellipseLeg").createLandmark("top", "center,center,max")

# scene().setVisible("ellipseLegInner", False)
# shape("ellipseLegCutout").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutout").scale("20+5mm,34+5mm,1in")
# shape("ellipseLegCutoutInner").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutoutInner").scale("20+2mm,34+2mm,2in")

# shape("ellipseLegCutout").subtract("ellipseLegCutoutInner").apply()
# shape("ellipseLegCutout").createLandmark("top", "center,center,max")

# scene().setVisible("ellipseLegCutoutInner", False)

# joint("ellipseLeg", "ellipseLegCutout", "top", "top").translateLandmarkOntoAnother()

# shape("ellipseLeg").subtract("ellipseLegCutout")

# scene().setVisible("ellipseLegCutout", False)
