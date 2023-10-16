# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import LightInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Light(LightInterface): 
    
    
    name:str
    description:Optional[str]=None

    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    def set_color(self, r_value:IntOrFloat, g_value:IntOrFloat, b_value:IntOrFloat):
        
        return self
        

    def create_sun(self, energy_level:float):
        
        return self
        

    def create_spot(self, energy_level:float):
        
        return self
        

    def create_point(self, energy_level:float):
        
        return self
        

    def create_area(self, energy_level:float):
        
        return self
        

    def translate_xyz(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def rotate_xyz(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        
        return self
        

    def is_exists(self) -> bool:
        
        raise NotImplementedError()
        

    def rename(self, new_name:str):
        
        return self
        

    def delete(self):
        
        return self
        

    def get_native_instance(self) -> object:
        
        raise NotImplementedError()
        

    def get_location_world(self) -> 'Point':
        
        raise NotImplementedError()
        

    def get_location_local(self) -> 'Point':
        
        raise NotImplementedError()
        

    def select(self):
        
        return self
        
    