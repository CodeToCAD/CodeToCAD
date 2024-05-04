from typing import Optional
from codetocad.interfaces.camera_interface import CameraInterface
from providers.onshape.onshape_provider.entity import Entity
from . import Entity


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

    def create_perspective(self):
        return self

    def create_orthogonal(self):
        return self

    def create_panoramic(self):
        print("create_panoramic called")
        return self

    def set_focal_length(self, length: "float"):
        return self
