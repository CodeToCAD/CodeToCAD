from typing import Optional
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.proxy.edge import Edge
from codetocad.proxy.vertex import Vertex
from codetocad.proxy.landmark import Landmark
from codetocad.proxy.part import Part
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
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
    from . import Part


class Wire(WireInterface, Entity):

    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
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
        center_entity_or_landmark: "str|EntityInterface",
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
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
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
        other: "str|BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    def subtract(
        self,
        other: "str|BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    def intersect(
        self,
        other: "str|BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self

    def extrude(self, length: "str|float|Dimension") -> "Part":
        if self.native_instance is None:
            raise ValueError("Native Instance is None")
        onshape_url = get_first_document_url_by_name(self.client, onshape_document_name)
        feature_id = self.native_instance["feature"]["featureId"]
        length_float = Dimension.from_dimension_or_its_float_or_string_value(
            length, None
        )
        create_extrude(self.client, onshape_url, feature_id, str(length_float))
        raise NotImplementedError()

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
    ):
        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")
        return self

    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        print("sweep called", f": {profile_name_or_instance}, {fill_cap}")
        return Part("a part")

    def offset(self, radius: "str|float|Dimension"):
        print("offset called", f": {radius}")
        return self

    def profile(self, profile_curve_name: "str"):
        print("profile called", f": {profile_curve_name}")
        return self

    def get_edges(self) -> "list[EdgeInterface]":
        print("get_edges called")
        return [
            Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            )
        ]

    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called", f": {strategy}, {amount}")
        return self

    def subdivide(self, amount: "float"):
        print("subdivide called", f": {amount}")
        return self

    def decimate(self, amount: "float"):
        print("decimate called", f": {amount}")
        return self
