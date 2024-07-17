from typing import Optional
from codetocad.proxy.part import Part
from codetocad.utilities import create_uuid_like_id
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.projectable_interface import ProjectableInterface
from codetocad.proxy.edge import Edge
from codetocad.proxy.vertex import Vertex
from codetocad.proxy.wire import Wire
from codetocad.proxy.landmark import Landmark
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.fusion360.fusion360_provider.entity import Entity
from codetocad.codetocad_types import *
from providers.fusion360.fusion360_provider.fusion_actions.base import (
    get_body,
    get_component,
)
from .fusion_actions.actions import (
    clone_sketch,
    create_circular_pattern_sketch,
    create_rectangular_pattern_sketch,
    create_text,
    mirror,
)
from .fusion_actions.curve import (
    make_arc,
    make_circle,
    make_line,
    make_point,
    make_rectangle,
)
from .fusion_actions.fusion_sketch import FusionSketch
from .fusion_actions.common import make_point3d


class Sketch(SketchInterface, Entity):
    name: str
    curve_type: Optional["CurveTypes"] = None
    description: Optional[str] = None
    native_instance = None
    curves = None

    def __init__(
        self,
        name: "str",
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        self.fusion_sketch = FusionSketch(name)
        # self.name = name
        self.name = self.fusion_sketch.instance.name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance
        self.resolution = 4

    @supported(SupportLevel.UNSUPPORTED)
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def mirror(
        self,
        mirror_across_entity: "str|EntityInterface",
        axis: "str|int|Axis",
        resulting_mirrored_entity_name: "str| None" = None,
    ):

        if isinstance(mirror_across_entity, str):
            component = get_component(mirror_across_entity)
            if get_body(component, mirror_across_entity):
                mirror_across_entity = Part(mirror_across_entity).fusion_body
            else:
                mirror_across_entity = Sketch(mirror_across_entity).fusion_sketch
        sketch, newPosition = mirror(
            self.fusion_sketch, mirror_across_entity.center, axis
        )
        part = self.__class__(sketch.name)
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        offset = Dimension.from_dimension_or_its_float_or_string_value(offset, None)
        create_rectangular_pattern_sketch(
            self.fusion_sketch.component, instance_count, offset.value, direction_axis
        )
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        if isinstance(center_entity_or_landmark, str):
            component = get_component(center_entity_or_landmark)
            if get_body(component, center_entity_or_landmark):
                center_entity_or_landmark = Part(center_entity_or_landmark).fusion_body
            else:
                center_entity_or_landmark = Sketch(
                    center_entity_or_landmark
                ).fusion_sketch
        center = center_entity_or_landmark.center
        create_circular_pattern_sketch(
            self.fusion_sketch,
            center,
            instance_count,
            separation_angle,
            normal_direction_axis,
        )
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        x = Dimension.from_dimension_or_its_float_or_string_value(x, None)
        y = Dimension.from_dimension_or_its_float_or_string_value(y, None)
        z = Dimension.from_dimension_or_its_float_or_string_value(z, None)
        self.fusion_sketch.scale(x.value, y.value, z.value)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_x(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(scale.value, 0, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_y(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(0, scale.value, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_z(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(0, 0, scale.value)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_x_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(scale_factor.value, 0, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_y_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(0, scale_factor.value, 0)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def scale_z_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(0, 0, scale_factor.value)
        return self

    # @check behavior with axis

    @supported(SupportLevel.UNSUPPORTED)
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale_uniform(scale.value)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "Sketch":
        new_sketch = clone_sketch(self.fusion_sketch.instance, new_name, copy_landmarks)
        return Sketch(new_sketch.name)

    @supported(SupportLevel.UNSUPPORTED)
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
    ):
        font_size = Dimension.from_dimension_or_its_float_or_string_value(
            font_size, None
        )
        create_text(
            self.fusion_sketch.instance,
            text,
            font_size.value,
            bold,
            italic,
            underlined,
            character_spacing,
            word_spacing,
            line_spacing,
            font_file_path,
        )
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> "Wire":

        edges = []
        for index in range(len(points) - 1):
            start = Vertex(points[index], "vertex")
            end = Vertex(points[index + 1], "vertex")
            edge = Edge(v1=start, v2=end, name=self.name, parent_entity=self.name)
            edges.append(edge)
        return Wire(edges=edges, name=create_uuid_like_id(), parent_entity=self.name)

    @supported(SupportLevel.UNSUPPORTED)
    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> "Vertex":

        sketch = self.fusion_sketch.instance
        make_point(sketch, point.x, point.y, point.z)
        return Vertex(location=point, name=create_uuid_like_id(), parent_entity=self)

    @supported(SupportLevel.UNSUPPORTED)
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "Edge":

        sketch = self.fusion_sketch.instance
        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)
        self.curves = make_line(sketch, start, end)
        line = self.curves[0]
        start = Point(
            line.startSketchPoint.geometry.x,
            line.startSketchPoint.geometry.y,
            line.startSketchPoint.geometry.z,
        )
        end = Point(
            line.endSketchPoint.geometry.x,
            line.endSketchPoint.geometry.y,
            line.endSketchPoint.geometry.z,
        )
        edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
        return edge

    @supported(SupportLevel.UNSUPPORTED)
    def create_circle(
        self,
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        sketch = self.fusion_sketch.instance
        self.curves = make_circle(sketch, radius.value, self.resolution)
        wire = self.create_from_vertices(self.curves)
        return wire

    @supported(SupportLevel.UNSUPPORTED)
    def create_ellipse(
        self,
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        # from . import Wire
        radius_minor = Dimension.from_dimension_or_its_float_or_string_value(
            radius_minor
        )
        radius_major = Dimension.from_dimension_or_its_float_or_string_value(
            radius_major
        )
        is_minor_lesser = radius_minor < radius_major
        wire = self.create_circle(radius_minor if is_minor_lesser else radius_major)
        if is_minor_lesser:
            self.scale_y(radius_major.value * 2)
        else:
            self.scale_x(radius_minor.value * 2)
        return wire

    @supported(SupportLevel.UNSUPPORTED)
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        sketch = self.fusion_sketch.instance
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)
        self.curves = make_arc(sketch, start, end, radius.value)
        wire = self.create_from_vertices(self.curves)
        return wire

    @supported(SupportLevel.UNSUPPORTED)
    def create_rectangle(
        self,
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        width = Dimension.from_dimension_or_its_float_or_string_value(width, None)
        sketch = self.fusion_sketch.instance
        self.curves = make_rectangle(sketch, length.value, width.value)
        self.name = sketch.name
        wire = self.create_from_vertices(self.curves)
        return wire

    @supported(SupportLevel.UNSUPPORTED)
    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @supported(SupportLevel.UNSUPPORTED)
    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @supported(SupportLevel.UNSUPPORTED)
    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @supported(SupportLevel.UNSUPPORTED)
    def create_landmark(
        self,
        landmark_name: "str",
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

    @supported(SupportLevel.UNSUPPORTED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

    @supported(SupportLevel.UNSUPPORTED)
    def get_wires(self) -> "list[WireInterface]":
        raise NotImplementedError()
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

    @supported(SupportLevel.UNSUPPORTED)
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        raise NotImplementedError()
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
