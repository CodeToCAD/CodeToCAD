from typing import Optional
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from providers.onshape.onshape_provider.entity import Entity
from providers.onshape.onshape_provider.vertex import Vertex
from providers.onshape.onshape_provider.landmark import Landmark
from providers.onshape.onshape_provider.part import Part
from providers.onshape.onshape_provider.edge import Edge
from codetocad.codetocad_types import *
from codetocad.interfaces.projectable_interface import ProjectableInterface
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Edge, Vertex
    from . import Sketch
    from . import Part


class Wire(WireInterface, Entity):
    def mirror(
        self,
        mirror_across_entity: "str|Entity",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|Entity",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        return self

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()

    edges: "list[Edge]"
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        edges: "list[Edge]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|Entity| None" = None,
    ):
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    def get_normal(self, flip: "bool| None" = False) -> "Point":
        print("get_normal called:", flip)
        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_vertices(self) -> "list[Vertex]":
        print("get_vertices called:")
        from . import Vertex

        return [Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex")]

    def get_is_closed(self) -> bool:
        raise NotImplementedError()

    def loft(self, other: "WireInterface", new_part_name: "str| None" = None) -> "Part":
        raise NotImplementedError()

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

    def union(
        self,
        other: "str|Booleanable",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    def subtract(
        self,
        other: "str|Booleanable",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    def intersect(
        self,
        other: "str|Booleanable",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self
