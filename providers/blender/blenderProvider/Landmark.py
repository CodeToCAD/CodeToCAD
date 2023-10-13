from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from CodeToCAD.interfaces import LandmarkInterface, EntityInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *

from . import Entity


class Landmark(LandmarkInterface):

    name: str
    parentEntity: EntityOrItsName
    description: Optional[str] = None

    def __init__(self, name: str, parentEntity: EntityOrItsName, description: Optional[str] = None):
        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    def getLandmarkEntityName(self
                              ) -> str:
        parentEntityName = self.parentEntity

        if isinstance(parentEntityName, EntityInterface):
            parentEntityName = parentEntityName.name

        entityName = formatLandmarkEntityName(
            parentEntityName, self.name)

        return entityName

    def getParentEntity(self
                        ) -> 'EntityInterface':

        if isinstance(self.parentEntity, str):
            return Entity(self.parentEntity)

        return self.parentEntity

    def isExists(self) -> bool:
        try:
            return BlenderActions.getObject(self.getLandmarkEntityName()) is not None
        except:
            return False

    def rename(self, newName: str
               ):

        assert Landmark(newName, self.parentEntity).isExists(
        ) == False, f"{newName} already exists."

        parentEntityName = self.parentEntity
        if isinstance(parentEntityName, EntityInterface):
            parentEntityName = parentEntityName.name

        BlenderActions.updateObjectName(self.getLandmarkEntityName(
        ), formatLandmarkEntityName(parentEntityName, newName))

        self.name = newName

        return self

    def delete(self):
        BlenderActions.removeObject(self.getLandmarkEntityName())
        return self

    def isVisible(self
                  ) -> bool:
        return BlenderActions.getObjectVisibility(self.getLandmarkEntityName())

    def setVisible(self, isVisible: bool
                   ):

        BlenderActions.setObjectVisibility(
            self.getLandmarkEntityName(), isVisible)

        return self

    def getNativeInstance(self
                          ):

        return BlenderActions.getObject(self.getLandmarkEntityName())

    def getLocationWorld(self
                         ) -> 'Point':

        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectWorldLocation(self.getLandmarkEntityName())

    def getLocationLocal(self
                         ) -> 'Point':

        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectLocalLocation(self.getLandmarkEntityName())

    def select(self
               ):
        BlenderActions.selectObject(self.getLandmarkEntityName())
        return self
