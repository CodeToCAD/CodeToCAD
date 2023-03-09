from CodeToCAD import *

Curve("centerline").createLine("1")
Curve("half-donut").createCircle("10cm").translateXYZ("-100cm",
                                                      0, 0).revolve("180d", "centerline",  "y")

Curve("ribbon").createArc("1cm", "45d").twist("180d", "2.5cm", 100, "z")
