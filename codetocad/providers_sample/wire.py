# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import WireInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

from . import Entity
from . import Mirrorable
from . import Patternable
from . import Projectable


class Wire(Entity,Mirrorable,Patternable,Projectable, WireInterface): 
    
    
    edges:'list[Edge]'
    parent_sketch:Optional[SketchOrItsName]=None
    name:str
    description:Optional[str]=None
    native_instance=None

    def __init__(self, edges: 'list[Edge]', parent_sketch: Optional[SketchOrItsName] = None, name: str, description: Optional[str] = None, native_instance = None):
        self.edges = edges
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def is_closed(self) -> bool:
        
        raise NotImplementedError()
        
    