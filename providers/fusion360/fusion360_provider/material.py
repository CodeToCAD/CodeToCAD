from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.codetocad_types import *

# The implementation diverges from Blender
# It's only set the body of the current object
# not creating a new material in Fusion 360


class Material(MaterialInterface):

    def __init__(self, name: "str", description: "str| None" = None):
        self.name = name
        self.description = description
        self.color = (0, 0, 0, 1)
        self.roughness = 1

    @supported(SupportLevel.PARTIAL, "Implementation needs improvement.")
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ):
        if r_value < 1:
            r_value = round(r_value * 255)
        if g_value < 1:
            g_value = round(g_value * 255)
        if b_value < 1:
            b_value = round(b_value * 255)
        self.color = (r_value, g_value, b_value, a_value)
        return self

    @supported(SupportLevel.PLANNED)
    def set_reflectivity(self, reflectivity: "float"):
        print("set_reflectivity called:", reflectivity)
        return self

    @supported(SupportLevel.PLANNED)
    def set_roughness(self, roughness: "float"):
        self.roughness = roughness
        return self

    @supported(SupportLevel.PLANNED)
    def set_image_texture(self, image_file_path: "str"):
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED)
    def get_preset(material_name: "PresetMaterial"):
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
