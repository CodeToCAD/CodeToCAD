# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import LandmarkTestInterface

class LandmarkTest(TestProviderCase, LandmarkTestInterface):
    
    
    @skip("TODO")
    def test_get_landmark_entity_name(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_landmark_entity_name("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_get_parent_entity(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_parent_entity("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_is_exists(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.is_exists("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_rename(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.rename("new_name")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_delete(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.delete("")

        
    @skip("TODO")
    def test_is_visible(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.is_visible("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_set_visible(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.set_visible("is_visible")

        
    @skip("TODO")
    def test_get_native_instance(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_native_instance("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_get_location_world(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_location_world("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_get_location_local(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.get_location_local("")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_select(self):
        instance = Landmark("name","parent_entity","description")

        value = instance.select("")

        