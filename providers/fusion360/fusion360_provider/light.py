from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.light_interface import LightInterface
from providers.fusion360.fusion360_provider.entity import Entity


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

    @supported(SupportLevel.UNSUPPORTED)
    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_sun(self, energy_level: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_spot(self, energy_level: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_point(self, energy_level: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_area(self, energy_level: "float"):
        raise NotImplementedError()
        return self
