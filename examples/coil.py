from codetocad import *


drumRadius = Dimension.fromString("5mm")
drumLength = Dimension.fromString("15.0 mm")

wireThickness = Dimension.fromString("1mm")
numberOfWindings = 10

grooveSpiral = Sketch("grooveSpiral").createSpiral(
    numberOfWindings, drumLength, drumRadius)

groove = Sketch("groove").createCircle(wireThickness/2)

grooveSpiral.sweep(groove)
