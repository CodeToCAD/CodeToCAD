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
        self, entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def measure_angle(
        self,
        entity_1: "EntityInterface",
        entity_2: "EntityInterface",
        pivot: "EntityInterface| None" = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def get_world_pose(self, entity: "EntityInterface") -> "list[float]":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def get_bounding_box(self, entity: "EntityInterface") -> "BoundaryBox":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def get_dimensions(self, entity: "EntityInterface") -> "Dimensions":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def log(self, message: "str"):
        return self
