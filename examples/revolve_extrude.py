from codetocad import *

Sketch("centerline").create_line("1")
Sketch("half-donut").create_circle("10cm").translate_xyz("-100cm",
                                                         0, 0).revolve("180d", "centerline",  "y")

Sketch("ribbon").create_arc("1cm", "45d").twist("180d", "2.5cm", 100, "z")
