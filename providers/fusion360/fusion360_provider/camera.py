from typing import Optional

from codetocad.interfaces import CameraInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from .fusion_actions.fusion_camera import FusionCamera


from . import Entity


class Camera(Entity, CameraInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.fusion_camera = FusionCamera()

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        x = Dimension.from_dimension_or_its_float_or_string_value(x, None).value
        y = Dimension.from_dimension_or_its_float_or_string_value(y, None).value
        z = Dimension.from_dimension_or_its_float_or_string_value(z, None).value

        self.fusion_camera.translate(x, y , z)

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

        if xAngle.value > 0:
            self.fusion_camera.rotate(Axis.X, xAngle)
        if yAngle.value > 0:
            self.fusion_camera.rotate(Axis.Y, yAngle)
        if zAngle.value > 0:
            self.fusion_camera.rotate(Axis.Z, zAngle)

        return self

    def create_perspective(self):
        print(
            "create_perspective called:",
        )
        return self

    def create_orthogonal(self):
        print(
            "create_orthogonal called:",
        )
        return self

    def set_focal_length(self, length: float):
        print("set_focal_length called:", length)
        return self
