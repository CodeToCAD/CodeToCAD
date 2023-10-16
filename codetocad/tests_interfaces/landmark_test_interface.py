# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Landmark

class LandmarkTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_get_landmark_entity_name(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_landmark_entity_name("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_parent_entity(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_parent_entity("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_is_exists(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.is_exists("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_rename(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.rename("new_name")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_delete(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.delete("")

        
    
    @abstractmethod
    def test_is_visible(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.is_visible("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_set_visible(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.set_visible("is_visible")

        
    
    @abstractmethod
    def test_get_native_instance(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_native_instance("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_location_world(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_location_world("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_location_local(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_location_local("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_select(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.select("")

        