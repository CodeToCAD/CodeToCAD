# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional, TYPE_CHECKING

from codetocad.interfaces import EntityInterface, LandmarkInterface

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


if TYPE_CHECKING:
    from . import Landmark

from . import blender_actions, blender_definitions


class Entity(EntityInterface):
    name: str
    description: Optional[str] = None
    native_instance = None

    def __init__(
        self, name: str, description: Optional[str] = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

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

    def apply(
        self,
        rotation: bool = True,
        scale: bool = True,
        location: bool = False,
        modifiers: bool = True,
    ):
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

    def get_native_instance(self) -> object:
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

    def create_landmark(
        self,
        landmark_name: str,
        x: DimensionOrItsFloatOrStringValue,
        y: DimensionOrItsFloatOrStringValue,
        z: DimensionOrItsFloatOrStringValue,
    ) -> "Landmark":
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

        from . import Part, Landmark

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
        )  # type: ignore

        return landmark

    def get_landmark(self, landmark_name: PresetLandmarkOrItsName) -> "Landmark":
        if isinstance(landmark_name, LandmarkInterface):
            landmark_name = landmark_name.name

        preset: Optional[PresetLandmark] = None

        if isinstance(landmark_name, str):
            preset = PresetLandmark.from_string(landmark_name)

        if isinstance(landmark_name, PresetLandmark):
            preset = landmark_name
            landmark_name = preset.name

        from . import Landmark

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
