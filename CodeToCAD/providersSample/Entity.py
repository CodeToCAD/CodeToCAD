# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import EntityInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Entity(EntityInterface): 
    
    
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    def createFromFile(self, filePath:str, fileType:Optional[str]=None):
        
        return self
        

    def isExists(self) -> bool:
        
        raise NotImplementedError()
        

    def rename(self, newName:str, renamelinkedEntitiesAndLandmarks:bool=True):
        
        return self
        

    def delete(self, removeChildren:bool):
        
        return self
        

    def isVisible(self) -> bool:
        
        raise NotImplementedError()
        

    def setVisible(self, isVisible:bool):
        
        return self
        

    def apply(self, rotation:bool=True, scale:bool=True, location:bool=False, modifiers:bool=True):
        
        return self
        

    def getNativeInstance(self) -> object:
        
        raise NotImplementedError()
        

    def getLocationWorld(self) -> 'Point':
        
        raise NotImplementedError()
        

    def getLocationLocal(self) -> 'Point':
        
        raise NotImplementedError()
        

    def select(self):
        
        return self
        

    def export(self, filePath:str, overwrite:bool=True, scale:float=1.0):
        
        return self
        

    def mirror(self, mirrorAcrossEntityOrLandmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName, resultingMirroredEntityName:Optional[str]=None):
        
        return self
        

    def linearPattern(self, instanceCount:'int', offset:DimensionOrItsFloatOrStringValue, directionAxis:AxisOrItsIndexOrItsName="z"):
        
        return self
        

    def circularPattern(self, instanceCount:'int', separationAngle:AngleOrItsFloatOrStringValue, centerEntityOrLandmark:EntityOrItsNameOrLandmark, normalDirectionAxis:AxisOrItsIndexOrItsName="z"):
        
        return self
        

    def translateXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def translateX(self, amount:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def translateY(self, amount:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def translateZ(self, amount:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def scaleXYZ(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def scaleX(self, scale:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def scaleY(self, scale:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def scaleZ(self, scale:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def scaleXByFactor(self, scaleFactor:float):
        
        return self
        

    def scaleYByFactor(self, scaleFactor:float):
        
        return self
        

    def scaleZByFactor(self, scaleFactor:float):
        
        return self
        

    def scaleKeepAspectRatio(self, scale:DimensionOrItsFloatOrStringValue, axis:AxisOrItsIndexOrItsName):
        
        return self
        

    def rotateXYZ(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        
        return self
        

    def rotateX(self, rotation:AngleOrItsFloatOrStringValue):
        
        return self
        

    def rotateY(self, rotation:AngleOrItsFloatOrStringValue):
        
        return self
        

    def rotateZ(self, rotation:AngleOrItsFloatOrStringValue):
        
        return self
        

    def twist(self, angle:AngleOrItsFloatOrStringValue, screwPitch:DimensionOrItsFloatOrStringValue, interations:'int'=1, axis:AxisOrItsIndexOrItsName="z"):
        
        return self
        

    def remesh(self, strategy:str, amount:float):
        
        return self
        

    def createLandmark(self, landmarkName:str, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue) -> 'LandmarkInterface':
        
        raise NotImplementedError()
        

    def getBoundingBox(self) -> 'BoundaryBox':
        
        raise NotImplementedError()
        

    def getDimensions(self) -> 'Dimensions':
        
        raise NotImplementedError()
        

    def getLandmark(self, landmarkName:PresetLandmarkOrItsName) -> 'LandmarkInterface':
        
        raise NotImplementedError()
        
    