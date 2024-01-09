from codetocad import *
from codetocad.enums import PresetMaterial

c1 = Part("c1").create_cube(1, 1, 1)
c1.set_material(PresetMaterial.blue)

c2 = Part("c2").create_cylinder(0.5, 1)
c2.set_material(PresetMaterial.red)
c2.translate_x(0.5)

c3 = Part("c3").create_cube(1, 1, 1)
c3.set_material(PresetMaterial.yellow)
c3.translate_x(-0.5)

c2.union(c1)
c2.union(c3)
