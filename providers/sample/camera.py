# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.camera_interface import CameraInterface


from providers.sample.entity import Entity


class Camera(CameraInterface, Entity):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_perspective(
        self,
    ) -> Self:

        print(
            "create_perspective called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_orthogonal(
        self,
    ) -> Self:

        print(
            "create_orthogonal called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_panoramic(
        self,
    ) -> Self:

        print(
            "create_panoramic called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_focal_length(self, length: "float") -> Self:

        print("set_focal_length called", f": {length}")

        return self
