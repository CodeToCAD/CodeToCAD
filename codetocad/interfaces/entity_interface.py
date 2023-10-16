
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *


class EntityInterface(metaclass=ABCMeta):
    '''Capabilities shared between Parts and Sketches.'''

    
    name:str
    description:Optional[str]=None

    @abstractmethod
    def __init__(self, name:str, description:Optional[str]=None):
        self.name = name
        self.description = description

    @abstractmethod
    def create_from_file(self, file_path:str, file_type:Optional[str]=None):
        '''
        Adds geometry to a part from a file. If the part does not exist, this will create it.
        '''
        
        print("create_from_file is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def is_exists(self) -> bool:
        '''
        Check if an entity exists
        '''
        
        print("is_exists is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def rename(self, new_name:str, renamelinked_entities_and_landmarks:bool=True):
        '''
        Rename the entity, with an option to rename linked landmarks and underlying data.
        '''
        
        print("rename is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def delete(self, remove_children:bool):
        '''
        Delete the entity from the scene. You may need to delete an associated joint or other features.
        '''
        
        print("delete is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def is_visible(self) -> bool:
        '''
        Returns whether the entity is visible in the scene.
        '''
        
        print("is_visible is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def set_visible(self, is_visible:bool):
        '''
        Toggles visibility of an entity in the scene.
        '''
        
        print("set_visible is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def apply(self, rotation:bool=True, scale:bool=True, location:bool=False, modifiers:bool=True):
        '''
        Apply any modifications. This is application specific, but a general function is that it finalizes any changes made to an entity.
        '''
        
        print("apply is called in an abstract method. Please override this method.")
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
        Get the entities XYZ location relative to World Space.
        '''
        
        print("get_location_world is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_location_local(self) -> 'Point':
        '''
        Get the entities XYZ location relative to Local Space.
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
        

    @abstractmethod
    def export(self, file_path:str, overwrite:bool=True, scale:float=1.0):
        '''
        Export Entity. Use the filePath to control the export type, e.g. '/path/to/cube.obj' or '/path/to/curve.svg'
        '''
        
        print("export is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def mirror(self, mirror_across_entity_or_landmark:EntityOrItsNameOrLandmark, axis:AxisOrItsIndexOrItsName, resulting_mirrored_entity_name:Optional[str]=None):
        '''
        Mirror an existing entity with respect to a landmark. If a name is provided, the mirror becomes a separate entity.
        '''
        
        print("mirror is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def linear_pattern(self, instance_count:'int', offset:DimensionOrItsFloatOrStringValue, direction_axis:AxisOrItsIndexOrItsName="z"):
        '''
        Pattern in a uniform direction.
        '''
        
        print("linear_pattern is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def circular_pattern(self, instance_count:'int', separation_angle:AngleOrItsFloatOrStringValue, center_entity_or_landmark:EntityOrItsNameOrLandmark, normal_direction_axis:AxisOrItsIndexOrItsName="z"):
        '''
        Pattern in a circular direction.
        '''
        
        print("circular_pattern is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translate_xyz(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("translate_xyz is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translate_x(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the X direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translate_x is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translate_y(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the Y direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translate_y is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def translate_z(self, amount:DimensionOrItsFloatOrStringValue):
        '''
        Translate in the z direction. Pass a number or Dimension or Dimension-String (e.g. '2cm') to translate to a specific length.
        '''
        
        print("translate_z is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_xyz(self, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the XYZ directions. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scale_xyz is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_x(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the X direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scale_x is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_y(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the Y direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scale_y is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_z(self, scale:DimensionOrItsFloatOrStringValue):
        '''
        Scale in the Z direction. Pass a number, Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scale_z is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_x_by_factor(self, scale_factor:float):
        '''
        Scale in the X direction by a multiple.
        '''
        
        print("scale_x_by_factor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_y_by_factor(self, scale_factor:float):
        '''
        Scale in the Y direction by a multiple.
        '''
        
        print("scale_y_by_factor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_z_by_factor(self, scale_factor:float):
        '''
        Scale in the X direction by a multiple.
        '''
        
        print("scale_z_by_factor is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def scale_keep_aspect_ratio(self, scale:DimensionOrItsFloatOrStringValue, axis:AxisOrItsIndexOrItsName):
        '''
        Scale in one axis and maintain the others. Pass a Dimension or Dimension-String (e.g. '2cm') to scale to a specific length.
        '''
        
        print("scale_keep_aspect_ratio is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotate_xyz(self, x:AngleOrItsFloatOrStringValue, y:AngleOrItsFloatOrStringValue, z:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the XYZ direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotate_xyz is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotate_x(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the X direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotate_x is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotate_y(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the Y direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotate_y is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def rotate_z(self, rotation:AngleOrItsFloatOrStringValue):
        '''
        Rotate in the Z direction. Default units is degrees. Pass in a number, Angle or Angle-String (e.g. 'PI/4radians' or 'PI/4r' or '90d'
        '''
        
        print("rotate_z is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def twist(self, angle:AngleOrItsFloatOrStringValue, screw_pitch:DimensionOrItsFloatOrStringValue, interations:'int'=1, axis:AxisOrItsIndexOrItsName="z"):
        '''
        AKA Helix, Screw. Revolve an entity
        '''
        
        print("twist is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def remesh(self, strategy:str, amount:float):
        '''
        Remeshing should be capable of voxel or vertex based reconstruction, including decimating unnecessary vertices (if applicable).
        '''
        
        print("remesh is called in an abstract method. Please override this method.")
        return self
        

    @abstractmethod
    def create_landmark(self, landmark_name:str, x:DimensionOrItsFloatOrStringValue, y:DimensionOrItsFloatOrStringValue, z:DimensionOrItsFloatOrStringValue) -> 'LandmarkInterface':
        '''
        Shortcut for creating and assigning a landmark to this entity. Returns a Landmark instance.
        '''
        
        print("create_landmark is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_bounding_box(self) -> 'BoundaryBox':
        '''
        Get the Boundary Box around the entity.
        '''
        
        print("get_bounding_box is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_dimensions(self) -> 'Dimensions':
        '''
        Get the length span in each coordinate axis (X,Y,Z).
        '''
        
        print("get_dimensions is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        

    @abstractmethod
    def get_landmark(self, landmark_name:PresetLandmarkOrItsName) -> 'LandmarkInterface':
        '''
        Get the landmark by name
        '''
        
        print("get_landmark is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        