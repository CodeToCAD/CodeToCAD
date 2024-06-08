# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.light_interface import LightInterface


from providers.sample.entity import Entity


class Light(LightInterface, Entity):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_color(
        self, r_value: "int|float", g_value: "int|float", b_value: "int|float"
    ) -> Self:

        print("set_color called", f": {r_value}, {g_value}, {b_value}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_sun(self, energy_level: "float") -> Self:

        print("create_sun called", f": {energy_level}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_spot(self, energy_level: "float") -> Self:

        print("create_spot called", f": {energy_level}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(self, energy_level: "float") -> Self:

        print("create_point called", f": {energy_level}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_area(self, energy_level: "float") -> Self:

        print("create_area called", f": {energy_level}")

        return self
