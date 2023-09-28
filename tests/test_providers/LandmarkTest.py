# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip, TestCase

from CodeToCAD import Landmark
from CodeToCAD.testsInterfaces import LandmarkTestInterface

class LandmarkTest(TestCase, LandmarkTestInterface):
    
    
    @skip("TODO")
    def test_getLandmarkEntityName(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLandmarkEntityName("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getParentEntity(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getParentEntity("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_isExists(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_rename(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_delete(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.delete("")

        
    @skip("TODO")
    def test_isVisible(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.isVisible("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_setVisible(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.setVisible("isVisible")

        
    @skip("TODO")
    def test_getNativeInstance(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationWorld(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationLocal(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_select(self):
        instance = Landmark("name","parentEntity","description")

        value = instance.select("")

        