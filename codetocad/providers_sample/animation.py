# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import AnimationInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


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

    def create_key_frame_location(self, entity: EntityOrItsName, frame_number: "int"):
        return self

    def create_key_frame_rotation(self, entity: EntityOrItsName, frame_number: "int"):
        return self
