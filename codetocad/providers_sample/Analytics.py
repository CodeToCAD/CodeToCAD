# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import AnalyticsInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *


class Analytics(AnalyticsInterface): 
    
    

    def __init__(self):
        pass

    def measure_distance(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark) -> 'Dimensions':
        
        raise NotImplementedError()
        

    def measure_angle(self, entity1:EntityOrItsNameOrLandmark, entity2:EntityOrItsNameOrLandmark, pivot:Optional[EntityOrItsNameOrLandmark]=None) -> 'list[Angle]':
        
        raise NotImplementedError()
        

    def get_world_pose(self, entity:EntityOrItsName) -> 'list[float]':
        
        raise NotImplementedError()
        

    def get_bounding_box(self, entity_name:EntityOrItsName) -> 'BoundaryBox':
        
        raise NotImplementedError()
        

    def get_dimensions(self, entity_name:EntityOrItsName) -> 'Dimensions':
        
        raise NotImplementedError()
        

    def log(self, message:str):
        
        return self
        
    