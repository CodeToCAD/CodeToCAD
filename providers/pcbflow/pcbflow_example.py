from pcbflow import *

# create a 40 mm x 30 mm PCB with outline
brd = Board((40, 30))
brd.add_outline()
# fill the top and bottom copper layers and merge nets named "GND"
brd.fill_layer("GTL", "GND")
brd.fill_layer("GBL", "GND")
# save the PCB asset files
brd.save("mypcb")

brd.add_inner_copper_layer(layer_count=1)
