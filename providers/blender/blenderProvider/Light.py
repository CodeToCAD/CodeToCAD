from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import LightInterface
from codetocad.CodeToCADTypes import *
from codetocad.utilities import *

from . import Entity


class Light(LightInterface):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def createSun(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="SUN")
        return self

    def createPoint(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="POINT")
        return self

    def createSpot(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="SPOT")
        return self

    def createArea(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="AREA")
        return self

    def setColor(self, rValue, gValue, bValue):
        BlenderActions.setLightColor(
            self.name, rValue, gValue, bValue)
        return self

    def translateXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                     ):

        Entity(self.name).translateXYZ(x, y, z)

        return self

    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):

        xAngle = Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Angle.fromAngleOrItsFloatOrStringValue(z)

        BlenderActions.rotateObject(
            self.name, [xAngle, yAngle, zAngle], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self

    def isExists(self
                 ) -> bool:

        return Entity(self.name).isExists()

    def rename(self, newName: str
               ):

        Entity(self.name).rename(newName, False)

        self.name = newName

        return self

    def delete(self):

        Entity(self.name).delete(False)

        return self

    def getNativeInstance(self
                          ):

        return Entity(self.name).getNativeInstance()

    def getLocationWorld(self
                         ) -> 'Point':

        return Entity(self.name).getLocationWorld()

    def getLocationLocal(self
                         ) -> 'Point':

        return Entity(self.name).getLocationLocal()

    def select(self
               ):

        Entity(self.name).select()

        return self
