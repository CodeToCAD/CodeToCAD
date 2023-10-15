# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import AnalyticsInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Analytics(AnalyticsInterface): 
    
    

    def __init__(self):
        pass

    def measureDistance(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark) -> 'Dimensions':
        
        raise NotImplementedError()
        

    def measureAngle(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark, pivot:Optional[EntityOrItsNameOrLandmark]=None) -> 'list[Angle]':
        
        raise NotImplementedError()
        

    def getWorldPose(self, entity:EntityOrItsName) -> 'list[float]':
        
        raise NotImplementedError()
        

    def getBoundingBox(self, entityName:EntityOrItsName) -> 'BoundaryBox':
        
        raise NotImplementedError()
        

    def getDimensions(self, entityName:EntityOrItsName) -> 'Dimensions':
        
        raise NotImplementedError()
        

    def log(self, message:str):
        
        return self
        
    