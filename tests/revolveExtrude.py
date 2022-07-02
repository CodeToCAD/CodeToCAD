from CodeToCADBlenderProvider import *

Curve("centerline").createLine("1")
Curve("donut").createCircle("10cm").translate("-100cm,0,0").revolve("180d", Utilities.Axis.Y, "centerline")

Curve("ribbon").createArc("1cm", "45d").screw("180d", Utilities.Axis.Z, "2.5cm", 100)