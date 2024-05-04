from typing import Optional
from codetocad.core.point import Point
from codetocad.interfaces.vertex_interface import VertexInterface
from providers.blender.blender_provider.entity import Entity
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities.override import override
from providers.blender.blender_provider.blender_actions.vertex_edge_wire import (
    get_vertex_location_from_blender_point,
)


class Vertex(VertexInterface, Entity):
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    @override
    def get_native_instance(self) -> object:
        return self.native_instance

    @override
    @property
    def location(self) -> Point:
        return get_vertex_location_from_blender_point(self.get_native_instance())

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|Entity| None" = None,
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

    def get_control_points(self) -> "list[Entity]":
        raise NotImplementedError()

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
