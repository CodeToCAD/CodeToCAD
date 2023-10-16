
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *


class LightInterface(metaclass=ABCMeta):
    '''Manipulate a light object.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def set_color(self, r_value:IntOrFloat, g_value:IntOrFloat, b_value:IntOrFloat):
        '''
        Set the color of an existing light.
        '''
        
        print("set_color is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_sun(self, energy_level:float):
        '''
        Create a Sun-type light.
        '''
        
        print("create_sun is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_spot(self, energy_level:float):
        '''
        Create a Spot-type light.
        '''
        
        print("create_spot is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_point(self, energy_level:float):
        '''
        Create a Point-type light.
        '''
        
        print("create_point is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_area(self, energy_level:float):
        '''
        Create an Area-type light.
        '''
        
        print("create_area is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translate_xyz(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("translate_xyz is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotate_xyz(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotate_xyz is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def is_exists(self) -> bool:
        '''
        Check if an light exists
        '''
        
        print("is_exists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, new_name:str):
        '''
        Rename the light.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Delete the light from the scene.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def get_native_instance(self) -> object:
        '''
        Get the native API's object instance. For example, in Blender API, this would return a bpy.object instance.
        '''
        
        print("get_native_instance is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_location_world(self) -> 'Point':
        '''
        Get the light XYZ location relative to World Space.
        '''
        
        print("get_location_world is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_location_local(self) -> 'Point':
        '''
        Get the light XYZ location relative to Local Space.
        '''
        
        print("get_location_local is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def select(self):
        '''
        Select the light (in UI).
        '''
        
        print("select is called in an abstract method. Please override this method.")
        return self
        