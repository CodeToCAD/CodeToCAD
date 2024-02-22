from typing import Optional
from codetocad.interfaces.projectable_interface import ProjectableInterface
from providers.onshape.onshape_provider.entity import Entity
from codetocad.interfaces import VertexInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class Vertex(VertexInterface, Entity):
    def project(self, project_onto: "ProjectableInterface") -> "Projectable":
        raise NotImplementedError()

    location: PointOrListOfFloatOrItsStringValue
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_control_points(self) -> "list[Entity]":
        raise NotImplementedError()

    @property
    def _center(self):
        return self.location
