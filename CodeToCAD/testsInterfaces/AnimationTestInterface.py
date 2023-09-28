# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from CodeToCAD import Animation

class AnimationTestInterface(metaclass=ABCMeta):
    
    
    
    
    @abstractmethod
    def test_setFrameStart(self):
        instance = Animation("")

        value = instance.setFrameStart("frameNumber")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setFrameEnd(self):
        instance = Animation("")

        value = instance.setFrameEnd("frameNumber")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_setFrameCurrent(self):
        instance = Animation("")

        value = instance.setFrameCurrent("frameNumber")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        value = instance.createKeyFrameLocation("entity","frameNumber")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        value = instance.createKeyFrameRotation("entity","frameNumber")

        
        assert value, "Modify method failed."
        