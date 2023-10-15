# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import LightInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Light(LightInterface): 
    
    
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    def setColor(self, rValue:IntOrFloat, gValue:IntOrFloat, bValue:IntOrFloat):
        
        return self
        

    def createSun(self, energyLevel:float):
        
        return self
        

    def createSpot(self, energyLevel:float):
        
        return self
        

    def createPoint(self, energyLevel:float):
        
        return self
        

    def createArea(self, energyLevel:float):
        
        return self
        

    def translateXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def rotateXYZ(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        
        return self
        

    def isExists(self) -> bool:
        
        raise NotImplementedError()
        

    def rename(self, newName:str):
        
        return self
        

    def delete(self):
        
        return self
        

    def getNativeInstance(self) -> object:
        
        raise NotImplementedError()
        

    def getLocationWorld(self) -> 'Point':
        
        raise NotImplementedError()
        

    def getLocationLocal(self) -> 'Point':
        
        raise NotImplementedError()
        

    def select(self):
        
        return self
        
    