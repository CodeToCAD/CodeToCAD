# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.scene_interface import SceneInterface


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.exportable_interface import ExportableInterface


class Scene(
    SceneInterface,
):

    def __init__(self, name: "str| None" = None, description: "str| None" = None):

        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def default() -> "SceneInterface":

        print(
            "default called",
        )

        return Scene()

    @supported(SupportLevel.SUPPORTED, notes="")
    def create(
        self,
    ) -> Self:

        print(
            "create called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(
        self,
    ) -> Self:

        print(
            "delete called",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(
        self,
    ) -> "bool":

        print(
            "is_exists called",
        )

        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_selected_entity(
        self,
    ) -> "EntityInterface":

        print(
            "get_selected_entity called",
        )

        return __import__("codetocad").Part("an entity")

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(
        self,
        file_path: "str",
        entities: "list[str|ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ) -> Self:

        print("export called", f": {file_path}, {entities}, {overwrite}, {scale}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_default_unit(self, unit: "str|LengthUnit") -> Self:

        print("set_default_unit called", f": {unit}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_group(self, name: "str") -> Self:

        print("create_group called", f": {name}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete_group(self, name: "str", remove_children: "bool") -> Self:

        print("delete_group called", f": {name}, {remove_children}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remove_from_group(self, entity_name: "str", group_name: "str") -> Self:

        print("remove_from_group called", f": {entity_name}, {group_name}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def assign_to_group(
        self,
        entities: "list[str|EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ) -> Self:

        print(
            "assign_to_group called",
            f": {entities}, {group_name}, {remove_from_other_groups}",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(
        self, entities: "list[str|EntityInterface]", is_visible: "bool"
    ) -> Self:

        print("set_visible called", f": {entities}, {is_visible}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ) -> Self:

        print(
            "set_background_image called", f": {file_path}, {location_x}, {location_y}"
        )

        return self
