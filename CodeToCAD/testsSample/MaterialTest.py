# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from CodeToCAD import Material
from CodeToCAD.testsInterfaces.MaterialTestInterface import MaterialTestInterface

class TestMaterial(MaterialTestInterface):
    
    
    @skip("TODO")
    def test_assignToPart(self):
        instance = Material("name","description")

        value = instance.assignToPart("partNameOrInstance")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setColor(self):
        instance = Material("name","description")

        value = instance.setColor("rValue","gValue","bValue","aValue")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setReflectivity(self):
        instance = Material("name","description")

        value = instance.setReflectivity("reflectivity")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_setRoughness(self):
        instance = Material("name","description")

        value = instance.setRoughness("roughness")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_addImageTexture(self):
        instance = Material("name","description")

        value = instance.addImageTexture("imageFilePath")

        
        assert value, "Modify method failed."
        