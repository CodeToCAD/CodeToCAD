

from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import AnalyticsInterface, EntityInterface, LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .entity import Entity


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @staticmethod
    def _get_entity_from_name_or_landmark(entity_or_landmark: EntityOrItsNameOrLandmark) -> Union[EntityInterface, LandmarkInterface]:
        if isinstance(entity_or_landmark, str):
            return Entity(entity_or_landmark)
        return entity_or_landmark

    def measure_distance(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark
                         ) -> 'Dimensions':
        distance = Analytics._get_entity_from_name_or_landmark(entity2).get_location_world(
        ) - Analytics._get_entity_from_name_or_landmark(entity1).get_location_world()
        return Dimensions.fromPoint(distance)

    def measure_angle(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark, pivot: Optional[EntityOrItsNameOrLandmark] = None
                      ) -> 'list[Angle]':
        raise NotImplementedError()

    def get_world_pose(self, entity: EntityOrItsName
                       ) -> 'list[float]':
        partName = entity
        if isinstance(partName, EntityInterface):
            partName = partName.name
        return blender_actions.get_object_world_pose(partName)

    def get_bounding_box(self, entity_name: EntityOrItsName
                         ) -> 'BoundaryBox':
        entity = entity_name
        if isinstance(entity, str):
            entity = Entity(entity)

        return entity.get_bounding_box()

    def get_dimensions(self, entity_name: EntityOrItsName
                       ) -> 'Dimensions':
        if isinstance(entity_name, Entity):
            return entity_name.get_dimensions()
        if isinstance(entity_name, str):
            return Entity(entity_name).get_dimensions()
        raise TypeError("entity_name must be a string or an Entity")

    def log(self, message):
        blender_actions.log_message(message)
        return self