# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from codetocad.interfaces import SketchInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part
    from . import Entity
    from . import Wire
    from . import Vertex
    from . import Edge


class Sketch(Entity, SketchInterface):
    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        print(
            "mirror called:", mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("linear_pattern called:", instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        print(
            "circular_pattern called:",
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        print("create_from_file called:", file_path, file_type)
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        print("export called:", file_path, overwrite, scale)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        print("scale_xyz called:", x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_x called:", scale)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_y called:", scale)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        print("scale_z called:", scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        print("scale_x_by_factor called:", scale_factor)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        print("scale_y_by_factor called:", scale_factor)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        print("scale_z_by_factor called:", scale_factor)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        print("scale_keep_aspect_ratio called:", scale, axis)
        return self

    def project(self, project_onto: "Sketch") -> "Projectable":
        print("project called:", project_onto)
        from . import Sketch

        return Sketch("a projected sketch")

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

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        print("clone called:", new_name, copy_landmarks)
        from . import Sketch

        return Sketch("a sketch")

    def revolve(
        self,
        angle: AngleOrItsFloatOrStringValue,
        about_entity_or_landmark: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName = "z",
    ) -> "Part":
        print("revolve called:", angle, about_entity_or_landmark, axis)
        from . import Part

        return Part("a part")

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> "Part":
        print("extrude called:", length)
        from . import Part

        return Part("a part")

    def sweep(
        self, profile_name_or_instance: SketchOrItsName, fill_cap: bool = True
    ) -> "Part":
        print("sweep called:", profile_name_or_instance, fill_cap)
        from . import Part

        return Part("a part")

    def offset(self, radius: DimensionOrItsFloatOrStringValue):
        print("offset called:", radius)
        return self

    def profile(self, profile_curve_name: str):
        print("profile called:", profile_curve_name)
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
        print(
            "create_text called:",
            text,
            font_size,
            bold,
            italic,
            underlined,
            character_spacing,
            word_spacing,
            line_spacing,
            font_file_path,
        )
        return self

    def create_from_vertices(
        self, points: list[PointOrListOfFloatOrItsStringValueOrVertex]
    ) -> "Wire":
        print("create_from_vertices called:", points)
        from . import Wire

        return Wire([], "a wire")

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
        print("create_point called:", point)
        from . import Vertex

        return Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex")

    def create_line(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        print("create_line called:", start_at, end_at)
        from . import Vertex

        from . import Edge

        return Edge(
            v1=Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex"),
            v2=Vertex(Point.from_list_of_float_or_string([0, 0, 0]), "a vertex"),
            name="an edge",
        )

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        print("create_circle called:", radius)
        from . import Wire

        return Wire([], "a wire")

    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        print("create_ellipse called:", radius_minor, radius_major)
        from . import Wire

        return Wire([], "a wire")

    def create_arc(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
        radius: DimensionOrItsFloatOrStringValue,
        flip: Optional[bool] = False,
    ) -> "Wire":
        print("create_arc called:", start_at, end_at, radius, flip)
        from . import Wire

        return Wire([], "a wire")

    def create_rectangle(
        self,
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        print("create_rectangle called:", length, width)
        from . import Wire

        return Wire([], "a wire")

    def create_polygon(
        self,
        number_of_sides: "int",
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        print("create_polygon called:", number_of_sides, length, width)
        from . import Wire

        return Wire([], "a wire")

    def create_trapezoid(
        self,
        length_upper: DimensionOrItsFloatOrStringValue,
        length_lower: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        print("create_trapezoid called:", length_upper, length_lower, height)
        from . import Wire

        return Wire([], "a wire")

    def create_spiral(
        self,
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
    ) -> "Wire":
        print(
            "create_spiral called:",
            number_of_turns,
            height,
            radius,
            is_clockwise,
            radius_end,
        )
        from . import Wire

        return Wire([], "a wire")
