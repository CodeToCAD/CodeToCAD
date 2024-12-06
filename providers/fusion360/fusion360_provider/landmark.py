from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.fusion_body import FusionBody
from providers.fusion360.fusion360_provider.fusion_actions.fusion_landmark import (
    FusionLandmark,
)


class Landmark(LandmarkInterface, Entity):

    def __init__(
        self,
        parent: "EntityInterface",
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    @property
    def _fusion_landmark(self):
        return FusionLandmark(self.name, self._get_parent_entity_instance().component)

    def _get_parent_entity_instance(self):
        if isinstance(self.parent_entity, str):
            return FusionBody(self.parent_entity)
        else:
            return FusionBody(self.parent_entity.name)

    @supported(SupportLevel.PARTIAL, "Offset is not supported.")
    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "EntityInterface| None" = None,
    ) -> "Landmark":
        if new_parent:
            if isinstance(new_parent, str):
                parent = Entity(new_parent)
            else:
                parent = new_parent
        else:
            parent = self.parent_entity
        sketch = self._fusion_landmark.clone(new_name, True)
        return Landmark(sketch.name, parent)
