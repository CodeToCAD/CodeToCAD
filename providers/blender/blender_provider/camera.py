from typing import Optional
from codetocad.interfaces.camera_interface import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider.entity import Entity

from providers.blender.blender_provider.blender_actions.camera import (
    create_camera,
    set_focal_length,
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

    def create_panoramic(self):
        create_camera(self.name, type="PANO")
        return self
