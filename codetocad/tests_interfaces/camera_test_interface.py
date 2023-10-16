# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Camera

class CameraTestInterface(metaclass=ABCMeta):
    
    
    
    @abstractmethod
    def test_create_perspective(self):
        instance = Camera("name","description")

        value = instance.create_perspective("")

        
        assert value.isExists(), "Create method failed."
        
    
    @abstractmethod
    def test_create_orthogonal(self):
        instance = Camera("name","description")

        value = instance.create_orthogonal("")

        
        assert value.isExists(), "Create method failed."
        
    
    @abstractmethod
    def test_set_focal_length(self):
        instance = Camera("name","description")

        value = instance.set_focal_length("length")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_translate_xyz(self):
        instance = Camera("name","description")

        value = instance.translate_xyz("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_rotate_xyz(self):
        instance = Camera("name","description")

        value = instance.rotate_xyz("x","y","z")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_is_exists(self):
        instance = Camera("name","description")

        value = instance.is_exists("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_rename(self):
        instance = Camera("name","description")

        value = instance.rename("new_name")

        
        assert value, "Modify method failed."
        
    
    @abstractmethod
    def test_delete(self):
        instance = Camera("name","description")

        value = instance.delete("")

        
    
    @abstractmethod
    def test_get_native_instance(self):
        instance = Camera("name","description")

        value = instance.get_native_instance("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_location_world(self):
        instance = Camera("name","description")

        value = instance.get_location_world("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_get_location_local(self):
        instance = Camera("name","description")

        value = instance.get_location_local("")

        
        assert value, "Get method failed."
        
    
    @abstractmethod
    def test_select(self):
        instance = Camera("name","description")

        value = instance.select("")

        