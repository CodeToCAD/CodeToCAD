from typing import Optional
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.vertex_interface import VertexInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.interfaces.part_interface import PartInterface
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.interfaces.edge_interface import EdgeInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.vertex import Vertex
from providers.fusion360.fusion360_provider.landmark import Landmark
from providers.fusion360.fusion360_provider.part import Part
from providers.fusion360.fusion360_provider.wire import Wire
from providers.fusion360.fusion360_provider.edge import Edge
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
    sweep,
)
from .fusion_actions.modifiers import make_revolve
from .fusion_actions.curve import (
    make_arc,
    make_circle,
    make_line,
    make_point,
    make_rectangle,
)
from .fusion_actions.fusion_sketch import FusionSketch
from .fusion_actions.common import make_point3d
from . import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part
    from . import Entity
    from . import Wire
    from . import Vertex
    from . import Edge


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
        from . import Part

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

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "str|Entity",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        from . import Part

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

    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        print("create_from_file called:", file_path, file_type)
        return self

    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        print("export called:", file_path, overwrite, scale)
        return self

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

    def scale_x(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(scale.value, 0, 0)
        return self

    def scale_y(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(0, scale.value, 0)
        return self

    def scale_z(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale(0, 0, scale.value)
        return self

    def scale_x_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(scale_factor.value, 0, 0)
        return self

    def scale_y_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(0, scale_factor.value, 0)
        return self

    def scale_z_by_factor(self, scale_factor: "float"):
        scale_factor = Dimension.from_dimension_or_its_float_or_string_value(
            scale_factor, None
        )
        self.fusion_sketch.scale_by_factor(0, 0, scale_factor.value)
        return self

    # @check behavior with axis

    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        self.fusion_sketch.scale_uniform(scale.value)
        return self

    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "Sketch":
        new_sketch = clone_sketch(self.fusion_sketch.instance, new_name, copy_landmarks)
        return Sketch(new_sketch.name)

    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|Entity",
        axis: "str|int|Axis" = "z",
    ) -> "Part":
        from . import Part

        if isinstance(about_entity_or_landmark, str):
            component = get_component(about_entity_or_landmark)
            if get_body(component, about_entity_or_landmark):
                about_entity_or_landmark = Part(about_entity_or_landmark).fusion_body
            else:
                about_entity_or_landmark = Sketch(
                    about_entity_or_landmark
                ).fusion_sketch
        body = make_revolve(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            angle,
            axis,
            start=about_entity_or_landmark.center,
        )
        part = Part(body.name)
        part.fusion_body.instance = body
        return part

    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    def extrude(self, length: "str|float|Dimension") -> "Part":
        from . import Part

        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        body = self.fusion_sketch.extrude(length.value)
        part = Part(body.name)
        part.fusion_body.instance = body
        return part

    def sweep(
        self, profile_name_or_instance: "str|Sketch", fill_cap: "bool" = True
    ) -> "Part":
        from . import Part

        name = sweep(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            profile_name_or_instance.fusion_sketch.component,
            profile_name_or_instance.fusion_sketch.instance,
        )
        return Part(name)

    def offset(self, radius: "str|float|Dimension"):
        print("offset called:", radius)
        return self

    def profile(self, profile_curve_name: "str"):
        print("profile called:", profile_curve_name)
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

    def create_from_vertices(
        self, points: "str|list[str]|list[float]|list[Dimension]|Point|Vertex]"
    ) -> "Wire":
        from . import Edge, Vertex, Wire

        edges = []
        for index in range(len(points) - 1):
            start = Vertex(points[index], "vertex")
            end = Vertex(points[index + 1], "vertex")
            edge = Edge(v1=start, v2=end, name=self.name, parent_entity=self.name)
            edges.append(edge)
        return Wire(edges=edges, name=create_uuid_like_id(), parent_entity=self.name)

    def create_point(
        self, point: "str|list[str]|list[float]|list[Dimension]|Point"
    ) -> "Vertex":
        from . import Vertex

        sketch = self.fusion_sketch.instance
        make_point(sketch, point.x, point.y, point.z)
        return Vertex(location=point, name=create_uuid_like_id(), parent_entity=self)

    def create_line(
        self,
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
    ) -> "Edge":
        from . import Edge

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

    def create_circle(self, radius: "str|float|Dimension") -> "Wire":
        from . import Wire, Edge, Vertex

        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        sketch = self.fusion_sketch.instance
        self.curves = make_circle(sketch, radius.value, self.resolution)
        wire = self.create_from_vertices(self.curves)
        return wire

    def create_ellipse(
        self, radius_minor: "str|float|Dimension", radius_major: "str|float|Dimension"
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

    def create_arc(
        self,
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|Vertex",
        radius: "str|float|Dimension",
        flip: "bool| None" = False,
    ) -> "Wire":
        from . import Wire, Edge, Vertex

        sketch = self.fusion_sketch.instance
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)
        self.curves = make_arc(sketch, start, end, radius.value)
        wire = self.create_from_vertices(self.curves)
        return wire

    def create_rectangle(
        self, length: "str|float|Dimension", width: "str|float|Dimension"
    ) -> "Wire":
        from . import Wire, Edge, Vertex

        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        width = Dimension.from_dimension_or_its_float_or_string_value(width, None)
        sketch = self.fusion_sketch.instance
        self.curves = make_rectangle(sketch, length.value, width.value)
        self.name = sketch.name
        wire = self.create_from_vertices(self.curves)
        return wire

    def create_polygon(
        self,
        number_of_sides: "int",
        length: "str|float|Dimension",
        width: "str|float|Dimension",
    ) -> "Wire":
        from . import Wire, Edge

        print("create_polygon called:", number_of_sides, length, width)
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    def create_trapezoid(
        self,
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
    ) -> "Wire":
        from . import Wire, Edge

        print("create_trapezoid called:", length_upper, length_lower, height)
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    def create_spiral(
        self,
        number_of_turns: "int",
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
    ) -> "Wire":
        from . import Wire, Edge

        print(
            "create_spiral called:",
            number_of_turns,
            height,
            radius,
            is_clockwise,
            radius_end,
        )
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

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
