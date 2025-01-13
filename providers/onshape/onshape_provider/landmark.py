from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
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
    parent: str | Entity
    description: Optional[str] = None
    native_instance = None

    def __init__(self, native_instance: "Any", parent: "EntityInterface"):
        self.name = name
        self.parent = parent
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "EntityInterface| None" = None,
    ) -> "Landmark":
        print("clone called:", new_name, offset, new_parent)
        from . import Landmark

        return Landmark("name", "parent")
