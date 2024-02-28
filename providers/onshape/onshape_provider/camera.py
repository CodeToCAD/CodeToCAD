from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.interfaces import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
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
