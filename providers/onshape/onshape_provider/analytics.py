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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_distance(
        entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_angle(
        entity_1: "EntityInterface",
        entity_2: "EntityInterface",
        pivot: "EntityInterface| None" = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_world_pose(entity: "EntityInterface") -> "list[float]":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(entity: "EntityInterface") -> "BoundaryBox":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(entity: "EntityInterface") -> "Dimensions":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def log(message: "str"):
        return self
