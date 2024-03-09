# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.animation_interface import AnimationInterface


from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Animation(
    AnimationInterface,
):
    @staticmethod
    def default() -> "AnimationInterface":
        print(
            "default called",
        )

        return Animation()

    def set_frame_start(self, frame_number: "int"):
        print("set_frame_start called", f": {frame_number}")

        return self

    def set_frame_end(self, frame_number: "int"):
        print("set_frame_end called", f": {frame_number}")

        return self

    def set_frame_current(self, frame_number: "int"):
        print("set_frame_current called", f": {frame_number}")

        return self

    def create_key_frame_location(self, entity: "EntityOrItsName", frame_number: "int"):
        print("create_key_frame_location called", f": {entity}, {frame_number}")

        return self

    def create_key_frame_rotation(self, entity: "EntityOrItsName", frame_number: "int"):
        print("create_key_frame_rotation called", f": {entity}, {frame_number}")

        return self
