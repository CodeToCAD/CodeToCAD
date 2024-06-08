# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.material_interface import MaterialInterface


class Material(
    MaterialInterface,
):

    def __init__(self, name: "str", description: "str| None" = None):

        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_preset(material_name: "PresetMaterial") -> "MaterialInterface":

        print("get_preset called", f": {material_name}")

        return Material("mat")

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ) -> Self:

        print("set_color called", f": {r_value}, {g_value}, {b_value}, {a_value}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_reflectivity(self, reflectivity: "float") -> Self:

        print("set_reflectivity called", f": {reflectivity}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_roughness(self, roughness: "float") -> Self:

        print("set_roughness called", f": {roughness}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_image_texture(self, image_file_path: "str") -> Self:

        print("set_image_texture called", f": {image_file_path}")

        return self
