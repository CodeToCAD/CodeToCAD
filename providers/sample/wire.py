# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import WireInterface


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.edge_interface import EdgeInterface


from providers.sample.landmark import Landmark

from providers.sample.vertex import Vertex

from providers.sample.part import Part

from providers.sample.entity import Entity

from providers.sample.edge import Edge


class Wire(WireInterface, Entity):
    def __init__(
        self,
        name: "str",
        edges: "list[Edge]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        self.name = name
        self.edges = edges
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    def get_normal(self, flip: "bool| None" = False) -> "Point":
        print("get_normal called", f": {flip}")

        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_vertices(
        self,
    ) -> "list[Vertex]":
        print(
            "get_vertices called",
        )

        return [Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0]))]

    def get_is_closed(
        self,
    ) -> "bool":
        print(
            "get_is_closed called",
        )

        return True

    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        print("loft called", f": {other}, {new_part_name}")

        return Part("a part")

    def mirror(
        self,
        mirror_across_entity: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName",
        resulting_mirrored_entity_name: "str| None" = None,
    ):
        print(
            "mirror called",
            f": {mirror_across_entity}, {axis}, {resulting_mirrored_entity_name}",
        )

        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "DimensionOrItsFloatOrStringValue",
        direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "AngleOrItsFloatOrStringValue",
        center_entity_or_landmark: "EntityOrItsName",
        normal_direction_axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print(
            "circular_pattern called",
            f": {instance_count}, {separation_angle}, {center_entity_or_landmark}, {normal_direction_axis}",
        )

        return self

    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        print("project called", f": {project_from}")

        return __import__("codetocad").Sketch("a projected sketch")

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

    def union(
        self,
        other: "BooleanableOrItsName",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")

        return self

    def subtract(
        self,
        other: "BooleanableOrItsName",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )

        return self

    def intersect(
        self,
        other: "BooleanableOrItsName",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )

        return self
