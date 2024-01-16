import json
from typing import Optional

from codetocad.interfaces import SketchInterface, ProjectableInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from providers.onshape.onshape_provider.onshape_actions import (
    create_extrude,
    create_rect,
    create_tab_part_studios,
    get_first_document_url_by_name,
    get_onshape_client_with_config_file,
)
from providers.onshape.onshape_provider import onshape_actions

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


class Sketch(Entity, SketchInterface):
    def project(self, project_onto: "Sketch") -> "ProjectableInterface":
        print("project called:", project_onto)
        from . import Sketch

        return Sketch("a projected sketch")

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

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        return self

    def scale_x_by_factor(self, scale_factor: float):
        return self

    def scale_y_by_factor(self, scale_factor: float):
        return self

    def scale_z_by_factor(self, scale_factor: float):
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        return self

    name: str
    curve_type: Optional["CurveTypes"] = None
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self,
        name: str,
        curve_type: Optional["CurveTypes"] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.name = name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance

    @classmethod
    def setUpClass(cls) -> None:
        import os

        configPath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../.onshape_client_config.yaml",
        )
        cls.client = get_onshape_client_with_config_file(config_filepath=configPath)
        cls.onshape_url = get_first_document_url_by_name(
            cls.client, onshape_document_name
        )

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        raise NotImplementedError()

    def revolve(
        self,
        angle: AngleOrItsFloatOrStringValue,
        about_entity_or_landmark: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName = "z",
    ) -> "Part":
        raise NotImplementedError()

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> "Part":
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
        self, profile_name_or_instance: EntityOrItsName, fill_cap: bool = True
    ) -> "Part":
        raise NotImplementedError()

    def offset(self, radius: DimensionOrItsFloatOrStringValue):
        return self

    def profile(self, profile_curve_name: str):
        return self

    def create_text(
        self,
        text: str,
        font_size: DimensionOrItsFloatOrStringValue = 1.0,
        bold: bool = False,
        italic: bool = False,
        underlined: bool = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: Optional[str] = None,
    ):
        return self

    def create_from_vertices(
        self, points: list[PointOrListOfFloatOrItsStringValueOrVertex]
    ) -> "Wire":
        raise NotImplementedError()

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
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
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        start_point = Point.from_list_of_float_or_string_or_Vertex(start_at)
        end_point = Point.from_list_of_float_or_string_or_Vertex(end_at)
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

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        radius_float = Dimension.from_dimension_or_its_float_or_string_value(radius)
        api_resp = onshape_actions.create_circle(
            self.client, self.onshape_url, self.name, radius_float
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(native_instance=json_native_data["feature"])

    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_arc(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
        radius: DimensionOrItsFloatOrStringValue,
        flip: Optional[bool] = False,
    ) -> "Wire":
        raise NotImplementedError()

    def create_rectangle(
        self,
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
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
        raise NotImplementedError()

    def create_polygon(
        self,
        number_of_sides: "int",
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_trapezoid(
        self,
        length_upper: DimensionOrItsFloatOrStringValue,
        length_lower: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        raise NotImplementedError()

    def create_spiral(
        self,
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
    ) -> "Wire":
        raise NotImplementedError()
