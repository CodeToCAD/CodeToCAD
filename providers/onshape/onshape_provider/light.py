from typing import Optional
from codetocad.interfaces.light_interface import LightInterface
from providers.onshape.onshape_provider.entity import Entity
from . import Entity


class Light(LightInterface, Entity):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ):
        return self

    def create_sun(self, energy_level: "float"):
        return self

    def create_spot(self, energy_level: "float"):
        return self

    def create_point(self, energy_level: "float"):
        return self

    def create_area(self, energy_level: "float"):
        return self
