from typing import Optional

import adsk.core, adsk.fusion

from codetocad.interfaces import SketchInterface, ProjectableInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from .fusion_actions.actions import clone_sketch, create_circular_pattern_sketch, create_rectangular_pattern_sketch, create_text, mirror, sweep
from .fusion_actions.modifiers import make_revolve

from .fusion_actions.curve import make_arc, make_circle, make_line, make_point, make_rectangle
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


class Sketch(Entity, SketchInterface):
    name: str
    curve_type: Optional["CurveTypes"] = None
    description: Optional[str] = None
    native_instance = None
    curves = None

    def __init__(
        self,
        name: str,
        curve_type: Optional["CurveTypes"] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        self.fusion_sketch = FusionSketch(name)
        # self.name = name
        self.name = self.fusion_sketch.instance.name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance
        self.resolution = 4

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
        sketch, newPosition = mirror(self.fusion_sketch, mirror_across_entity.center, axis)
        part = self.__class__(sketch.name)
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        create_rectangular_pattern_sketch(
            self.fusion_sketch.component,
            instance_count,
            offset,
            direction_axis
        )
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        center = center_entity_or_landmark.center

        create_circular_pattern_sketch(
            # self.fusion_sketch.component,
            self.fusion_sketch,
            center,
            instance_count,
            separation_angle,
            normal_direction_axis
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
        self.fusion_sketch.scale(x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_sketch.scale(scale, 0, 0)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_sketch.scale(0, scale, 0)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        self.fusion_sketch.scale(0, 0, scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        self.fusion_sketch.scale_by_factor(scale_factor, 0, 0)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        self.fusion_sketch.scale_by_factor(0, scale_factor, 0)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        self.fusion_sketch.scale_by_factor(0, 0, scale_factor)
        return self

    # @check behavior with axis
    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName = None
        # self, scale: DimensionOrItsFloatOrStringValue
    ):
        self.fusion_sketch.scale_uniform(scale)
        return self


    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        new_sketch = clone_sketch(self.fusion_sketch.instance, new_name, copy_landmarks)
        return Sketch(new_sketch.name)

    def revolve(
        self,
        angle: AngleOrItsFloatOrStringValue,
        about_entity_or_landmark: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName = "z",
    ) -> "Part":
        from . import Part

        body = make_revolve(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            angle,
            about_entity_or_landmark,
            axis,
        )

        return Part(body.name)

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
        from . import Part
        body = self.fusion_sketch.extrude(length)
        return Part(body.name)

    def sweep(
        self, profile_name_or_instance: SketchOrItsName, fill_cap: bool = True
    ) -> "Part":
        from . import Part
        name = sweep(
            self.fusion_sketch.component,
            self.fusion_sketch.instance,
            profile_name_or_instance.fusion_sketch.component,
            profile_name_or_instance.fusion_sketch.instance,
        )
        return Part(name)

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
        create_text(
            self.fusion_sketch.instance,
            text,
            font_size,
            bold,
            italic,
            underlined,
            character_spacing,
            word_spacing,
            line_spacing,
            font_file_path
        )
        return self

    def create_from_vertices(
        self, points: list[PointOrListOfFloatOrItsStringValueOrVertex]
    ) -> "Wire":
        parsed_points = [Point.from_dimension_or_its_float_or_string_value(point) for point in points]

        is_closed = False
        if len(parsed_points) > 1 and parsed_points[0] == parsed_points[-1]:
            is_closed = True
            parsed_points = parsed_points[:-1]

        # is_closed = False
        # if len(parsed_points) > 1 and parsed_points[0] == parsed_points[-1]:
        #     is_closed = True
        #     parsed_points = parsed_points[:-1]

        # curve_data, parsed_points = create_curve(self.name, points)


        return Wire(edges=points, name=create_uuid_like_id(), parent_entity=self.name)

    def create_point(self, point: PointOrListOfFloatOrItsStringValue) -> "Vertex":
        from . import Vertex
        sketch = self.fusion_sketch.instance

        make_point(sketch, point.x, point.y, point.z)

        return Vertex(
            location=point,
            name=create_uuid_like_id(),
            parent_entity=self,
        )

    def create_line(
        self,
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
    ) -> "Edge":
        from . import Edge
        sketch = self.fusion_sketch.instance

        # sketchLines = sketch.sketchCurves.sketchLines
        # self.curves = sketchLines
        # # start = adsk.core.Point3D.create(start_at.x.value, start_at.y.value, start_at.z.value)
        # # end = adsk.core.Point3D.create(end_at.x.value, end_at.y.value, end_at.z.value)
        # start = adsk.core.Point3D.create(start_at.x, start_at.y, start_at.z)
        # end = adsk.core.Point3D.create(end_at.x, end_at.y, end_at.z)
        # sketchLines.addByTwoPoints(start, end)

        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)

        # self.curves = make_point(sketch, start, end)
        self.curves = make_line(sketch, start, end)

        line = self.curves[0]
        start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
        end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
        edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)

        # return Edge.get_dummy_edge()
        return edge

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        from . import Wire, Edge

        sketch = self.fusion_sketch.instance

        # radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        # points = circle.get_circle_points(radius, self.resolution)
        # points = [adsk.core.Point3D.create(point.x.value, point.y.value, point.z.value) for point in points]

        # control_points = adsk.core.ObjectCollection_create()
        # for point in points:
        #     control_points.add(point)

        # spline = sketch.sketchCurves.sketchFittedSplines.add(control_points)

        # circles = sketch.sketchCurves.sketchCircles
        # circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius.value)

        # self.curves = circles
        # self.curves = sketch.sketchCurves.sketchFittedSplines
        self.curves = make_circle(sketch, radius, self.resolution)

        edges = []
        for line in self.curves:
            start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
            end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
            edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
            edges.append(edge)

        return Wire(
            edges=edges,
            name=create_uuid_like_id(),
            parent_entity=self.name,
        )

    # @check wrong scaling
    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
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
        start_at: PointOrListOfFloatOrItsStringValueOrVertex,
        end_at: PointOrListOfFloatOrItsStringValueOrVertex,
        radius: DimensionOrItsFloatOrStringValue,
        flip: Optional[bool] = False,
    ) -> "Wire":
        from . import Wire, Edge
        sketch = self.fusion_sketch.instance

        # startPoint = adsk.core.Point3D.create(start_at.x, start_at.y, start_at.z)
        # alongPoint = adsk.core.Point3D.create((start_at.x + end_at.x) / 2, start_at.y + radius, start_at.z)
        # endPoint = adsk.core.Point3D.create(end_at.x, end_at.y, end_at.z)

        # arcs = sketch.sketchCurves.sketchArcs
        # self.curves = arcs
        # arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

        start = make_point3d(start_at.x, start_at.y, start_at.z)
        end = make_point3d(end_at.x, end_at.y, end_at.z)

        self.curves = make_arc(sketch, start, end, radius)

        edges = []
        for line in self.curves:
            start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
            end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
            edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
            edges.append(edge)

        return Wire(
            edges=edges,
            name=create_uuid_like_id(),
            parent_entity=self.name,
        )

    def create_rectangle(
        self,
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        from . import Wire, Edge

        sketch = self.fusion_sketch.instance

        self.curves = make_rectangle(sketch, length, width)

        edges = []
        for line in self.curves:
            start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
            end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
            edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
            edges.append(edge)

        return Wire(
            edges=edges,
            name=create_uuid_like_id(),
            parent_entity=self.name,
        )

    def create_polygon(
        self,
        number_of_sides: "int",
        length: DimensionOrItsFloatOrStringValue,
        width: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        from . import Wire, Edge

        print("create_polygon called:", number_of_sides, length, width)
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    def create_trapezoid(
        self,
        length_upper: DimensionOrItsFloatOrStringValue,
        length_lower: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        from . import Wire, Edge

        print("create_trapezoid called:", length_upper, length_lower, height)
        return Wire(edges=[Edge(v1=(0, 0), v2=(5, 5), name="myEdge")], name="myWire")

    def create_spiral(
        self,
        number_of_turns: "int",
        height: DimensionOrItsFloatOrStringValue,
        radius: DimensionOrItsFloatOrStringValue,
        is_clockwise: bool = True,
        radius_end: Optional[DimensionOrItsFloatOrStringValue] = None,
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
