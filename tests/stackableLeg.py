from CodeToCADBlenderProvider import *

scene().setDefaultUnit("mm")

curve("legExtrudePath").createLine("5in").rotate("0,0,90d")
curve("stackingCutoutExtrudePath").createLine("1in").rotate("0,0,90d")

curve("ellipseLeg").createEllipse("14mm", "27mm") \
    .sweep("legExtrudePath", False) \
    .thicken("5mm") \
    .landmark("top","center,center,max")\
    .landmark("bottom","center,center,min")

curve("ellipseLegOuterCutout").createEllipse("14+3mm", "27+3mm") \
    .sweep("stackingCutoutExtrudePath", False) \
    .thicken("5mm") \
    .landmark("top","center,center,max")

joint("ellipseLeg", "ellipseLegOuterCutout", "top", "top").transformLandmarkOntoAnother()

curve("ellipseLeg").subtract("ellipseLegOuterCutout")

# shape("ellipseLeg").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLeg").scale("20+3mm,34+3mm,5in")
# shape("ellipseLegInner").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLegInner").scale("20mm,34mm,6in")

# shape("ellipseLeg").subtract("ellipseLegInner")
# shape("ellipseLeg").landmark("top", "center,center,max")

# scene().setShapeVisibility("ellipseLegInner", False)
# shape("ellipseLegCutout").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutout").scale("20+5mm,34+5mm,1in")
# shape("ellipseLegCutoutInner").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutoutInner").scale("20+2mm,34+2mm,2in")

# shape("ellipseLegCutout").subtract("ellipseLegCutoutInner").apply()
# shape("ellipseLegCutout").landmark("top", "center,center,max")

# scene().setShapeVisibility("ellipseLegCutoutInner", False)

# joint("ellipseLeg", "ellipseLegCutout", "top", "top").transformLandmarkOntoAnother()

# shape("ellipseLeg").subtract("ellipseLegCutout")

# scene().setShapeVisibility("ellipseLegCutout", False)
