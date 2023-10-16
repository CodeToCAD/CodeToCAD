from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import MaterialInterface, PartInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Material(MaterialInterface):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

        try:
            blender_actions.get_material(self.name)
        except:
            blender_actions.create_material(self.name)

    def assign_to_part(self, part_name: PartOrItsName
                       ):
        if isinstance(part_name, PartInterface):
            part_name = part_name.name
        blender_actions.set_material_to_object(self.name, part_name)
        return self

    def set_color(self, r_value: IntOrFloat, g_value: IntOrFloat, b_value: IntOrFloat, a_value: IntOrFloat = 1.0
                  ):
        blender_actions.set_material_color(
            self.name, r_value, g_value, b_value, a_value)
        return self

    def set_reflectivity(self, reflectivity: float):

        blender_actions.set_material_metallicness(self.name, reflectivity)

        return self

    def set_roughness(self, roughness: float):

        blender_actions.set_material_roughness(self.name, roughness)

        return self

    def add_image_texture(self, image_file_path: str
                          ):
        absoluteFilePath = getAbsoluteFilepath(image_file_path)

        blender_actions.add_texture_to_material(self.name, absoluteFilePath)
        return self
