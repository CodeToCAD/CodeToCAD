from typing import Optional
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.entity_interface import EntityInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Vertex(VertexInterface, Entity):
    def project(self, project_from: "ProjectableInterface") -> "Projectable":
        from . import Sketch

        print("project called:", project_from)
        return Sketch("a projected sketch")

    location: "Point"
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|Entity| None" = None,
    ):
        self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_control_points(self) -> "list[Vertex]":
        print("get_control_points called:", parameter)
        return [Vertex(location=(0, 0), name="myVertex")]
