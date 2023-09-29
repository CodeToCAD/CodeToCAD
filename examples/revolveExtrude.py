from CodeToCAD import *

Sketch("centerline").createLine("1")
Sketch("half-donut").createCircle("10cm").translateXYZ("-100cm",
                                                       0, 0).revolve("180d", "centerline",  "y")

Sketch("ribbon").createArc("1cm", "45d").twist("180d", "2.5cm", 100, "z")
