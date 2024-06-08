from typing import Optional
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.codetocad_types import *


class Vertex(VertexInterface, Entity):

    @supported(SupportLevel.UNSUPPORTED)
    def project(self, project_from: "ProjectableInterface") -> "Projectable":
        raise NotImplementedError()

    location: str | list[str] | list[float] | list[Dimension] | Point
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
    def get_control_points(self) -> "list[Entity]":
        raise NotImplementedError()

    @property
    def _center(self):
        return self.location

    @supported(SupportLevel.UNSUPPORTED)
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        print("set_control_points called", f": {points}")
        return self
