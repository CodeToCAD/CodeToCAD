# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.analytics_interface import AnalyticsInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Analytics(
    AnalyticsInterface,
):

    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_distance(
        self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"
    ) -> "Dimensions":

        print("measure_distance called", f": {entity1}, {entity2}")

        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_angle(
        self,
        entity1: "str|EntityInterface",
        entity2: "str|EntityInterface",
        pivot: "str|EntityInterface| None" = None,
    ) -> "list[Angle]":

        print("measure_angle called", f": {entity1}, {entity2}, {pivot}")

        return [Angle(90)]

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_world_pose(self, entity: "str|EntityInterface") -> "list[float]":

        print("get_world_pose called", f": {entity}")

        return [0.0]

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(self, entity_name: "str|EntityInterface") -> "BoundaryBox":

        print("get_bounding_box called", f": {entity_name}")

        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(self, entity_name: "str|EntityInterface") -> "Dimensions":

        print("get_dimensions called", f": {entity_name}")

        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.SUPPORTED, notes="")
    def log(self, message: "str") -> Self:

        print("log called", f": {message}")

        return self
