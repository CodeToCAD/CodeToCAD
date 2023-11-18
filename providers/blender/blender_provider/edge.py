from typing import Optional

from codetocad.interfaces import EdgeInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Vertex


class Edge(Entity, EdgeInterface):
    v1: "Vertex"
    v2: "Vertex"
    parent_sketch: Optional[SketchOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str,
        parent_sketch: Optional[SketchOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.v1 = v1
        self.v2 = v2
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def offset(self, distance: DimensionOrItsFloatOrStringValue) -> "Edge":
        raise NotImplementedError()

    def fillet(self, other_edge: "Edge", amount: AngleOrItsFloatOrStringValue):
        return self

    def set_is_construction(self, is_construction: bool):
        return self

    def get_is_construction(self) -> bool:
        raise NotImplementedError()

    def remesh(self, strategy: str, amount: float):
        raise NotImplementedError()
        return self

    def subdivide(self, amount: float):
        raise NotImplementedError()
        return self

    def decimate(self, amount: float):
        raise NotImplementedError()
        return self

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
