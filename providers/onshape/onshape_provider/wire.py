from typing import Optional

from codetocad.interfaces import WireInterface

from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Edge, Vertex
    from . import Sketch
    from . import Part


class Wire(Entity, WireInterface):
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        return self

    def project(self, project_onto: "Sketch") -> "ProjectableInterface":
        raise NotImplementedError()

    edges: "list[Edge]"
    parent_entity: Optional[EntityOrItsName] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        edges: "list[Edge]",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def clone(
        self, new_name: str, new_parent: Optional[SketchOrItsName] = None
    ) -> "Wire":
        print("clone called:", new_name, new_parent)
        from . import Wire

        return Wire([], "a wire")

    def get_normal(self, flip: Optional[bool] = False) -> "Point":
        print("get_normal called:", flip)
        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_vertices(self) -> "list[Vertex]":
        print(
            "get_vertices called:",
        )
        from . import Vertex

        return [Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex")]

    def get_is_closed(self) -> bool:
        raise NotImplementedError()

    def loft(self, other: "Wire", new_part_name: Optional[str] = None) -> "Part":
        raise NotImplementedError()
