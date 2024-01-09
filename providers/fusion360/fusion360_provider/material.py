from typing import Optional

from codetocad.interfaces import MaterialInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part


class Material(MaterialInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def assign_to_part(self, part_name_or_instance: PartOrItsName):
        print("assign_to_part called:", part_name_or_instance)
        return self

    def set_color(
        self,
        r_value: IntOrFloat,
        g_value: IntOrFloat,
        b_value: IntOrFloat,
        a_value: IntOrFloat = 1.0,
    ):
        print("set_color called:", r_value, g_value, b_value, a_value)
        return self

    def set_reflectivity(self, reflectivity: float):
        print("set_reflectivity called:", reflectivity)
        return self

    def set_roughness(self, roughness: float):
        print("set_roughness called:", roughness)
        return self

    def set_image_texture(self, image_file_path: str):
        print("set_image_texture called:", image_file_path)
        return self

    @classmethod
    def get_sample_mat_instance(cls):
        return cls(name="myMaterial", description="material is created for testing")