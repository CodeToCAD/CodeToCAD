# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Analytics

class AnalyticsTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_measure_distance(self):
        instance = Analytics("")

        value = instance.measure_distance("entity1","entity2")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_measure_angle(self):
        instance = Analytics("")

        value = instance.measure_angle("entity1","entity2","pivot")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_world_pose(self):
        instance = Analytics("")

        value = instance.get_world_pose("entity")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_bounding_box(self):
        instance = Analytics("")

        value = instance.get_bounding_box("entity_name")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_dimensions(self):
        instance = Analytics("")

        value = instance.get_dimensions("entity_name")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_log(self):
        instance = Analytics("")

        value = instance.log("message")

        
        assert value, "Modify method failed."
        