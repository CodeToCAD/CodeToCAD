from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.exportable_interface import ExportableInterface
from codetocad.proxy.entity import Entity
from codetocad.interfaces.scene_interface import SceneInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *


class Scene(SceneInterface):

    def __init__(self, name: "str| None" = None, description: "str| None" = None):
        self.name = name
        self.description = description

    @staticmethod
    @supported(SupportLevel.PLANNED)
    def default() -> "Scene":
        return Scene()

    @supported(SupportLevel.PLANNED)
    def create(self):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def delete(self):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def get_selected_entity(self) -> "EntityInterface":
        raise NotImplementedError()
        return Entity("an entity")

    @supported(SupportLevel.PLANNED)
    def export(
        self,
        file_path: "str",
        entities: "list[str|ExportableInterface]",
        overwrite: "bool" = True,
        scale: "float" = 1.0,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def set_default_unit(self, unit: "str|LengthUnit"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def create_group(self, name: "str"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def delete_group(self, name: "str", remove_children: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def remove_from_group(self, entity_name: "str", group_name: "str"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def assign_to_group(
        self,
        entities: "list[str|EntityInterface]",
        group_name: "str",
        remove_from_other_groups: "bool| None" = True,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def set_visible(self, entities: "list[str|EntityInterface]", is_visible: "bool"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def set_background_image(
        self,
        file_path: "str",
        location_x: "str|float|Dimension| None" = 0,
        location_y: "str|float|Dimension| None" = 0,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def is_exists(self):
        raise NotImplementedError()
        return True
