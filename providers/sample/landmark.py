# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.entity_interface import EntityInterface


from providers.sample.entity import Entity


class Landmark(LandmarkInterface, Entity):

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def clone(
        self,
        new_name: "str",
        offset: "str|list[str]|list[float]|list[Dimension]|Dimensions| None" = None,
        new_parent: "str|EntityInterface| None" = None,
    ) -> "LandmarkInterface":

        print("clone called", f": {new_name}, {offset}, {new_parent}")

        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark_entity_name(
        self,
    ) -> "str":

        print(
            "get_landmark_entity_name called",
        )

        return "String"

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_parent_entity(
        self,
    ) -> "EntityInterface":

        print(
            "get_parent_entity called",
        )

        return __import__("codetocad").Part("an entity")
