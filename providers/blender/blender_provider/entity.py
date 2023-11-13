import math
from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import EntityInterface, LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def is_exists(self) -> bool:
        try:
            return blender_actions.get_object(self.name) is not None
        except:  # noqa: E722
            return False

    def rename(self, new_name: str, renamelinked_entities_and_landmarks: bool = True):
        assert Entity(new_name).is_exists() is False, f"{new_name} already exists."

        blender_actions.update_object_name(self.name, new_name)

        if renamelinked_entities_and_landmarks:
            blender_actions.update_object_data_name(new_name, new_name)

            blender_actions.update_object_landmark_names(new_name, self.name, new_name)

        self.name = new_name

        return self

    def delete(self, remove_children: bool = True):
        blender_actions.remove_object(self.name, remove_children)
        return self

    def is_visible(self) -> bool:
        return blender_actions.get_object_visibility(self.name)

    def set_visible(self, is_visible: bool):
        blender_actions.set_object_visibility(self.name, is_visible)

        return self

    def _apply_modifiers_only(self):
        return self.apply(rotation=False, scale=False, location=False, modifiers=True)

    def _apply_rotation_and_scale_only(self):
        return self.apply(rotation=True, scale=True, location=False, modifiers=False)

    def apply(self, rotation=True, scale=True, location=False, modifiers=True):
        blender_actions.update_view_layer()

        from . import Part  # noqa: F811

        if modifiers and isinstance(self, Part):
            # Only apply modifiers for Blender Objects that have meshes

            blender_actions.apply_dependency_graph(self.name)

            blender_actions.remove_mesh(self.name)

            blender_actions.update_object_data_name(self.name, self.name)

            blender_actions.clear_modifiers(self.name)

        if rotation or scale or location:
            blender_actions.apply_object_transformations(
                self.name, rotation, scale, location
            )

        return self

    def get_native_instance(self):
        return blender_actions.get_object(self.name)

    def get_location_world(self) -> "Point":
        blender_actions.update_view_layer()
        return blender_actions.get_object_world_location(self.name)

    def get_location_local(self) -> "Point":
        blender_actions.update_view_layer()
        return blender_actions.get_object_local_location(self.name)

    def select(self):
        blender_actions.select_object(self.name)
        return self

    def export(self, file_path: str, overwrite: bool = True, scale: float = 1.0):
        absoluteFilePath = get_absolute_filepath(file_path)

        blender_actions.export_object(self.name, absoluteFilePath, overwrite, scale)
        return self

    def mirror(
        self,
        mirror_across_entity: EntityOrItsName,
        axis: AxisOrItsIndexOrItsName,
        resulting_mirrored_entity_name: Optional[str],
    ):
        if resulting_mirrored_entity_name is not None:
            raise NotImplementedError("Not yet supported. COD-113")

        mirrorAcrossEntityName = mirror_across_entity
        if isinstance(mirrorAcrossEntityName, LandmarkInterface):
            mirrorAcrossEntityName = mirrorAcrossEntityName.get_landmark_entity_name()
        elif isinstance(mirrorAcrossEntityName, EntityInterface):
            mirrorAcrossEntityName = mirrorAcrossEntityName.name

        axis = Axis.from_string(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        blender_actions.apply_mirror_modifier(self.name, mirrorAcrossEntityName, axis)

        return self._apply_modifiers_only()

    def linear_pattern(
        self,
        instance_count: "int",
        offset: DimensionOrItsFloatOrStringValue,
        direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        axis = Axis.from_string(direction_axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        if isinstance(offset, str):
            offset = Dimension.from_string(offset)

        if isinstance(offset, Dimension):
            offset = (
                blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                    offset
                )
            )
            offset = offset.value

        blender_actions.apply_linear_pattern(self.name, instance_count, axis, offset)

        return self._apply_modifiers_only()

    def circular_pattern(
        self,
        instance_count: "int",
        separation_angle: AngleOrItsFloatOrStringValue,
        center_entity_or_landmark: EntityOrItsName,
        normal_direction_axis: AxisOrItsIndexOrItsName = "z",
    ):
        center_entity_or_landmark_name = center_entity_or_landmark
        if isinstance(center_entity_or_landmark_name, LandmarkInterface):
            center_entity_or_landmark_name = (
                center_entity_or_landmark_name.get_landmark_entity_name()
            )
        elif isinstance(center_entity_or_landmark_name, EntityInterface):
            center_entity_or_landmark_name = center_entity_or_landmark_name.name

        pivotLandmarkName = create_uuid_like_id()

        self.create_landmark(pivotLandmarkName, 0, 0, 0)

        pivotLandmarkEntityName = self.get_landmark(
            pivotLandmarkName
        ).get_landmark_entity_name()

        blender_actions.apply_pivot_constraint(
            pivotLandmarkEntityName, center_entity_or_landmark_name
        )

        axis = Axis.from_string(normal_direction_axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        angles: list[Optional[Angle]] = [Angle(0) for _ in range(3)]

        angle = separation_angle
        if isinstance(angle, str):
            angle = Angle.from_string(angle)
        elif isinstance(angle, (float, int)):
            angle = Angle(angle)

        angles[axis.value] = angle

        blender_actions.rotate_object(
            pivotLandmarkEntityName,
            angles,
            blender_definitions.BlenderRotationTypes.EULER,
        )

        blender_actions.apply_circular_pattern(
            self.name, instance_count, pivotLandmarkEntityName
        )

        self._apply_modifiers_only()

        self.get_landmark(pivotLandmarkName).delete()

        return self

    @staticmethod
    def _translation_dimension_from_dimension_or_its_float_or_string_value(
        dimension_or_its_float_or_string_value: DimensionOrItsFloatOrStringValue,
        boundary_axis: BoundaryAxis,
    ):
        dimension = Dimension.from_dimension_or_its_float_or_string_value(
            dimension_or_its_float_or_string_value, boundary_axis
        )

        return blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
            dimension
        )

    def translate_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        boundingBox = blender_actions.get_bounding_box(self.name)

        assert (
            boundingBox.x and boundingBox.y and boundingBox.z
        ), "Could not get bounding box"

        xDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                x, boundingBox.x
            )
        )
        yDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                y, boundingBox.y
            )
        )
        zDimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                z, boundingBox.z
            )
        )

        blender_actions.translate_object(
            self.name,
            [xDimension, yDimension, zDimension],
            blender_definitions.BlenderTranslationTypes.ABSOLUTE,
        )

        return self

    def translate_x(self, amount: DimensionOrItsFloatOrStringValue):
        boundingBox = blender_actions.get_bounding_box(self.name)

        assert boundingBox.x, "Could not get bounding box"

        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.x
            )
        )

        blender_actions.translate_object(
            self.name,
            [dimension, None, None],
            blender_definitions.BlenderTranslationTypes.ABSOLUTE,
        )

        return self

    def translate_y(self, amount: DimensionOrItsFloatOrStringValue):
        boundingBox = blender_actions.get_bounding_box(self.name)

        assert boundingBox.y, "Could not get bounding box"

        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.y
            )
        )

        blender_actions.translate_object(
            self.name,
            [None, dimension, None],
            blender_definitions.BlenderTranslationTypes.ABSOLUTE,
        )

        return self

    def translate_z(self, amount: DimensionOrItsFloatOrStringValue):
        boundingBox = blender_actions.get_bounding_box(self.name)

        assert boundingBox.z, "Could not get bounding box"

        dimension = (
            Entity._translation_dimension_from_dimension_or_its_float_or_string_value(
                amount, boundingBox.z
            )
        )

        blender_actions.translate_object(
            self.name,
            [None, None, dimension],
            blender_definitions.BlenderTranslationTypes.ABSOLUTE,
        )

        return self

    @staticmethod
    def _scale_factor_from_dimension_or_its_float_or_string_value(
        dimension_or_its_float_or_string_value: DimensionOrItsFloatOrStringValue,
        current_value_in_blender: float,
    ):
        value = Dimension.from_dimension_or_its_float_or_string_value(
            dimension_or_its_float_or_string_value, None
        )
        valueInBlenderDefaultLength = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(value)
        )
        return (valueInBlenderDefaultLength / current_value_in_blender).value

    def scale_xyz(
        self,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        currentDimensions = self.get_dimensions()
        xScaleFactor: float = (
            Entity._scale_factor_from_dimension_or_its_float_or_string_value(
                x, currentDimensions.x.value
            )
        )
        yScaleFactor: float = (
            Entity._scale_factor_from_dimension_or_its_float_or_string_value(
                y, currentDimensions.y.value
            )
        )
        zScaleFactor: float = (
            Entity._scale_factor_from_dimension_or_its_float_or_string_value(
                z, currentDimensions.z.value
            )
        )

        blender_actions.scale_object(
            self.name, xScaleFactor, yScaleFactor, zScaleFactor
        )

        return self._apply_rotation_and_scale_only()

    def scale_x(self, scale: DimensionOrItsFloatOrStringValue):
        scale_factor = Entity._scale_factor_from_dimension_or_its_float_or_string_value(
            scale, self.get_dimensions().x.value
        )
        blender_actions.scale_object(self.name, scale_factor, None, None)
        return self._apply_rotation_and_scale_only()

    def scale_y(self, scale: DimensionOrItsFloatOrStringValue):
        scale_factor = Entity._scale_factor_from_dimension_or_its_float_or_string_value(
            scale, self.get_dimensions().y.value
        )
        blender_actions.scale_object(self.name, None, scale_factor, None)
        return self._apply_rotation_and_scale_only()

    def scale_z(self, scale: DimensionOrItsFloatOrStringValue):
        scale_factor = Entity._scale_factor_from_dimension_or_its_float_or_string_value(
            scale, self.get_dimensions().z.value
        )
        blender_actions.scale_object(self.name, None, None, scale_factor)
        return self._apply_rotation_and_scale_only()

    def scale_x_by_factor(self, scale_factor: float):
        blender_actions.scale_object(self.name, scale_factor, None, None)
        return self._apply_rotation_and_scale_only()

    def scale_y_by_factor(self, scale_factor: float):
        blender_actions.scale_object(self.name, None, scale_factor, None)
        return self._apply_rotation_and_scale_only()

    def scale_z_by_factor(self, scale_factor: float):
        blender_actions.scale_object(self.name, None, None, scale_factor)
        return self._apply_rotation_and_scale_only()

    def scale_keep_aspect_ratio(
        self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
    ):
        scale = Dimension.from_dimension_or_its_float_or_string_value(scale, None)
        valueInBlenderDefaultLength = (
            blender_definitions.BlenderLength.convert_dimension_to_blender_unit(scale)
        )

        dimensionInAxis = self.get_dimensions()[Axis.from_string(axis).value]
        scale_factor: float = (valueInBlenderDefaultLength / dimensionInAxis).value

        blender_actions.scale_object(
            self.name, scale_factor, scale_factor, scale_factor
        )
        return self._apply_rotation_and_scale_only()

    def rotate_xyz(
        self,
        x: AngleOrItsFloatOrStringValue,
        y: AngleOrItsFloatOrStringValue,
        z: AngleOrItsFloatOrStringValue,
    ):
        xAngle = Angle.from_angle_or_its_float_or_string_value(x)
        yAngle = Angle.from_angle_or_its_float_or_string_value(y)
        zAngle = Angle.from_angle_or_its_float_or_string_value(z)

        blender_actions.rotate_object(
            self.name,
            [xAngle, yAngle, zAngle],
            blender_definitions.BlenderRotationTypes.EULER,
        )

        return self._apply_rotation_and_scale_only()

    def rotate_x(self, rotation: AngleOrItsFloatOrStringValue):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)

        blender_actions.rotate_object(
            self.name,
            [angle, None, None],
            blender_definitions.BlenderRotationTypes.EULER,
        )

        return self._apply_rotation_and_scale_only()

    def rotate_y(self, rotation: AngleOrItsFloatOrStringValue):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)

        blender_actions.rotate_object(
            self.name,
            [None, angle, None],
            blender_definitions.BlenderRotationTypes.EULER,
        )
        return self._apply_rotation_and_scale_only()

    def rotate_z(self, rotation: AngleOrItsFloatOrStringValue):
        angle = Angle.from_angle_or_its_float_or_string_value(rotation)

        blender_actions.rotate_object(
            self.name,
            [None, None, angle],
            blender_definitions.BlenderRotationTypes.EULER,
        )
        return self._apply_rotation_and_scale_only()

    def twist(
        self,
        angle: AngleOrItsFloatOrStringValue,
        screw_pitch: DimensionOrItsFloatOrStringValue,
        interations: "int" = 1,
        axis: AxisOrItsIndexOrItsName = "z",
    ):
        axis = Axis.from_string(axis)

        angleParsed = Angle.from_string(angle)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        screw_pitch = Dimension.from_string(screw_pitch)

        blender_actions.apply_screw_modifier(
            self.name,
            angleParsed.to_radians(),
            axis,
            screw_pitch=screw_pitch,
            iterations=interations,
        )

        return self._apply_modifiers_only()

    def remesh(self, strategy: str, amount: float):
        if strategy == "decimate":
            blender_actions.apply_decimate_modifier(self.name, int(amount))
        else:
            if strategy == "crease":
                blender_actions.set_edges_mean_crease(self.name, 1.0)
            if strategy == "edgesplit":
                blender_actions.apply_modifier(
                    self.name,
                    blender_definitions.BlenderModifiers.EDGE_SPLIT,
                    name="EdgeDiv",
                    split_angle=math.radians(30),
                )

            blender_actions.apply_modifier(
                self.name,
                blender_definitions.BlenderModifiers.SUBSURF,
                name="Subdivision",
                levels=amount,
            )

        self._apply_modifiers_only()

        if strategy == "crease":
            blender_actions.set_edges_mean_crease(self.name, 0)

        return self

    def create_landmark(
        self,
        landmark_name: str,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ):
        boundingBox = blender_actions.get_bounding_box(self.name)

        localPositions = [
            Dimension.from_dimension_or_its_float_or_string_value(x, boundingBox.x),
            Dimension.from_dimension_or_its_float_or_string_value(y, boundingBox.y),
            Dimension.from_dimension_or_its_float_or_string_value(z, boundingBox.z),
        ]

        localPositions = (
            blender_definitions.BlenderLength.convert_dimensions_to_blender_unit(
                localPositions
            )
        )

        from . import Landmark  # noqa: F811
        from . import Part  # noqa: F811

        landmark = Landmark(landmark_name, self.name)
        landmarkObjectName = landmark.get_landmark_entity_name()

        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        _ = Part(landmarkObjectName)._create_primitive("Empty", "0")

        # Assign the landmark to the parent's collection
        blender_actions.assign_object_to_collection(
            landmarkObjectName, blender_actions.get_object_collection_name(self.name)
        )

        # Parent the landmark to the object
        blender_actions.make_parent(landmarkObjectName, self.name)

        blender_actions.translate_object(
            landmarkObjectName,
            localPositions,
            blender_definitions.BlenderTranslationTypes.ABSOLUTE,
        )

        return landmark

    def get_bounding_box(self) -> "BoundaryBox":
        return blender_actions.get_bounding_box(self.name)

    def get_dimensions(self) -> "Dimensions":
        dimensions = blender_actions.get_object(self.name).dimensions
        dimensions = [
            Dimension.from_string(
                dimension,
                blender_definitions.BlenderLength.DEFAULT_BLENDER_UNIT.value,
            )
            for dimension in dimensions
        ]
        return Dimensions(dimensions[0], dimensions[1], dimensions[2])

    def get_landmark(
        self, landmark_name: PresetLandmarkOrItsName
    ) -> "LandmarkInterface":
        if isinstance(landmark_name, LandmarkInterface):
            landmark_name = landmark_name.name

        preset: Optional[PresetLandmark] = None

        if isinstance(landmark_name, str):
            preset = PresetLandmark.from_string(landmark_name)

        if isinstance(landmark_name, PresetLandmark):
            preset = landmark_name
            landmark_name = preset.name

        from . import Landmark  # noqa: F811

        landmark = Landmark(landmark_name, self.name)

        if preset is not None:
            # if preset does not exist, create it.
            try:
                blender_actions.get_object(landmark.get_landmark_entity_name())
            except:  # noqa: E722
                presetXYZ = preset.get_xyz()
                self.create_landmark(
                    landmark_name, presetXYZ[0], presetXYZ[1], presetXYZ[2]
                )

                return landmark

        assert (
            blender_actions.get_object(landmark.get_landmark_entity_name()) is not None
        ), f"Landmark {landmark_name} does not exist for {self.name}."
        return landmark
