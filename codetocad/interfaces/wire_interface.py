
# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod
from codetocad.codetocad_types import *
from codetocad.core import *
from codetocad.enums import *

from codetocad.interfaces import EntityInterface
from codetocad.interfaces import MirrorableInterface
from codetocad.interfaces import PatternableInterface
from codetocad.interfaces import ProjectableInterface


class WireInterface(EntityInterface,MirrorableInterface,PatternableInterface,ProjectableInterface, metaclass=ABCMeta):
    '''A collection of connected edges.'''

    
    edges:'list[Edge]'
    parent_sketch:Optional[SketchOrItsName]=None

    @abstractmethod
    def __init__(self, edges: 'list[Edge]', parent_sketch: Optional[SketchOrItsName] = None, name: str, description: Optional[str] = None, native_instance = None):
        super().__init__(name, description, native_instance)
        self.edges = edges
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def is_closed(self) -> bool:
        '''
        A closed wire is a Face.
        '''
        
        print("is_closed is called in an abstract method. Please override this method.")
        raise NotImplementedError()
        