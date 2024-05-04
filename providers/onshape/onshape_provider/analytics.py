from codetocad.interfaces.analytics_interface import AnalyticsInterface
from providers.onshape.onshape_provider.entity import Entity
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
        raise NotImplementedError()

    def measure_angle(
        self,
        entity1: "str|Entity",
        entity2: "str|Entity",
        pivot: "str|Entity| None" = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    def get_world_pose(self, entity: "str|Entity") -> "list[float]":
        raise NotImplementedError()

    def get_bounding_box(self, entity_name: "str|Entity") -> "BoundaryBox":
        raise NotImplementedError()

    def get_dimensions(self, entity_name: "str|Entity") -> "Dimensions":
        raise NotImplementedError()

    def log(self, message: "str"):
        return self
