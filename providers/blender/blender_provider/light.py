from codetocad.interfaces.light_interface import LightInterface
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from providers.blender.blender_provider.blender_actions.light import (
    create_light,
    set_light_color,
)
from providers.blender.blender_provider.entity import Entity


class Light(LightInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_sun(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        create_light(self.name, energy_level, type="SUN")
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        create_light(self.name, energy_level, type="POINT")
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_spot(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        create_light(self.name, energy_level, type="SPOT")
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_area(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        create_light(self.name, energy_level, type="AREA")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ):
        set_light_color(self.name, r_value, g_value, b_value)
        return self
