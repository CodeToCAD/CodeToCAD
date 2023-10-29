from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import JointInterface, EntityInterface, LandmarkInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Entity


class Joint(JointInterface):
    entity1: EntityOrItsName
    entity2: EntityOrItsName

    def __init__(self, entity1: EntityOrItsName, entity2: EntityOrItsName):
        self.entity1 = entity1
        self.entity2 = entity2

    def translate_landmark_onto_another(self):
        if not isinstance(self.entity1, LandmarkInterface) or not isinstance(
            self.entity2, LandmarkInterface
        ):
            raise TypeError("Entities 1 and 2 should be landmarks.")

        landmark1: LandmarkInterface = self.entity1
        landmark2: LandmarkInterface = self.entity2
        entityForLandmark2 = self.entity2.get_parent_entity()

        translation = landmark1.get_location_world() - landmark2.get_location_world()

        entityForLandmark2.translate_xyz(translation.x, translation.y, translation.z)

        return self

    @staticmethod
    def _get_entity_or_landmark_name(entity_or_landmark) -> str:
        if isinstance(entity_or_landmark, str):
            return entity_or_landmark
        elif isinstance(entity_or_landmark, LandmarkInterface):
            return entity_or_landmark.get_landmark_entity_name()
        elif isinstance(entity_or_landmark, EntityInterface):
            return entity_or_landmark.name

        raise TypeError("Only Entity or Landmark types are allowed.")

    @staticmethod
    def _get_entity_or_landmark_parent_name(entity_or_landmark) -> str:
        if isinstance(entity_or_landmark, str):
            return entity_or_landmark
        elif isinstance(entity_or_landmark, LandmarkInterface):
            return entity_or_landmark.get_parent_entity().name
        elif isinstance(entity_or_landmark, EntityInterface):
            return entity_or_landmark.name

        raise TypeError("Only Entity or Landmark types are allowed.")

    def pivot(self):
        objectToPivotName = Joint._get_entity_or_landmark_name(self.entity2)

        objectToPivotAboutName = Joint._get_entity_or_landmark_name(self.entity1)

        blender_actions.apply_pivot_constraint(
            objectToPivotName, objectToPivotAboutName
        )

        return self

    def gear_ratio(self, ratio: float):
        object1 = Joint._get_entity_or_landmark_name(self.entity2)

        object2 = Joint._get_entity_or_landmark_name(self.entity1)

        blender_actions.apply_gear_constraint(object1, object2, ratio)

        return self

    @staticmethod
    def _get_limit_location_pair(min, max) -> list[Optional[Dimension]]:
        locationPair: list[Optional[Dimension]] = [None, None]

        if min is not None:
            locationPair[
                0
            ] = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(min)
            )
        if max is not None:
            locationPair[
                1
            ] = blender_definitions.BlenderLength.convert_dimension_to_blender_unit(
                Dimension.from_string(max)
            )

        return locationPair

    def _limit_location_xyz(
        self,
        x: Optional[list[Optional[Dimension]]],
        y: Optional[list[Optional[Dimension]]],
        z: Optional[list[Optional[Dimension]]],
    ):
        objectToLimitOrItsName = self.entity2
        object_to_limit_name = objectToLimitOrItsName

        relativeToObjectName = Joint._get_entity_or_landmark_name(self.entity1)

        if isinstance(object_to_limit_name, LandmarkInterface):
            landmarkEntity = object_to_limit_name

            object_to_limit_name = object_to_limit_name.get_parent_entity().name

            offset = landmarkEntity.get_location_local() * -1

            if x and x[0]:
                x[0] += offset.x
            if x and x[1]:
                x[1] += offset.x
            if y and y[0]:
                y[0] += offset.y
            if y and y[1]:
                y[1] += offset.y
            if z and z[0]:
                z[0] += offset.z
            if z and z[1]:
                z[1] += offset.z
        elif isinstance(object_to_limit_name, EntityInterface):
            object_to_limit_name = object_to_limit_name.name

        # SA: Blender's Limit Location must be paired with Copy Location if we don't want the objectToLimit's rotation and scale to be affected by relativeToObject's transformations.
        blender_actions.apply_limit_location_constraint(
            object_to_limit_name, x, y, z, None
        )
        blender_actions.apply_copy_location_constraint(
            object_to_limit_name, relativeToObjectName, True, True, True, True
        )
        self._apply_pivot_constraint_if_location_and_rotation_limit_constraints_exist(
            object_to_limit_name, relativeToObjectName
        )

    def _apply_pivot_constraint_if_location_and_rotation_limit_constraints_exist(
        self, object_to_limit_name, pivot_object_name
    ):
        blender_actions.update_view_layer()

        locationConstraint = blender_actions.get_constraint(
            object_to_limit_name,
            blender_definitions.BlenderConstraintTypes.LIMIT_LOCATION.format_constraint_name(
                object_to_limit_name, None
            ),
        )

        rotationConstraint = blender_actions.get_constraint(
            object_to_limit_name,
            blender_definitions.BlenderConstraintTypes.LIMIT_ROTATION.format_constraint_name(
                object_to_limit_name, None
            ),
        )

        if locationConstraint and rotationConstraint:
            blender_actions.apply_pivot_constraint(
                object_to_limit_name, pivot_object_name
            )

    def limit_location_xyz(
        self,
        x: Optional[DimensionOrItsFloatOrStringValue] = None,
        y: Optional[DimensionOrItsFloatOrStringValue] = None,
        z: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensionsX = Joint._get_limit_location_pair(x, x) if x is not None else None
        dimensionsY = Joint._get_limit_location_pair(y, y) if y is not None else None
        dimensionsZ = Joint._get_limit_location_pair(z, z) if y is not None else None

        self._limit_location_xyz(dimensionsX, dimensionsY, dimensionsZ)

        return self

    def limit_location_x(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(dimensions, None, None)
        return self

    def limit_location_y(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(None, dimensions, None)
        return self

    def limit_location_z(
        self,
        min: Optional[DimensionOrItsFloatOrStringValue] = None,
        max: Optional[DimensionOrItsFloatOrStringValue] = None,
    ):
        dimensions = Joint._get_limit_location_pair(min, max)

        self._limit_location_xyz(None, None, dimensions)
        return self

    @staticmethod
    def _get_limit_rotation_pair(min, max) -> list[Optional[Angle]]:
        rotationPair: list[Optional[Angle]] = [None, None]

        if min is not None:
            rotationPair[0] = Angle.from_string(min)
        if max is not None:
            rotationPair[1] = Angle.from_string(max)

        return rotationPair

    def _limit_rotation_xyz(self, rotation_pair_x, rotation_pair_y, rotation_pair_z):
        object_to_limit_name = self.entity2
        if isinstance(object_to_limit_name, LandmarkInterface):
            object_to_limit_name = object_to_limit_name.get_parent_entity().name
        elif isinstance(object_to_limit_name, EntityInterface):
            object_to_limit_name = object_to_limit_name.name

        relativeToObjectName = Joint._get_entity_or_landmark_name(self.entity1)

        relativeToObjectOrParentName = Joint._get_entity_or_landmark_parent_name(
            self.entity1
        )

        # blender_actions.applyLimitRotapply_limit_rotation_constraintationConstraint(
        #     object_to_limit_name, rotation_pair_x, rotation_pair_y, rotation_pair_z, relativeToObjectName)
        blender_actions.apply_limit_rotation_constraint(
            object_to_limit_name,
            rotation_pair_x,
            rotation_pair_y,
            rotation_pair_z,
            None,
        )
        copyX = rotation_pair_x is not None and all(
            [value is not None for value in rotation_pair_x]
        )
        copyY = rotation_pair_y is not None and all(
            [value is not None for value in rotation_pair_y]
        )
        copyZ = rotation_pair_z is not None and all(
            [value is not None for value in rotation_pair_z]
        )
        blender_actions.apply_copy_rotation_constraint(
            object_to_limit_name, relativeToObjectOrParentName, copyX, copyY, copyZ
        )
        self._apply_pivot_constraint_if_location_and_rotation_limit_constraints_exist(
            object_to_limit_name, relativeToObjectName
        )

        return self

    def limit_rotation_xyz(
        self,
        x: Optional[AngleOrItsFloatOrStringValue] = None,
        y: Optional[AngleOrItsFloatOrStringValue] = None,
        z: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotation_pair_x = (
            Joint._get_limit_rotation_pair(x, x) if x is not None else None
        )
        rotation_pair_y = (
            Joint._get_limit_rotation_pair(y, y) if y is not None else None
        )
        rotation_pair_z = (
            Joint._get_limit_rotation_pair(z, z) if z is not None else None
        )

        return self._limit_rotation_xyz(
            rotation_pair_x, rotation_pair_y, rotation_pair_z
        )

    def limit_rotation_x(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(rotationPair, None, None)

    def limit_rotation_y(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, rotationPair, None)

    def limit_rotation_z(
        self,
        min: Optional[AngleOrItsFloatOrStringValue] = None,
        max: Optional[AngleOrItsFloatOrStringValue] = None,
    ):
        rotationPair = Joint._get_limit_rotation_pair(min, max)
        return self._limit_rotation_xyz(None, None, rotationPair)
