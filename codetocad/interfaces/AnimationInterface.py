
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

from abc import ABCMeta, abstractmethod
from CodeToCAD.CodeToCADTypes import *


class AnimationInterface(metaclass=ABCMeta):
    '''Animation related functionality.'''

    

    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def default() -> 'AnimationInterface':
        raise RuntimeError()
        

    @abstractmethod
    def setFrameStart(self, frameNumber:'int'):
        '''
        Set the start animation frame in the scene.
        '''
        
        print("setFrameStart is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setFrameEnd(self, frameNumber:'int'):
        '''
        Set the end animation frame in the scene.
        '''
        
        print("setFrameEnd is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def setFrameCurrent(self, frameNumber:'int'):
        '''
        Set the current animation frame in the scene.
        '''
        
        print("setFrameCurrent is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createKeyFrameLocation(self, entity:EntityOrItsName, frameNumber:'int'):
        '''
        Create an animation key-frame using the location of the entity.
        '''
        
        print("createKeyFrameLocation is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def createKeyFrameRotation(self, entity:EntityOrItsName, frameNumber:'int'):
        '''
        Create an animation key-frame using the rotation of the entity.
        '''
        
        print("createKeyFrameRotation is called in an abstract method. Please override this method.")
        return self
        