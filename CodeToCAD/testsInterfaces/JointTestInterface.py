# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from CodeToCAD import Joint

class JointTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_translateLandmarkOntoAnother(self):
        instance = Joint("entity1","entity2")

        value = instance.translateLandmarkOntoAnother("")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_pivot(self):
        instance = Joint("entity1","entity2")

        value = instance.pivot("")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_gearRatio(self):
        instance = Joint("entity1","entity2")

        value = instance.gearRatio("ratio")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitLocationXYZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitLocationX(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationX("min","max")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitLocationY(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationY("min","max")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitLocationZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitLocationZ("min","max")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitRotationXYZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationXYZ("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitRotationX(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationX("min","max")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitRotationY(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationY("min","max")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_limitRotationZ(self):
        instance = Joint("entity1","entity2")

        value = instance.limitRotationZ("min","max")

        
        assert value, "Modify method failed."
        