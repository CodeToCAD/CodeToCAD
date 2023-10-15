# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from CodeToCAD import Entity

class EntityTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_createFromFile(self):
        instance = Part("name","description")

        value = instance.createFromFile("filePath","fileType")

        
        assert value.isExists(), "Create method failed."
        
    
    @abstractmethod
    def test_isExists(self):
        instance = Part("name","description")

        value = instance.isExists("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_rename(self):
        instance = Part("name","description")

        value = instance.rename("newName","renamelinkedEntitiesAndLandmarks")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_delete(self):
        instance = Part("name","description")

        value = instance.delete("removeChildren")

        
    
    @abstractmethod
    def test_isVisible(self):
        instance = Part("name","description")

        value = instance.isVisible("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_setVisible(self):
        instance = Part("name","description")

        value = instance.setVisible("isVisible")

        
    
    @abstractmethod
    def test_apply(self):
        instance = Part("name","description")

        value = instance.apply("rotation","scale","location","modifiers")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_getNativeInstance(self):
        instance = Part("name","description")

        value = instance.getNativeInstance("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getLocationWorld(self):
        instance = Part("name","description")

        value = instance.getLocationWorld("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getLocationLocal(self):
        instance = Part("name","description")

        value = instance.getLocationLocal("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_select(self):
        instance = Part("name","description")

        value = instance.select("")

        
    
    @abstractmethod
    def test_export(self):
        instance = Part("name","description")

        value = instance.export("filePath","overwrite","scale")

        
    
    @abstractmethod
    def test_mirror(self):
        instance = Part("name","description")

        value = instance.mirror("mirrorAcrossEntityOrLandmark","axis","resultingMirroredEntityName")

        
        assert value.isExists(), "Create method failed."
        
    
    @abstractmethod
    def test_linearPattern(self):
        instance = Part("name","description")

        value = instance.linearPattern("instanceCount","offset","directionAxis")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_circularPattern(self):
        instance = Part("name","description")

        value = instance.circularPattern("instanceCount","separationAngle","centerEntityOrLandmark","normalDirectionAxis")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_translateXYZ(self):
        instance = Part("name","description")

        value = instance.translateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_translateX(self):
        instance = Part("name","description")

        value = instance.translateX("amount")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_translateY(self):
        instance = Part("name","description")

        value = instance.translateY("amount")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_translateZ(self):
        instance = Part("name","description")

        value = instance.translateZ("amount")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleXYZ(self):
        instance = Part("name","description")

        value = instance.scaleXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleX(self):
        instance = Part("name","description")

        value = instance.scaleX("scale")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleY(self):
        instance = Part("name","description")

        value = instance.scaleY("scale")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleZ(self):
        instance = Part("name","description")

        value = instance.scaleZ("scale")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleXByFactor(self):
        instance = Part("name","description")

        value = instance.scaleXByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleYByFactor(self):
        instance = Part("name","description")

        value = instance.scaleYByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleZByFactor(self):
        instance = Part("name","description")

        value = instance.scaleZByFactor("scaleFactor")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_scaleKeepAspectRatio(self):
        instance = Part("name","description")

        value = instance.scaleKeepAspectRatio("scale","axis")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_rotateXYZ(self):
        instance = Part("name","description")

        value = instance.rotateXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_rotateX(self):
        instance = Part("name","description")

        value = instance.rotateX("rotation")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_rotateY(self):
        instance = Part("name","description")

        value = instance.rotateY("rotation")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_rotateZ(self):
        instance = Part("name","description")

        value = instance.rotateZ("rotation")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_twist(self):
        instance = Part("name","description")

        value = instance.twist("angle","screwPitch","interations","axis")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_remesh(self):
        instance = Part("name","description")

        value = instance.remesh("strategy","amount")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_createLandmark(self):
        instance = Part("name","description")

        value = instance.createLandmark("landmarkName","x","y","z")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getBoundingBox(self):
        instance = Part("name","description")

        value = instance.getBoundingBox("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getDimensions(self):
        instance = Part("name","description")

        value = instance.getDimensions("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getLandmark(self):
        instance = Part("name","description")

        value = instance.getLandmark("landmarkName")

        
        assert value, "Get method failed."
        