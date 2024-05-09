# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.analytics_interface import AnalyticsInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Analytics(
    AnalyticsInterface,
):
    """
    Tools for collecting data about the entities and scene.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self,
    ):

        self.__proxied = get_provider(AnalyticsInterface)()  # type: ignore

    def measure_distance(
        self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"
    ) -> "Dimensions":
        return self.__proxied.measure_distance(entity1, entity2)

    def measure_angle(
        self,
        entity1: "str|EntityInterface",
        entity2: "str|EntityInterface",
        pivot: "str|EntityInterface| None" = None,
    ) -> "list[Angle]":
        return self.__proxied.measure_angle(entity1, entity2, pivot)

    def get_world_pose(self, entity: "str|EntityInterface") -> "list[float]":
        return self.__proxied.get_world_pose(entity)

    def get_bounding_box(self, entity_name: "str|EntityInterface") -> "BoundaryBox":
        return self.__proxied.get_bounding_box(entity_name)

    def get_dimensions(self, entity_name: "str|EntityInterface") -> "Dimensions":
        return self.__proxied.get_dimensions(entity_name)

    def log(self, message: "str") -> Self:
        return self.__proxied.log(message)
