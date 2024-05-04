from typing import Optional
from codetocad.interfaces.animation_interface import AnimationInterface
from codetocad.interfaces.entity_interface import EntityInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Animation(AnimationInterface):
    def __init__(self):
        pass

    @staticmethod
    def default() -> "Animation":
        return Animation()

    def set_frame_start(self, frame_number: "int"):
        return self

    def set_frame_end(self, frame_number: "int"):
        return self

    def set_frame_current(self, frame_number: "int"):
        return self

    def create_key_frame_location(self, entity: "str|Entity", frame_number: "int"):
        return self

    def create_key_frame_rotation(self, entity: "str|Entity", frame_number: "int"):
        return self
