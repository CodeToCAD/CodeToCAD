from typing import Optional

from codetocad.interfaces import PartInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *

from . import blender_actions, blender_definitions, implementables, Entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Joint  # noqa: F401


class Part(Entity, PartInterface):
    def create_from_file(self, file_path: str, file_type: Optional[str] = None):
        assert self.is_exists() is False, f"{self.name} already exists."

        absoluteFilePath = get_absolute_filepath(file_path)

        importedFileName = blender_actions.import_file(absoluteFilePath, file_type)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != importedFileName:
            from . import Part  # noqa: F811

            Part(importedFileName).rename(self.name)

        return self

    def create_cube(
        self,
        width: DimensionOrItsFloatOrStringValue,
        length: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        cube_sketch = Sketch(self.name)
        cube_sketch.create_rectangle(length, width)
        cube_sketch.extrude(height)

        return self

    def create_cone(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        draft_radius: DimensionOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch, Wire

        base = Sketch(self.name).create_circle(radius)

        top = Sketch(self.name + "_temp_top")
        top_wire: Wire
        if draft_radius == Dimension(0):
            top_wire = top.create_from_vertices([(0, 0, 0)])
        else:
            top_wire = top.create_circle(draft_radius)
        top.translate_z(height)

        base.loft(top_wire)

        return self

    def create_cylinder(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        sketch = Sketch(self.name)
        sketch.create_circle(radius)
        sketch.extrude(height)

        return self

    def create_torus(
        self,
        inner_radius: DimensionOrItsFloatOrStringValue,
        outer_radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        inner_radius = Dimension.from_dimension_or_its_float_or_string_value(
            inner_radius
        )
        outer_radius = Dimension.from_dimension_or_its_float_or_string_value(
            outer_radius
        )

        circle_radius = outer_radius - inner_radius

        origin = Sketch(self.name + "_temp_origin")
        origin.create_from_vertices([(0, 0, 0)])

        sketch = Sketch(self.name)
        sketch.create_circle(circle_radius)
        sketch.rotate_x(90)
        sketch.translate_x(inner_radius + outer_radius / 2)
        sketch.revolve(360, origin, "z")

        origin.delete()

    def create_sphere(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        keyword_arguments: Optional[dict] = None,
    ):
        from . import Sketch

        sketch = Sketch(self.name)
        sketch.create_circle(radius)
        sketch.revolve(360, sketch.get_landmark("center"), "x")

        return self

    def create_gear(
        self,
        outer_radius: DimensionOrItsFloatOrStringValue,
        addendum: DimensionOrItsFloatOrStringValue,
        inner_radius: DimensionOrItsFloatOrStringValue,
        dedendum: DimensionOrItsFloatOrStringValue,
        height: DimensionOrItsFloatOrStringValue,
        pressure_angle: AngleOrItsFloatOrStringValue = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: AngleOrItsFloatOrStringValue = 0,
        conical_angle: AngleOrItsFloatOrStringValue = 0,
        crown_angle: AngleOrItsFloatOrStringValue = 0,
        keyword_arguments: Optional[dict] = None,
    ):
        blender_actions.create_gear(
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
        Part("Gear").rename(self.name, True)

        return self

    def clone(self, new_name: str, copy_landmarks: bool = True) -> "PartInterface":
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."

        blender_actions.duplicate_object(self.name, new_name, copy_landmarks)

        return Part(new_name, self.description)

    def union(
        self,
        with_part: PartOrItsName,
        delete_after_union: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        assert self.is_colliding_with_part(partName) == True, "Parts must be colliding to be unioned."

        blender_actions.apply_boolean_modifier(
            self.name, blender_definitions.BlenderBooleanTypes.UNION, partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        materials = blender_actions.material.get_materials(partName)
        for material in materials:
            blender_actions.set_material_to_object(material.name, self.name, is_union=True)

        self._apply_modifiers_only()

        if delete_after_union:
            blender_actions.remove_object(partName, remove_children=True)

        return self

    def subtract(
        self,
        with_part: PartOrItsName,
        delete_after_subtract: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        assert self.is_colliding_with_part(partName) == True, "Parts must be colliding to be subtracted."

        blender_actions.apply_boolean_modifier(
            self.name, blender_definitions.BlenderBooleanTypes.DIFFERENCE, partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        self._apply_modifiers_only()

        if delete_after_subtract:
            blender_actions.remove_object(partName, remove_children=True)
        return self

    def intersect(
        self,
        with_part: PartOrItsName,
        delete_after_intersect: bool = True,
        is_transfer_landmarks: bool = False,
    ):
        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        assert self.is_colliding_with_part(partName) == True, "Parts must be colliding to be intersected."

        blender_actions.apply_boolean_modifier(
            self.name, blender_definitions.BlenderBooleanTypes.INTERSECT, partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        self._apply_modifiers_only()

        if delete_after_intersect:
            blender_actions.remove_object(partName, remove_children=True)

        return self

    def hollow(
        self,
        thickness_x: DimensionOrItsFloatOrStringValue,
        thickness_y: DimensionOrItsFloatOrStringValue,
        thickness_z: DimensionOrItsFloatOrStringValue,
        start_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
    ):
        axis = Axis.from_string(start_axis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        start_landmark_location = [center, center, center]
        start_landmark_location[axis.value] = min if flip_axis else max

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
            for dimension in blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(
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

        blender_actions.scale_object(inside_part.name, scale_x, scale_y, scale_z)

        self._apply_rotation_and_scale_only()

        from . import Joint  # noqa: F811

        Joint(start_axis_landmark, inside_part_start).translate_landmark_onto_another()

        self.subtract(inside_part, is_transfer_landmarks=False)

        start_axis_landmark.delete()

        return self._apply_modifiers_only()

    def thicken(self, radius: DimensionOrItsFloatOrStringValue) -> "PartInterface":
        radius = Dimension.from_string(radius)

        blender_actions.apply_solidify_modifier(self.name, radius)

        return self._apply_modifiers_only()

    def hole(
        self,
        hole_landmark: LandmarkOrItsName,
        radius: DimensionOrItsFloatOrStringValue,
        depth: DimensionOrItsFloatOrStringValue,
        normal_axis: AxisOrItsIndexOrItsName = "z",
        flip_axis: bool = False,
        initial_rotation_x: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_y: AngleOrItsFloatOrStringValue = 0.0,
        initial_rotation_z: AngleOrItsFloatOrStringValue = 0.0,
        mirror_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        mirror_axis: AxisOrItsIndexOrItsName = "x",
        mirror: bool = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: AngleOrItsFloatOrStringValue = 0.0,
        circular_pattern_instance_axis: AxisOrItsIndexOrItsName = "z",
        circular_pattern_about_entity_or_landmark: Optional[EntityOrItsName] = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern_instance_axis: AxisOrItsIndexOrItsName = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: DimensionOrItsFloatOrStringValue = 0.0,
        linear_pattern2nd_instance_axis: AxisOrItsIndexOrItsName = "y",
    ):
        axis = Axis.from_string(normal_axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        hole = Part(create_uuid_like_id()).create_cylinder(radius, depth)
        hole_head = hole.create_landmark(
            "hole", center, center, min if flip_axis else max
        )

        axisRotation = Angle(-90, AngleUnit.DEGREES)

        if axis is Axis.X:
            initial_rotation_y = (axisRotation + initial_rotation_y).value
        elif axis is Axis.Y:
            initial_rotation_x = (axisRotation + initial_rotation_x).value
        hole.rotate_xyz(initial_rotation_x, initial_rotation_y, initial_rotation_z)

        from . import Joint  # noqa: F811

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
                resulting_mirrored_entity_name=None,
            )

        self.subtract(hole, delete_after_subtract=True, is_transfer_landmarks=False)
        return self._apply_modifiers_only()

    def set_material(self, material_name: MaterialOrItsName):
        material = material_name

        if isinstance(material, str) or isinstance(material, PresetMaterial):
            from . import Material

            material = Material.get_preset(material)

        material.assign_to_part(self.name)
        return self

    def is_colliding_with_part(self, other_part: PartOrItsName):
        other_partName = other_part
        if isinstance(other_partName, PartInterface):
            other_partName = other_partName.name

        if other_partName == self.name:
            raise NameError("Collision must be checked between different Parts.")

        return blender_actions.is_collision_between_two_objects(
            self.name, other_partName
        )

    def fillet_all_edges(
        self, radius: DimensionOrItsFloatOrStringValue, use_width: bool = False
    ):
        return self.bevel(radius, chamfer=False, use_width=use_width)

    def fillet_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        return self.bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=False,
            use_width=use_width,
        )

    def fillet_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
        use_width: bool = False,
    ):
        return self.bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=False,
            use_width=use_width,
        )

    def chamfer_all_edges(self, radius: DimensionOrItsFloatOrStringValue):
        return self.bevel(radius, chamfer=True, use_width=False)

    def chamfer_edges(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_edges: list[LandmarkOrItsName],
    ):
        return self.bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=True,
            use_width=False,
        )

    def chamfer_faces(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        landmarks_near_faces: list[LandmarkOrItsName],
    ):
        return self.bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=True,
            use_width=False,
        )

    def _add_edges_near_landmarks_to_vertex_group(
        self, bevel_edges_nearlandmark_names: list[LandmarkOrItsName], vertex_group_name
    ):
        kdTree = blender_actions.create_kd_tree_for_object(self.name)
        vertexGroupObject = blender_actions.create_object_vertex_group(
            self.name, vertex_group_name
        )

        for landmarkOrItsName in bevel_edges_nearlandmark_names:
            landmark = (
                self.get_landmark(landmarkOrItsName)
                if isinstance(landmarkOrItsName, str)
                else landmarkOrItsName
            )
            vertexIndecies = [
                index
                for (_, index, _) in blender_actions.get_closest_points_to_vertex(
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

            blender_actions.add_verticies_to_vertex_group(
                vertexGroupObject, vertexIndecies
            )

    def _add_faces_near_landmarks_to_vertex_group(
        self, bevel_faces_nearlandmark_names: list[LandmarkOrItsName], vertex_group_name
    ):
        vertexGroupObject = blender_actions.create_object_vertex_group(
            self.name, vertex_group_name
        )

        for landmarkOrItsName in bevel_faces_nearlandmark_names:
            landmark = (
                self.get_landmark(landmarkOrItsName)
                if isinstance(landmarkOrItsName, str)
                else landmarkOrItsName
            )

            blenderPolygon = blender_actions.get_closest_face_to_vertex(
                self.name,
                [
                    dimension.value
                    for dimension in landmark.get_location_world().to_list()
                ],
            )

            faceIndecies: list[int] = blenderPolygon.vertices

            blender_actions.add_verticies_to_vertex_group(
                vertexGroupObject, faceIndecies
            )

    def bevel(
        self,
        radius: DimensionOrItsFloatOrStringValue,
        bevel_edges_nearlandmark_names: Optional[list[LandmarkOrItsName]] = None,
        bevel_faces_nearlandmark_names: Optional[list[LandmarkOrItsName]] = None,
        use_width=False,
        chamfer=False,
        keyword_arguments: Optional[dict] = None,
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

        radiusDimension = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                radiusDimension
            )
        )

        blender_actions.apply_bevel_modifier(
            self.name,
            radiusDimension,
            vertex_group_name=vertex_group_name,
            use_edges=True,
            use_width=use_width,
            chamfer=chamfer,
            **(keyword_arguments or {}),
        )

        return self._apply_modifiers_only()

    def select_vertex_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        raise NotImplementedError()
        return self

    def select_edge_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        raise NotImplementedError()
        return self

    def select_face_near_landmark(
        self, landmark_name: Optional[LandmarkOrItsName] = None
    ):
        raise NotImplementedError()
        return self

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        iterations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.twist(self, angle, screw_pitch, iterations, axis)
        return self

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str] = None,
    ):
        implementables.mirror(
            self, mirror_across_entity, axis, resulting_mirrored_entity_name
        )
        return self

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.linear_pattern(self, instance_count, offset, direction_axis)
        return self

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        implementables.circular_pattern(
            self,
            instance_count,
            separation_angle,
            center_entity_or_landmark,
            normal_direction_axis,
        )
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        implementables.export(self, file_path, overwrite, scale)
        return self

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        implementables.scale_xyz(self, x, y, z)
        return self

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_x(self, scale)
        return self

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_y(self, scale)
        return self

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        implementables.scale_z(self, scale)
        return self

    def scale_x_by_factor(self, scale_factor: float):
        implementables.scale_x_by_factor(self, scale_factor)
        return self

    def scale_y_by_factor(self, scale_factor: float):
        implementables.scale_y_by_factor(self, scale_factor)
        return self

    def scale_z_by_factor(self, scale_factor: float):
        implementables.scale_z_by_factor(self, scale_factor)
        return self

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        implementables.scale_keep_aspect_ratio(self, scale, axis)
        return self

    def remesh(self, strategy: str, amount: float):
        implementables.remesh(self, strategy, amount)
        return self

    def subdivide(self, amount: float):
        raise NotImplementedError()
        return self

    def decimate(self, amount: float):
        raise NotImplementedError()
        return self
