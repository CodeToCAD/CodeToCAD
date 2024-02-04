from typing import Optional

import adsk.core, adsk.fusion
from adsk import fusion

from codetocad.interfaces import SketchInterface, ProjectableInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

from .fusion_actions.common import clone_sketch, create_circular_pattern_sketch, create_retangular_pattern_sketch, create_text, get_component, get_sketch, rotate_sketch, scale_by_factor_sketch, scale_sketch, scale_sketch_uniform, sweep, translate_sketch


from . import Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Part
    from . import Entity
    from . import Wire
    from . import Vertex
    from . import Edge


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
        create_retangular_pattern_sketch(self.name, instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        create_circular_pattern_sketch(
            self.name,
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis
        )
        return self

    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        print("create_from_file called:", file_path, file_type)
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        print("export called:", file_path, overwrite, scale)
        return self

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        return self

    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        rotate_sketch(self.name, "x", rotation)
        return self

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        rotate_sketch(self.name, "y", rotation)
        return self

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        rotate_sketch(self.name, "z", rotation)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        scale_sketch(self.name, x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        scale_sketch(self.name, scale, 0, 0)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        scale_sketch(self.name, 0, scale, 0)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        scale_sketch(self.name, 0, 0, scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        scale_by_factor_sketch(self.name, scale_factor, 0, 0)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        scale_by_factor_sketch(self.name, 0, scale_factor, 0)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        scale_by_factor_sketch(self.name, 0, 0, scale_factor)
        return self

    def scale_keep_aspect_ratio(
        # self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
        self, scale: DimensionOrItsFloatOrStringValue
    ):
        scale_sketch_uniform(self.name, scale)
        return self

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
        self.name = name
        self.curve_type = curve_type
        self.description = description
        self.native_instance = native_instance
        self.resolution = 4

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "Sketch":
        clone_sketch(self.name, new_name)
        return Sketch("a sketch")

    def revolve(
        self,
        angle: AngleOrItsFloatOrStringValue,
        # about_entity_or_landmark: EntityOrItsName,
        axis,
    ) -> "Part":
        from . import Part

        app = adsk.core.Application.get()
        design = app.activeProduct
        root_comp = design.rootComponent
        sketches = root_comp.sketches;
        xyPlane = root_comp.xYConstructionPlane;
        sketch = sketches.add(xyPlane)

        # revolve_axes = design.rootComponent.constructionAxes
        # axis_input = revolve_axes.createInput()
        # axis_input.setByLine(adsk.core.InfiniteLine3D.create(adsk.core.Point3D.create(0), axis))
        # axis_input.setByTwoPoints(adsk.core.Point3D.create(0), axis)
        # revolve_axis = revolve_axes.add(axis_input)
        # revolve_axis = revolve_axes.add(axis_input)

        axis_line = sketch.sketchCurves.sketchLines
        revolve_axis = axis_line.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), axis)

        sketch = get_sketch(self.name)

        operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

        revolveFeatures = root_comp.features.revolveFeatures
        input = revolveFeatures.createInput(sketch.profiles.item(0), revolve_axis, operation)
        angle = adsk.core.ValueInput.createByReal(angle)
        input.setAngleExtent(False, angle)
        revolveFeature = revolveFeatures.add(input)

        body = design.rootComponent.bRepBodies.item(design.rootComponent.bRepBodies.count - 1)
        body.name = self.name

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
        comp = get_component(self.name)

        sketch = get_sketch(self.name)
        # adsk.core.Application.get().userInterface.messageBox(f"{sketch.name}")
        prof = sketch.profiles.item(0)
        extrudes = comp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(length)
        extInput.setDistanceExtent(False, distance)
        extInput.isSolid = True
        ext = extrudes.add(extInput)

        body = comp.bRepBodies.item(comp.bRepBodies.count - 1)
        body.name = self.name

        return Part(self.name)

    def sweep(
        self, profile_name_or_instance: SketchOrItsName, fill_cap: bool = True
    ) -> "Part":
        from . import Part
        sweep(self.name, profile_name_or_instance)
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
        create_text(
            self.name,
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
        app = adsk.core.Application.get()
        design = app.activeProduct

        newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane

        sketch = sketches.add(xyPlane)
        sketch.name = self.name

        somePoint = adsk.core.Point3D.create(point.x, point.y, point.z)
        sketchPoints = sketch.sketchPoints
        self.curve = sketchPoints
        point = sketchPoints.add(somePoint)

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

        app = adsk.core.Application.get()
        design = app.activeProduct

        newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane

        sketch = sketches.add(xyPlane)
        sketch.name = self.name

        sketchLines = sketch.sketchCurves.sketchLines
        self.curves = sketchLines
        # start = adsk.core.Point3D.create(start_at.x.value, start_at.y.value, start_at.z.value)
        # end = adsk.core.Point3D.create(end_at.x.value, end_at.y.value, end_at.z.value)
        start = adsk.core.Point3D.create(start_at.x, start_at.y, start_at.z)
        end = adsk.core.Point3D.create(end_at.x, end_at.y, end_at.z)
        sketchLines.addByTwoPoints(start, end)

        line = self.curves[0]
        start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
        end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
        edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)

        # return Edge.get_dummy_edge()
        return edge

    def create_circle(self, radius: DimensionOrItsFloatOrStringValue) -> "Wire":
        from .fusion_actions import circle
        from . import Wire, Edge

        app = adsk.core.Application.get()
        design = app.activeProduct

        newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        sketch.name = self.name

        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        points = circle.get_circle_points(radius, self.resolution)
        points = [adsk.core.Point3D.create(point.x.value, point.y.value, point.z.value) for point in points]

        control_points = adsk.core.ObjectCollection_create()
        for point in points:
            control_points.add(point)

        spline = sketch.sketchCurves.sketchFittedSplines.add(control_points)

        # circles = sketch.sketchCurves.sketchCircles
        # circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius.value)

        # self.curves = circles
        self.curves = sketch.sketchCurves.sketchFittedSplines

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

    def create_ellipse(
        self,
        radius_minor: DimensionOrItsFloatOrStringValue,
        radius_major: DimensionOrItsFloatOrStringValue,
    ) -> "Wire":
        from . import Wire

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
        app = adsk.core.Application.get()
        design = app.activeProduct

        newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane

        sketch = sketches.add(xyPlane)
        sketch.name = self.name

        startPoint = adsk.core.Point3D.create(start_at.x, start_at.y, start_at.z)
        alongPoint = adsk.core.Point3D.create((start_at.x + end_at.x) / 2, start_at.y + radius, start_at.z)
        endPoint = adsk.core.Point3D.create(end_at.x, end_at.y, end_at.z)

        arcs = sketch.sketchCurves.sketchArcs
        self.curves = arcs
        arc = arcs.addByThreePoints(startPoint, alongPoint, endPoint)

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
        half_length = (
            Dimension.from_dimension_or_its_float_or_string_value(length, None) / 2
        )
        half_width = (
            Dimension.from_dimension_or_its_float_or_string_value(width, None) / 2
        )
        left_top = Point(half_length * -1, half_width, Dimension(0))
        left_bottom = Point(half_length * -1, half_width * -1, Dimension(0))
        right_bottom = Point(half_length, half_width * -1, Dimension(0))
        right_top = Point(half_length, half_width, Dimension(0))

        points = [left_top, left_bottom, right_bottom, right_top, left_top]

        app = adsk.core.Application.get()
        design = app.activeProduct
        rootComp = design.rootComponent

        newComp = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane

        sketch = sketches.add(xyPlane)
        sketch.name = self.name
        self.name = sketch.name

        sketchLines = sketch.sketchCurves.sketchLines
        self.curves = sketchLines
        for i in range(len(points) - 1):
            start = adsk.core.Point3D.create(points[i].x.value, points[i].y.value, points[i].z.value)
            end = adsk.core.Point3D.create(points[i + 1].x.value, points[i + 1].y.value, points[i + 1].z.value)
            sketchLines.addByTwoPoints(start, end)

        # startPoint = adsk.core.Point3D.create(0, 0, 0)
        # endPoint = adsk.core.Point3D.create(width, length, 0)
        # sketchLines.addTwoPointRectangle(startPoint, endPoint)

        edges = []
        for line in self.curves:
            start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
            end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
            edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
            edges.append(edge)

        return self

        # return Wire(
        #     edges=edges,
        #     name=create_uuid_like_id(),
        #     parent_entity=self.name,
        # )

    def create_lines(
        self,
        points,
    ) -> "Wire":
        app = adsk.core.Application.get()
        design = app.activeProduct

        newComp = design.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
        newComp.name = self.name
        self.name = newComp.name

        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane

        sketch = sketches.add(xyPlane)
        sketch.name = self.name

        lines = sketch.sketchCurves.sketchLines

        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            lines.addByTwoPoints(start, end)

        self.curves = lines
        edges = []
        for line in self.curves:
            start = Point(line.startSketchPoint.geometry.x, line.startSketchPoint.geometry.y, line.startSketchPoint.geometry.z)
            end = Point(line.endSketchPoint.geometry.x, line.endSketchPoint.geometry.y, line.endSketchPoint.geometry.z)
            edge = Edge(v1=start, v2=end, name=sketch.name, parent_entity=self.name)
            edges.append(edge)

        return None

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
