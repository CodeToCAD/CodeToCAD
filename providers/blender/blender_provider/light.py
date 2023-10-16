from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import LightInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .entity import Entity


class Light(LightInterface):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def create_sun(self, energy_level=100):
        blender_actions.create_light(self.name, energy_level, type="SUN")
        return self

    def create_point(self, energy_level=100):
        blender_actions.create_light(self.name, energy_level, type="POINT")
        return self

    def create_spot(self, energy_level=100):
        blender_actions.create_light(self.name, energy_level, type="SPOT")
        return self

    def create_area(self, energy_level=100):
        blender_actions.create_light(self.name, energy_level, type="AREA")
        return self

    def set_color(self, r_value, g_value, b_value):
        blender_actions.set_light_color(
            self.name, r_value, g_value, b_value)
        return self

    def translate_xyz(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                      ):

        Entity(self.name).translate_xyz(x, y, z)

        return self

    def rotate_xyz(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                   ):

        xAngle = Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Angle.fromAngleOrItsFloatOrStringValue(z)

        blender_actions.rotate_object(
            self.name, [xAngle, yAngle, zAngle], blender_definitions.BlenderRotationTypes.EULER)

        return self

    def is_exists(self
                  ) -> bool:

        return Entity(self.name).is_exists()

    def rename(self, new_name: str
               ):

        Entity(self.name).rename(new_name, False)

        self.name = new_name

        return self

    def delete(self):

        Entity(self.name).delete(False)

        return self

    def get_native_instance(self
                            ):

        return Entity(self.name).get_native_instance()

    def get_location_world(self
                           ) -> 'Point':

        return Entity(self.name).get_location_world()

    def get_location_local(self
                           ) -> 'Point':

        return Entity(self.name).get_location_local()

    def select(self
               ):

        Entity(self.name).select()

        return self
