# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import EntityInterface


class LightInterface(EntityInterface, metaclass=ABCMeta):
    """Manipulate a light object."""

    name: str
    description: Optional[str] = None

    @abstractmethod
    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def set_color(self, r_value: IntOrFloat, g_value: IntOrFloat, b_value: IntOrFloat):
        """
        Set the color of an existing light.
        """

        print("set_color is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def create_sun(self, energy_level: float):
        """
        Create a Sun-type light.
        """

        print(
            "create_sun is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_spot(self, energy_level: float):
        """
        Create a Spot-type light.
        """

        print(
            "create_spot is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_point(self, energy_level: float):
        """
        Create a Point-type light.
        """

        print(
            "create_point is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def create_area(self, energy_level: float):
        """
        Create an Area-type light.
        """

        print(
            "create_area is called in an abstract method. Please override this method."
        )
        return self
