# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from CodeToCAD import Analytics

class AnalyticsTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1","entity2")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1","entity2","pivot")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getWorldPose(self):
        instance = Analytics("")

        value = instance.getWorldPose("entity")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getBoundingBox(self):
        instance = Analytics("")

        value = instance.getBoundingBox("entityName")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_getDimensions(self):
        instance = Analytics("")

        value = instance.getDimensions("entityName")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_log(self):
        instance = Analytics("")

        value = instance.log("message")

        
        assert value, "Modify method failed."
        