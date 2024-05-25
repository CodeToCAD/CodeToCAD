# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.wire_interface import WireInterface


from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.booleanable_interface import BooleanableInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.entity_interface import EntityInterface


from codetocad.proxy.edge import Edge

from codetocad.proxy.part import Part

from codetocad.proxy.vertex import Vertex

from codetocad.proxy.landmark import Landmark


from providers.sample.entity import Entity


class Wire(WireInterface, Entity):

    def __init__(
        self,
        name: "str",
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.name = name
        self.edges = edges
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    def get_normal(self, flip: "bool| None" = False) -> "Point":

        print("get_normal called", f": {flip}")

        return Point.from_list_of_float_or_string([0, 0, 0])

    def get_edges(
        self,
    ) -> "list[EdgeInterface]":

        print(
            "get_edges called",
        )

        return [
            Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            )
        ]

    def get_vertices(
        self,
    ) -> "list[VertexInterface]":

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

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":

        print("revolve called", f": {angle}, {about_entity_or_landmark}, {axis}")

        return Part("a part")

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ) -> Self:

        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")

        return self

    def extrude(self, length: "str|float|Dimension") -> "PartInterface":

        print("extrude called", f": {length}")

        return Part("a part")

    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":

        print("sweep called", f": {profile_name_or_instance}, {fill_cap}")

        return Part("a part")

    def offset(self, radius: "str|float|Dimension") -> "WireInterface":

        print("offset called", f": {radius}")

        return Wire(
            "a wire",
            [
                Edge(
                    v1=Vertex(
                        "a vertex", Point.from_list_of_float_or_string([0, 0, 0])
                    ),
                    v2=Vertex(
                        "a vertex", Point.from_list_of_float_or_string([0, 0, 0])
                    ),
                    name="an edge",
                )
            ],
        )

    def profile(self, profile_curve_name: "str") -> Self:

        print("profile called", f": {profile_curve_name}")

        return self

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ) -> Self:

        print(
            "mirror called",
            f": {mirror_across_entity}, {axis}, {resulting_mirrored_entity_name}",
        )

        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ) -> Self:

        print(
            "linear_pattern called", f": {instance_count}, {offset}, {direction_axis}"
        )

        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ) -> Self:

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
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:

        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")

        return self

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:

        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )

        return self

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ) -> Self:

        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )

        return self

    def remesh(self, strategy: "str", amount: "float") -> Self:

        print("remesh called", f": {strategy}, {amount}")

        return self

    def subdivide(self, amount: "float") -> Self:

        print("subdivide called", f": {amount}")

        return self

    def decimate(self, amount: "float") -> Self:

        print("decimate called", f": {amount}")

        return self
