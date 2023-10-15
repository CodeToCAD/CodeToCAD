# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from CodeToCAD.interfaces import AnimationInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Animation(AnimationInterface): 
    
    

    def __init__(self):
        pass

    @staticmethod
    def default() -> 'AnimationInterface':
        return Animation()

    def setFrameStart(self, frameNumber:'int'):
        
        return self
        

    def setFrameEnd(self, frameNumber:'int'):
        
        return self
        

    def setFrameCurrent(self, frameNumber:'int'):
        
        return self
        

    def createKeyFrameLocation(self, entity:EntityOrItsName, frameNumber:'int'):
        
        return self
        

    def createKeyFrameRotation(self, entity:EntityOrItsName, frameNumber:'int'):
        
        return self
        
    