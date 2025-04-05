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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def measure_distance(
        entity_1: "EntityInterface", entity_2: "EntityInterface"
    ) -> "Dimensions":
        distance = (
            Analytics._get_entity_from_name_or_landmark(entity_2).get_location_world()
            - Analytics._get_entity_from_name_or_landmark(entity_1).get_location_world()
        )
        return Dimensions.from_point(distance)

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
        part_name = entity
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        return get_object_world_pose(part_name)

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_bounding_box(entity: "EntityInterface") -> "BoundaryBox":
        if isinstance(entity, str):
            entity = Entity(entity)
        return entity.get_bounding_box()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_dimensions(entity: "EntityInterface") -> "Dimensions":
        return entity.get_dimensions()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def log(message: "str") -> None:
        log_message(message)
        return self
