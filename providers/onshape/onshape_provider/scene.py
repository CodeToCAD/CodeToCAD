# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import SceneInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Scene(SceneInterface):
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name
        self.description = description

    @staticmethod
    def default() -> "Scene":
        return Scene()

    def create(self):
        return self

    def delete(self):
        return self

    def get_selected_entity(self) -> "Entity":
        raise NotImplementedError()

    def export(
        self,
        file_path: str,
        entities: list[EntityOrItsName],
        overwrite: bool = True,
        scale: float = 1.0,
    ):
        return self

    def set_default_unit(self, unit: LengthUnitOrItsName):
        return self

    def create_group(self, name: str):
        return self

    def delete_group(self, name: str, remove_children: bool):
        return self

    def remove_from_group(self, entity_name: str, group_name: str):
        return self

    def assign_to_group(
        self,
        entities: list[EntityOrItsName],
        group_name: str,
        remove_from_other_groups: Optional[bool] = True,
    ):
        return self

    def set_visible(self, entities: list[EntityOrItsName], is_visible: bool):
        return self

    def set_background_image(
        self,
        file_path: str,
        location_x: Optional[DimensionOrItsFloatOrStringValue] = 0,
        location_y: Optional[DimensionOrItsFloatOrStringValue] = 0,
    ):
        return self
