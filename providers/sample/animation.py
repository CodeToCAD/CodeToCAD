# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.animation_interface import AnimationInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Animation(
    AnimationInterface,
):

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def default() -> "AnimationInterface":

        print(
            "default called",
        )

        return Animation()

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_start(self, frame_number: "int") -> Self:

        print("set_frame_start called", f": {frame_number}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_end(self, frame_number: "int") -> Self:

        print("set_frame_end called", f": {frame_number}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_current(self, frame_number: "int") -> Self:

        print("set_frame_current called", f": {frame_number}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_key_frame_location(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:

        print("create_key_frame_location called", f": {entity}, {frame_number}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_key_frame_rotation(
        self, entity: "str|EntityInterface", frame_number: "int"
    ) -> Self:

        print("create_key_frame_rotation called", f": {entity}, {frame_number}")

        return self
