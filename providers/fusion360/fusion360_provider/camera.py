from typing import Optional
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.interfaces import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.utilities.override import override
from codetocad.core import *
from codetocad.enums import *
from .fusion_actions.fusion_camera import FusionCamera


class Camera(CameraInterface, Entity):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.fusion_camera = FusionCamera()

    @override
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
        print("create_perspective called:")
        return self

    def create_orthogonal(self):
        print("create_orthogonal called:")
        return self

    def create_panoramic(
        self,
    ):
        print(
            "create_panoramic called",
        )

        return self

    def set_focal_length(self, length: "float"):
        print("set_focal_length called:", length)
        return self

    @override
    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        x = Dimension.from_dimension_or_its_float_or_string_value(x, None).value
        y = Dimension.from_dimension_or_its_float_or_string_value(y, None).value
        z = Dimension.from_dimension_or_its_float_or_string_value(z, None).value
        self.fusion_camera.translate(x, y, z)
        return self
