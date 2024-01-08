from codetocad import *
from codetocad.enums import PresetMaterial

Part("cube").create_cube(1, 1, 1).set_material(PresetMaterial.blue)

Part("Cylinder").create_cylinder(1, 4).set_material(PresetMaterial.red).translate_xyz(
    5, 0, 0
)
