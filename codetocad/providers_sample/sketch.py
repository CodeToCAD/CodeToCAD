# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import SketchInterface


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.edge_interface import EdgeInterface


from codetocad.providers_sample.entity import Entity

from codetocad.providers_sample.vertex import Vertex

from codetocad.providers_sample.landmark import Landmark

from codetocad.providers_sample.part import Part

from codetocad.providers_sample.wire import Wire

from codetocad.providers_sample.edge import Edge


class Sketch(SketchInterface, Entity):
    def __init__(
        self,
        name: "str",
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.curve_type = curve_type

    def clone(
        self, new_name: "str", copy_landmarks: "bool" = True
    ) -> "SketchInterface":
        print("clone called", f": {new_name}, {copy_landmarks}")

        return Sketch("a sketch")

    def revolve(
        self,
        angle: "AngleOrItsFloatOrStringValue",
        about_entity_or_landmark: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName" = "z",
    ) -> "PartInterface":
        print("revolve called", f": {angle}, {about_entity_or_landmark}, {axis}")

        return Part("a part")

    def twist(
        self,
        angle: "AngleOrItsFloatOrStringValue",
        screw_pitch: "DimensionOrItsFloatOrStringValue",
        iterations: "int" = 1,
        axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        print("twist called", f": {angle}, {screw_pitch}, {iterations}, {axis}")

        return self

    def extrude(self, length: "DimensionOrItsFloatOrStringValue") -> "PartInterface":
        print("extrude called", f": {length}")

        return Part("a part")

    def sweep(
        self, profile_name_or_instance: "SketchOrItsName", fill_cap: "bool" = True
    ) -> "PartInterface":
        print("sweep called", f": {profile_name_or_instance}, {fill_cap}")

        return Part("a part")

    def offset(self, radius: "DimensionOrItsFloatOrStringValue"):
        print("offset called", f": {radius}")

        return self

    def profile(self, profile_curve_name: "str"):
        print("profile called", f": {profile_curve_name}")

        return self

    def create_text(
        self,
        text: "str",
        font_size: "DimensionOrItsFloatOrStringValue" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
    ):
        print(
            "create_text called",
            f": {text}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}",
        )

        return self

    def create_from_vertices(
        self, points: "list[PointOrListOfFloatOrItsStringValueOrVertex]"
    ) -> "WireInterface":
        print("create_from_vertices called", f": {points}")

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

    def create_point(
        self, point: "PointOrListOfFloatOrItsStringValue"
    ) -> "VertexInterface":
        print("create_point called", f": {point}")

        return Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0]))

    def create_line(
        self,
        start_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        end_at: "PointOrListOfFloatOrItsStringValueOrVertex",
    ) -> "EdgeInterface":
        print("create_line called", f": {start_at}, {end_at}")

        return Edge(
            v1=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            v2=Vertex("a vertex", Point.from_list_of_float_or_string([0, 0, 0])),
            name="an edge",
        )

    def create_circle(
        self, radius: "DimensionOrItsFloatOrStringValue"
    ) -> "WireInterface":
        print("create_circle called", f": {radius}")

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

    def create_ellipse(
        self,
        radius_minor: "DimensionOrItsFloatOrStringValue",
        radius_major: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        print("create_ellipse called", f": {radius_minor}, {radius_major}")

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

    def create_arc(
        self,
        start_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        end_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        radius: "DimensionOrItsFloatOrStringValue",
        flip: "bool| None" = False,
    ) -> "WireInterface":
        print("create_arc called", f": {start_at}, {end_at}, {radius}, {flip}")

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

    def create_rectangle(
        self,
        length: "DimensionOrItsFloatOrStringValue",
        width: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        print("create_rectangle called", f": {length}, {width}")

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

    def create_polygon(
        self,
        number_of_sides: "int",
        length: "DimensionOrItsFloatOrStringValue",
        width: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        print("create_polygon called", f": {number_of_sides}, {length}, {width}")

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

    def create_trapezoid(
        self,
        length_upper: "DimensionOrItsFloatOrStringValue",
        length_lower: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        print("create_trapezoid called", f": {length_upper}, {length_lower}, {height}")

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

    def create_spiral(
        self,
        number_of_turns: "int",
        height: "DimensionOrItsFloatOrStringValue",
        radius: "DimensionOrItsFloatOrStringValue",
        is_clockwise: "bool" = True,
        radius_end: "DimensionOrItsFloatOrStringValue| None" = None,
    ) -> "WireInterface":
        print(
            "create_spiral called",
            f": {number_of_turns}, {height}, {radius}, {is_clockwise}, {radius_end}",
        )

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

    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        print("create_from_file called", f": {file_path}, {file_type}")

        return self

    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        print("export called", f": {file_path}, {overwrite}, {scale}")

        return self

    def scale_xyz(
        self,
        x: "DimensionOrItsFloatOrStringValue",
        y: "DimensionOrItsFloatOrStringValue",
        z: "DimensionOrItsFloatOrStringValue",
    ):
        print("scale_xyz called", f": {x}, {y}, {z}")

        return self

    def scale_x(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_x called", f": {scale}")

        return self

    def scale_y(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_y called", f": {scale}")

        return self

    def scale_z(self, scale: "DimensionOrItsFloatOrStringValue"):
        print("scale_z called", f": {scale}")

        return self

    def scale_x_by_factor(self, scale_factor: "float"):
        print("scale_x_by_factor called", f": {scale_factor}")

        return self

    def scale_y_by_factor(self, scale_factor: "float"):
        print("scale_y_by_factor called", f": {scale_factor}")

        return self

    def scale_z_by_factor(self, scale_factor: "float"):
        print("scale_z_by_factor called", f": {scale_factor}")

        return self

    def scale_keep_aspect_ratio(
        self, scale: "DimensionOrItsFloatOrStringValue", axis: "AxisOrItsIndexOrItsName"
    ):
        print("scale_keep_aspect_ratio called", f": {scale}, {axis}")

        return self

    def project(self, project_onto: "ProjectableInterface") -> "ProjectableInterface":
        print("project called", f": {project_onto}")

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
