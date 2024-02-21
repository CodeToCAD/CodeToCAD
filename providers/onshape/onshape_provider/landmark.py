from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.interfaces import LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Landmark(LandmarkInterface):
    name: str
    parent_entity: EntityOrItsName
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        parent_entity: "EntityOrItsName",
        description: "str| None" = None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description
        self.native_instance = native_instance

    def clone(
        self,
        new_name: "str",
        offset: "DimensionsOrItsListOfFloatOrString| None" = None,
        new_parent: "EntityOrItsName| None" = None,
    ) -> "Landmark":
        print("clone called:", new_name, offset, new_parent)
        from . import Landmark

        return Landmark("name", "parent")

    def get_landmark_entity_name(self) -> str:
        raise NotImplementedError()

    def get_parent_entity(self) -> "Entity":
        raise NotImplementedError()

    def get_location_world(self) -> "Point":
        print("get_location_world called")
        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_location_local(self) -> "Point":
        print("get_location_local called")
        return Point.from_list_of_float_or_string([0, 0, 0])

    def translate_xyz(
        self,
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ):
        print("translate_xyz called", f": {x}, {y}, {z}")
        return self
