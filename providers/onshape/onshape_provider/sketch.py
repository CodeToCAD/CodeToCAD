from dataclasses import dataclass
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
)
from providers.onshape.onshape_provider import onshape_actions, onshape_definitions
from providers.onshape.onshape_provider.onshape_actions import (
    create_or_update_sketch,
    OnshapeContext,
)

from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part
    from . import Wire
    from . import Vertex
    from . import Edge


@dataclass
class SketchRef:
    onshape_url: onshape_definitions.OnshapeUrl
    feature_id: str


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
    native_instance: SketchRef

    def __init__(
        self,
        name: str,
        curve_type: Optional["CurveTypes"] = None,
        description: Optional[str] = None,
        native_instance: SketchRef | None = None,
    ):
        self.name = name
        self.curve_type = curve_type
        self.description = description

        context = OnshapeContext.get_active()

        self.native_instance = native_instance or create_or_update_sketch(
            context.active_client, context.active_tab_url, name, []
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
            raise RuntimeError("Feature ID is missing, cannot locate this feature.")

        feature_id = self.native_instance.feature_id
        length_float = Dimension.from_dimension_or_its_float_or_string_value(
            length, None
        )

        context = OnshapeContext.get_active()

        create_extrude(
            context.active_client,
            self.native_instance.onshape_url,
            feature_id,
            str(length_float),
        )

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

        context = OnshapeContext.get_active()

        api_resp = onshape_actions.create_point(
            context.active_client, self.native_instance.onshape_url, self.name, point
        )
        json_native_data = json.loads(api_resp.data)
        return Vertex(
            location=point,
            name=create_uuid_like_id(),
            native_instance=json_native_data["feature"]["entities"][0],
        )

    def create_line(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        start_point = Point.from_list_of_float_or_string_or_Vertex(start_at)
        end_point = Point.from_list_of_float_or_string_or_Vertex(end_at)

        context = OnshapeContext.get_active()

        api_resp = onshape_actions.create_line(
            context.active_client,
            self.native_instance.onshape_url,
            self.name,
            start_point,
            end_point,
        )
        json_native_data = json.loads(api_resp.data)
        return Edge(
            v1=None,
            v2=None,
            name=create_uuid_like_id(),
            native_instance=json_native_data["feature"]["entities"][0],
        )

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        radius_float = Dimension.from_dimension_or_its_float_or_string_value(radius)

        context = OnshapeContext.get_active()

        api_resp = onshape_actions.create_circle(
            context.active_client,
            self.native_instance.onshape_url,
            self.name,
            radius_float,
        )
        json_native_data = json.loads(api_resp.data)
        return Wire(
            edges=[],
            name=create_uuid_like_id(),
            native_instance=json_native_data["feature"],
        )

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

        # Define the location of the point in 3D space
        corner1_x = Dimension(-width_float / 2, "mm")
        corner1_y = Dimension(length_float / 2, "mm")
        corner2_x = Dimension(width_float / 2, "mm")
        corner2_y = Dimension(-length_float / 2, "mm")

        context = OnshapeContext.get_active()

        # Create a point in the part studio
        sketch_info = create_rect(
            context.active_client,
            self.native_instance.onshape_url,
            create_uuid_like_id(),
            Point(corner1_x, corner1_y, Dimension.zero()),
            Point(corner2_x, corner2_y, Dimension.zero()),
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
