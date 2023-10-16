
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *


class CameraInterface(metaclass=ABCMeta):
    '''Manipulate a camera object.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def create_perspective(self):
        '''
        Create a perspective camera in the scene.
        '''
        
        print("create_perspective is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_orthogonal(self):
        '''
        Create an orthogonal camera in the scene.
        '''
        
        print("create_orthogonal is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def set_focal_length(self, length:float):
        '''
        Set the focal length of the camera.
        '''
        
        print("set_focal_length is called in an abstract method. Please override this method.")
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
        Check if an camera exists
        '''
        
        print("is_exists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, new_name:str):
        '''
        Rename the camera.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Delete the camera from the scene.
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
        Get the camera XYZ location relative to World Space.
        '''
        
        print("get_location_world is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_location_local(self) -> 'Point':
        '''
        Get the camera XYZ location relative to Local Space.
        '''
        
        print("get_location_local is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def select(self):
        '''
        Select the entity (in UI).
        '''
        
        print("select is called in an abstract method. Please override this method.")
        return self
        