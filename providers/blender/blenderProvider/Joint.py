# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from typing import Optional

from . import BlenderActions
from . import BlenderDefinitions

from CodeToCAD.interfaces import JointInterface, EntityInterface, LandmarkInterface
from CodeToCAD.CodeToCADTypes import *
from CodeToCAD.utilities import *


class Joint(JointInterface):

    entity1: EntityOrItsNameOrLandmark
    entity2: EntityOrItsNameOrLandmark

    def __init__(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    def translateLandmarkOntoAnother(self
                                     ):
        if not isinstance(self.entity1, LandmarkInterface) or not isinstance(self.entity2, LandmarkInterface):
            raise TypeError("Entities 1 and 2 should be landmarks.")

        landmark1: LandmarkInterface = self.entity1
        landmark2: LandmarkInterface = self.entity2
        entityForLandmark2 = self.entity2.getParentEntity()

        translation = landmark1.getLocationWorld() - landmark2.getLocationWorld()

        entityForLandmark2.translateXYZ(
            translation.x, translation.y, translation.z)

        return self

    @staticmethod
    def _getEntityOrLandmarkName(entityOrLandmark) -> str:
        if isinstance(entityOrLandmark, str):
            return entityOrLandmark
        elif isinstance(entityOrLandmark, EntityInterface):
            return entityOrLandmark.name
        elif isinstance(entityOrLandmark, LandmarkInterface):
            return entityOrLandmark.getLandmarkEntityName()

        raise TypeError("Only Entity or Landmark types are allowed.")

    def pivot(self
              ):

        objectToPivotName = Joint._getEntityOrLandmarkName(self.entity2)

        objectToPivotAboutName = Joint._getEntityOrLandmarkName(self.entity1)

        BlenderActions.applyPivotConstraint(
            objectToPivotName, objectToPivotAboutName)

        return self

    def gearRatio(self, ratio: float
                  ):

        object1 = Joint._getEntityOrLandmarkName(self.entity2)

        object2 = Joint._getEntityOrLandmarkName(self.entity1)

        BlenderActions.applyGearConstraint(
            object1, object2, ratio)

        return self

    @staticmethod
    def _getLimitLocationPair(min, max) -> list[Optional[Dimension]]:
        locationPair: list[Optional[Dimension]] = [None, None]

        if min is not None:
            locationPair[0] = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
                Dimension.fromString(min))
        if max is not None:
            locationPair[1] = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
                Dimension.fromString(max))

        return locationPair

    def _limitLocationXYZ(self, x: Optional[list[Optional[Dimension]]], y: Optional[list[Optional[Dimension]]], z: Optional[list[Optional[Dimension]]]):

        objectToLimitOrItsName = self.entity2
        objectToLimitName = objectToLimitOrItsName

        relativeToObjectName = Joint._getEntityOrLandmarkName(self.entity1)

        if isinstance(objectToLimitName, EntityInterface):
            objectToLimitName = objectToLimitName.name
        elif isinstance(objectToLimitName, LandmarkInterface):

            landmarkEntity = objectToLimitName

            objectToLimitName = objectToLimitName.getParentEntity().name

            offset = landmarkEntity.getLocationLocal() * -1

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

        # SA: Blender's Limit Location must be paired with Copy Location if we don't want the objectToLimit's rotation and scale to be affected by relativeToObject's transformations.
        BlenderActions.applyLimitLocationConstraint(
            objectToLimitName, x, y, z, None)
        BlenderActions.applyCopyLocationConstraint(
            objectToLimitName, relativeToObjectName, True, True, True, True)
        self._applyPivotConstraintIfLocationAndRotationLimitConstraintsExist(
            objectToLimitName, relativeToObjectName)

    def _applyPivotConstraintIfLocationAndRotationLimitConstraintsExist(self, objectToLimitName, pivotObjectName):

        BlenderActions.updateViewLayer()

        locationConstraint = BlenderActions.getConstraint(
            objectToLimitName, BlenderDefinitions.BlenderConstraintTypes.LIMIT_LOCATION.formatConstraintName(objectToLimitName, None))

        rotationConstraint = BlenderActions.getConstraint(
            objectToLimitName, BlenderDefinitions.BlenderConstraintTypes.LIMIT_ROTATION.formatConstraintName(objectToLimitName, None))

        if locationConstraint and rotationConstraint:
            BlenderActions.applyPivotConstraint(
                objectToLimitName, pivotObjectName)

    def limitLocationXYZ(self, x: Optional[DimensionOrItsFloatOrStringValue] = None, y: Optional[DimensionOrItsFloatOrStringValue] = None, z: Optional[DimensionOrItsFloatOrStringValue] = None
                         ):

        dimensionsX = Joint._getLimitLocationPair(
            x, x) if x is not None else None
        dimensionsY = Joint._getLimitLocationPair(
            y, y) if y is not None else None
        dimensionsZ = Joint._getLimitLocationPair(
            z, z) if y is not None else None

        self._limitLocationXYZ(dimensionsX, dimensionsY, dimensionsZ)

        return self

    def limitLocationX(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):

        dimensions = Joint._getLimitLocationPair(min, max)

        self._limitLocationXYZ(dimensions, None, None)
        return self

    def limitLocationY(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        dimensions = Joint._getLimitLocationPair(min, max)

        self._limitLocationXYZ(None, dimensions, None)
        return self

    def limitLocationZ(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        dimensions = Joint._getLimitLocationPair(min, max)

        self._limitLocationXYZ(None, None, dimensions)
        return self

    @staticmethod
    def _getLimitRotationPair(min, max) -> list[Optional[Angle]]:
        rotationPair: list[Optional[Angle]] = [None, None]

        if min is not None:
            rotationPair[0] = Angle.fromString(min)
        if max is not None:
            rotationPair[1] = Angle.fromString(max)

        return rotationPair

    def _limitRotationXYZ(self, rotationPairX, rotationPairY, rotationPairZ):
        objectToLimitName = self.entity2
        if isinstance(objectToLimitName, EntityInterface):
            objectToLimitName = objectToLimitName.name
        elif isinstance(objectToLimitName, LandmarkInterface):
            objectToLimitName = objectToLimitName.getParentEntity().name

        relativeToObjectName = Joint._getEntityOrLandmarkName(self.entity1)

        # BlenderActions.applyLimitRotationConstraint(
        #     objectToLimitName, rotationPairX, rotationPairY, rotationPairZ, relativeToObjectName)
        BlenderActions.applyLimitRotationConstraint(
            objectToLimitName, rotationPairX, rotationPairY, rotationPairZ, None)
        copyX = rotationPairX is not None and all(
            [value is not None for value in rotationPairX])
        copyY = rotationPairY is not None and all(
            [value is not None for value in rotationPairY])
        copyZ = rotationPairZ is not None and all(
            [value is not None for value in rotationPairZ])
        BlenderActions.applyCopyRotationConstraint(
            objectToLimitName, relativeToObjectName, copyX, copyY, copyZ)
        self._applyPivotConstraintIfLocationAndRotationLimitConstraintsExist(
            objectToLimitName, relativeToObjectName)

        return self

    def limitRotationXYZ(self, x: Optional[AngleOrItsFloatOrStringValue] = None, y: Optional[AngleOrItsFloatOrStringValue] = None, z: Optional[AngleOrItsFloatOrStringValue] = None
                         ):

        rotationPairX = Joint._getLimitRotationPair(
            x, x) if x is not None else None
        rotationPairY = Joint._getLimitRotationPair(
            y, y) if y is not None else None
        rotationPairZ = Joint._getLimitRotationPair(
            z, z) if z is not None else None

        return self._limitRotationXYZ(rotationPairX, rotationPairY, rotationPairZ)

    def limitRotationX(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):

        rotationPair = Joint._getLimitRotationPair(min, max)
        return self._limitRotationXYZ(rotationPair, None, None)

    def limitRotationY(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        rotationPair = Joint._getLimitRotationPair(min, max)
        return self._limitRotationXYZ(None, rotationPair, None)

    def limitRotationZ(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        rotationPair = Joint._getLimitRotationPair(min, max)
        return self._limitRotationXYZ(None, None, rotationPair)
