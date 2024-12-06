from typing import Optional
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from typing import Self
from codetocad.interfaces.vertex_interface import VertexInterface
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

    @supported(SupportLevel.UNSUPPORTED)
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()

    edges: "list[Edge]"
    parent_entity: Optional[str | Entity] = None
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        edges: "list[EdgeInterface]",
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
        parent: "EntityInterface| None" = None,
    ):
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.UNSUPPORTED)
    def get_normal(self, flip: "bool| None" = False) -> "Point":
        print("get_normal called:", flip)
        return Point.from_list_of_float_or_string([0, 0, 0])

    @supported(SupportLevel.UNSUPPORTED)
    def get_vertices(self) -> "list[Vertex]":
        print("get_vertices called:")
        from . import Vertex

        return [Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex")]

    @supported(SupportLevel.UNSUPPORTED)
    def get_is_closed(self) -> bool:
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def loft(
        self,
        other: "WireInterface",
        union_connecting_parts: "bool| None" = True,
        new_name: "str| None" = None,
    ) -> "Part":
        raise NotImplementedError()

    @supported(SupportLevel.UNSUPPORTED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")
        return Landmark("name", "parent")

    @supported(SupportLevel.UNSUPPORTED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        print("get_landmark called", f": {landmark_name}")
        return Landmark("name", "parent")

    @supported(SupportLevel.UNSUPPORTED)
    def union(
        self,
        other: "BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print("union called", f": {other}, {delete_after_union}, {is_transfer_data}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def subtract(
        self,
        other: "BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "subtract called", f": {other}, {delete_after_subtract}, {is_transfer_data}"
        )
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def intersect(
        self,
        other: "BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        print(
            "intersect called",
            f": {other}, {delete_after_intersect}, {is_transfer_data}",
        )
        return self

    @supported(SupportLevel.UNSUPPORTED)
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

    @supported(SupportLevel.UNSUPPORTED)
    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":
        print("revolve called", f": {angle}, {about_entity_or_landmark}, {axis}")
        return Part("a part")

    @supported(SupportLevel.UNSUPPORTED)
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def sweep(
        self, profile: "WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        print("sweep called", f": {profile_name_or_instance}, {fill_cap}")
        return Part("a part")

    @supported(SupportLevel.UNSUPPORTED)
    def offset(self, radius: "str|float|Dimension"):
        print("offset called", f": {radius}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def profile(self, profile_curve: "WireInterface|SketchInterface"):
        print("profile called", f": {profile_curve_name}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def get_edges(self) -> "list[EdgeInterface]":
        print("get_edges called")
        return [
            Edge(
                v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
                name="an edge",
            )
        ]

    @supported(SupportLevel.UNSUPPORTED)
    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called", f": {strategy}, {amount}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def subdivide(self, amount: "float"):
        print("subdivide called", f": {amount}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def decimate(self, amount: "float"):
        print("decimate called", f": {amount}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
    ) -> Self:
        print("create_from_vertices called", f": {points}, {options}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_point(
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> Self:
        print("create_point called", f": {point}, {options}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> Self:
        print("create_line called", f": {length}, {angle}, {start_at}, {options}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
    ) -> Self:
        print("create_line_to called", f": {to}, {start_at}, {options}")
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
    ) -> Self:
        print(
            "create_arc called", f": {end_at}, {radius}, {start_at}, {flip}, {options}"
        )
        return self
