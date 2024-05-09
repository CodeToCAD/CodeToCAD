from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.fusion_landmark import (
    FusionLandmark,
)
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
        from . import Part

        if isinstance(parent_entity, str):
            parent_entity = Part(parent_entity)
        self.fusion_landmark = FusionLandmark(name, parent_entity.fusion_body.component)
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
        from . import Landmark

        if new_parent:
            if isinstance(new_parent, str):
                parent = Entity(new_parent)
            else:
                parent = new_parent
        else:
            parent = self.parent_entity
        sketch = self.fusion_landmark.clone(new_name, True)
        return Landmark(sketch.name, parent)

    def get_landmark_entity_name(self) -> str:
        return self.fusion_landmark.instance.name

    def get_parent_entity(self) -> "Entity":
        if isinstance(self.parent_entity, str):
            return Entity(self.parent_entity)
        return self.parent_entity
