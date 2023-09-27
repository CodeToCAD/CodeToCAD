# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from CodeToCAD import Camera
from CodeToCAD.testsInterfaces.CameraTestInterface import CameraTestInterface

class TestCamera(CameraTestInterface):
    
    
    @skip("TODO")
    def test_createPerspective(self):
        instance = Camera("name","description")

        value = instance.createPerspective("")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_createOrthogonal(self):
        instance = Camera("name","description")

        value = instance.createOrthogonal("")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_setFocalLength(self):
        instance = Camera("name","description")

        value = instance.setFocalLength("length")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_translateXYZ(self):
        instance = Camera("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_rotateXYZ(self):
        instance = Camera("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_isExists(self):
        instance = Camera("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_rename(self):
        instance = Camera("name","description")

        value = instance.rename("newName")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_delete(self):
        instance = Camera("name","description")

        value = instance.delete("")

        
    @skip("TODO")
    def test_getNativeInstance(self):
        instance = Camera("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationWorld(self):
        instance = Camera("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_getLocationLocal(self):
        instance = Camera("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_select(self):
        instance = Camera("name","description")

        value = instance.select("")

        