from codetocad.interfaces.camera_interface import CameraInterface
from typing import Self
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from providers.blender.blender_provider.entity import Entity
from providers.blender.blender_provider.blender_actions.camera import (
    create_camera,
    set_focal_length,
)


class Camera(CameraInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_perspective(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        create_camera(self.name, type="PERSP")
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_orthogonal(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        create_camera(self.name, type="ORTHO")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_focal_length(self, length: "float") -> "Self":
        set_focal_length(self.name, length)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_panoramic(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        create_camera(self.name, type="PANO")
        return self
