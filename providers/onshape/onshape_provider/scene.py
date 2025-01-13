from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.exportable_interface import ExportableInterface
from codetocad.proxy.entity import Entity
from codetocad.interfaces.scene_interface import SceneInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Scene(SceneInterface):
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def default() -> "Scene":
        return Scene()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create(name: "str| None" = None, description: "str| None" = None):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete(self):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_exists(self) -> bool:
        raise NotImplementedError()
        return

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_selected_entity(self) -> "Entity":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(
        self,
        file_path: "str",
        entities: "list[ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_default_unit(self, unit: "str|LengthUnit"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_group(self, name: "str"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def delete_group(self, name: "str", remove_children: "bool"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remove_from_group(self, entity: "EntityInterface", group_name: "str"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def assign_to_group(
        self,
        entities: "list[EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_visible(self, entities: "list[EntityInterface]", is_visible: "bool"):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ):
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_by_name(name: "str") -> "SceneInterface":
        print("get_by_name called", f": {name}")
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_native_instance(self) -> "object":
        print("get_native_instance called")
        return "instance"
