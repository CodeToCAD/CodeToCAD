from typing import Optional

from codetocad.interfaces import EdgeInterface
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from providers.blender.blender_provider import Entity, Vertex


class Edge(Entity, EdgeInterface):
    v1: "Vertex"
    v2: "Vertex"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def get_native_instance(self) -> object:
        return self.native_instance

    def __init__(
        self,
        v1: "Vertex",
        v2: "Vertex",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
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

    def offset(self, distance: DimensionOrItsFloatOrStringValue) -> "Edge":
        raise NotImplementedError()

    def fillet(self, other_edge: "Edge", amount: AngleOrItsFloatOrStringValue):
        return self

    def set_is_construction(self, is_construction: bool):
        return self

    def get_is_construction(self) -> bool:
        raise NotImplementedError()

    def remesh(self, strategy: str, amount: float):
        raise NotImplementedError()
        return self

    def subdivide(self, amount: float):
        raise NotImplementedError()
        return self

    def decimate(self, amount: float):
        raise NotImplementedError()
        return self

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        raise NotImplementedError()
        return self

    def project(self, project_onto: "SketchInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        raise NotImplementedError()
        return self
