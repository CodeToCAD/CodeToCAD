# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import LandmarkInterface


from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.providers_sample.entity import Entity


class Landmark(
    LandmarkInterface,
):
    def __init__(
        self,
        name: "str",
        parent_entity: "EntityOrItsName",
        description: "str| None" = None,
    ):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description

    def get_location_world(
        self,
    ) -> "Point":
        print(
            "get_location_world called",
        )

        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_location_local(
        self,
    ) -> "Point":
        print(
            "get_location_local called",
        )

        return Point.from_list_of_float_or_string([0, 0, 0])

    def translate_xyz(
        self,
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ):
        print("translate_xyz called", f": {x}, {y}, {z}")

        return self

    def clone(
        self,
        new_name: "str",
        offset: "DimensionsOrItsListOfFloatOrString| None" = None,
        new_parent: "EntityOrItsName| None" = None,
    ) -> "LandmarkInterface":
        print("clone called", f": {new_name}, {offset}, {new_parent}")

        return Landmark("name", "parent")

    def get_landmark_entity_name(
        self,
    ) -> "str":
        print(
            "get_landmark_entity_name called",
        )

        return "String"

    def get_parent_entity(
        self,
    ) -> "EntityInterface":
        print(
            "get_parent_entity called",
        )

        return __import__("codetocad").Part("an entity")
