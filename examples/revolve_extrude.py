from codetocad import *

Sketch("centerline").create_line([0, 0, 0], [0, 1, 0])

half_donut = Sketch("half-donut")
half_donut.create_circle("10cm")
half_donut.translate_xyz("-100cm", 0, 0).revolve("180d", "centerline", "y")

ribbon = Sketch("ribbon")
ribbon.create_arc([0, 0, 0], ["1cm", "1cm", 0], 0)
ribbon.twist("180d", "2.5cm", 100, "z")
