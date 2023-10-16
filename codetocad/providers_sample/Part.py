# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import PartInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from . import Entity


class Part(Entity, PartInterface): 
    
    

    def create_cube(self, width:DimensionOrItsFloatOrStringValue, length:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def create_cone(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, draft_radius:DimensionOrItsFloatOrStringValue=0, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def create_cylinder(self, radius:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def create_torus(self, inner_radius:DimensionOrItsFloatOrStringValue, outer_radius:DimensionOrItsFloatOrStringValue, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def create_sphere(self, radius:DimensionOrItsFloatOrStringValue, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def create_gear(self, outer_radius:DimensionOrItsFloatOrStringValue, addendum:DimensionOrItsFloatOrStringValue, inner_radius:DimensionOrItsFloatOrStringValue, dedendum:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue, pressure_angle:AngleOrItsFloatOrStringValue="20d", number_of_teeth:'int'=12, skew_angle:AngleOrItsFloatOrStringValue=0, conical_angle:AngleOrItsFloatOrStringValue=0, crown_angle:AngleOrItsFloatOrStringValue=0, keyword_arguments:Optional[dict]=None):
        
        return self
        

    def clone(self, new_name:str, copy_landmarks:bool=True) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def loft(self, landmark1:'LandmarkInterface', landmark2:'LandmarkInterface'):
        
        return self
        

    def union(self, with_part:PartOrItsName, delete_after_union:bool=True, is_transfer_landmarks:bool=False):
        
        return self
        

    def subtract(self, with_part:PartOrItsName, delete_after_subtract:bool=True, is_transfer_landmarks:bool=False):
        
        return self
        

    def intersect(self, with_part:PartOrItsName, delete_after_intersect:bool=True, is_transfer_landmarks:bool=False):
        
        return self
        

    def hollow(self, thickness_x:DimensionOrItsFloatOrStringValue, thickness_y:DimensionOrItsFloatOrStringValue, thickness_z:DimensionOrItsFloatOrStringValue, start_axis:AxisOrItsIndexOrItsName="z", flip_axis:bool=False):
        
        return self
        

    def thicken(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def hole(self, hole_landmark:LandmarkOrItsName, radius:DimensionOrItsFloatOrStringValue, depth:DimensionOrItsFloatOrStringValue, normal_axis:AxisOrItsIndexOrItsName="z", flip_axis:bool=False, initial_rotation_x:AngleOrItsFloatOrStringValue=0.0, initial_rotation_y:AngleOrItsFloatOrStringValue=0.0, initial_rotation_z:AngleOrItsFloatOrStringValue=0.0, mirror_about_entity_or_landmark:Optional[EntityOrItsNameOrLandmark]=None, mirror_axis:AxisOrItsIndexOrItsName="x", mirror:bool=False, circular_pattern_instance_count:'int'=1, circular_pattern_instance_separation:AngleOrItsFloatOrStringValue=0.0, circular_pattern_instance_axis:AxisOrItsIndexOrItsName="z", circular_pattern_about_entity_or_landmark:Optional[EntityOrItsNameOrLandmark]=None, linear_pattern_instance_count:'int'=1, linear_pattern_instance_separation:DimensionOrItsFloatOrStringValue=0.0, linear_pattern_instance_axis:AxisOrItsIndexOrItsName="x", linear_pattern2nd_instance_count:'int'=1, linear_pattern2nd_instance_separation:DimensionOrItsFloatOrStringValue=0.0, linear_pattern2nd_instance_axis:AxisOrItsIndexOrItsName="y"):
        
        return self
        

    def set_material(self, material_name:MaterialOrItsName):
        
        return self
        

    def is_colliding_with_part(self, other_part:PartOrItsName) -> bool:
        
        raise NotImplementedError()
        

    def fillet_all_edges(self, radius:DimensionOrItsFloatOrStringValue, use_width:bool=False):
        
        return self
        

    def fillet_edges(self, radius:DimensionOrItsFloatOrStringValue, landmarks_near_edges:list[LandmarkOrItsName], use_width:bool=False):
        
        return self
        

    def fillet_faces(self, radius:DimensionOrItsFloatOrStringValue, landmarks_near_faces:list[LandmarkOrItsName], use_width:bool=False):
        
        return self
        

    def chamfer_all_edges(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def chamfer_edges(self, radius:DimensionOrItsFloatOrStringValue, landmarks_near_edges:list[LandmarkOrItsName]):
        
        return self
        

    def chamfer_faces(self, radius:DimensionOrItsFloatOrStringValue, landmarks_near_faces:list[LandmarkOrItsName]):
        
        return self
        

    def select_vertex_near_landmark(self, landmark_name:Optional[LandmarkOrItsName]=None):
        
        return self
        

    def select_edge_near_landmark(self, landmark_name:Optional[LandmarkOrItsName]=None):
        
        return self
        

    def select_face_near_landmark(self, landmark_name:Optional[LandmarkOrItsName]=None):
        
        return self
        
    