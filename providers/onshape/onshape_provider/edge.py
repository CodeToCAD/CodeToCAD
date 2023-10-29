# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import EdgeInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity, Mirrorable, Patternable, Subdividable, Projectable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Vertex
    from . import Sketch


class Edge(Entity, Mirrorable, Patternable, Subdividable, Projectable, EdgeInterface):
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
