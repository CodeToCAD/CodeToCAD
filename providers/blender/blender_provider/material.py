from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.utilities import get_absolute_filepath
from providers.blender.blender_provider.blender_actions.material import (
    add_texture_to_material,
    create_material,
    get_material,
    set_material_color,
    set_material_metallicness,
    set_material_roughness,
)


class Material(MaterialInterface):

    def __init__(self, name: "str| None" = None, description: "str| None" = None):
        self.name = name
        self.description = description
        try:
            get_material(self.name)
        except:  # noqa: E722
            create_material(self.name)

    @supported(SupportLevel.SUPPORTED)
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ):
        set_material_color(self.name, r_value, g_value, b_value, a_value)
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_reflectivity(self, reflectivity: "float"):
        set_material_metallicness(self.name, reflectivity)
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_roughness(self, roughness: "float"):
        set_material_roughness(self.name, roughness)
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_image_texture(self, image_file_path: "str"):
        absoluteFilePath = get_absolute_filepath(image_file_path)
        add_texture_to_material(self.name, absoluteFilePath)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED)
    def get_preset(material_name: "PresetMaterial"):
        if isinstance(material_name, str):
            try:
                material_name = getattr(PresetMaterial, material_name)
            except:  # noqa
                material = Material(material_name)
        if isinstance(material_name, PresetMaterial):
            material = Material(material_name.name)
            material.set_color(*material_name.color)
            material.set_reflectivity(material_name.reflectivity)
            material.set_roughness(material_name.roughness)
        return material
