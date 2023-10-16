# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Animation

class AnimationTestInterface(metaclass=ABCMeta):
    
    
    
    
    @abstractmethod
    def test_set_frame_start(self):
        instance = Animation("")

        value = instance.set_frame_start("frame_number")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_set_frame_end(self):
        instance = Animation("")

        value = instance.set_frame_end("frame_number")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_set_frame_current(self):
        instance = Animation("")

        value = instance.set_frame_current("frame_number")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_create_key_frame_location(self):
        instance = Animation("")

        value = instance.create_key_frame_location("entity","frame_number")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_create_key_frame_rotation(self):
        instance = Animation("")

        value = instance.create_key_frame_rotation("entity","frame_number")

        
        assert value, "Modify method failed."
        