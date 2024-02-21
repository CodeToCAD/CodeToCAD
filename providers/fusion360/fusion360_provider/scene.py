from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.interfaces import SceneInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity
    from . import Exportable


class Scene(SceneInterface):
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, name: "str| None" = None, description: "str| None" = None):
        self.name = name
        self.description = description

    @staticmethod
    def default() -> "Scene":
        return Scene()

    def create(self):
        print("create called:")
        return self

    def delete(self):
        print("delete called:")
        return self

    def is_exists(self) -> bool:
        raise NotImplementedError()
        return

    def get_selected_entity(self) -> "Entity":
        from . import Entity

        print("get_selected_entity called:")
        return Entity("an entity")

    def export(
        self,
        file_path: "str",
        entities: "list[ExportableOrItsName]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ):
        print("export called:", file_path, entities, overwrite, scale)
        return self

    def set_default_unit(self, unit: "LengthUnitOrItsName"):
        print("set_default_unit called:", unit)
        return self

    def create_group(self, name: "str"):
        print("create_group called:", name)
        return self

    def delete_group(self, name: "str", remove_children: "bool"):
        print("delete_group called:", name, remove_children)
        return self

    def remove_from_group(self, entity_name: "str", group_name: "str"):
        print("remove_from_group called:", entity_name, group_name)
        return self

    def assign_to_group(
        self,
        entities: "list[EntityOrItsName]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ):
        print("assign_to_group called:", entities, group_name, remove_from_other_groups)
        return self

    def set_visible(self, entities: "list[EntityOrItsName]", is_visible: "bool"):
        print("set_visible called:", entities, is_visible)
        return self

    def set_background_image(
        self,
        file_path: "str",
        location_x: "DimensionOrItsFloatOrStringValue| None" = 0,
        location_y: "DimensionOrItsFloatOrStringValue| None" = 0,
    ):
        print("set_background_image called:", file_path, location_x, location_y)
        return self

    def is_exists(self):
        print("is_exists called")
        return True
