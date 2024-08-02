from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.codetocad_types import *
from typing import Self
from codetocad.core.point import Point
from codetocad.interfaces.vertex_interface import VertexInterface
from providers.blender.blender_provider.entity import Entity
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities.override import override
from providers.blender.blender_provider.blender_actions.vertex_edge_wire import (
    get_control_points,
    get_vertex_location_from_blender_point,
    set_control_points,
)


class Vertex(VertexInterface, Entity):

    def __init__(
        self,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
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

    @override
    @supported(SupportLevel.SUPPORTED)
    def get_native_instance(self) -> object:
        return self.native_instance

    @property
    @override
    @supported(SupportLevel.SUPPORTED)
    def location(self) -> Point:
        return get_vertex_location_from_blender_point(self.get_native_instance())

    @supported(SupportLevel.UNSUPPORTED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()

    @supported(SupportLevel.SUPPORTED)
    def get_control_points(self) -> "list[Point]":
        return get_control_points(self.get_native_instance())  # type:ignore

    @supported(SupportLevel.SUPPORTED)
    def set_control_points(
        self, points: "list[str|list[str]|list[float]|list[Dimension]|Point]"
    ) -> Self:
        parsed_points = [Point.from_list_of_float_or_string(point) for point in points]
        set_control_points(self.get_native_instance(), parsed_points)  # type:ignore
        return self
