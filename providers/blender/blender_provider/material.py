from codetocad.interfaces.material_interface import MaterialInterface
from typing import Self
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ) -> "Self":
        set_material_color(self.name, r_value, g_value, b_value, a_value)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_reflectivity(self, reflectivity: "float") -> "Self":
        set_material_metallicness(self.name, reflectivity)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_roughness(self, roughness: "float") -> "Self":
        set_material_roughness(self.name, roughness)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_image_texture(self, image_file_path: "str") -> "Self":
        absoluteFilePath = get_absolute_filepath(image_file_path)
        add_texture_to_material(self.name, absoluteFilePath)
        return self
