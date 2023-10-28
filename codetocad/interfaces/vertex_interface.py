
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *
from codetocad.core import *
from codetocad.enums import *

from codetocad.interfaces import EntityInterface
from codetocad.interfaces import ProjectableInterface


class VertexInterface(EntityInterface,ProjectableInterface, metaclass=ABCMeta):
    '''A single point in space, or a control point.'''

    
    location:PointOrListOfFloatOrItsStringValue
    parent_sketch:Optional[SketchOrItsName]=None

    @abstractmethod
    def __init__(self, location: PointOrListOfFloatOrItsStringValue, parent_sketch: Optional[SketchOrItsName] = None, name: str, description: Optional[str] = None, native_instance = None):
        super().__init__(name, description, native_instance)
        self.location = location
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def get_control_points(self, parameter = "") -> 'list[Entity]':
        '''
        
        '''
        
        print("get_control_points is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        