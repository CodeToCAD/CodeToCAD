from typing import Optional
from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import PartInterface, LandmarkInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .material import Material
from .entity import Entity
from .joint import Joint


class Part(Entity, PartInterface):

    def _create_primitive(self, primitive_name: str, dimensions: str, **kwargs
                          ):

        assert self.is_exists() is False, f"{self.name} already exists."

        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType: blender_definitions.BlenderObjectPrimitiveTypes = getattr(
            blender_definitions.BlenderObjectPrimitiveTypes, primitive_name.lower())
        expectedNameOfObjectInBlender = primitiveType.default_name_in_blender(
        ) if primitiveType else None

        assert expectedNameOfObjectInBlender is not None, \
            f"Primitive type with name {primitive_name} is not supported."

        blender_actions.add_primitive(
            primitiveType, dimensions, **kwargs)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != expectedNameOfObjectInBlender:
            Part(expectedNameOfObjectInBlender).rename(
                self.name, primitiveType.has_data())

        return self

    def create_cube(self, width: DimensionOrItsFloatOrStringValue, length: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keyword_arguments: Optional[dict] = None
                    ):
        return self._create_primitive("cube", "{},{},{}".format(width, length, height), **(keyword_arguments or {}))

    def create_cone(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, draft_radius: DimensionOrItsFloatOrStringValue = 0, keyword_arguments: Optional[dict] = None
                    ):
        return self._create_primitive("cone", "{},{},{}".format(radius, draft_radius, height), **(keyword_arguments or {}))

    def create_cylinder(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keyword_arguments: Optional[dict] = None
                        ):
        return self._create_primitive("cylinder", "{},{}".format(radius, height), **(keyword_arguments or {}))

    def create_torus(self, inner_radius: DimensionOrItsFloatOrStringValue, outer_radius: DimensionOrItsFloatOrStringValue, keyword_arguments: Optional[dict] = None
                     ):
        return self._create_primitive("torus", "{},{}".format(inner_radius, outer_radius), **(keyword_arguments or {}))

    def create_sphere(self, radius: DimensionOrItsFloatOrStringValue, keyword_arguments: Optional[dict] = None
                      ):
        return self._create_primitive("uvsphere", "{}".format(radius), **(keyword_arguments or {}))

    def create_gear(self, outer_radius: DimensionOrItsFloatOrStringValue, addendum: DimensionOrItsFloatOrStringValue, inner_radius: DimensionOrItsFloatOrStringValue, dedendum: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, pressure_angle: AngleOrItsFloatOrStringValue = "20d", number_of_teeth: 'int' = 12, skew_angle: AngleOrItsFloatOrStringValue = 0, conical_angle: AngleOrItsFloatOrStringValue = 0, crown_angle: AngleOrItsFloatOrStringValue = 0, keyword_arguments: Optional[dict] = None
                    ):
        blender_actions.create_gear(
            self.name, outer_radius, addendum, inner_radius, dedendum, height, pressure_angle, number_of_teeth, skew_angle, conical_angle, crown_angle
        )

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part("Gear").rename(self.name, True)

        return self

    def clone(self, new_name: str, copy_landmarks: bool = True
              ) -> 'PartInterface':

        assert Entity(
            new_name).is_exists() is False, f"{new_name} already exists."

        blender_actions.duplicate_object(self.name, new_name, copy_landmarks)

        return Part(new_name, self.description)

    def loft(self, landmark1: 'LandmarkInterface', landmark2: 'LandmarkInterface'
             ):
        raise NotImplementedError()
        return self

    def union(self, with_part: PartOrItsName, delete_after_union: bool = True, is_transfer_landmarks: bool = False
              ):
        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        blender_actions.apply_boolean_modifier(
            self.name,
            blender_definitions.BlenderBooleanTypes.UNION,
            partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        self._apply_modifiers_only()

        if delete_after_union:
            blender_actions.remove_object(partName, remove_children=True)

        return self

    def subtract(self, with_part: PartOrItsName, delete_after_subtract: bool = True, is_transfer_landmarks: bool = False
                 ):
        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        blender_actions.apply_boolean_modifier(
            self.name,
            blender_definitions.BlenderBooleanTypes.DIFFERENCE,
            partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        self._apply_modifiers_only()

        if delete_after_subtract:
            blender_actions.remove_object(partName, remove_children=True)
        return self

    def intersect(self, with_part: PartOrItsName, delete_after_intersect: bool = True, is_transfer_landmarks: bool = False
                  ):

        partName = with_part
        if isinstance(partName, EntityInterface):
            partName = partName.name

        blender_actions.apply_boolean_modifier(
            self.name,
            blender_definitions.BlenderBooleanTypes.INTERSECT,
            partName
        )

        if is_transfer_landmarks:
            blender_actions.transfer_landmarks(partName, self.name)

        self._apply_modifiers_only()

        if delete_after_intersect:
            blender_actions.remove_object(partName, remove_children=True)

        return self

    def hollow(self, thickness_x: DimensionOrItsFloatOrStringValue, thickness_y: DimensionOrItsFloatOrStringValue, thickness_z: DimensionOrItsFloatOrStringValue, start_axis: AxisOrItsIndexOrItsName = "z", flip_axis: bool = False
               ):

        axis = Axis.from_string(start_axis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        startLandmarkLocation = [center, center, center]
        startLandmarkLocation[axis.value] = min if flip_axis else max

        start_axisLandmark = self.create_landmark(
            create_uuid_like_id(), startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        insidePart = self.clone(create_uuid_like_id(), copy_landmarks=False)
        insidePart_start = insidePart.create_landmark(
            "start", startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        thickness_xYZ: list[Dimension] = [dimension for dimension in blender_definitions.BlenderLength.convert_dimensions_to_blender_unit([
            Dimension.from_string(thickness_x),
            Dimension.from_string(thickness_y),
            Dimension.from_string(thickness_z),
        ])]

        dimensions = self.get_dimensions()
        currentDimensionX: Dimension = dimensions[0]  # type:ignore
        currentDimensionY: Dimension = dimensions[1]  # type:ignore
        currentDimensionZ: Dimension = dimensions[2]  # type:ignore

        def scaleValue(mainDimension: float, thickness: float, subtractBothSides: bool) -> float:
            return (mainDimension-thickness * (2 if subtractBothSides else 1)) / mainDimension

        scale_x: float = scaleValue(
            currentDimensionX.value, thickness_xYZ[0].value, axis.value == 0)
        scale_y = scaleValue(
            currentDimensionY.value, thickness_xYZ[1].value, axis.value == 1)
        scale_z = scaleValue(
            currentDimensionZ.value, thickness_xYZ[2].value, axis.value == 2)

        blender_actions.scale_object(
            insidePart.name, scale_x, scale_y, scale_z)

        self._apply_rotation_and_scale_only()

        Joint(start_axisLandmark, insidePart_start).translate_landmark_onto_another()

        self.subtract(insidePart, is_transfer_landmarks=False)

        start_axisLandmark.delete()

        return self._apply_modifiers_only()

    def thicken(self, radius: DimensionOrItsFloatOrStringValue) -> 'PartInterface':

        radius = Dimension.from_string(radius)

        blender_actions.apply_solidify_modifier(
            self.name, radius)

        return self._apply_modifiers_only()

    def hole(self, hole_landmark: LandmarkOrItsName, radius: DimensionOrItsFloatOrStringValue, depth: DimensionOrItsFloatOrStringValue, normal_axis: AxisOrItsIndexOrItsName = "z", flip_axis: bool = False, initial_rotation_x: AngleOrItsFloatOrStringValue = 0.0, initial_rotation_y: AngleOrItsFloatOrStringValue = 0.0, initial_rotation_z: AngleOrItsFloatOrStringValue = 0.0, mirror_about_entity_or_landmark: Optional[EntityOrItsNameOrLandmark] = None, mirror_axis: AxisOrItsIndexOrItsName = "x", mirror: bool = False, circular_pattern_instance_count: 'int' = 1, circular_pattern_instance_separation: AngleOrItsFloatOrStringValue = 0.0, circular_pattern_instance_axis: AxisOrItsIndexOrItsName = "z", circular_pattern_about_entity_or_landmark: Optional[EntityOrItsNameOrLandmark] = None, linear_pattern_instance_count: 'int' = 1, linear_pattern_instance_separation: DimensionOrItsFloatOrStringValue = 0.0, linear_pattern_instance_axis: AxisOrItsIndexOrItsName = "x", linear_pattern2nd_instance_count: 'int' = 1, linear_pattern2nd_instance_separation: DimensionOrItsFloatOrStringValue = 0.0, linear_pattern2nd_instance_axis: AxisOrItsIndexOrItsName = "y"):

        axis = Axis.from_string(normal_axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        hole = Part(create_uuid_like_id()).create_cylinder(radius, depth)
        hole_head = hole.create_landmark(
            "hole", center, center, min if flip_axis else max)

        axisRotation = Angle(-90, AngleUnit.DEGREES)

        if axis is Axis.X:
            initial_rotation_y = (axisRotation+initial_rotation_y).value
        elif axis is Axis.Y:
            initial_rotation_x = (axisRotation+initial_rotation_x).value
        hole.rotate_xyz(initial_rotation_x,
                        initial_rotation_y, initial_rotation_z)

        Joint(hole_landmark, hole_head).limit_location_x(0, 0)
        Joint(hole_landmark, hole_head).limit_location_y(0, 0)
        Joint(hole_landmark, hole_head).limit_location_z(0, 0)

        if circular_pattern_instance_count > 1:
            circular_pattern_about_entity_or_landmark = circular_pattern_about_entity_or_landmark or self
            instanceSeparation = 360.0 / \
                float(
                    circular_pattern_instance_count) if circular_pattern_instance_separation == 0 else circular_pattern_instance_separation
            hole.circular_pattern(
                circular_pattern_instance_count, instanceSeparation, circular_pattern_about_entity_or_landmark, circular_pattern_instance_axis)

        if linear_pattern_instance_count > 1:
            hole.linear_pattern(
                linear_pattern_instance_count, linear_pattern_instance_separation, linear_pattern_instance_axis)

        if linear_pattern2nd_instance_count > 1:
            hole.linear_pattern(
                linear_pattern2nd_instance_count, linear_pattern2nd_instance_separation, linear_pattern2nd_instance_axis)

        if mirror and mirror_about_entity_or_landmark:
            hole.mirror(mirror_about_entity_or_landmark, mirror_axis,
                        resulting_mirrored_entity_name=None)

        self.subtract(hole, delete_after_subtract=True,
                      is_transfer_landmarks=False)
        return self._apply_modifiers_only()

    def set_material(self, material_name: MaterialOrItsName
                     ):
        material = material_name

        if isinstance(material, str):
            material = Material(material)

        material.assign_to_part(self.name)
        return self

    def is_colliding_with_part(self, other_part: PartOrItsName
                               ):
        other_partName = other_part
        if isinstance(other_partName, PartInterface):
            other_partName = other_partName.name

        if other_partName == self.name:
            raise NameError(
                "Collision must be checked between different Parts.")

        return blender_actions.is_collision_between_two_objects(self.name, other_partName)

    def fillet_all_edges(self, radius: DimensionOrItsFloatOrStringValue, use_width: bool = False
                         ):
        return self.bevel(
            radius,
            chamfer=False,
            use_width=use_width
        )

    def fillet_edges(self, radius: DimensionOrItsFloatOrStringValue, landmarks_near_edges: list[LandmarkOrItsName], use_width: bool = False
                     ):
        return self.bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=False,
            use_width=use_width
        )

    def fillet_faces(self, radius: DimensionOrItsFloatOrStringValue, landmarks_near_faces: list[LandmarkOrItsName], use_width: bool = False
                     ):
        return self.bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=False,
            use_width=use_width
        )

    def chamfer_all_edges(self, radius: DimensionOrItsFloatOrStringValue
                          ):
        return self.bevel(
            radius,
            chamfer=True,
            use_width=False
        )

    def chamfer_edges(self, radius: DimensionOrItsFloatOrStringValue, landmarks_near_edges: list[LandmarkOrItsName]
                      ):
        return self.bevel(
            radius,
            bevel_edges_nearlandmark_names=landmarks_near_edges,
            chamfer=True,
            use_width=False
        )

    def chamfer_faces(self, radius: DimensionOrItsFloatOrStringValue, landmarks_near_faces: list[LandmarkOrItsName]
                      ):
        return self.bevel(
            radius,
            bevel_faces_nearlandmark_names=landmarks_near_faces,
            chamfer=True,
            use_width=False
        )

    def _add_edges_near_landmarks_to_vertex_group(self, bevel_edges_nearlandmark_names: list[LandmarkOrItsName], vertex_group_name):

        kdTree = blender_actions.create_kd_tree_for_object(self.name)
        vertexGroupObject = blender_actions.create_object_vertex_group(
            self.name, vertex_group_name)

        for landmarkOrItsName in bevel_edges_nearlandmark_names:
            landmark = self.get_landmark(landmarkOrItsName) if isinstance(
                landmarkOrItsName, str) else landmarkOrItsName
            vertexIndecies = [index for (_, index, _) in blender_actions.get_closest_points_to_vertex(self.name, [
                dimension.value for dimension in landmark.get_location_world().to_list()], number_of_points=2, object_kd_tree=kdTree)]

            assert len(
                vertexIndecies) == 2, f"Could not find edges near landmark {landmark.get_landmark_entity_name()}"

            blender_actions.add_verticies_to_vertex_group(
                vertexGroupObject, vertexIndecies)

    def _add_faces_near_landmarks_to_vertex_group(self, bevel_faces_nearlandmark_names: list[LandmarkOrItsName], vertex_group_name):
        vertexGroupObject = blender_actions.create_object_vertex_group(
            self.name, vertex_group_name)

        for landmarkOrItsName in bevel_faces_nearlandmark_names:
            landmark = self.get_landmark(landmarkOrItsName) if isinstance(
                landmarkOrItsName, str) else landmarkOrItsName

            blenderPolygon = blender_actions.get_closest_face_to_vertex(
                self.name, [dimension.value for dimension in landmark.get_location_world().to_list()])

            faceIndecies: list[int] = blenderPolygon.vertices  # type: ignore

            blender_actions.add_verticies_to_vertex_group(
                vertexGroupObject, faceIndecies)

    def bevel(self,
              radius: DimensionOrItsFloatOrStringValue,
              bevel_edges_nearlandmark_names: Optional[list[LandmarkOrItsName]] = None,
              bevel_faces_nearlandmark_names: Optional[list[LandmarkOrItsName]] = None,
              use_width=False,
              chamfer=False,
              keyword_arguments: Optional[dict] = None
              ):
        vertex_group_name = None

        if bevel_edges_nearlandmark_names is not None:
            vertex_group_name = create_uuid_like_id()
            self._add_edges_near_landmarks_to_vertex_group(
                bevel_edges_nearlandmark_names, vertex_group_name)

        if bevel_faces_nearlandmark_names is not None:
            vertex_group_name = vertex_group_name or create_uuid_like_id()
            self._add_faces_near_landmarks_to_vertex_group(
                bevel_faces_nearlandmark_names, vertex_group_name)

        radiusDimension = Dimension.from_string(radius)

        radiusDimension = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            radiusDimension)

        blender_actions.apply_bevel_modifier(
            self.name,
            radiusDimension,
            vertex_group_name=vertex_group_name,
            use_edges=True,
            use_width=use_width,
            chamfer=chamfer,
            **(keyword_arguments or {})
        )

        return self._apply_modifiers_only()

    def select_vertex_near_landmark(self, landmark_name: Optional[LandmarkOrItsName] = None
                                    ):

        raise NotImplementedError()
        return self

    def select_edge_near_landmark(self, landmark_name: Optional[LandmarkOrItsName] = None
                                  ):

        raise NotImplementedError()
        return self

    def select_face_near_landmark(self, landmark_name: Optional[LandmarkOrItsName] = None
                                  ):

        raise NotImplementedError()
        return self
