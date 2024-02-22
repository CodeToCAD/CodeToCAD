from codetocad.interfaces import AnimationInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.blender.blender_provider import blender_definitions
from providers.blender.blender_provider.blender_actions.animation import (
    add_keyframe_to_object,
    set_frame_current,
    set_frame_end,
    set_frame_start,
)


class Animation(AnimationInterface):
    def __init__(self):
        pass

    @staticmethod
    def default() -> "Animation":
        return Animation()

    def set_frame_start(self, frame_number: "int"):
        set_frame_start(frame_number, None)
        return self

    def set_frame_end(self, frame_number: "int"):
        set_frame_end(frame_number, None)
        return self

    def set_frame_current(self, frame_number: "int"):
        set_frame_current(frame_number, None)
        return self

    def create_key_frame_location(self, entity: "EntityOrItsName", frame_number: "int"):
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        add_keyframe_to_object(
            part_name,
            frame_number,
            blender_definitions.BlenderTranslationTypes.ABSOLUTE.value,
        )
        return self

    def create_key_frame_rotation(self, entity: "EntityOrItsName", frame_number: "int"):
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        add_keyframe_to_object(
            part_name,
            frame_number,
            blender_definitions.BlenderRotationTypes.EULER.value,
        )
        return self
