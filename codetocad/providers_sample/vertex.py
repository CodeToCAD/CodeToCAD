# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import VertexInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Sketch
    from . import Entity


class Vertex(Entity, VertexInterface):
    def project(self, project_onto: "Sketch") -> "Projectable":
        raise NotImplementedError()

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
