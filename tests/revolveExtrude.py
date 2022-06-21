from CodeToCADBlenderProvider import *

curve("centerline").createLine("1")
curve("donut").createCircle("10cm").translate("-100cm,0,0").revolve("180d", Axis.Y, "centerline")

curve("ribbon").createArc("1cm", "45d").screw("180d", Axis.Z, "2.5cm", 100)