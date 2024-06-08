from codetocad.interfaces.analytics_interface import AnalyticsInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @supported(SupportLevel.UNSUPPORTED)
    def measure_distance(
        self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"
    ) -> "Dimensions":
        print("measure_distance called:", entity1, entity2)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.UNSUPPORTED)
    def measure_angle(
        self,
        entity1: "str|EntityInterface",
        entity2: "str|EntityInterface",
        pivot: "str|EntityInterface| None" = None,
    ) -> "list[Angle]":
        print("measure_angle called:", entity1, entity2, pivot)
        return [Angle(90)]

    @supported(SupportLevel.UNSUPPORTED)
    def get_world_pose(self, entity: "str|EntityInterface") -> "list[float]":
        print("get_world_pose called:", entity)
        return [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ]

    @supported(SupportLevel.UNSUPPORTED)
    def get_bounding_box(self, entity_name: "str|EntityInterface") -> "BoundaryBox":
        print("get_bounding_box called:", entity_name)
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    @supported(SupportLevel.UNSUPPORTED)
    def get_dimensions(self, entity_name: "str|EntityInterface") -> "Dimensions":
        print("get_dimensions called:", entity_name)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.UNSUPPORTED)
    def log(self, message: "str"):
        print("log called:", message)
        return self
