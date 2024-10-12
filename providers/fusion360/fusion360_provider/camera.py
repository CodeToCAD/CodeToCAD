from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from codetocad.utilities.override import override
from providers.fusion360.fusion360_provider.fusion_actions.fusion_camera import (
    FusionCamera,
)


class Camera(CameraInterface, Entity):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @override
    @supported(SupportLevel.SUPPORTED)
    def rotate_xyz(
        self, x: str | float | Angle, y: str | float | Angle, z: str | float | Angle
    ):
        xAngle = Angle.from_angle_or_its_float_or_string_value(x)
        yAngle = Angle.from_angle_or_its_float_or_string_value(y)
        zAngle = Angle.from_angle_or_its_float_or_string_value(z)
        if xAngle.value > 0:
            FusionCamera().rotate(Axis.X, xAngle)
        if yAngle.value > 0:
            FusionCamera().rotate(Axis.Y, yAngle)
        if zAngle.value > 0:
            FusionCamera().rotate(Axis.Z, zAngle)
        return self

    @supported(SupportLevel.PLANNED)
    def create_perspective(self):
        print("create_perspective called:")
        return self

    @supported(SupportLevel.PLANNED)
    def create_orthogonal(self):
        print("create_orthogonal called:")
        return self

    @supported(SupportLevel.PLANNED)
    def create_panoramic(self):
        print("create_panoramic called")
        return self

    @supported(SupportLevel.PLANNED)
    def set_focal_length(self, length: "float"):
        print("set_focal_length called:", length)
        return self

    @override
    @supported(SupportLevel.SUPPORTED)
    def translate_xyz(
        self,
        x: str | float | Dimension,
        y: str | float | Dimension,
        z: str | float | Dimension,
    ):
        x = Dimension.from_dimension_or_its_float_or_string_value(x, None).value
        y = Dimension.from_dimension_or_its_float_or_string_value(y, None).value
        z = Dimension.from_dimension_or_its_float_or_string_value(z, None).value
        FusionCamera().translate(x, y, z)
        return self
