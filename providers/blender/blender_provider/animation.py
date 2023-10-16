

from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import AnimationInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Animation(AnimationInterface):

    def __init__(self):
        pass

    @staticmethod
    def default(
    ) -> 'Animation':
        return Animation()

    def set_frame_start(self, frame_number: 'int'
                        ):

        blender_actions.set_frame_start(frame_number, None)

        return self

    def set_frame_end(self, frame_number: 'int'
                      ):

        blender_actions.set_frame_end(frame_number, None)

        return self

    def set_frame_current(self, frame_number: 'int'
                          ):

        blender_actions.set_frame_current(frame_number, None)

        return self

    def create_key_frame_location(self, entity: EntityOrItsName, frame_number: 'int'
                                  ):
        partName = entity

        if isinstance(partName, EntityInterface):
            partName = partName.name

        blender_actions.add_keyframe_to_object(
            partName, frame_number, blender_definitions.BlenderTranslationTypes.ABSOLUTE.value)

        return self

    def create_key_frame_rotation(self, entity: EntityOrItsName, frame_number: 'int'
                                  ):
        partName = entity

        if isinstance(partName, EntityInterface):
            partName = partName.name

        blender_actions.add_keyframe_to_object(
            partName, frame_number, blender_definitions.BlenderRotationTypes.EULER.value)

        return self
