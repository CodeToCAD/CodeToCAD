from typing import Optional
from codetocad.interfaces.analytics_interface import AnalyticsInterface
from codetocad.interfaces.entity_interface import EntityInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Analytics(AnalyticsInterface):
    def __init__(self):
        pass

    def measure_distance(
        self, entity1: "str|Entity", entity2: "str|Entity"
    ) -> "Dimensions":
        print("measure_distance called:", entity1, entity2)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def measure_angle(
        self,
        entity1: "str|Entity",
        entity2: "str|Entity",
        pivot: "str|Entity| None" = None,
    ) -> "list[Angle]":
        print("measure_angle called:", entity1, entity2, pivot)
        return [Angle(90)]

    def get_world_pose(self, entity: "str|Entity") -> "list[float]":
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

    def get_bounding_box(self, entity_name: "str|Entity") -> "BoundaryBox":
        print("get_bounding_box called:", entity_name)
        return BoundaryBox(BoundaryAxis(0, 0), BoundaryAxis(0, 0), BoundaryAxis(0, 0))

    def get_dimensions(self, entity_name: "str|Entity") -> "Dimensions":
        print("get_dimensions called:", entity_name)
        return Dimensions.from_point(Point.from_list_of_float_or_string([0, 0, 0]))

    def log(self, message: "str"):
        print("log called:", message)
        return self
