from codetocad.interfaces.camera_interface import CameraInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from providers.blender.blender_provider.entity import Entity
from providers.blender.blender_provider.blender_actions.camera import (
    create_camera,
    set_focal_length,
)


class Camera(CameraInterface, Entity):

    def __init__(
        self,
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.description = description

    @supported(SupportLevel.SUPPORTED)
    def create_perspective(self):
        create_camera(self.name, type="PERSP")
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_orthogonal(self):
        create_camera(self.name, type="ORTHO")
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_focal_length(self, length: "float"):
        set_focal_length(self.name, length)
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_panoramic(self):
        create_camera(self.name, type="PANO")
        return self
