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
from providers.fusion360.fusion360_provider.fusion_actions.fusion_body import FusionBody
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

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance
        self.resolution = 4

    @supported(SupportLevel.SUPPORTED, notes="")
    def project(self, project_from: "ProjectableInterface") -> "ProjectableInterface":
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        fusionMirrorEntity = FusionBody(self.name)
        if isinstance(mirror_across_entity, str):
            component = get_component(mirror_across_entity)
            if not get_body(component, mirror_across_entity):
                fusionMirrorEntity = FusionSketch(mirror_across_entity)
        sketch, newPosition = mirror(
            FusionSketch(self.name), fusionMirrorEntity.center, axis
        )
        part = self.__class__(sketch.name)
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        offset = Dimension.from_dimension_or_its_float_or_string_value(offset, None)
        create_rectangular_pattern_sketch(
            FusionSketch(self.name).component,
            instance_count,
            offset.value,
            direction_axis,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        fusionEntity = FusionBody(self.name)
        if isinstance(center_entity_or_landmark, str):
            component = get_component(center_entity_or_landmark)
            if not get_body(component, center_entity_or_landmark):
                fusionEntity = FusionSketch(center_entity_or_landmark)
        create_circular_pattern_sketch(
            FusionSketch(self.name),
            fusionEntity.center,
            instance_count,
            separation_angle,
            normal_direction_axis,
        )
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_file(file_path: "str", file_type: "str| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        x = Dimension.from_dimension_or_its_float_or_string_value(x, None)
        y = Dimension.from_dimension_or_its_float_or_string_value(y, None)
        z = Dimension.from_dimension_or_its_float_or_string_value(z, None)
        FusionSketch(self.name).scale(x.value, y.value, z.value)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionSketch(self.name).scale(scale.value, 0, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionSketch(self.name).scale(0, scale.value, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionSketch(self.name).scale(0, 0, scale.value)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x_by_factor(self, scale_factor: "float"):
        FusionSketch(self.name).scale_by_factor(scale_factor, 0, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y_by_factor(self, scale_factor: "float"):
        FusionSketch(self.name).scale_by_factor(0, scale_factor, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z_by_factor(self, scale_factor: "float"):
        FusionSketch(self.name).scale_by_factor(0, 0, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionSketch(self.name).scale_uniform(scale.value)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def clone(
        self, new_name: "str| None" = None, copy_landmarks: "bool| None" = True
    ) -> "Sketch":
        new_sketch = clone_sketch(
            FusionSketch(self.name).instance, new_name, copy_landmarks
        )
        return Sketch(new_sketch.name)

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_text(
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
        profile_curve: "WireInterface|SketchInterface| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ):
        font_size = Dimension.from_dimension_or_its_float_or_string_value(
            font_size, None
        )
        create_text(
            FusionSketch(self.name).instance,
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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_vertices(
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        edges = []
        for index in range(len(points) - 1):
            start = Vertex(location=points[index], name="vertex")
            end = Vertex(location=points[index + 1], name="vertex")
            edge = Edge(v1=start, v2=end, name=self.name)
            edges.append(edge)
        return Wire(name=create_uuid_like_id())

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_point(
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Vertex":
        sketch = FusionSketch(self.name).instance
        make_point(sketch, point.x, point.y, point.z)
        return Vertex(location=point, name=create_uuid_like_id())

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line_to(
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "WireInterface":
        sketch = FusionSketch(self.name).instance
        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(to.x, to.y, to.z)
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
        edge = Edge(v1=start, v2=end, name=sketch.name)
        return edge

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_line(
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Edge":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_circle(
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        sketch = FusionSketch(self.name).instance
        self.curves = make_circle(sketch, radius.value, self.resolution)
        wire = self.create_from_vertices(self.curves)
        return wire

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_ellipse(
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_arc(
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        sketch = FusionSketch(self.name).instance
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)
        self.curves = make_arc(sketch, start, end, radius.value)
        wire = self.create_from_vertices(self.curves)
        return wire

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_rectangle(
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        width = Dimension.from_dimension_or_its_float_or_string_value(width, None)
        sketch = FusionSketch(self.name).instance
        self.curves = make_rectangle(sketch, length.value, width.value)
        self.name = sketch.name
        wire = self.create_from_vertices(self.curves)
        return wire

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_polygon(
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_trapezoid(
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_spiral(
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
        curve_type: "CurveTypes| None" = None,
    ) -> "Wire":
        raise NotImplementedError()
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_landmark(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
        landmark_name: "str| None" = None,
    ) -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        raise NotImplementedError()
        return Landmark("name", "parent")

    @supported(SupportLevel.SUPPORTED, notes="")
    def get_wires(self) -> "list[WireInterface]":
        raise NotImplementedError()

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_by_name(name: "str") -> "SketchInterface":
        print("get_by_name called", f": {name}")
        return Sketch("a sketch")
