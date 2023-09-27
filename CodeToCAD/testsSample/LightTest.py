# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from CodeToCAD import Light
from CodeToCAD.testsInterfaces.LightTestInterface import LightTestInterface

class TestLight(LightTestInterface):
    
    
    @skip("TODO")
    def test_setColor(self):
        instance = Light("name","description")

        value = instance.setColor("rValue","gValue","bValue")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_createSun(self):
        instance = Light("name","description")

        value = instance.createSun("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createSpot(self):
        instance = Light("name","description")

        value = instance.createSpot("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createPoint(self):
        instance = Light("name","description")

        value = instance.createPoint("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createArea(self):
        instance = Light("name","description")

        value = instance.createArea("energyLevel")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_translateXYZ(self):
        instance = Light("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_rotateXYZ(self):
        instance = Light("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_isExists(self):
        instance = Light("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_rename(self):
        instance = Light("name","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_delete(self):
        instance = Light("name","description")

        value = instance.delete("")

        
    @skip("TODO")
    def test_getNativeInstance(self):
        instance = Light("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationWorld(self):
        instance = Light("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationLocal(self):
        instance = Light("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_select(self):
        instance = Light("name","description")

        value = instance.select("")

        