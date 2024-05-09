# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.scene_interface import SceneInterface


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.exportable_interface import ExportableInterface


class Scene(
    SceneInterface,
):
    """
    Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = [
        "__proxied",
    ]

    def __init__(self, name: "str| None" = None, description: "str| None" = None):

        self.__proxied = get_provider(SceneInterface)(name, description)  # type: ignore

    @staticmethod
    def default() -> "SceneInterface":
        return get_provider(SceneInterface).default()

    def create(
        self,
    ) -> Self:
        return self.__proxied.create()

    def delete(
        self,
    ) -> Self:
        return self.__proxied.delete()

    def is_exists(
        self,
    ) -> "bool":
        return self.__proxied.is_exists()

    def get_selected_entity(
        self,
    ) -> "EntityInterface":
        return self.__proxied.get_selected_entity()

    def export(
        self,
        file_path: "str",
        entities: "list[str|ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ) -> Self:
        return self.__proxied.export(file_path, entities, overwrite, scale)

    def set_default_unit(self, unit: "str|LengthUnit") -> Self:
        return self.__proxied.set_default_unit(unit)

    def create_group(self, name: "str") -> Self:
        return self.__proxied.create_group(name)

    def delete_group(self, name: "str", remove_children: "bool") -> Self:
        return self.__proxied.delete_group(name, remove_children)

    def remove_from_group(self, entity_name: "str", group_name: "str") -> Self:
        return self.__proxied.remove_from_group(entity_name, group_name)

    def assign_to_group(
        self,
        entities: "list[str|EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ) -> Self:
        return self.__proxied.assign_to_group(
            entities, group_name, remove_from_other_groups
        )

    def set_visible(
        self, entities: "list[str|EntityInterface]", is_visible: "bool"
    ) -> Self:
        return self.__proxied.set_visible(entities, is_visible)

    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ) -> Self:
        return self.__proxied.set_background_image(file_path, location_x, location_y)
