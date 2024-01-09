from typing import Optional

from codetocad.interfaces import VertexInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Vertex(Entity, VertexInterface):
    def project(self, project_onto: "Sketch") -> "Projectable":
        from . import Sketch

        print("project called:", project_onto)
        return Sketch("a projected sketch")

    location: "Point"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        location: "Point",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_control_points(self, parameter="") -> "list[Vertex]":
        print("get_control_points called:", parameter)
        return [Vertex(location=(0, 0), name="myVertex")]
