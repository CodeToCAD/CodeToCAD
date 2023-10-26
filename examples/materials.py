from codetocad import *

material = Material("material").set_color(169, 76, 181, 0.8)
Part("Cube").create_cube(1, 1, 1).set_material(material)

material_with_texture = Material("materialWithTexture").set_image_texture("./bark.jpg")
Part("Cylinder").create_cylinder(1, 4).set_material(
    material_with_texture
).translate_xyz(5, 0, 0)
