from codetocad.interfaces.landmark_interface import LandmarkInterface
from codetocad.proxy.sketch import Sketch
from typing import Self
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.proxy.landmark import Landmark
from codetocad.interfaces.part_interface import PartInterface
from providers.fusion360.fusion360_provider.entity import Entity
from providers.fusion360.fusion360_provider.landmark import Landmark
from providers.fusion360.fusion360_provider.sketch import Sketch
from codetocad.codetocad_types import *
from .fusion_actions.actions import (
    chamfer_all_edges,
    combine,
    create_circular_pattern_sketch,
    create_rectangular_pattern,
    fillet_all_edges,
    hole,
    hollow,
    intersect,
    mirror,
    set_material,
    subtract,
)
from .fusion_actions.fusion_sketch import FusionSketch
from .fusion_actions.base import delete_occurrence, get_body, get_component
from .fusion_actions.curve import make_arc, make_circle, make_lines, make_rectangle
from .fusion_actions.modifiers import make_loft, make_revolve
from .fusion_actions.fusion_body import FusionBody
from .fusion_actions.common import make_point3d


class Part(PartInterface, Entity):

    def __init__(self, native_instance: "Any"):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.SUPPORTED, notes="")
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        fusionEntity = FusionBody(mirror_across_entity)
        if isinstance(mirror_across_entity, str):
            component = get_component(mirror_across_entity)
            if not get_body(component, mirror_across_entity):
                fusionEntity = FusionSketch(mirror_across_entity)
        body, newPosition = mirror(FusionBody(self.name), fusionEntity.center, axis)
        part = self.__class__(body.name)
        part.translate_xyz(newPosition.x, newPosition.y, newPosition.z)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        create_rectangular_pattern(
            FusionBody(self.name).component, instance_count, offset, direction_axis
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
        fusionPatternEntity = FusionBody(self.name)
        if isinstance(center_entity_or_landmark, str):
            component = get_component(center_entity_or_landmark)
            if get_body(component, center_entity_or_landmark):
                fusionPatternEntity = FusionBody(center_entity_or_landmark)
            else:
                fusionPatternEntity = FusionSketch(center_entity_or_landmark)
        create_circular_pattern_sketch(
            FusionBody(self.name),
            fusionPatternEntity.center,
            instance_count,
            separation_angle,
            normal_direction_axis,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def remesh(self, strategy: "str", amount: "float"):
        print("remesh called:", strategy, amount)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subdivide(self, amount: "float"):
        print("subdivide called:", amount)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def decimate(self, amount: "float"):
        print("decimate called:", amount)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_from_file(file_path: "str", file_type: "str| None" = None):
        print("create_from_file called:", file_path, file_type)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        print("export called:", file_path, overwrite, scale)
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
        FusionBody(self.name).scale(x, y, z)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionBody(self.name).scale(scale.value, 0, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionBody(self.name).scale(0, scale.value, 0)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z(self, scale: "str|float|Dimension"):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionBody(self.name).scale(0, 0, scale.value)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_x_by_factor(self, scale_factor: "float"):
        FusionBody(self.name).scale_by_factor(scale_factor, 1, 1)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_y_by_factor(self, scale_factor: "float"):
        FusionBody(self.name).scale_by_factor(1, scale_factor, 1)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_z_by_factor(self, scale_factor: "float"):
        FusionBody(self.name).scale_by_factor(1, 1, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        FusionBody(self.name).scale_uniform(scale.value)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_cube(
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        width = Dimension.from_dimension_or_its_float_or_string_value(width, None)
        length = Dimension.from_dimension_or_its_float_or_string_value(length, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)
        sketch = FusionSketch(FusionBody(self.name).sketch.name)
        _ = make_rectangle(sketch.instance, width.value, length.value)
        FusionBody(self.name).instance = sketch.extrude(height.value)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_cone(
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)
        draft_radius = Dimension.from_dimension_or_its_float_or_string_value(
            draft_radius, None
        )
        if draft_radius == Dimension(0):
            import math

            points = [
                make_point3d(0, 0, 0),
                make_point3d(0, 0, height.value),
                make_point3d(radius.value, 0, 0),
                make_point3d(0, 0, 0),
            ]
            _ = make_lines(FusionBody(self.name).sketch, points)
            FusionBody(self.name).instance = make_revolve(
                FusionBody(self.name).component,
                FusionBody(self.name).sketch,
                math.pi * 2,
                make_point3d(0, 0, 0),
                make_point3d(0, 0, radius.value),
            )
        else:
            base = Sketch(FusionBody(self.name).sketch.name + "_temp_base")
            _ = base.create_circle(radius)
            top = Sketch(FusionBody(self.name).sketch.name + "_temp_top")
            _ = top.create_circle(draft_radius)
            top.translate_z(height.value)
            base_instance = FusionSketch(base.name).instance
            top_instance = FusionSketch(top.name).instance
            FusionBody(self.name).instance = make_loft(
                FusionBody(self.name).component, base_instance, top_instance
            )
            delete_occurrence(base_instance.name)
            delete_occurrence(top_instance.name)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_cylinder(
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        height = Dimension.from_dimension_or_its_float_or_string_value(height, None)
        sketch = FusionSketch(FusionBody(self.name).sketch.name)
        _ = make_circle(sketch.instance, radius.value, 4)
        FusionBody(self.name).instance = sketch.extrude(height.value)
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_torus(
        inner_radius: "str|float|Dimension",
        outer_radius: "str|float|Dimension",
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        import math

        inner_radius = Dimension.from_dimension_or_its_float_or_string_value(
            inner_radius
        )
        outer_radius = Dimension.from_dimension_or_its_float_or_string_value(
            outer_radius
        )
        sketch = FusionSketch(self.name).instance
        circles = sketch.sketchCurves.sketchCircles
        # TODO: move adsk reference to a FusionActions method
        _ = circles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), inner_radius.value
        )
        FusionBody(self.name).instance = make_revolve(
            FusionBody(self.name).component,
            sketch,
            math.pi * 2,
            "x",
            start=make_point3d(-inner_radius.value, -outer_radius.value, 0),
            end=make_point3d(inner_radius.value, -outer_radius.value, 0),
        )
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_sphere(
        radius: "str|float|Dimension",
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        import math

        radius = Dimension.from_dimension_or_its_float_or_string_value(radius)
        start = make_point3d(radius.value, 0, 0)
        end = make_point3d(-radius.value, 0, 0)
        sketch = Sketch(FusionBody(self.name).sketch.name)
        sketch_instance = FusionSketch(sketch.name).instance
        make_arc(sketch_instance, start, end, radius.value, True)
        FusionBody(self.name).instance = make_revolve(
            FusionBody(self.name).component,
            sketch_instance,
            math.pi * 2,
            start=make_point3d(0, 0, 0),
            end=end,
        )
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_gear(
        outer_radius: "str|float|Dimension",
        addendum: "str|float|Dimension",
        inner_radius: "str|float|Dimension",
        dedendum: "str|float|Dimension",
        height: "str|float|Dimension",
        pressure_angle: "str|float|Angle" = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: "str|float|Angle" = 0,
        conical_angle: "str|float|Angle" = 0,
        crown_angle: "str|float|Angle" = 0,
        name: "str| None" = None,
        description: "str| None" = None,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def clone(
        self, new_name: "str| None" = None, copy_landmarks: "bool| None" = True
    ) -> "Part":
        body, sketch = FusionBody(self.name).clone(new_name, copy_landmarks)
        part = Part(body.name)
        return part

    @supported(SupportLevel.SUPPORTED, notes="")
    def union(
        self,
        other: "BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        if not isinstance(other, str):
            raise NotImplementedError()
        combine(
            FusionBody(self.name).instance,
            FusionBody(other).instance,
            delete_after_union,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def subtract(
        self,
        other: "BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        if not isinstance(other, str):
            raise NotImplementedError()
        subtract(
            FusionBody(self.name).instance,
            FusionBody(other).instance,
            delete_after_subtract,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def intersect(
        self,
        other: "BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        if not isinstance(other, str):
            raise NotImplementedError()
        intersect(
            FusionBody(self.name).instance,
            FusionBody(other).instance,
            delete_after_intersect,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def hollow(
        self,
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ):
        hollow(
            FusionBody(self.name).component, FusionBody(self.name).instance, thickness_x
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def thicken(self, radius: "str|float|Dimension"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def hole(
        self,
        hole_landmark: "str|LandmarkInterface",
        radius: "str|float|Dimension",
        depth: "str|float|Dimension",
        normal_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "str|float|Angle" = 0.0,
        initial_rotation_y: "str|float|Angle" = 0.0,
        initial_rotation_z: "str|float|Angle" = 0.0,
        mirror_about_entity_or_landmark: "EntityInterface| None" = None,
        mirror_axis: "str|int|Axis" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "str|float|Angle" = 0.0,
        circular_pattern_instance_axis: "str|int|Axis" = "z",
        circular_pattern_about_entity_or_landmark: "EntityInterface| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern_instance_axis: "str|int|Axis" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern2nd_instance_axis: "str|int|Axis" = "y",
    ):
        fusion_entity = FusionBody(self.name)
        if isinstance(hole_landmark, str):
            component = get_component(hole_landmark)
            if get_body(component, hole_landmark):
                fusion_entity = FusionBody(hole_landmark)
            else:
                fusion_entity = FusionSketch(hole_landmark)
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        depth = Dimension.from_dimension_or_its_float_or_string_value(depth, None)
        hole(
            FusionBody(self.name).component,
            FusionBody(self.name).instance,
            fusion_entity.center,
            radius.value,
            depth.value,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        print("twist called:", angle, screw_pitch, iterations, axis)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_material(self, material: "MaterialInterface"):
        set_material(FusionBody(self.name), material_name)
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def is_colliding_with_part(self, other_part: "PartInterface") -> bool:
        print("is_colliding_with_part called:", other_part)
        return True

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        fillet_all_edges(
            FusionBody(self.name).component,
            FusionBody(self.name).instance,
            radius.value,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def fillet_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def chamfer_all_edges(self, radius: "str|float|Dimension"):
        radius = Dimension.from_dimension_or_its_float_or_string_value(radius, None)
        chamfer_all_edges(
            FusionBody(self.name).component,
            FusionBody(self.name).instance,
            radius.value,
        )
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def chamfer_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
    ):
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def chamfer_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
    ):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def select_vertex_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def select_edge_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def select_face_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

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

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def create_text(
        text: "str",
        extrude_amount: "str|float|Dimension",
        font_size: "str|float|Dimension" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
        profile_curve: "WireInterface|SketchInterface| None" = None,
        name: "str| None" = None,
        description: "str| None" = None,
    ) -> Self:
        print(
            "create_text called",
            f": {text}, {extrude_amount}, {font_size}, {bold}, {italic}, {underlined}, {character_spacing}, {word_spacing}, {line_spacing}, {font_file_path}, {profile_curve}, {options}",
        )
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def get_by_name(name: "str") -> "PartInterface":
        print("get_by_name called", f": {name}")
        return Part("a part")
