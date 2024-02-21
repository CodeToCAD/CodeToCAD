from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider.entity import Entity
from . import blender_actions
from . import blender_definitions
from codetocad.interfaces import LightInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from . import Entity


class Light(LightInterface, Entity):
    name: str
    description: Optional[str] = None

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description

    def create_sun(self, energy_level: "float"):
        blender_actions.create_light(self.name, energy_level, type="SUN")
        return self

    def create_point(self, energy_level: "float"):
        blender_actions.create_light(self.name, energy_level, type="POINT")
        return self

    def create_spot(self, energy_level: "float"):
        blender_actions.create_light(self.name, energy_level, type="SPOT")
        return self

    def create_area(self, energy_level: "float"):
        blender_actions.create_light(self.name, energy_level, type="AREA")
        return self

    def set_color(
        self, r_value: "IntOrFloat", g_value: "IntOrFloat", b_value: "IntOrFloat"
    ):
        blender_actions.set_light_color(self.name, r_value, g_value, b_value)
        return self

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        xAngle = Angle.from_angle_or_its_float_or_string_value(x)
        yAngle = Angle.from_angle_or_its_float_or_string_value(y)
        zAngle = Angle.from_angle_or_its_float_or_string_value(z)
        blender_actions.rotate_object(
            self.name,
            [xAngle, yAngle, zAngle],
            blender_definitions.BlenderRotationTypes.EULER,
        )
        return self

    def rename(self, new_name: str):
        Entity(self.name).rename(new_name, False)
        self.name = new_name
        return self

    def get_native_instance(self):
        return Entity(self.name).get_native_instance()

    def get_location_local(self) -> "Point":
        return Entity(self.name).get_location_local()
