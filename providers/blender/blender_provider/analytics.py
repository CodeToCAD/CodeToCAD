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

    @staticmethod
    def _get_entity_from_name_or_landmark(
        entity_or_landmark: str | EntityInterface,
    ) -> EntityInterface:
        if isinstance(entity_or_landmark, str):
            return Entity(entity_or_landmark)
        return entity_or_landmark

    @supported(SupportLevel.SUPPORTED)
    def measure_distance(
        self, entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        distance = (
            Analytics._get_entity_from_name_or_landmark(entity_2).get_location_world()
            - Analytics._get_entity_from_name_or_landmark(entity_1).get_location_world()
        )
        return Dimensions.from_point(distance)

    @supported(SupportLevel.PLANNED)
    def measure_angle(
        self,
        entity_1: "EntityInterface",
        entity_2: "EntityInterface",
        pivot: "EntityInterface| None" = None,
    ) -> "list[Angle]":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED)
    def get_world_pose(self, entity: "EntityInterface") -> "list[float]":
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        return get_object_world_pose(part_name)

    @supported(SupportLevel.SUPPORTED)
    def get_bounding_box(self, entity: "EntityInterface") -> "BoundaryBox":
        if isinstance(entity, str):
            entity = Entity(entity)
        return entity.get_bounding_box()

    @supported(SupportLevel.SUPPORTED)
    def get_dimensions(self, entity: "EntityInterface") -> "Dimensions":
        return entity.get_dimensions()

    @supported(SupportLevel.SUPPORTED)
    def log(self, message: "str"):
        log_message(message)
        return self
