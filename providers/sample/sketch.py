# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *

from typing import Self

from codetocad.proxy.edge import Edge
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.sketch_interface import SketchInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.projectable_interface import ProjectableInterface


from codetocad.interfaces.entity_interface import EntityInterface


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

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_wires(
        self,
    ) -> "list[WireInterface]":

        print(
            "get_wires called",
        )

        return [
            Wire(
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
        ]

    @supported(SupportLevel.SUPPORTED, notes="")
    def clone(
        self, new_name: "str", copy_landmarks: "bool" = True
    ) -> "SketchInterface":

        print("clone called", f": {new_name}, {copy_landmarks}")

        return Sketch("a sketch")

    @supported(SupportLevel.SUPPORTED, notes="")
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
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_text called",
            f": {text}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}, {center_at}, {options}",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_from_vertices called", f": {points}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_point called", f": {point}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_line called", f": {length}, {angle}, {start_at}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_line_to called", f": {to}, {start_at}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_circle(
        self,
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_circle called", f": {radius}, {center_at}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_ellipse(
        self,
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_ellipse called",
            f": {radius_minor}, {radius_major}, {center_at}, {options}",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_arc called", f": {end_at}, {radius}, {start_at}, {flip}, {options}"
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_rectangle(
        self,
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print("create_rectangle called", f": {length}, {width}, {center_at}, {options}")

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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_polygon called",
            f": {number_of_sides}, {length}, {width}, {center_at}, {options}",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_trapezoid called",
            f": {length_upper}, {length_lower}, {height}, {center_at}, {options}",
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":

        print(
            "create_spiral called",
            f": {number_of_turns}, {height}, {radius}, {is_clockwise}, {radius_end}, {center_at}, {options}",
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

    @supported(SupportLevel.SUPPORTED, notes="")
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

    @supported(SupportLevel.SUPPORTED, notes="")
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

    @supported(SupportLevel.SUPPORTED, notes="")
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

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_file(self, file_path: "str", file_type: "str| None" = None) -> Self:

        print("create_from_file called", f": {file_path}, {file_type}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(
        self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0
    ) -> Self:

        print("export called", f": {file_path}, {overwrite}, {scale}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> Self:

        print("scale_xyz called", f": {x}, {y}, {z}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x(self, scale: "str|float|Dimension") -> Self:

        print("scale_x called", f": {scale}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y(self, scale: "str|float|Dimension") -> Self:

        print("scale_y called", f": {scale}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z(self, scale: "str|float|Dimension") -> Self:

        print("scale_z called", f": {scale}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x_by_factor(self, scale_factor: "float") -> Self:

        print("scale_x_by_factor called", f": {scale_factor}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y_by_factor(self, scale_factor: "float") -> Self:

        print("scale_y_by_factor called", f": {scale_factor}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z_by_factor(self, scale_factor: "float") -> Self:

        print("scale_z_by_factor called", f": {scale_factor}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ) -> Self:

        print("scale_keep_aspect_ratio called", f": {scale}, {axis}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":

        print("project called", f": {project_from}")

        return __import__("codetocad").Sketch("a projected sketch")

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":

        print("create_landmark called", f": {landmark_name}, {x}, {y}, {z}")

        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":

        print("get_landmark called", f": {landmark_name}")

        return Landmark("name", "parent")
