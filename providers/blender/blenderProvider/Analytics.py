

from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import AnalyticsInterface, EntityInterface, LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from . import Entity


class Analytics(AnalyticsInterface):

    def __init__(self):
        pass

    @staticmethod
    def _getEntityFromNameOrLandmark(entityOrLandmark: EntityOrItsNameOrLandmark) -> Union[EntityInterface, LandmarkInterface]:
        if isinstance(entityOrLandmark, str):
            return Entity(entityOrLandmark)
        return entityOrLandmark

    def measureDistance(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark
                        ) -> 'Dimensions':
        distance = Analytics._getEntityFromNameOrLandmark(entity2).getLocationWorld(
        ) - Analytics._getEntityFromNameOrLandmark(entity1).getLocationWorld()
        return Dimensions.fromPoint(distance)

    def measureAngle(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark, pivot: Optional[EntityOrItsNameOrLandmark] = None
                     ) -> 'list[Angle]':
        raise NotImplementedError()

    def getWorldPose(self, entity: EntityOrItsName
                     ) -> 'list[float]':
        partName = entity
        if isinstance(partName, EntityInterface):
            partName = partName.name
        return BlenderActions.getObjectWorldPose(partName)

    def getBoundingBox(self, entityName: EntityOrItsName
                       ) -> 'BoundaryBox':
        entity = entityName
        if isinstance(entity, str):
            entity = Entity(entity)

        return entity.getBoundingBox()

    def getDimensions(self, entityName: EntityOrItsName
                      ) -> 'Dimensions':
        if isinstance(entityName, Entity):
            return entityName.getDimensions()
        if isinstance(entityName, str):
            return Entity(entityName).getDimensions()
        raise TypeError("entityName must be a string or an Entity")

    def log(self, message):
        BlenderActions.logMessage(message)
        return self
