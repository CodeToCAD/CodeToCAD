
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *

from codetocad.interfaces import EntityInterface


class SketchInterface(EntityInterface, metaclass=ABCMeta):
    '''Capabilities related to adding, multiplying, and/or modifying a curve.'''

    
    name:str
    curve_type:Optional['CurveTypes']=None
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, curve_type:Optional['CurveTypes']=None, description:Optional[str]=None):
        super().__init__(name,description)
    
        self.name = name
        self.curve_type = curve_type
        self.description = description

    @abstractmethod
    def clone(self, new_name:str, copy_landmarks:bool=True) -> 'SketchInterface':
        '''
        Clone an existing sketch with its geometry and properties. Returns the new Sketch.
        '''
        
        print("clone is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def revolve(self, angle:AngleOrItsFloatOrStringValue, about_entity_or_landmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName="z") -> 'PartInterface':
        '''
        Revolve a Sketch around another Entity or Landmark
        '''
        
        print("revolve is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def extrude(self, length:DimensionOrItsFloatOrStringValue) -> 'PartInterface':
        '''
        Extrude a curve by a specified length. Returns a Part type.
        '''
        
        print("extrude is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def sweep(self, profile_name_or_instance:SketchOrItsName, fill_cap:bool=True) -> 'PartInterface':
        '''
        Extrude this Sketch along the path of another Sketch
        '''
        
        print("sweep is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def offset(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Uniformly add a wall around a Sketch.
        '''
        
        print("offset is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def profile(self, profile_curve_name:str):
        '''
        Bend this curve along the path of another
        '''
        
        print("profile is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_text(self, text:str, font_size:DimensionOrItsFloatOrStringValue=1.0, bold:bool=False, italic:bool=False, underlined:bool=False, character_spacing:'int'=1, word_spacing:'int'=1, line_spacing:'int'=1, font_file_path:Optional[str]=None):
        '''
        Adds text to a sketch.
        '''
        
        print("create_text is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_from_vertices(self, coordinates:list[PointOrListOfFloatOrItsStringValue], interpolation:'int'=64):
        '''
        Create a curve from 2D/3D points.
        '''
        
        print("create_from_vertices is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_point(self, coordinate:PointOrListOfFloatOrItsStringValue):
        '''
        Create a point
        '''
        
        print("create_point is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_line(self, length:DimensionOrItsFloatOrStringValue, angle_x:AngleOrItsFloatOrStringValue=0.0, angle_y:AngleOrItsFloatOrStringValue=0.0, symmetric:bool=False):
        '''
        Create a line
        '''
        
        print("create_line is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_line_between_points(self, end_at:PointOrListOfFloatOrItsStringValue, start_at:Optional[PointOrListOfFloatOrItsStringValue]=None):
        '''
        Create a line between two points
        '''
        
        print("create_line_between_points is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_circle(self, radius:DimensionOrItsFloatOrStringValue):
        '''
        Create a circle
        '''
        
        print("create_circle is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_ellipse(self, radius_a:DimensionOrItsFloatOrStringValue, radius_b:DimensionOrItsFloatOrStringValue):
        '''
        Create an ellipse
        '''
        
        print("create_ellipse is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_arc(self, radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        '''
        Create an arc
        '''
        
        print("create_arc is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_arc_between_three_points(self, point_a:'Point', point_b:'Point', center_point:'Point'):
        '''
        Create a 3-point arc
        '''
        
        print("create_arc_between_three_points is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_segment(self, inner_radius:DimensionOrItsFloatOrStringValue, outer_radius:DimensionOrItsFloatOrStringValue, angle:AngleOrItsFloatOrStringValue="180d"):
        '''
        Create a segment (intersection of two circles)
        '''
        
        print("create_segment is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_rectangle(self, length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        '''
        Create a rectangle
        '''
        
        print("create_rectangle is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_polygon(self, number_of_sides:'int', length:DimensionOrItsFloatOrStringValue, width:DimensionOrItsFloatOrStringValue):
        '''
        Create an n-gon
        '''
        
        print("create_polygon is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_trapezoid(self, length_upper:DimensionOrItsFloatOrStringValue, length_lower:DimensionOrItsFloatOrStringValue, height:DimensionOrItsFloatOrStringValue):
        '''
        Create a trapezoid
        '''
        
        print("create_trapezoid is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_spiral(self, number_of_turns:'int', height:DimensionOrItsFloatOrStringValue, radius:DimensionOrItsFloatOrStringValue, is_clockwise:bool=True, radius_end:Optional[DimensionOrItsFloatOrStringValue]=None):
        '''
        Create a trapezoid
        '''
        
        print("create_spiral is called in an abstract method. Please override this method.")
        return self
        