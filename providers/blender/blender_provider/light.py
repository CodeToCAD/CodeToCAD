from codetocad.interfaces.light_interface import LightInterface
from providers.blender.blender_provider.blender_actions.light import (
    create_light,
    set_light_color,
)
from providers.blender.blender_provider.entity import Entity


class Light(LightInterface, Entity):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description

    def create_sun(self, energy_level: "float"):
        create_light(self.name, energy_level, type="SUN")
        return self

    def create_point(self, energy_level: "float"):
        create_light(self.name, energy_level, type="POINT")
        return self

    def create_spot(self, energy_level: "float"):
        create_light(self.name, energy_level, type="SPOT")
        return self

    def create_area(self, energy_level: "float"):
        create_light(self.name, energy_level, type="AREA")
        return self

    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ):
        set_light_color(self.name, r_value, g_value, b_value)
        return self
