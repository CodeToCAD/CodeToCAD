from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider.entity import Entity
from codetocad.interfaces import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.blender.blender_provider import blender_definitions, Entity
from providers.blender.blender_provider.blender_actions.camera import (
    create_camera,
    set_focal_length,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    rotate_object,
)


class Camera(CameraInterface, Entity):
    name: str
    description: Optional[str] = None

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description

    def create_perspective(self):
        create_camera(self.name, type="PERSP")
        return self

    def create_orthogonal(self):
        create_camera(self.name, type="ORTHO")
        return self

    def set_focal_length(self, length: "float"):
        set_focal_length(self.name, length)
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
        rotate_object(
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
