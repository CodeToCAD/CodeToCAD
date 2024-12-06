from codetocad.interfaces.analytics_interface import AnalyticsInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @supported(SupportLevel.PLANNED)
    def measure_distance(
        self, entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        print("measure_distance called:", entity1, entity2)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.PLANNED)
    def measure_angle(
        self,
        entity_1: "EntityInterface",
        entity_2: "EntityInterface",
        pivot: "EntityInterface| None" = None,
    ) -> "list[Angle]":
        print("measure_angle called:", entity1, entity2, pivot)
        return [Angle(90)]

    @supported(SupportLevel.PLANNED)
    def get_world_pose(self, entity: "EntityInterface") -> "list[float]":
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

    @supported(SupportLevel.PLANNED)
    def get_bounding_box(self, entity: "EntityInterface") -> "BoundaryBox":
        print("get_bounding_box called:", entity_name)
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    @supported(SupportLevel.PLANNED)
    def get_dimensions(self, entity: "EntityInterface") -> "Dimensions":
        print("get_dimensions called:", entity_name)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @supported(SupportLevel.PLANNED)
    def log(self, message: "str"):
        print("log called:", message)
        return self
