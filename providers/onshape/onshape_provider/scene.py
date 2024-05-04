from typing import Optional
from codetocad.interfaces.scene_interface import SceneInterface
from providers.onshape.onshape_provider.entity import Entity
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
    def default() -> "Scene":
        return Scene()

    def create(self):
        return self

    def delete(self):
        return self

    def is_exists(self) -> bool:
        raise NotImplementedError()
        return

    def get_selected_entity(self) -> "Entity":
        raise NotImplementedError()

    def export(
        self,
        file_path: "str",
        entities: "list[str|Exportable]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ):
        return self

    def set_default_unit(self, unit: "str|LengthUnit"):
        return self

    def create_group(self, name: "str"):
        return self

    def delete_group(self, name: "str", remove_children: "bool"):
        return self

    def remove_from_group(self, entity_name: "str", group_name: "str"):
        return self

    def assign_to_group(
        self,
        entities: "list[str|Entity]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ):
        return self

    def set_visible(self, entities: "list[str|Entity]", is_visible: "bool"):
        return self

    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ):
        return self
