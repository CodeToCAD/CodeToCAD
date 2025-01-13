from typing import Optional
from typing import Self
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.material_interface import MaterialInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Material(MaterialInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: "str| None" = None, description: "str| None" = None):
        self.name = name
        self.description = description

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ) -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_reflectivity(self, reflectivity: "float") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_roughness(self, roughness: "float") -> "Self":
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_image_texture(self, image_file_path: "str") -> "Self":
        return self
