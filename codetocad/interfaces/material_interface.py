# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import PartInterface


class MaterialInterface(metaclass=ABCMeta):
    """Materials affect the appearance and simulation properties of the parts."""

    name: str
    description: Optional[str] = None

    @abstractmethod
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    @abstractmethod
    def assign_to_part(self, part_name_or_instance: PartOrItsName):
        """
        Assigns the material to a part.
        """

        print(
            "assign_to_part is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_color(
        self,
        r_value: IntOrFloat,
        g_value: IntOrFloat,
        b_value: IntOrFloat,
        a_value: IntOrFloat = 1.0,
    ):
        """
        Set the RGBA color of an entity. Supports 0-255 int or 0.0-1.0 float values.
        """

        print("set_color is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def set_reflectivity(self, reflectivity: float):
        """
        Change the surface reflectivity (metallic luster) of the material.
        """

        print(
            "set_reflectivity is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_roughness(self, roughness: float):
        """
        Change the surface roughness of the material.
        """

        print(
            "set_roughness is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def set_image_texture(self, image_file_path: str):
        """
        Add a texture from an image file.
        """

        print(
            "set_image_texture is called in an abstract method. Please override this method."
        )
        return self
