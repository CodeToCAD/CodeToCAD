

from typing import Optional

from codetocad.interfaces import LandmarkInterface, EntityInterface
from codetocad.CodeToCADTypes import *
from codetocad.utilities import *


class Landmark(LandmarkInterface):

    name: str
    parentEntity: EntityOrItsName
    description: Optional[str] = None

    def __init__(self, name: str, parentEntity: EntityOrItsName, description: Optional[str] = None):
        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    def getLandmarkEntityName(self) -> str:

        raise NotImplementedError()

    def getParentEntity(self) -> EntityInterface:

        raise NotImplementedError()

    def isExists(self) -> bool:

        raise NotImplementedError()

    def rename(self, newName: str):

        return self

    def delete(self):

        return self

    def isVisible(self) -> bool:

        raise NotImplementedError()

    def setVisible(self, isVisible: bool):

        return self

    def getNativeInstance(self) -> object:

        raise NotImplementedError()

    def getLocationWorld(self) -> 'Point':

        raise NotImplementedError()

    def getLocationLocal(self) -> 'Point':

        raise NotImplementedError()

    def select(self):

        return self
