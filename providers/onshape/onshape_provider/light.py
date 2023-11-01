# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

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
        return self

    def create_sun(self, energy_level: float):
        return self

    def create_spot(self, energy_level: float):
        return self

    def create_point(self, energy_level: float):
        return self

    def create_area(self, energy_level: float):
        return self
