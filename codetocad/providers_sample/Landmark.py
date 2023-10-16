# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Landmark(LandmarkInterface): 
    
    
    name:str
    parent_entity:EntityOrItsName
    description:Optional[str]=None

    def __init__(self, name:str, parent_entity:EntityOrItsName, description:Optional[str]=None):
        self.name = name
        self.parent_entity = parent_entity
        self.description = description

    def get_landmark_entity_name(self) -> str:
        
        raise NotImplementedError()
        

    def get_parent_entity(self) -> 'EntityInterface':
        
        raise NotImplementedError()
        

    def is_exists(self) -> bool:
        
        raise NotImplementedError()
        

    def rename(self, new_name:str):
        
        return self
        

    def delete(self):
        
        return self
        

    def is_visible(self) -> bool:
        
        raise NotImplementedError()
        

    def set_visible(self, is_visible:bool):
        
        return self
        

    def get_native_instance(self) -> object:
        
        raise NotImplementedError()
        

    def get_location_world(self) -> 'Point':
        
        raise NotImplementedError()
        

    def get_location_local(self) -> 'Point':
        
        raise NotImplementedError()
        

    def select(self):
        
        return self
        
    