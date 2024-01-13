# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import LandmarkInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Landmark(Entity, LandmarkInterface):
    name: str
    parent_entity: EntityOrItsName
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: str,
        parent_entity: EntityOrItsName,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    def clone(
        self,
        new_name: str,
        offset: Optional[DimensionsOrItsListOfFloatOrString] = None,
        new_parent: Optional[EntityOrItsName] = None,
    ) -> "Landmark":
        print("clone called:", new_name, offset, new_parent)
        from . import Landmark

        return Landmark("name", "parent")

    def get_landmark_entity_name(self) -> str:
        print(
            "get_landmark_entity_name called:",
        )
        return "String"

    def get_parent_entity(self) -> "Entity":
        print(
            "get_parent_entity called:",
        )
        from . import Entity

        return Entity("an entity")
