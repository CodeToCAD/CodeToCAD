from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface
from providers.onshape.onshape_provider.entity import Entity
from . import Entity


class Camera(CameraInterface, Entity):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.UNSUPPORTED)
    def create_perspective(self):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_orthogonal(self):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_panoramic(self):
        print("create_panoramic called")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_focal_length(self, length: "float"):
        return self
