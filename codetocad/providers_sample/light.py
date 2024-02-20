# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import LightInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.providers_sample.entity import Entity


class Light(LightInterface, Entity):
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def set_color(
        self, r_value: "IntOrFloat", g_value: "IntOrFloat", b_value: "IntOrFloat"
    ):
        print("set_color called", f": {r_value}, {g_value}, {b_value}")

        return self

    def create_sun(self, energy_level: "float"):
        print("create_sun called", f": {energy_level}")

        return self

    def create_spot(self, energy_level: "float"):
        print("create_spot called", f": {energy_level}")

        return self

    def create_point(self, energy_level: "float"):
        print("create_point called", f": {energy_level}")

        return self

    def create_area(self, energy_level: "float"):
        print("create_area called", f": {energy_level}")

        return self
