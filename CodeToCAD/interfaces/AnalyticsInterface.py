
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class AnalyticsInterface(metaclass=ABCMeta):
    '''Tools for collecting data about the entities and scene.'''

    

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def measureDistance(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark) -> 'Dimensions':
        '''
        The ubiquitous ruler.
        '''
        
        print("measureDistance is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def measureAngle(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark, pivot:Optional[EntityOrItsNameOrLandmark]=None) -> 'list[Angle]':
        '''
        The ubiquitous ruler.
        '''
        
        print("measureAngle is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getWorldPose(self, entity:EntityOrItsName) -> 'list[float]':
        '''
        Returns the world pose of an entity.
        '''
        
        print("getWorldPose is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getBoundingBox(self, entityName:EntityOrItsName) -> 'BoundaryBox':
        '''
        Returns the bounding box of an entity.
        '''
        
        print("getBoundingBox is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def getDimensions(self, entityName:EntityOrItsName) -> 'Dimensions':
        '''
        Returns the dimensions of an entity.
        '''
        
        print("getDimensions is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def log(self, message:str):
        '''
        Write a message
        '''
        
        print("log is called in an abstract method. Please override this method.")
        return self
        