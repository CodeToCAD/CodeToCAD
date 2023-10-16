
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *


class LandmarkInterface(metaclass=ABCMeta):
    '''Landmarks are named positions on an entity.'''

    
    name:str
    parent_entity:EntityOrItsName
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, parent_entity:EntityOrItsName, description:Optional[str]=None):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description

    @abstractmethod
    def get_landmark_entity_name(self) -> str:
        '''
        Get the landmark object name in the scene, which may be different to the name of the landmark when it was first created. For example, the generated name may be {parentName}_{landmarkName}.
        '''
        
        print("get_landmark_entity_name is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_parent_entity(self) -> 'EntityInterface':
        '''
        Get the name of the entity this landmark belongs to.
        '''
        
        print("get_parent_entity is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def is_exists(self) -> bool:
        '''
        Check if an landmark exists
        '''
        
        print("is_exists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, new_name:str):
        '''
        Rename the landmark.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self):
        '''
        Delete the landmark from the scene.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def is_visible(self) -> bool:
        '''
        Returns whether the landmark is visible in the scene.
        '''
        
        print("is_visible is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def set_visible(self, is_visible:bool):
        '''
        Toggles visibility of an landmark in the scene.
        '''
        
        print("set_visible is called in an abstract method. Please override this method.")
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
        Get the landmark XYZ location relative to World Space.
        '''
        
        print("get_location_world is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_location_local(self) -> 'Point':
        '''
        Get the landmark XYZ location relative to Local Space.
        '''
        
        print("get_location_local is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def select(self):
        '''
        Select the landmark (in UI).
        '''
        
        print("select is called in an abstract method. Please override this method.")
        return self
        