# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import SketchInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from . import Entity


class Sketch(Entity, SketchInterface): 
    
    
    name:str
    curve_type:Optional['CurveTypes']=None
    description:Optional[str]=None

    def __init__(self, name:str, curve_type:Optional['CurveTypes']=None, description:Optional[str]=None):
        self.name = name
        self.curve_type = curve_type
        self.description = description

    def clone(self, new_name:str, copy_landmarks:bool=True) -> 'SketchInterface':
        
        raise NotImplementedError()
        

    def revolve(self, angle:AngleOrItsFloatOrStringValue, about_entity_or_landmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName="z") -> 'PartInterface':
        
        raise NotImplementedError()
        

    def extrude(self, length:DimensionOrItsFloatOrStringValue) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def sweep(self, profile_name_or_instance:SketchOrItsName, fill_cap:bool=True) -> 'PartInterface':
        
        raise NotImplementedError()
        

    def offset(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def profile(self, profile_curve_name:str):
        
        return self
        

    def create_text(self, text:str, font_size:DimensionOrItsFloatOrStringValue=1.0, bold:bool=False, italic:bool=False, underlined:bool=False, character_spacing:'int'=1, word_spacing:'int'=1, line_spacing:'int'=1, font_file_path:Optional[str]=None):
        
        return self
        

    def create_from_vertices(self, coordinates:list[PointOrListOfFloatOrItsStringValue], interpolation:'int'=64):
        
        return self
        

    def create_point(self, coordinate:PointOrListOfFloatOrItsStringValue):
        
        return self
        

    def create_line(self, length:DimensionOrItsFloatOrStringValue, angle_x:AngleOrItsFloatOrStringValue=0.0, angle_y:AngleOrItsFloatOrStringValue=0.0, symmetric:bool=False):
        
        return self
        

    def create_line_between_points(self, end_at:PointOrListOfFloatOrItsStringValue, start_at:Optional[PointOrListOfFloatOrItsStringValue]=None):
        
        return self
        

    def create_circle(self, radius:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def create_ellipse(self, radius_a:DimensionOrItsFloatOrStringValue, radius_b:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def create_arc(self, radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        
        return self
        

    def create_arc_between_three_points(self, point_a:'Point', point_b:'Point', center_point:'Point'):
        
        return self
        

    def create_segment(self, inner_radius:DimensionOrItsFloatOrStringValue, outer_radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        
        return self
        

    def create_rectangle(self, length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def create_polygon(self, number_of_sides:'int', length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def create_trapezoid(self, length_upper:DimensionOrItsFloatOrStringValue, length_lower:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue):
        
        return self
        

    def create_spiral(self, number_of_turns:'int', height:DimensionOrItsFloatOrStringValue, radius:DimensionOrItsFloatOrStringValue, is_clockwise:bool=True, radius_end:Optional[DimensionOrItsFloatOrStringValue]=None):
        
        return self
        
    