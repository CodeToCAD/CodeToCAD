# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


class MaterialInterface(metaclass=ABCMeta):
    """
    Materials affect the appearance and simulation properties of the parts.
    """

    @abstractmethod
    def __init__(self, name: "str", description: "str| None" = None):

        self.name = name
        self.description = description

    @staticmethod
    def get_preset(material_name: "PresetMaterial") -> "MaterialInterface":
        """
        Get a material from a preset
        """

        print(
            "get_preset is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_color(
        self,
        r_value: "int|float",
        g_value: "int|float",
        b_value: "int|float",
        a_value: "int|float" = 1.0,
    ) -> Self:
        """
        Set the RGBA color of an entity. Supports 0-255 int or 0.0-1.0 float values.
        """

        print("set_color is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_reflectivity(self, reflectivity: "float") -> Self:
        """
        Change the surface reflectivity (metallic luster) of the material.
        """

        print(
            "set_reflectivity is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_roughness(self, roughness: "float") -> Self:
        """
        Change the surface roughness of the material.
        """

        print(
            "set_roughness is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_image_texture(self, image_file_path: "str") -> Self:
        """
        Add a texture from an image file.
        """

        print(
            "set_image_texture is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
