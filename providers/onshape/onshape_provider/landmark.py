from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Landmark(LandmarkInterface, Entity):
    name: str
    parent_entity: str | Entity
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        parent_entity: "str|EntityInterface",
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "str|EntityInterface| None" = None,
    ) -> "Landmark":
        print("clone called:", new_name, offset, new_parent)
        from . import Landmark

        return Landmark("name", "parent")

    def get_landmark_entity_name(self) -> str:
        raise NotImplementedError()

    def get_parent_entity(self) -> "Entity":
        raise NotImplementedError()
