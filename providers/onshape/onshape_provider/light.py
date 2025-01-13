from typing import Optional
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.light_interface import LightInterface
from providers.onshape.onshape_provider.entity import Entity
from . import Entity


class Light(LightInterface, Entity):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ):
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_sun(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_spot(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_area(
        energy_level: "float", name: "str| None" = None, description: "str| None" = None
    ):
        return self
