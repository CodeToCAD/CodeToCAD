from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Vertex(VertexInterface, Entity):

    @supported(SupportLevel.UNSUPPORTED)
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
        parent_entity: "str|EntityInterface| None" = None,
    ):
        self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.UNSUPPORTED)
    def get_control_points(self) -> "list[Vertex]":
        print("get_control_points called:", parameter)
        return [Vertex(location=(0, 0), name="myVertex")]

    @supported(SupportLevel.UNSUPPORTED)
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        print("set_control_points called", f": {points}")
        return self
