# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from CodeToCAD import Animation
from CodeToCAD.testsInterfaces import AnimationTestInterface

class TestAnimation(AnimationTestInterface):
    
    
    
    @skip("TODO")
    def test_setFrameStart(self):
        instance = Animation("")

        value = instance.setFrameStart("frameNumber")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setFrameEnd(self):
        instance = Animation("")

        value = instance.setFrameEnd("frameNumber")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setFrameCurrent(self):
        instance = Animation("")

        value = instance.setFrameCurrent("frameNumber")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        value = instance.createKeyFrameLocation("entity","frameNumber")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        value = instance.createKeyFrameRotation("entity","frameNumber")

        
        assert value, "Modify method failed."
        