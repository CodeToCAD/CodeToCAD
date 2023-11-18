from typing import Optional

from codetocad.interfaces import VertexInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity


class Vertex(Entity, VertexInterface):
    location: PointOrListOfFloatOrItsStringValue
    parent_sketch: Optional[SketchOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        location: PointOrListOfFloatOrItsStringValue,
        name: str,
        parent_sketch: Optional[SketchOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.location = location
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_control_points(self, parameter="") -> "list[Entity]":
        raise NotImplementedError()

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
