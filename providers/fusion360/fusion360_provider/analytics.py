from codetocad.interfaces.analytics_interface import AnalyticsInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_distance(
        entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        print("measure_distance called:", entity_1, entity_2)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_angle(
        entity_1: "EntityInterface",
        entity_2: "EntityInterface",
        pivot: "EntityInterface| None" = None,
    ) -> "list[Angle]":
        print("measure_angle called:", entity_1, entity_2, pivot)
        return [Angle(90)]

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_world_pose(entity: "EntityInterface") -> "list[float]":
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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(entity: "EntityInterface") -> "BoundaryBox":
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(entity: "EntityInterface") -> "Dimensions":
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def log(message: "str"):
        print("log called:", message)
        return self
