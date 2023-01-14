from BlenderProvider import *

Curve("centerline").createLine("1")
Curve("half-donut").createCircle("10cm").translate("-100cm",0,0).revolve("180d", "y", "centerline")

Curve("ribbon").createArc("1cm", "45d").screw("180d", "z", "2.5cm", 100)