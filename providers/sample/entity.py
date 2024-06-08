# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.entity_interface import EntityInterface


class Entity(
    EntityInterface,
):

    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):

        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(
        self,
    ) -> "bool":

        print(
            "is_exists called",
        )

        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def rename(
        self, new_name: "str", renamelinked_entities_and_landmarks: "bool" = True
    ) -> Self:

        print("rename called", f": {new_name}, {renamelinked_entities_and_landmarks}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(self, remove_children: "bool" = True) -> Self:

        print("delete called", f": {remove_children}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_visible(
        self,
    ) -> "bool":

        print(
            "is_visible called",
        )

        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(self, is_visible: "bool") -> Self:

        print("set_visible called", f": {is_visible}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def apply(
        self,
        rotation: "bool" = True,
        scale: "bool" = True,
        location: "bool" = False,
        modifiers: "bool" = True,
    ) -> Self:

        print("apply called", f": {rotation}, {scale}, {location}, {modifiers}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_native_instance(
        self,
    ) -> "object":

        print(
            "get_native_instance called",
        )

        return "instance"

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_world(
        self,
    ) -> "Point":

        print(
            "get_location_world called",
        )

        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_location_local(
        self,
    ) -> "Point":

        print(
            "get_location_local called",
        )

        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.SUPPORTED, notes="")
    def select(
        self,
    ) -> Self:

        print(
            "select called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:

        print("translate_xyz called", f": {x}, {y}, {z}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_x(self, amount: "str|float|Dimension") -> Self:

        print("translate_x called", f": {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_y(self, amount: "str|float|Dimension") -> Self:

        print("translate_y called", f": {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def translate_z(self, amount: "str|float|Dimension") -> Self:

        print("translate_z called", f": {amount}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_xyz(
        self, x: "str|float|Angle", y: "str|float|Angle", z: "str|float|Angle"
    ) -> Self:

        print("rotate_xyz called", f": {x}, {y}, {z}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_x(self, rotation: "str|float|Angle") -> Self:

        print("rotate_x called", f": {rotation}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_y(self, rotation: "str|float|Angle") -> Self:

        print("rotate_y called", f": {rotation}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def rotate_z(self, rotation: "str|float|Angle") -> Self:

        print("rotate_z called", f": {rotation}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(
        self,
    ) -> "BoundaryBox":

        print(
            "get_bounding_box called",
        )

        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(
        self,
    ) -> "Dimensions":

        print(
            "get_dimensions called",
        )

        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))
