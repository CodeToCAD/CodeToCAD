from codetocad.interfaces.animation_interface import AnimationInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider.blender_actions.animation import (
    add_keyframe_to_object,
    set_frame_current,
    set_frame_end,
    set_frame_start,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderRotationTypes,
    BlenderTranslationTypes,
)


class Animation(AnimationInterface):

    @staticmethod
    @supported(SupportLevel.SUPPORTED)
    def default() -> "Animation":
        return Animation()

    @supported(SupportLevel.SUPPORTED)
    def set_frame_start(self, frame_number: "int"):
        set_frame_start(frame_number, None)
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_frame_end(self, frame_number: "int"):
        set_frame_end(frame_number, None)
        return self

    @supported(SupportLevel.SUPPORTED)
    def set_frame_current(self, frame_number: "int"):
        set_frame_current(frame_number, None)
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_key_frame_location(self, entity: "EntityInterface", frame_number: "int"):
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        add_keyframe_to_object(
            part_name, frame_number, BlenderTranslationTypes.ABSOLUTE.value
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_key_frame_rotation(self, entity: "EntityInterface", frame_number: "int"):
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        add_keyframe_to_object(
            part_name, frame_number, BlenderRotationTypes.EULER.value
        )
        return self
