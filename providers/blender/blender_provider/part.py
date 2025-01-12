from codetocad.interfaces.part_interface import PartInterface
from codetocad.proxy.sketch import Sketch
from typing import Self
from codetocad.interfaces.sketch_interface import SketchInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.booleanable_interface import BooleanableInterface
from codetocad.interfaces.wire_interface import WireInterface
from codetocad.proxy.material import Material
from codetocad.utilities import create_uuid_like_id, get_absolute_filepath
from codetocad.interfaces.material_interface import MaterialInterface
from codetocad.interfaces.entity_interface import EntityInterface
from codetocad.interfaces.landmark_interface import LandmarkInterface
from providers.blender.blender_provider.blender_definitions import (
    BlenderBooleanTypes,
    BlenderLength,
)
from providers.blender.blender_provider.joint import Joint
from providers.blender.blender_provider.entity import Entity
from codetocad.codetocad_types import *
import providers.blender.blender_provider.implementables as implementables
from providers.blender.blender_provider.blender_actions.import_export import import_file
from providers.blender.blender_provider.blender_actions.material import (
    get_materials,
    set_material_to_object,
)
from providers.blender.blender_provider.blender_actions.mesh import (
    create_kd_tree_for_object,
    get_closest_face_to_vertex,
    get_closest_points_to_vertex,
    is_collision_between_two_objects,
)
from providers.blender.blender_provider.blender_actions.modifiers import (
    apply_bevel_modifier,
    apply_boolean_modifier,
    apply_solidify_modifier,
)
from providers.blender.blender_provider.blender_actions.objects import (
    add_verticies_to_vertex_group,
    create_gear,
    create_object_vertex_group,
    remove_object,
)
from providers.blender.blender_provider.blender_actions.objects_transmute import (
    transfer_landmarks,
    duplicate_object,
)
from providers.blender.blender_provider.blender_actions.transformations import (
    scale_object,
)
from providers.blender.blender_provider.sketch import Sketch


class Part(PartInterface, Entity):

    def __init__(
        self,
        name: "str| None" = None,
        description: "str| None" = None,
        native_instance=None,
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @supported(SupportLevel.PARTIAL, "Only stl, ply, obj types are supported.")
    def create_from_file(self, file_path: "str", file_type: "str| None" = None):
        assert self.is_exists() is False, f"{self.name} already exists."
        absoluteFilePath = get_absolute_filepath(file_path)
        importedFileName = import_file(absoluteFilePath, file_type)
        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != importedFileName:
            Part(importedFileName).set_name(self.name)
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_cube(
        self,
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
    ):
        return (
            Sketch(self.name)
            .create_rectangle(length, width)
            .extrude(height)
            .set_name(self.name)
        )

    @supported(
        SupportLevel.PARTIAL,
        "Only cones with a draft_radius > 0 can be created at the moment. Options is not implemented.",
    )
    def create_cone(
        self,
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
    ):
        base_sketch = Sketch(self.name)
        base = base_sketch.create_circle(radius)
        top = Sketch(self.name + "_temp_top")
        top_wire: WireInterface
        if draft_radius == Dimension(0):
            # top_wire = top.create_from_vertices([(0, 0, 0)])
            # This is temporary until the bug of lofting to a single vertex is fixed:
            top_wire = top.create_circle(0.0001)
        else:
            top_wire = top.create_circle(draft_radius)
        top_wire.translate_z(height)
        new_part = base.loft(top_wire, self.name)
        top.delete()
        return new_part

    @supported(SupportLevel.SUPPORTED)
    def create_cylinder(
        self, radius: "str|float|Dimension", height: "str|float|Dimension"
    ):
        return (
            Sketch(self.name).create_circle(radius).extrude(height).set_name(self.name)
        )

    @supported(SupportLevel.SUPPORTED)
    def create_torus(
        self, inner_radius: "str|float|Dimension", outer_radius: "str|float|Dimension"
    ):
        inner_radius = Dimension.from_dimension_or_its_float_or_string_value(
            inner_radius
        )
        outer_radius = Dimension.from_dimension_or_its_float_or_string_value(
            outer_radius
        )
        inner_radius = BlenderLength.convert_dimension_to_blender_unit(inner_radius)
        outer_radius = BlenderLength.convert_dimension_to_blender_unit(outer_radius)
        circle_radius = (outer_radius - inner_radius) / 2
        origin = Sketch(self.name + "_temp_origin")
        origin.create_from_vertices([(0, 0, 0)])
        sketch = Sketch(self.name)
        circle = sketch.create_circle(circle_radius)
        sketch.rotate_x(90)
        sketch.translate_x(inner_radius + circle_radius)
        new_part = circle.revolve(360, origin, "z")
        origin.delete()
        return new_part

    @supported(SupportLevel.SUPPORTED)
    def create_sphere(self, radius: "str|float|Dimension"):
        sketch = Sketch(self.name)
        circle = sketch.create_circle(radius)
        new_part = circle.revolve(180, sketch.get_landmark("center"), "x")
        return new_part.set_name(self.name)

    @supported(SupportLevel.SUPPORTED)
    def create_gear(
        self,
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
    ):
        create_gear(
            self.name,
            outer_radius,
            addendum,
            inner_radius,
            dedendum,
            height,
            pressure_angle,
            number_of_teeth,
            skew_angle,
            conical_angle,
            crown_angle,
        )
        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part("Gear").set_name(self.name, True)
        return self

    @supported(SupportLevel.SUPPORTED)
    def clone(
        self, new_name: "str| None" = None, copy_landmarks: "bool| None" = True
    ) -> "PartInterface":
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."
        duplicate_object(self.name, new_name, copy_landmarks)
        return Part(new_name, self.description)

    @supported(SupportLevel.SUPPORTED)
    def union(
        self,
        other: "BooleanableInterface",
        delete_after_union: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        part_name = other
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        # TODO: add a flag for collision detection
        # assert (
        #     self.is_colliding_with_part(part_name) is True
        # ), "Parts must be colliding to be unioned."
        apply_boolean_modifier(self.name, BlenderBooleanTypes.UNION, part_name)
        if is_transfer_data:
            transfer_landmarks(part_name, self.name)
        materials = get_materials(part_name)
        for material in materials:
            set_material_to_object(material.name, self.name, is_union=True)
        self._apply_modifiers_only()
        if delete_after_union:
            remove_object(part_name, remove_children=True)
        return self

    @supported(SupportLevel.SUPPORTED)
    def subtract(
        self,
        other: "BooleanableInterface",
        delete_after_subtract: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        part_name = other
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        assert (
            self.is_colliding_with_part(part_name) is True
        ), "Parts must be colliding to be subtracted."
        apply_boolean_modifier(self.name, BlenderBooleanTypes.DIFFERENCE, part_name)
        if is_transfer_data:
            transfer_landmarks(part_name, self.name)
        self._apply_modifiers_only()
        if delete_after_subtract:
            remove_object(part_name, remove_children=True)
        return self

    @supported(SupportLevel.SUPPORTED)
    def intersect(
        self,
        other: "BooleanableInterface",
        delete_after_intersect: "bool" = True,
        is_transfer_data: "bool" = False,
    ):
        part_name = other
        if isinstance(part_name, EntityInterface):
            part_name = part_name.name
        assert (
            self.is_colliding_with_part(part_name) is True
        ), "Parts must be colliding to be intersected."
        apply_boolean_modifier(self.name, BlenderBooleanTypes.INTERSECT, part_name)
        if is_transfer_data:
            transfer_landmarks(part_name, self.name)
        self._apply_modifiers_only()
        if delete_after_intersect:
            remove_object(part_name, remove_children=True)
        return self

    @supported(
        SupportLevel.PARTIAL,
        "This implementation works with simple geometry like cubes and cylinders. This implementation fails when working with geometry that has splines or curves in one or more edges.",
    )
    def hollow(
        self,
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ):
        axis = Axis.from_string(start_axis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"
        start_landmark_location = ["center", "center", "center"]
        start_landmark_location[axis.value] = "min" if flip_axis else "max"
        start_axis_landmark = self.create_landmark(
            create_uuid_like_id(),
            start_landmark_location[0],
            start_landmark_location[1],
            start_landmark_location[2],
        )
        inside_part = self.clone(create_uuid_like_id(), copy_landmarks=False)
        inside_part_start = inside_part.create_landmark(
            "start",
            start_landmark_location[0],
            start_landmark_location[1],
            start_landmark_location[2],
        )
        thickness_xyz: list[Dimension] = [
            dimension
            for dimension in BlenderLength.convert_dimensions_to_blender_unit(
                [
                    Dimension.from_string(thickness_x),
                    Dimension.from_string(thickness_y),
                    Dimension.from_string(thickness_z),
                ]
            )
        ]
        dimensions = self.get_dimensions()
        current_dimension_x: Dimension = dimensions[0]  # type:ignore
        current_dimension_y: Dimension = dimensions[1]  # type:ignore
        current_dimension_z: Dimension = dimensions[2]  # type:ignore

        def scaleValue(
            main_dimension: float, thickness: float, subtract_both_sides: bool
        ) -> float:
            return (
                main_dimension - thickness * (2 if subtract_both_sides else 1)
            ) / main_dimension

        scale_x: float = scaleValue(
            current_dimension_x.value, thickness_xyz[0].value, axis.value == 0
        )
        scale_y = scaleValue(
            current_dimension_y.value, thickness_xyz[1].value, axis.value == 1
        )
        scale_z = scaleValue(
            current_dimension_z.value, thickness_xyz[2].value, axis.value == 2
        )
        scale_object(inside_part.name, scale_x, scale_y, scale_z)
        self._apply_rotation_and_scale_only()
        Joint(start_axis_landmark, inside_part_start).translate_landmark_onto_another()
        self.subtract(inside_part, is_transfer_data=False)
        start_axis_landmark.delete()
        return self._apply_modifiers_only()

    @supported(SupportLevel.SUPPORTED)
    def thicken(self, radius: "str|float|Dimension") -> "PartInterface":
        radius = Dimension.from_string(radius)
        apply_solidify_modifier(self.name, radius)
        return self._apply_modifiers_only()

    @supported(SupportLevel.SUPPORTED)
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
        axis = Axis.from_string(normal_axis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"
        hole = Part(create_uuid_like_id()).create_cylinder(radius, depth)
        hole_head = hole.create_landmark(
            "hole", "center", "center", "min" if flip_axis else "max"
        )
        axisRotation = Angle(-90, AngleUnit.DEGREES)
        if axis is Axis.X:
            initial_rotation_y = (axisRotation + initial_rotation_y).value
        elif axis is Axis.Y:
            initial_rotation_x = (axisRotation + initial_rotation_x).value
        hole.rotate_xyz(initial_rotation_x, initial_rotation_y, initial_rotation_z)
        Joint(hole_landmark, hole_head).limit_location_x(0, 0)
        Joint(hole_landmark, hole_head).limit_location_y(0, 0)
        Joint(hole_landmark, hole_head).limit_location_z(0, 0)
        if circular_pattern_instance_count > 1:
            circular_pattern_about_entity_or_landmark = (
                circular_pattern_about_entity_or_landmark or self
            )
            instanceSeparation = (
                360.0 / float(circular_pattern_instance_count)
                if circular_pattern_instance_separation == 0
                else circular_pattern_instance_separation
            )
            hole.circular_pattern(
                circular_pattern_instance_count,
                instanceSeparation,
                circular_pattern_about_entity_or_landmark,
                circular_pattern_instance_axis,
            )
        if linear_pattern_instance_count > 1:
            hole.linear_pattern(
                linear_pattern_instance_count,
                linear_pattern_instance_separation,
                linear_pattern_instance_axis,
            )
        if linear_pattern2nd_instance_count > 1:
            hole.linear_pattern(
                linear_pattern2nd_instance_count,
                linear_pattern2nd_instance_separation,
                linear_pattern2nd_instance_axis,
            )
        if mirror and mirror_about_entity_or_landmark:
            hole.mirror(
                mirror_about_entity_or_landmark,
                mirror_axis,
                separate_resulting_entity=None,
            )
        self.subtract(hole, delete_after_subtract=True, is_transfer_data=False)
        return self._apply_modifiers_only()

    @supported(SupportLevel.SUPPORTED)
    def set_material(self, material: "MaterialInterface"):
        if isinstance(material_name, MaterialInterface):
            material_name = material_name.name
        elif (
            isinstance(material_name, str)
            and material_name in PresetMaterial
            or isinstance(material_name, PresetMaterial)
        ):
            preset_mat = material_name
            if isinstance(preset_mat, str):
                preset_mat = PresetMaterial(preset_mat)
            material_name = Material.get_preset(preset_mat).name
        set_material_to_object(material_name, self.name)
        return self

    @supported(SupportLevel.SUPPORTED)
    def is_colliding_with_part(self, other_part: "PartInterface"):
        other_part_name = other_part
        if isinstance(other_part_name, PartInterface):
            other_part_name = other_part_name.name
        if other_part_name == self.name:
            raise NameError("Collision must be checked between different Parts.")
        return is_collision_between_two_objects(self.name, other_part_name)

    def _bevel(
        self,
        radius: str | float | Dimension,
        bevel_edges_nearlandmark_names: list[str | LandmarkInterface] | None = None,
        bevel_faces_nearlandmark_names: list[str | LandmarkInterface] | None = None,
        use_width=False,
        chamfer=False,
        keyword_arguments: dict | None = None,
    ):
        vertex_group_name = None
        if bevel_edges_nearlandmark_names is not None:
            vertex_group_name = create_uuid_like_id()
            self._add_edges_near_landmarks_to_vertex_group(
                bevel_edges_nearlandmark_names, vertex_group_name
            )
        if bevel_faces_nearlandmark_names is not None:
            vertex_group_name = vertex_group_name or create_uuid_like_id()
            self._add_faces_near_landmarks_to_vertex_group(
                bevel_faces_nearlandmark_names, vertex_group_name
            )
        radiusDimension = Dimension.from_string(radius)
        radiusDimension = BlenderLength.convert_dimension_to_blender_unit(
            radiusDimension
        )
        apply_bevel_modifier(
            self.name,
            radiusDimension,
            vertex_group_name=vertex_group_name,
            use_edges=True,
            use_width=use_width,
            chamfer=chamfer,
            **keyword_arguments or {},
        )
        return self._apply_modifiers_only()

    @supported(SupportLevel.SUPPORTED)
    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ):
        return self._bevel(radius, chamfer=False, use_width=use_width)

    @supported(SupportLevel.SUPPORTED)
    def fillet_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):
        return self._bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=False,
            use_width=use_width,
        )

    @supported(SupportLevel.SUPPORTED)
    def fillet_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ):
        return self._bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=False,
            use_width=use_width,
        )

    @supported(SupportLevel.SUPPORTED)
    def chamfer_all_edges(self, radius: "str|float|Dimension"):
        return self._bevel(radius, chamfer=True, use_width=False)

    @supported(SupportLevel.SUPPORTED)
    def chamfer_edges(
        self,
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
    ):
        return self._bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=True,
            use_width=False,
        )

    @supported(SupportLevel.SUPPORTED)
    def chamfer_faces(
        self,
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
    ):
        return self._bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=True,
            use_width=False,
        )

    def _add_edges_near_landmarks_to_vertex_group(
        self,
        bevel_edges_nearlandmark_names: list[str | LandmarkInterface],
        vertex_group_name,
    ):
        kdTree = create_kd_tree_for_object(self.name)
        vertexGroupObject = create_object_vertex_group(self.name, vertex_group_name)
        for landmarkOrItsName in bevel_edges_nearlandmark_names:
            landmark = (
                self.get_landmark(landmarkOrItsName)
                if isinstance(landmarkOrItsName, str)
                else landmarkOrItsName
            )
            vertexIndecies = [
                index
                for _, index, _ in get_closest_points_to_vertex(
                    self.name,
                    [
                        dimension.value
                        for dimension in landmark.get_location_world().to_list()
                    ],
                    number_of_points=2,
                    object_kd_tree=kdTree,
                )
            ]
            assert (
                len(vertexIndecies) == 2
            ), f"Could not find edges near landmark {landmark.get_landmark_entity_name()}"
            add_verticies_to_vertex_group(vertexGroupObject, vertexIndecies)

    def _add_faces_near_landmarks_to_vertex_group(
        self,
        bevel_faces_nearlandmark_names: list[str | LandmarkInterface],
        vertex_group_name,
    ):
        vertex_group_object = create_object_vertex_group(
            self.get_native_instance(), vertex_group_name
        )
        for landmark_or_its_name in bevel_faces_nearlandmark_names:
            landmark = (
                self.get_landmark(landmark_or_its_name)
                if isinstance(landmark_or_its_name, str)
                else landmark_or_its_name
            )
            blender_polygon = get_closest_face_to_vertex(
                self.name,
                [
                    dimension.value
                    for dimension in landmark.get_location_world().to_list()
                ],
            )
            face_indecies: list[int] = blender_polygon.vertices
            add_verticies_to_vertex_group(vertex_group_object, face_indecies)

    @supported(SupportLevel.SUPPORTED)
    def select_vertex_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def select_edge_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def select_face_near_landmark(self, landmark: "LandmarkInterface| None" = None):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ):
        implementables.twist(self, angle, screw_pitch, iterations, axis)
        return self

    @supported(SupportLevel.SUPPORTED)
    def mirror(
        self,
        mirror_across_entity: "EntityInterface",
        axis: "str|int|Axis",
        separate_resulting_entity: "bool| None" = False,
    ):
        implementables.mirror(
            self, mirror_across_entity, axis, separate_resulting_entity
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def linear_pattern(
        self,
        instance_count: "int",
        offset: "str|float|Dimension",
        direction_axis: "str|int|Axis" = "z",
    ):
        implementables.linear_pattern(self, instance_count, offset, direction_axis)
        return self

    @supported(SupportLevel.SUPPORTED)
    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: "str|float|Angle",
        center_entity_or_landmark: "EntityInterface",
        normal_direction_axis: "str|int|Axis" = "z",
    ):
        implementables.circular_pattern(
            self,
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    @supported(SupportLevel.SUPPORTED)
    def export(self, file_path: "str", overwrite: "bool" = True, scale: "float" = 1.0):
        implementables.export(self, file_path, overwrite, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_xyz(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
    ):
        implementables.scale_xyz(self, x, y, z)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_x(self, scale: "str|float|Dimension"):
        implementables.scale_x(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_y(self, scale: "str|float|Dimension"):
        implementables.scale_y(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_z(self, scale: "str|float|Dimension"):
        implementables.scale_z(self, scale)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_x_by_factor(self, scale_factor: "float"):
        implementables.scale_x_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_y_by_factor(self, scale_factor: "float"):
        implementables.scale_y_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_z_by_factor(self, scale_factor: "float"):
        implementables.scale_z_by_factor(self, scale_factor)
        return self

    @supported(SupportLevel.SUPPORTED)
    def scale_keep_aspect_ratio(
        self, scale: "str|float|Dimension", axis: "str|int|Axis"
    ):
        implementables.scale_keep_aspect_ratio(self, scale, axis)
        return self

    @supported(
        SupportLevel.PARTIAL,
        "The strategy parameter will probably be broken down into remesh_[strategy] methods in the future.",
    )
    def remesh(self, strategy: "str", amount: "float"):
        implementables.remesh(self, strategy, amount)
        return self

    @supported(SupportLevel.PLANNED)
    def subdivide(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.PLANNED)
    def decimate(self, amount: "float"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.SUPPORTED)
    def create_landmark(
        self,
        x: "str|float|Dimension",
        y: "str|float|Dimension",
        z: "str|float|Dimension",
        landmark_name: "str| None" = None,
    ) -> "LandmarkInterface":
        return implementables.create_landmark(
            self, landmark_name=landmark_name, x=x, y=y, z=z
        )

    @supported(SupportLevel.SUPPORTED)
    def get_landmark(self, landmark_name: "str|PresetLandmark") -> "LandmarkInterface":
        return implementables.get_landmark(self, landmark_name)

    @supported(SupportLevel.SUPPORTED, notes="")
    def create_text(
        self,
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
    ) -> Self:
        sketch = Sketch(self.name + "_" + create_uuid_like_id()).create_text(
            text=text,
            font_size=font_size,
            bold=bold,
            italic=italic,
            underlined=underlined,
            character_spacing=character_spacing,
            word_spacing=word_spacing,
            line_spacing=line_spacing,
            font_file_path=font_file_path,
            profile_curve=profile_curve,
        )
        wires = sketch.get_wires()
        part = wires[0].extrude(extrude_amount)
        for wireIndex in range(1, len(wires)):
            part.union(wires[wireIndex].extrude(extrude_amount))
        part.set_name(self.name)
        sketch.delete()
        return self
