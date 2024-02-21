from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.blender.blender_provider.entity import Entity
from providers.blender.blender_provider.vertex import Vertex
from providers.blender.blender_provider.landmark import Landmark
from codetocad.interfaces import EdgeInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.blender.blender_provider import Entity, Vertex


class Edge(EdgeInterface, Entity):
    v1: "Vertex"
    v2: "Vertex"
    parent_entity: Optional[EntityOrItsName] = None
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
        parent_entity: "EntityOrItsName| None" = None,
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

    def offset(self, distance: "DimensionOrItsFloatOrStringValue") -> "Edge":
        raise NotImplementedError()

    def fillet(
        self, other_edge: "EdgeInterface", amount: "AngleOrItsFloatOrStringValue"
    ):
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
        mirror_across_entity: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_onto: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "DimensionOrItsFloatOrStringValue",
        direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        raise NotImplementedError()
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "AngleOrItsFloatOrStringValue",
        center_entity_or_landmark: "EntityOrItsName",
        normal_direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        raise NotImplementedError()
        return self

    def create_landmark(
        self,
        landmark_name: "str",
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    def get_landmark(
        self, landmark_name: "PresetLandmarkOrItsName"
    ) -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")
