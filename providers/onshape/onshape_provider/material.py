from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Material(MaterialInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: "str", description: "str| None" = None):
        self.name = name
        self.description = description

    @supported(SupportLevel.UNSUPPORTED)
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_reflectivity(self, reflectivity: "float"):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_roughness(self, roughness: "float"):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_image_texture(self, image_file_path: "str"):
        return self

    @staticmethod
    @supported(SupportLevel.UNSUPPORTED)
    def get_preset(material_name: "PresetMaterial") -> "MaterialInterface":
        print("get_preset called", f": {parameter}")
        return Material("mat")
