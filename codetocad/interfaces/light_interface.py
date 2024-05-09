# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from typing import Self


from codetocad.interfaces.entity_interface import EntityInterface


class LightInterface(EntityInterface, metaclass=ABCMeta):
    """
    Manipulate a light object.
    """

    @abstractmethod
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ) -> Self:
        """
        Set the color of an existing light.
        """

        print("set_color is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def create_sun(self, energy_level: "float") -> Self:
        """
        Create a Sun-type light.
        """

        print(
            "create_sun is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_spot(self, energy_level: "float") -> Self:
        """
        Create a Spot-type light.
        """

        print(
            "create_spot is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_point(self, energy_level: "float") -> Self:
        """
        Create a Point-type light.
        """

        print(
            "create_point is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_area(self, energy_level: "float") -> Self:
        """
        Create an Area-type light.
        """

        print(
            "create_area is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
