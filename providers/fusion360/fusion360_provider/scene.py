from codetocad.utilities.supported import supported
from typing import Self
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.exportable_interface import ExportableInterface
from codetocad.proxy.entity import Entity
from codetocad.interfaces.scene_interface import SceneInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *


class Scene(SceneInterface):

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def default() -> "SceneInterface":
        return Scene()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create(
        name: "str| None" = None, description: "str| None" = None
    ) -> "SceneInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(self) -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_selected_entity(self) -> "EntityInterface":
        raise NotImplementedError()
        return Entity("an entity")

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(
        self,
        file_path: "str",
        entities: "list[ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ) -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_default_unit(self, unit: "str|LengthUnit") -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_group(self, name: "str") -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete_group(self, name: "str", remove_children: "bool") -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remove_from_group(self, entity: "EntityInterface", group_name: "str") -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def assign_to_group(
        self,
        entities: "list[EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ) -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(
        self, entities: "list[EntityInterface]", is_visible: "bool"
    ) -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ) -> "Self":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(self) -> "bool":
        raise NotImplementedError()
        return True

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_by_name(name: "str") -> "SceneInterface":
        print("get_by_name called", f": {name}")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_native_instance(self) -> "object":
        print("get_native_instance called")
        return "instance"
