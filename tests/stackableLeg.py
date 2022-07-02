from CodeToCADBlenderProvider import *

Scene().setDefaultUnit("mm")

Sketch("legExtrudePath").createLine("5in").rotate("0,0,90d")
Sketch("stackingCutoutExtrudePath").createLine("1in").rotate("0,0,90d")

Sketch("ellipseLeg").createEllipse("14mm", "27mm") \
    .sweep("legExtrudePath", False) \
    .thicken("5mm") \
    .landmark("top","center,center,max")\
    .landmark("bottom","center,center,min")

Sketch("ellipseLegOuterCutout").createEllipse("14+3mm", "27+3mm") \
    .sweep("stackingCutoutExtrudePath", False) \
    .thicken("5mm") \
    .landmark("top","center,center,max")

Joint("ellipseLeg", "ellipseLegOuterCutout", "top", "top").transformLandmarkOntoAnother()

# Sketch("ellipseLeg").subtract("ellipseLegOuterCutout")

# shape("ellipseLeg").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLeg").scale("20+3mm,34+3mm,5in")
# shape("ellipseLegInner").createPrimitive("cylinder", "1,1,1").remesh().apply()
# shape("ellipseLegInner").scale("20mm,34mm,6in")

# shape("ellipseLeg").subtract("ellipseLegInner")
# shape("ellipseLeg").landmark("top", "center,center,max")

# scene().setVisibility("ellipseLegInner", False)
# shape("ellipseLegCutout").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutout").scale("20+5mm,34+5mm,1in")
# shape("ellipseLegCutoutInner").createPrimitive("cylinder", "1,1,1")
# shape("ellipseLegCutoutInner").scale("20+2mm,34+2mm,2in")

# shape("ellipseLegCutout").subtract("ellipseLegCutoutInner").apply()
# shape("ellipseLegCutout").landmark("top", "center,center,max")

# scene().setVisibility("ellipseLegCutoutInner", False)

# joint("ellipseLeg", "ellipseLegCutout", "top", "top").transformLandmarkOntoAnother()

# shape("ellipseLeg").subtract("ellipseLegCutout")

# scene().setVisibility("ellipseLegCutout", False)
