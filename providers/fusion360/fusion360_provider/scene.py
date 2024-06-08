from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.exportable_interface import ExportableInterface
from codetocad.proxy.entity import Entity
from codetocad.interfaces.scene_interface import SceneInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Scene(SceneInterface):
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, name: "str| None" = None, description: "str| None" = None):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.UNSUPPORTED)
    def default() -> "Scene":
        return Scene()

    @supported(SupportLevel.UNSUPPORTED)
    def create(self):
        print("create called:")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def delete(self):
        print("delete called:")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def is_exists(self) -> bool:
        raise NotImplementedError()
        return

    @supported(SupportLevel.UNSUPPORTED)
    def get_selected_entity(self) -> "Entity":
        from . import Entity

        print("get_selected_entity called:")
        return Entity("an entity")

    @supported(SupportLevel.UNSUPPORTED)
    def export(
        self,
        file_path: "str",
        entities: "list[str|ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ):
        print("export called:", file_path, entities, overwrite, scale)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_default_unit(self, unit: "str|LengthUnit"):
        print("set_default_unit called:", unit)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_group(self, name: "str"):
        print("create_group called:", name)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def delete_group(self, name: "str", remove_children: "bool"):
        print("delete_group called:", name, remove_children)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def remove_from_group(self, entity_name: "str", group_name: "str"):
        print("remove_from_group called:", entity_name, group_name)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def assign_to_group(
        self,
        entities: "list[str|EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ):
        print("assign_to_group called:", entities, group_name, remove_from_other_groups)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_visible(self, entities: "list[str|EntityInterface]", is_visible: "bool"):
        print("set_visible called:", entities, is_visible)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ):
        print("set_background_image called:", file_path, location_x, location_y)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def is_exists(self):
        print("is_exists called")
        return True
