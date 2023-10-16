from codetocad import *

gear = Part("gear").create_gear(1, 0.1, 0.8, 0.2, 0.2)

gear2 = Part("gear2").create_gear(.5, 0.05, 0.4, 0.1, 0.2, "20d", 6)

gear2.translate_xyz(0, 1.515, 0)

Joint(gear, gear2).gear_ratio(2)
