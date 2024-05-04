from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from providers.blender.blender_provider.vertex import Vertex
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.blender.blender_provider.entity import Entity
from providers.blender.blender_provider.landmark import Landmark
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface


class Edge(EdgeInterface, Entity):
    v1: "Vertex"
    v2: "Vertex"
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|Entity| None" = None,
    ):
        """
        NOTE: Blender Provider's Edge requires a parent_entity and a native_instance
        """
        assert (
            parent_entity is not None and native_instance is not None
        ), "Blender Provider's Edge requires a parent_entity and a native_instance"
        self.v1 = v1
        self.v2 = v2
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def offset(self, distance: "str|float|Dimension") -> "Edge":
        raise NotImplementedError()

    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle"):
        return self

    def set_is_construction(self, is_construction: "bool"):
        return self

    def get_is_construction(self) -> bool:
        raise NotImplementedError()

    def remesh(self, strategy: "str", amount: "float"):
        raise NotImplementedError()
        return self

    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        return self

    def decimate(self, amount: "float"):
        raise NotImplementedError()
        return self

    def mirror(
        self,
        mirror_across_entity: "str|Entity",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|Entity",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        raise NotImplementedError()
        return self

    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")
