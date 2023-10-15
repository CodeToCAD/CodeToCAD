

from typing import Optional
from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import EntityInterface, LandmarkInterface
from codetocad.CodeToCADTypes import *
from codetocad.utilities import *


class Entity(EntityInterface):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def createFromFile(self, filePath: str, fileType: Optional[str] = None
                       ):
        assert self.isExists() == False, f"{self.name} already exists."

        absoluteFilePath = getAbsoluteFilepath(filePath)

        importedFileName = BlenderActions.importFile(
            absoluteFilePath, fileType)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != importedFileName:
            from . import Part
            Part(importedFileName).rename(self.name)

        return self

    def isExists(self
                 ) -> bool:
        try:
            return BlenderActions.getObject(self.name) is not None
        except:
            return False

    def rename(self, newName: str, renamelinkedEntitiesAndLandmarks: bool = True
               ):

        assert Entity(newName).isExists(
        ) == False, f"{newName} already exists."

        BlenderActions.updateObjectName(self.name, newName)

        if renamelinkedEntitiesAndLandmarks:
            BlenderActions.updateObjectDataName(newName, newName)

            BlenderActions.updateObjectLandmarkNames(
                newName, self.name, newName)

        self.name = newName

        return self

    def delete(self, removeChildren: bool
               ):
        BlenderActions.removeObject(self.name, removeChildren)
        return self

    def isVisible(self
                  ) -> bool:
        return BlenderActions.getObjectVisibility(self.name)

    def setVisible(self, isVisible: bool
                   ):

        BlenderActions.setObjectVisibility(self.name, isVisible)

        return self

    def _applyModifiersOnly(self):
        return self.apply(rotation=False, scale=False, location=False, modifiers=True)

    def _applyRotationAndScaleOnly(self):
        return self.apply(rotation=True, scale=True, location=False, modifiers=False)

    def apply(self, rotation=True, scale=True, location=False, modifiers=True):

        BlenderActions.updateViewLayer()

        from . import Part

        if modifiers and isinstance(self, Part):
            # Only apply modifiers for Blender Objects that have meshes

            BlenderActions.applyDependencyGraph(self.name)

            BlenderActions.removeMesh(self.name)

            BlenderActions.updateObjectDataName(self.name, self.name)

            BlenderActions.clearModifiers(self.name)

        if rotation or scale or location:
            BlenderActions.applyObjectTransformations(
                self.name, rotation, scale, location)

        return self

    def getNativeInstance(self
                          ):
        return BlenderActions.getObject(self.name)

    def getLocationWorld(self
                         ) -> 'Point':
        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectWorldLocation(self.name)

    def getLocationLocal(self
                         ) -> 'Point':
        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectLocalLocation(self.name)

    def select(self):
        BlenderActions.selectObject(self.name)
        return self

    def export(self, filePath: str, overwrite: bool = True, scale: float = 1.0
               ):
        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.exportObject(
            self.name, absoluteFilePath, overwrite, scale)
        return self

    def mirror(self, mirrorAcrossEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName, resultingMirroredEntityName: Optional[str]
               ):

        if resultingMirroredEntityName is not None:
            raise NotImplementedError("Not yet supported. COD-113")

        mirrorAcrossEntityName = mirrorAcrossEntityOrLandmark
        if isinstance(mirrorAcrossEntityName, LandmarkInterface):
            mirrorAcrossEntityName = mirrorAcrossEntityName.getLandmarkEntityName()
        elif isinstance(mirrorAcrossEntityName, EntityInterface):
            mirrorAcrossEntityName = mirrorAcrossEntityName.name

        axis = Axis.fromString(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        BlenderActions.applyMirrorModifier(
            self.name, mirrorAcrossEntityName, axis)

        return self._applyModifiersOnly()

    def linearPattern(self, instanceCount: 'int', offset: DimensionOrItsFloatOrStringValue, directionAxis: AxisOrItsIndexOrItsName = "z"):

        axis = Axis.fromString(directionAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        if isinstance(offset, str):
            offset = Dimension.fromString(offset)

        if isinstance(offset, Dimension):
            offset = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
                offset)
            offset = offset.value

        BlenderActions.applyLinearPattern(
            self.name, instanceCount, axis, offset)

        return self._applyModifiersOnly()

    def circularPattern(self, instanceCount: 'int', separationAngle: AngleOrItsFloatOrStringValue, centerEntityOrLandmark: EntityOrItsNameOrLandmark, normalDirectionAxis: AxisOrItsIndexOrItsName = "z"):
        centerEntityOrLandmarkName = centerEntityOrLandmark
        if isinstance(centerEntityOrLandmarkName, LandmarkInterface):
            centerEntityOrLandmarkName = centerEntityOrLandmarkName.getLandmarkEntityName()
        elif isinstance(centerEntityOrLandmarkName, EntityInterface):
            centerEntityOrLandmarkName = centerEntityOrLandmarkName.name

        pivotLandmarkName = createUUIDLikeId()

        self.createLandmark(pivotLandmarkName, 0, 0, 0)

        pivotLandmarkEntityName = self.getLandmark(
            pivotLandmarkName).getLandmarkEntityName()

        BlenderActions.applyPivotConstraint(
            pivotLandmarkEntityName, centerEntityOrLandmarkName)

        axis = Axis.fromString(normalDirectionAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        angles: list[Optional[Angle]] = [Angle(0) for _ in range(3)]

        angle = separationAngle
        if isinstance(angle, str):
            angle = Angle.fromString(angle)
        elif isinstance(angle, (float, int)):
            angle = Angle(angle)

        angles[axis.value] = angle

        BlenderActions.rotateObject(
            pivotLandmarkEntityName, angles, BlenderDefinitions.BlenderRotationTypes.EULER)

        BlenderActions.applyCircularPattern(
            self.name, instanceCount, pivotLandmarkEntityName)

        self._applyModifiersOnly()

        self.getLandmark(pivotLandmarkName).delete()

        return self

    @staticmethod
    def _translationDimensionFromDimensionOrItsFloatOrStringValue(dimensionOrItsFloatOrStringValue: DimensionOrItsFloatOrStringValue, boundaryAxis: BoundaryAxis):

        dimension = Dimension.fromDimensionOrItsFloatOrStringValue(
            dimensionOrItsFloatOrStringValue, boundaryAxis)

        return BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            dimension)

    def translateXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                     ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        assert boundingBox.x and boundingBox.y and boundingBox.z, "Could not get bounding box"

        xDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            x, boundingBox.x)
        yDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            y, boundingBox.y)
        zDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            z, boundingBox.z)

        BlenderActions.translateObject(
            self.name, [xDimension, yDimension, zDimension], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateX(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        assert boundingBox.x, "Could not get bounding box"

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.x)

        BlenderActions.translateObject(
            self.name, [dimension, None, None], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateY(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        assert boundingBox.y, "Could not get bounding box"

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.y)

        BlenderActions.translateObject(
            self.name, [None, dimension, None], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateZ(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        assert boundingBox.z, "Could not get bounding box"

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.z)

        BlenderActions.translateObject(
            self.name, [None, None, dimension], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    @staticmethod
    def _scaleFactorFromDimensionOrItsFloatOrStringValue(dimensionOrItsFloatOrStringValue: DimensionOrItsFloatOrStringValue, currentValueInBlender: float):

        value = Dimension.fromDimensionOrItsFloatOrStringValue(
            dimensionOrItsFloatOrStringValue, None)
        valueInBlenderDefaultLength = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            value)
        return (valueInBlenderDefaultLength /
                currentValueInBlender).value

    def scaleXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                 ):
        currentDimensions = self.getDimensions()
        xScaleFactor: float = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            x, currentDimensions.x.value)
        yScaleFactor: float = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            y, currentDimensions.y.value)
        zScaleFactor: float = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            z, currentDimensions.z.value)

        BlenderActions.scaleObject(
            self.name, xScaleFactor, yScaleFactor, zScaleFactor)

        return self._applyRotationAndScaleOnly()

    def scaleX(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().x.value)
        BlenderActions.scaleObject(self.name, scaleFactor, None, None)
        return self._applyRotationAndScaleOnly()

    def scaleY(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().y.value)
        BlenderActions.scaleObject(self.name, None, scaleFactor, None)
        return self._applyRotationAndScaleOnly()

    def scaleZ(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().z.value)
        BlenderActions.scaleObject(self.name, None, None, scaleFactor)
        return self._applyRotationAndScaleOnly()

    def scaleXByFactor(self, scaleFactor: float
                       ):
        BlenderActions.scaleObject(self.name, scaleFactor, None, None)
        return self._applyRotationAndScaleOnly()

    def scaleYByFactor(self, scaleFactor: float
                       ):
        BlenderActions.scaleObject(self.name, None, scaleFactor, None)
        return self._applyRotationAndScaleOnly()

    def scaleZByFactor(self, scaleFactor: float
                       ):
        BlenderActions.scaleObject(self.name, None, None, scaleFactor)
        return self._applyRotationAndScaleOnly()

    def scaleKeepAspectRatio(self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
                             ):
        scale = Dimension.fromDimensionOrItsFloatOrStringValue(
            scale, None)
        valueInBlenderDefaultLength = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            scale)

        dimensionInAxis = self.getDimensions(
        )[Axis.fromString(axis).value]
        scaleFactor: float = (
            valueInBlenderDefaultLength / dimensionInAxis).value

        BlenderActions.scaleObject(
            self.name, scaleFactor, scaleFactor, scaleFactor)
        return self._applyRotationAndScaleOnly()

    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):

        xAngle = Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Angle.fromAngleOrItsFloatOrStringValue(z)

        BlenderActions.rotateObject(
            self.name, [xAngle, yAngle, zAngle], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self._applyRotationAndScaleOnly()

    def rotateX(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [angle, None, None], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self._applyRotationAndScaleOnly()

    def rotateY(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [None, angle, None], BlenderDefinitions.BlenderRotationTypes.EULER)
        return self._applyRotationAndScaleOnly()

    def rotateZ(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [None, None, angle], BlenderDefinitions.BlenderRotationTypes.EULER)
        return self._applyRotationAndScaleOnly()

    def twist(self, angle: AngleOrItsFloatOrStringValue, screwPitch: DimensionOrItsFloatOrStringValue, interations: 'int' = 1, axis: AxisOrItsIndexOrItsName = "z"
              ):

        axis = Axis.fromString(axis)

        angleParsed = Angle.fromString(angle)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        screwPitch = Dimension.fromString(screwPitch)

        BlenderActions.applyScrewModifier(
            self.name, angleParsed.toRadians(), axis, screwPitch=screwPitch, iterations=interations)

        return self._applyModifiersOnly()

    def remesh(self, strategy: str, amount: float
               ):

        if strategy == "decimate":
            BlenderActions.applyDecimateModifier(self.name, int(amount))
        else:
            if strategy == "crease":
                BlenderActions.setEdgesMeanCrease(self.name, 1.0)
            if strategy == "edgesplit":
                BlenderActions.applyModifier(
                    self.name,
                    BlenderDefinitions.BlenderModifiers.EDGE_SPLIT,
                    name="EdgeDiv",
                    split_angle=math.radians(30)
                )

            BlenderActions.applyModifier(
                self.name,
                BlenderDefinitions.BlenderModifiers.SUBSURF,
                name="Subdivision",
                levels=amount
            )

        self._applyModifiersOnly()

        if strategy == "crease":
            BlenderActions.setEdgesMeanCrease(self.name, 0)

        return self

    def createLandmark(self, landmarkName: str, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                       ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        localPositions = [
            Dimension.fromDimensionOrItsFloatOrStringValue(x, boundingBox.x),
            Dimension.fromDimensionOrItsFloatOrStringValue(y, boundingBox.y),
            Dimension.fromDimensionOrItsFloatOrStringValue(z, boundingBox.z),
        ]

        localPositions = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(
            localPositions)

        from . import Part, Landmark

        landmark = Landmark(landmarkName, self.name)
        landmarkObjectName = landmark.getLandmarkEntityName()

        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        _ = Part(landmarkObjectName) \
            ._createPrimitive("Empty", "0")  # type: ignore

        # Assign the landmark to the parent's collection
        BlenderActions.assignObjectToCollection(
            landmarkObjectName, BlenderActions.getObjectCollectionName(self.name))

        # Parent the landmark to the object
        BlenderActions.makeParent(landmarkObjectName, self.name)

        BlenderActions.translateObject(
            landmarkObjectName, localPositions, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)  # type: ignore

        return landmark

    def getBoundingBox(self
                       ) -> 'BoundaryBox':
        return BlenderActions.getBoundingBox(self.name)

    def getDimensions(self
                      ) -> 'Dimensions':
        dimensions = BlenderActions.getObject(self.name).dimensions
        dimensions = [
            Dimension.fromString(
                dimension,
                BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value  # type: ignore
            )
            for dimension in dimensions
        ]
        return Dimensions(dimensions[0], dimensions[1], dimensions[2])

    def getLandmark(self, landmarkName: PresetLandmarkOrItsName
                    ) -> 'LandmarkInterface':
        if isinstance(landmarkName, LandmarkInterface):
            landmarkName = landmarkName.name

        preset: Optional[PresetLandmark] = None

        if isinstance(landmarkName, str):
            try:
                preset = PresetLandmark.fromString(landmarkName)
            except Exception as e:
                pass

        if isinstance(landmarkName, PresetLandmark):
            preset = landmarkName
            landmarkName = preset.name

        from . import Landmark

        landmark = Landmark(landmarkName, self.name)

        if preset != None:
            # if preset does not exist, create it.
            try:
                BlenderActions.getObject(landmark.getLandmarkEntityName())
            except:
                presetXYZ = preset.getXYZ()
                self.createLandmark(
                    landmarkName, presetXYZ[0], presetXYZ[1], presetXYZ[2])

                return landmark

        assert BlenderActions.getObject(landmark.getLandmarkEntityName(
        )) is not None, f"Landmark {landmarkName} does not exist for {self.name}."
        return landmark
