# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import CameraInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.providers_sample.entity import Entity


class Camera(CameraInterface, Entity):
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def create_perspective(
        self,
    ):
        print(
            "create_perspective called",
        )

        return self

    def create_orthogonal(
        self,
    ):
        print(
            "create_orthogonal called",
        )

        return self

    def set_focal_length(self, length: "float"):
        print("set_focal_length called", f": {length}")

        return self
