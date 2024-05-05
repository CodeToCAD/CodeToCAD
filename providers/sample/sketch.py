# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.interfaces.sketch_interface import SketchInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.proxy.edge import Edge
from codetocad.proxy.vertex import Vertex

from codetocad.proxy.wire import Wire

from codetocad.proxy.landmark import Landmark


from providers.sample.entity import Entity


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
    ) -> "WireInterface":

        print(
            "create_text called",
            f": {text}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}",
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

    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
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
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> "WireInterface":

        print("create_point called", f": {point}")

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

    def create_line(
        self,
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
    ) -> "WireInterface":

        print("create_line called", f": {start_at}, {end_at}")

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

    def create_circle(self, radius: "str|float|Dimension") -> "WireInterface":

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
        self, radius_minor: "str|float|Dimension", radius_major: "str|float|Dimension"
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
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
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
        self, length: "str|float|Dimension", width: "str|float|Dimension"
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
        length: "str|float|Dimension",
        width: "str|float|Dimension",
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
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
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
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
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
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
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
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):

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
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):

        print("scale_xyz called", f": {x}, {y}, {z}")

        return self

    def scale_x(self, scale: "str|float|Dimension"):

        print("scale_x called", f": {scale}")

        return self

    def scale_y(self, scale: "str|float|Dimension"):

        print("scale_y called", f": {scale}")

        return self

    def scale_z(self, scale: "str|float|Dimension"):

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
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):

        print("scale_keep_aspect_ratio called", f": {scale}, {axis}")

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
