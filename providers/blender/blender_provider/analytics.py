from codetocad.interfaces.analytics_interface import AnalyticsInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.proxy.entity import Entity
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.codetocad_types import *
from providers.blender.blender_provider.blender_actions.context import log_message
from providers.blender.blender_provider.blender_actions.objects import (
    get_object_world_pose,
)


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @staticmethod
    def _get_entity_from_name_or_landmark(
        entity_or_landmark: str | Entity,
    ) -> EntityInterface:
        if isinstance(entity_or_landmark, str):
            return Entity(entity_or_landmark)
        return entity_or_landmark

    @supported(SupportLevel.UNSUPPORTED)
    def measure_distance(
        self, entity1: "str|EntityInterface", entity2: "str|EntityInterface"
    ) -> "Dimensions":
        distance = (
            Analytics._get_entity_from_name_or_landmark(entity2).get_location_world()
            - Analytics._get_entity_from_name_or_landmark(entity1).get_location_world()
        )
        return Dimensions.from_point(distance)

    @supported(SupportLevel.UNSUPPORTED)
    def measure_angle(
        self,
        entity1: "str|EntityInterface",
        entity2: "str|EntityInterface",
        pivot: "str|EntityInterface| None" = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def get_world_pose(self, entity: "str|EntityInterface") -> "list[float]":
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        return get_object_world_pose(part_name)

    @supported(SupportLevel.UNSUPPORTED)
    def get_bounding_box(self, entity_name: "str|EntityInterface") -> "BoundaryBox":
        entity = entity_name
        if isinstance(entity, str):
            entity = Entity(entity)
        return entity.get_bounding_box()

    @supported(SupportLevel.UNSUPPORTED)
    def get_dimensions(self, entity_name: "str|EntityInterface") -> "Dimensions":
        if isinstance(entity_name, Entity):
            return entity_name.get_dimensions()
        if isinstance(entity_name, str):
            return Entity(entity_name).get_dimensions()
        raise TypeError("entity_name must be a string or an Entity")

    @supported(SupportLevel.UNSUPPORTED)
    def log(self, message: "str"):
        log_message(message)
        return self
