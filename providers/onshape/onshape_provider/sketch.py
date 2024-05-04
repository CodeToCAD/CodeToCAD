import json
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from providers.onshape.onshape_provider.entity import Entity
from providers.onshape.onshape_provider.vertex import Vertex
from providers.onshape.onshape_provider.landmark import Landmark
from providers.onshape.onshape_provider.part import Part
from providers.onshape.onshape_provider.wire import Wire
from providers.onshape.onshape_provider.edge import Edge
from typing import Optional
from codetocad.codetocad_types import *
from providers.onshape.onshape_provider.onshape_actions import (
    create_extrude,
    create_rect,
    create_tab_part_studios,
    get_first_document_url_by_name,
    get_onshape_client_with_config_file,
)
from providers.onshape.onshape_provider import onshape_actions
from providers.onshape.onshape_provider.utils import get_polygon_points
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part
    from . import Entity
    from . import Wire
    from . import Vertex
    from . import Edge
# Note: you must create a "CodeToCAD-onshape_actions" document to run tests that use it.
onshape_document_name = "CodeToCAD-onshape_actions"


class Sketch(SketchInterface, Entity):
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        print("project called:", project_from)
        from . import Sketch

        return Sketch("a projected sketch")

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

    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        return self

    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        return self

    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        return self

    def scale_x(self, scale: "str|float|Dimension"):
        return self

    def scale_y(self, scale: "str|float|Dimension"):
        return self

    def scale_z(self, scale: "str|float|Dimension"):
        return self

    def scale_x_by_factor(self, scale_factor: "float"):
        return self

    def scale_y_by_factor(self, scale_factor: "float"):
        return self

    def scale_z_by_factor(self, scale_factor: "float"):
        return self

    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        return self

    name: str
    curve_type: Optional["CurveTypes"] = None
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: "str",
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        self.name = name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance

    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "Sketch":
        raise NotImplementedError()

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|Entity",
        axis: "str|int|Axis" = "z",
    ) -> "Part":
        raise NotImplementedError()

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
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

    def sweep(
        self, profile_name_or_instance: "str|Sketch", fill_cap: "bool" = True
    ) -> "Part":
        raise NotImplementedError()

    def offset(self, radius: "str|float|Dimension"):
        return self

    def profile(self, profile_curve_name: "str"):
        return self

    def create_text(
        self,
        text: "str",
        font_size: "str|float|Dimension" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
    ):
        pointLocation1 = Dimension(0.0, "mm")
        pointLocation2 = Dimension(0.2, "mm")
        corner1 = Point(pointLocation1, pointLocation1, pointLocation1)
        corner2 = Point(pointLocation2, pointLocation2, pointLocation2)
        api_resp = onshape_actions.create_text(
            self.client,
            self.onshape_url,
            self.name,
            text,
            corner1,
            corner2,
            bold=bold,
            italic=italic,
        )
        json_native_data = json.loads(api_resp.data)
        self.native_instance = json_native_data
        return self

    def create_from_vertices(
        self, points: "str|list[str]|list[float]|list[Dimension]|Point|Vertex]"
    ) -> "Wire":
        raise NotImplementedError()

    def create_point(
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> "Vertex":
        point = Point.from_list_of_float_or_string(point)
        api_resp = onshape_actions.create_point(
            self.client, self.onshape_url, self.name, point
        )
        json_native_data = json.loads(api_resp.data)
        return Vertex(
            location=point, native_instance=json_native_data["feature"]["entities"][0]
        )

    def create_line(
        self,
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
    ) -> "Edge":
        start_point = Point.from_list_of_float_or_string(start_at)
        end_point = Point.from_list_of_float_or_string(end_at)
        api_resp = onshape_actions.create_line(
            self.client, self.onshape_url, self.name, start_point, end_point
        )
        json_native_data = json.loads(api_resp.data)
        return Edge(
            v1=None,
            v2=None,
            name="",
            native_instance=json_native_data["feature"]["entities"][0],
        )

    def create_circle(self, radius: "str|float|Dimension") -> "Wire":
        radius_float = Dimension.from_dimension_or_its_float_or_string_value(radius)
        api_resp = onshape_actions.create_circle(
            self.client, self.onshape_url, self.name, radius_float.value
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_ellipse(
        self, radius_minor: "str|float|Dimension", radius_major: "str|float|Dimension"
    ) -> "Wire":
        radius_minor_float = Dimension.from_dimension_or_its_float_or_string_value(
            radius_minor
        )
        radius_major_float = Dimension.from_dimension_or_its_float_or_string_value(
            radius_major
        )
        api_resp = onshape_actions.create_ellipse(
            self.client,
            self.onshape_url,
            self.name,
            radius_minor_float.value,
            radius_major_float.value,
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_arc(
        self,
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        radius: "str|float|Dimension",
        flip: "bool| None" = False,
    ) -> "Wire":
        start_point = Point.from_list_of_float_or_string(start_at)
        end_point = Point.from_list_of_float_or_string(end_at)
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        api_resp = onshape_actions.create_arc(
            self.client,
            self.onshape_url,
            self.name,
            radius.value,
            start_point,
            end_point,
            flip if flip else False,
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_rectangle(
        self, length: "str|float|Dimension", width: "str|float|Dimension"
    ) -> "Wire":
        length_float = Dimension.from_dimension_or_its_float_or_string_value(
            length, None
        ).value
        width_float = Dimension.from_dimension_or_its_float_or_string_value(
            width, None
        ).value
        onshape_url = get_first_document_url_by_name(self.client, onshape_document_name)
        # Create a new tab in the part studio
        part_studio_id = create_tab_part_studios(
            self.client, onshape_url, create_uuid_like_id()
        )
        # Set the tab_id for subsequent operations
        onshape_url.tab_id = part_studio_id
        # Define the location of the point in 3D space
        corner1_x = Dimension(-width_float / 2, "mm")
        corner1_y = Dimension(length_float / 2, "mm")
        corner2_x = Dimension(width_float / 2, "mm")
        corner2_y = Dimension(-length_float / 2, "mm")
        # Create a point in the part studio
        sketch_info = create_rect(
            self.client,
            onshape_url,
            "Test Point",
            Point(corner1_x, corner1_y, Dimension(0, "mm")),
            Point(corner2_x, corner2_y, Dimension(0, "mm")),
        )
        self.native_instance = json.loads(sketch_info.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
    ) -> "Wire":
        points = get_polygon_points(number_of_sides, length)
        new_points: list[Point] = []
        for point in points:
            new_points.append(
                Point(
                    Dimension(point[0], "m"),
                    Dimension(point[1], "m"),
                    Dimension(0.0, "m"),
                )
            )
        api_resp = onshape_actions.create_polygon(
            self.client, self.onshape_url, self.name, new_points
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
    ) -> "Wire":
        api_resp = onshape_actions.create_trapezoid(
            self.client, self.onshape_url, self.name, length_upper, length_lower, height
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
    ) -> "Wire":
        if self.native_instance is None:
            raise ValueError("Native Instance is None")
        height = Dimension.from_dimension_or_its_float_or_string_value(height)
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        radius_end = (
            Dimension.from_dimension_or_its_float_or_string_value(radius)
            if radius_end is not None
            else None
        )
        api_resp = onshape_actions.create_spiral(
            self.client,
            self.onshape_url,
            self.name,
            number_of_turns,
            height,
            radius,
            is_clockwise,
            radius_end,
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

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
