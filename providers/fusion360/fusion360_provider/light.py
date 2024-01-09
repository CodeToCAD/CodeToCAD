from typing import Optional

from codetocad.interfaces import LightInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity


class Light(Entity, LightInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def set_color(self, r_value: IntOrFloat, g_value: IntOrFloat, b_value: IntOrFloat):
        print("set_color called:", r_value, g_value, b_value)
        return self

    def create_sun(self, energy_level: float):
        print("create_sun called:", energy_level)
        return self

    def create_spot(self, energy_level: float):
        print("create_spot called:", energy_level)
        return self

    def create_point(self, energy_level: float):
        print("create_point called:", energy_level)
        return self

    def create_area(self, energy_level: float):
        print("create_area called:", energy_level)
        return self

    @classmethod
    def get_sample_light(cls):
        return cls(name="test-light", description="light instance for testing")
