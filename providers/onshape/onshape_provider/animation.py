from codetocad.interfaces.animation_interface import AnimationInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Animation(AnimationInterface):

    def __init__(self):
        pass

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def default() -> "Animation":
        return Animation()

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_start(self, frame_number: "int"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_end(self, frame_number: "int"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_current(self, frame_number: "int"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_key_frame_location(self, entity: "EntityInterface", frame_number: "int"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_key_frame_rotation(self, entity: "EntityInterface", frame_number: "int"):
        return self
