from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .entity import Entity


class Camera(CameraInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def create_perspective(self):
        blender_actions.create_camera(self.name, type="PERSP")
        return self

    def create_orthogonal(self):
        blender_actions.create_camera(self.name, type="ORTHO")
        return self

    def create_panoramic(self):
        blender_actions.create_camera(self.name, type="PANO")
        return self

    def set_focal_length(self, length):
        blender_actions.set_focal_length(self.name, length)
        return self

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        Entity(self.name).translate_xyz(x, y, z)

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

    def is_exists(self) -> bool:
        return Entity(self.name).is_exists()

    def rename(self, new_name: str):
        Entity(self.name).rename(new_name, False)

        self.name = new_name

        return self

    def delete(self):
        Entity(self.name).delete(False)

        return self

    def get_native_instance(self):
        return Entity(self.name).get_native_instance()

    def get_location_world(self) -> "Point":
        return Entity(self.name).get_location_world()

    def get_location_local(self) -> "Point":
        return Entity(self.name).get_location_local()

    def select(self):
        Entity(self.name).select()

        return self
