from codetocad.interfaces.animation_interface import AnimationInterface
from codetocad.interfaces.entity_interface import EntityInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Animation(AnimationInterface):

    def __init__(self):
        pass

    @staticmethod
    def default() -> "Animation":
        return Animation()

    def set_frame_start(self, frame_number: "int"):
        print("set_frame_start called:", frame_number)
        return self

    def set_frame_end(self, frame_number: "int"):
        print("set_frame_end called:", frame_number)
        return self

    def set_frame_current(self, frame_number: "int"):
        print("set_frame_current called:", frame_number)
        return self

    def create_key_frame_location(
        self, entity: "str|EntityInterface", frame_number: "int"
    ):
        print("create_key_frame_location called:", entity, frame_number)
        return self

    def create_key_frame_rotation(
        self, entity: "str|EntityInterface", frame_number: "int"
    ):
        print("create_key_frame_rotation called:", entity, frame_number)
        return self
