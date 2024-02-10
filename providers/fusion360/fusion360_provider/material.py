from typing import Optional

from codetocad.interfaces import MaterialInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

from providers.fusion360.fusion360_provider.fusion_actions.base import UiLogger

if TYPE_CHECKING:
    from . import Part

# The implementation diverges from Blender
# It's only set the body of the current object
# not creating a new material in Fusion 360

class Material(MaterialInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
        self.color = (0, 0, 0, 1)
        self.roughness = 1

    def assign_to_part(self, part_name_or_instance: PartOrItsName):
        from . import Part
        if isinstance(part_name_or_instance, str):
            part_name_or_instance = Part(part_name_or_instance)
        part_name_or_instance.set_material(self)
        return self

    def set_color(
        self,
        r_value: IntOrFloat,
        g_value: IntOrFloat,
        b_value: IntOrFloat,
        a_value: IntOrFloat = 1.0,
    ):
        if r_value < 1:
            r_value = round(r_value * 255)
        if g_value < 1:
            g_value = round(g_value * 255)
        if b_value < 1:
            b_value = round(b_value * 255)
        self.color = r_value, g_value, b_value, a_value
        return self

    def set_reflectivity(self, reflectivity: float):
        print("set_reflectivity called:", reflectivity)
        return self

    def set_roughness(self, roughness: float):
        self.roughness = roughness
        return self

    def set_image_texture(self, image_file_path: str):
        print("set_image_texture called:", image_file_path)
        return self

    @staticmethod
    def get_preset(material_name: Union[str, PresetMaterial]):
        if isinstance(material_name, str):
            try:
                material_name = getattr(PresetMaterial, material_name)
            except:
                raise Exception(f"Preset {material_name} not found!")

        if isinstance(material_name, PresetMaterial):
            material = Material(material_name.name)
            material.set_color(*material_name.color)
            material.set_reflectivity(material_name.reflectivity)
            material.set_roughness(material_name.roughness)

        return material
