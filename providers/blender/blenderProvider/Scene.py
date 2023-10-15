from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import SceneInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .Part import Part
from .Entity import Entity


class Scene(SceneInterface):

    # Blender's default Scene name is "Scene"
    name: str = "Scene"
    description: Optional[str] = None

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.name
        self.description = description

    @staticmethod
    def default(
    ) -> 'Scene':
        return Scene()

    def create(self
               ):
        raise NotImplementedError()
        return self

    def delete(self
               ):
        raise NotImplementedError()
        return self

    def getSelectedEntity(self) -> 'EntityInterface':

        return Entity(BlenderActions.getSelectedObjectName())

    def export(self, filePath: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        for entity in entities:
            part = entity
            if isinstance(part, str):
                part = Part(part)
            part.export(filePath, overwrite, scale)
        return self

    def setDefaultUnit(self, unit: LengthUnitOrItsName
                       ):
        if isinstance(unit, str):
            unit = LengthUnit.fromString(unit)

        blenderUnit = BlenderDefinitions.BlenderLength.fromLengthUnit(unit)

        BlenderActions.setDefaultUnit(blenderUnit, self.name)
        return self

    def createGroup(self, name: str
                    ):
        BlenderActions.createCollection(name, self.name)
        return self

    def deleteGroup(self, name: str, removeChildren: bool
                    ):
        BlenderActions.removeCollection(
            name=name,
            sceneName=self.name,
            removeChildren=removeChildren
        )
        return self

    def removeFromGroup(self, entityName: str, groupName: str
                        ):
        if isinstance(entityName, Entity):
            entityName = entityName.name

        BlenderActions.removeObjectFromCollection(
            existingObjectName=entityName,
            collectionName=groupName,
            sceneName=self.name
        )
        return self

    def assignToGroup(self, entities: list[EntityOrItsName], groupName: str, removeFromOtherGroups: Optional[bool] = True
                      ):
        for entity in entities:
            entityName = entity
            if isinstance(entityName, EntityInterface):
                entityName = entityName.name

            BlenderActions.assignObjectToCollection(
                entityName, groupName, self.name, removeFromOtherGroups or True)

        return self

    def setVisible(self, entities: list[EntityOrItsName], isVisible: bool
                   ):

        for entity in entities:
            if isinstance(entity, EntityInterface):
                entity = entity.name

            BlenderActions.setObjectVisibility(entity, isVisible)

        return self

    def setBackgroundImage(self, filePath: str, locationX: Optional[DimensionOrItsFloatOrStringValue] = 0, locationY: Optional[DimensionOrItsFloatOrStringValue] = 0):

        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.addHDRTexture(self.name, absoluteFilePath)

        x = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(locationX or 0)).value
        y = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(locationY or 0)).value

        BlenderActions.setBackgroundLocation(self.name, x, y)

        return self
