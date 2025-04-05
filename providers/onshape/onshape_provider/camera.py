from typing import Optional
from typing import Self
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface
from providers.onshape.onshape_provider.entity import Entity
from . import Entity


class Camera(CameraInterface, Entity):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_perspective(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_orthogonal(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_panoramic(
        name: "str| None" = None, description: "str| None" = None
    ) -> "CameraInterface":
        print("create_panoramic called")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_focal_length(self, length: "float") -> "Self":
        return self
