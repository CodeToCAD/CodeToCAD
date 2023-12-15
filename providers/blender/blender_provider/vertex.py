from typing import Optional

from codetocad.interfaces import VertexInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.blender.blender_provider import blender_actions


from . import Entity


class Vertex(Entity, VertexInterface):
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    @property
    def location(self) -> Point:
        return blender_actions.get_vertex_location_from_blender_point(
            self.native_instance
        )

    def get_native_instance(self) -> object:
        return self.native_instance

    def __init__(
        self,
        location: Point,
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        """
        NOTE: Blender Provider's Vertex requires a parent_entity and a native_instance
        """
        assert (
            parent_entity is not None and native_instance is not None
        ), "Blender Provider's Vertex requires a parent_entity and a native_instance"

        # self.location = location
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_control_points(self, parameter="") -> "list[Entity]":
        raise NotImplementedError()

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
