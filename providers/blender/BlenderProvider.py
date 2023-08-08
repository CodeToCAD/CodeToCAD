# This file was forked from CodeToCAD/CodeToCADProvider.py

import math
from typing import Optional, Union

import BlenderActions
import BlenderDefinitions

import CodeToCAD.CodeToCADInterface as CodeToCADInterface
from CodeToCAD.CodeToCADInterface import *

from CodeToCAD.utilities import (Angle, AngleUnit, CurvePrimitiveTypes, BoundaryAxis, BoundaryBox, CurveTypes, Dimension, Dimensions,
                                 Point, PresetLandmark, center, createUUIDLikeId, getAbsoluteFilepath, formatLandmarkEntityName, FileFormats, getFileExtension, max, min)


if BlenderActions.getBlenderVersion() and BlenderActions.getBlenderVersion() < BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value:
    print(
        f"CodeToCAD BlenderProvider only supports Blender versions {'.'.join(tuple, BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value)}+. You are running version {'.'.join(BlenderActions.getBlenderVersion())}")  # type: ignore


def injectBlenderProvider(globalContext: Optional[dict]) -> None:
    from CodeToCAD import setPartProvider, setSketchProvider, setMaterialProvider, setLandmarkProvider, setJointProvider, setAnimationProvider, setSceneProvider, setAnalyticsProvider, setCameraProvider, setLightProvider, setRenderProvider

    setPartProvider(Part, globalContext)
    setSketchProvider(Sketch, globalContext)
    setMaterialProvider(Material, globalContext)
    setLandmarkProvider(Landmark, globalContext)
    setJointProvider(Joint, globalContext)
    setAnimationProvider(Animation, globalContext)
    setSceneProvider(Scene, globalContext)
    setAnalyticsProvider(Analytics, globalContext)
    setCameraProvider(Camera, globalContext)
    setLightProvider(Light, globalContext)
    setRenderProvider(Render, globalContext)


class Entity(CodeToCADInterface.Entity):

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
        if isinstance(mirrorAcrossEntityName, CodeToCADInterface.Landmark):
            mirrorAcrossEntityName = mirrorAcrossEntityName.getLandmarkEntityName()
        elif isinstance(mirrorAcrossEntityName, CodeToCADInterface.Entity):
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
        if isinstance(centerEntityOrLandmarkName, CodeToCADInterface.Landmark):
            centerEntityOrLandmarkName = centerEntityOrLandmarkName.getLandmarkEntityName()
        elif isinstance(centerEntityOrLandmarkName, CodeToCADInterface.Entity):
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

        landmark = Landmark(landmarkName, self.name)
        landmarkObjectName = landmark.getLandmarkEntityName()

        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        _ = Part(landmarkObjectName)._createPrimitive("Empty", "0")

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
                    ) -> 'Landmark':
        if isinstance(landmarkName, Landmark):
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


class Part(Entity, CodeToCADInterface.Part):

    def _createPrimitive(self, primitiveName: str, dimensions: str, **kwargs
                         ):

        assert self.isExists() == False, f"{self.name} already exists."

        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType: BlenderDefinitions.BlenderObjectPrimitiveTypes = getattr(
            BlenderDefinitions.BlenderObjectPrimitiveTypes, primitiveName.lower())
        expectedNameOfObjectInBlender = primitiveType.defaultNameInBlender(
        ) if primitiveType else None

        assert expectedNameOfObjectInBlender is not None, \
            f"Primitive type with name {primitiveName} is not supported."

        BlenderActions.addPrimitive(
            primitiveType, dimensions, **kwargs)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != expectedNameOfObjectInBlender:
            Part(expectedNameOfObjectInBlender).rename(
                self.name, primitiveType.hasData())

        return self

    def createCube(self, width: DimensionOrItsFloatOrStringValue, length: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                   ):
        return self._createPrimitive("cube", "{},{},{}".format(width, length, height), **(keywordArguments or {}))

    def createCone(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, draftRadius: DimensionOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        return self._createPrimitive("cone", "{},{},{}".format(radius, draftRadius, height), **(keywordArguments or {}))

    def createCylinder(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                       ):
        return self._createPrimitive("cylinder", "{},{}".format(radius, height), **(keywordArguments or {}))

    def createTorus(self, innerRadius: DimensionOrItsFloatOrStringValue, outerRadius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                    ):
        return self._createPrimitive("torus", "{},{}".format(innerRadius, outerRadius), **(keywordArguments or {}))

    def createSphere(self, radius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                     ):
        return self._createPrimitive("uvsphere", "{}".format(radius), **(keywordArguments or {}))

    def createGear(self, outerRadius: DimensionOrItsFloatOrStringValue, addendum: DimensionOrItsFloatOrStringValue, innerRadius: DimensionOrItsFloatOrStringValue, dedendum: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, pressureAngle: AngleOrItsFloatOrStringValue = "20d", numberOfTeeth: 'int' = 12, skewAngle: AngleOrItsFloatOrStringValue = 0, conicalAngle: AngleOrItsFloatOrStringValue = 0, crownAngle: AngleOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        BlenderActions.createGear(
            self.name, outerRadius, addendum, innerRadius, dedendum, height, pressureAngle, numberOfTeeth, skewAngle, conicalAngle, crownAngle
        )

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part("Gear").rename(self.name, True)

        return self

    def clone(self, newName: str, copyLandmarks: bool = True
              ) -> 'Part':

        assert Entity(
            newName).isExists() == False, f"{newName} already exists."

        BlenderActions.duplicateObject(self.name, newName, copyLandmarks)

        return Part(newName, self.description)

    def loft(self, Landmark1: 'Landmark', Landmark2: 'Landmark'
             ):
        raise NotImplementedError()
        return self

    def union(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
              ):
        partName = withPart
        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.UNION,
            partName
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(partName, self.name)

        self._applyModifiersOnly()

        if deleteAfterUnion:
            BlenderActions.removeObject(partName, removeChildren=True)

        return self

    def subtract(self, withPart: PartOrItsName, deleteAfterSubtract: bool = True, isTransferLandmarks: bool = False
                 ):
        partName = withPart
        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.DIFFERENCE,
            partName
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(partName, self.name)

        self._applyModifiersOnly()

        if deleteAfterSubtract:
            BlenderActions.removeObject(partName, removeChildren=True)
        return self

    def intersect(self, withPart: PartOrItsName, deleteAfterIntersect: bool = True, isTransferLandmarks: bool = False
                  ):

        partName = withPart
        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.INTERSECT,
            partName
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(partName, self.name)

        self._applyModifiersOnly()

        if deleteAfterIntersect:
            BlenderActions.removeObject(partName, removeChildren=True)

        return self

    def hollow(self, thicknessX: DimensionOrItsFloatOrStringValue, thicknessY: DimensionOrItsFloatOrStringValue, thicknessZ: DimensionOrItsFloatOrStringValue, startAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False
               ):

        axis = Axis.fromString(startAxis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        startLandmarkLocation = [center, center, center]
        startLandmarkLocation[axis.value] = min if flipAxis else max

        startAxisLandmark = self.createLandmark(
            createUUIDLikeId(), startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        insidePart = self.clone(createUUIDLikeId(), copyLandmarks=False)
        insidePart_start = insidePart.createLandmark(
            "start", startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        thicknessXYZ: list[Dimension] = [dimension for dimension in BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit([
            Dimension.fromString(thicknessX),
            Dimension.fromString(thicknessY),
            Dimension.fromString(thicknessZ),
        ])]

        dimensions = self.getDimensions()
        currentDimensionX: Dimension = dimensions[0]  # type:ignore
        currentDimensionY: Dimension = dimensions[1]  # type:ignore
        currentDimensionZ: Dimension = dimensions[2]  # type:ignore

        def scaleValue(mainDimension: float, thickness: float, subtractBothSides: bool) -> float:
            return (mainDimension-thickness * (2 if subtractBothSides else 1)) / mainDimension

        scaleX: float = scaleValue(
            currentDimensionX.value, thicknessXYZ[0].value, axis.value == 0)
        scaleY = scaleValue(
            currentDimensionY.value, thicknessXYZ[1].value, axis.value == 1)
        scaleZ = scaleValue(
            currentDimensionZ.value, thicknessXYZ[2].value, axis.value == 2)

        BlenderActions.scaleObject(
            insidePart.name, scaleX, scaleY, scaleZ)

        self._applyRotationAndScaleOnly()

        Joint(startAxisLandmark, insidePart_start).translateLandmarkOntoAnother()

        self.subtract(insidePart, isTransferLandmarks=False)

        startAxisLandmark.delete()

        return self._applyModifiersOnly()

    def thicken(self, radius: DimensionOrItsFloatOrStringValue) -> 'Part':

        radius = Dimension.fromString(radius)

        BlenderActions.applySolidifyModifier(
            self.name, radius)

        return self._applyModifiersOnly()

    def hole(self, holeLandmark: LandmarkOrItsName, radius: DimensionOrItsFloatOrStringValue, depth: DimensionOrItsFloatOrStringValue, normalAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False, initialRotationX: AngleOrItsFloatOrStringValue = 0.0, initialRotationY: AngleOrItsFloatOrStringValue = 0.0, initialRotationZ: AngleOrItsFloatOrStringValue = 0.0, mirrorAboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, mirrorAxis: AxisOrItsIndexOrItsName = "x", mirror: bool = False, circularPatternInstanceCount: 'int' = 1, circularPatternInstanceSeparation: AngleOrItsFloatOrStringValue = 0.0, circularPatternInstanceAxis: AxisOrItsIndexOrItsName = "z", circularPatternAboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, linearPatternInstanceCount: 'int' = 1, linearPatternInstanceSeparation: DimensionOrItsFloatOrStringValue = 0.0, linearPatternInstanceAxis: AxisOrItsIndexOrItsName = "x", linearPattern2ndInstanceCount: 'int' = 1, linearPattern2ndInstanceSeparation: DimensionOrItsFloatOrStringValue = 0.0, linearPattern2ndInstanceAxis: AxisOrItsIndexOrItsName = "y"):

        axis = Axis.fromString(normalAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        hole = Part(createUUIDLikeId()).createCylinder(radius, depth)
        hole_head = hole.createLandmark(
            "hole", center, center, min if flipAxis else max)

        axisRotation = Angle(-90, AngleUnit.DEGREES)

        if axis is Axis.X:
            initialRotationY = (axisRotation+initialRotationY).value
        elif axis is Axis.Y:
            initialRotationX = (axisRotation+initialRotationX).value
        hole.rotateXYZ(initialRotationX, initialRotationY, initialRotationZ)

        Joint(holeLandmark, hole_head).limitLocationX(0, 0)
        Joint(holeLandmark, hole_head).limitLocationY(0, 0)
        Joint(holeLandmark, hole_head).limitLocationZ(0, 0)

        if circularPatternInstanceCount > 1:
            circularPatternAboutEntityOrLandmark = circularPatternAboutEntityOrLandmark or self
            instanceSeparation = 360.0 / \
                float(
                    circularPatternInstanceCount) if circularPatternInstanceSeparation == 0 else circularPatternInstanceSeparation
            hole.circularPattern(
                circularPatternInstanceCount, instanceSeparation, circularPatternAboutEntityOrLandmark, circularPatternInstanceAxis)

        if linearPatternInstanceCount > 1:
            hole.linearPattern(
                linearPatternInstanceCount, linearPatternInstanceSeparation, linearPatternInstanceAxis)

        if linearPattern2ndInstanceCount > 1:
            hole.linearPattern(
                linearPattern2ndInstanceCount, linearPattern2ndInstanceSeparation, linearPattern2ndInstanceAxis)

        if mirror and mirrorAboutEntityOrLandmark:
            hole.mirror(mirrorAboutEntityOrLandmark, mirrorAxis,
                        resultingMirroredEntityName=None)

        self.subtract(hole, deleteAfterSubtract=True,
                      isTransferLandmarks=False)
        return self._applyModifiersOnly()

    def setMaterial(self, materialName: MaterialOrItsName
                    ):
        material = materialName

        if isinstance(material, str):
            material = Material(material)

        material.assignToPart(self.name)
        return self

    def isCollidingWithPart(self, otherPart: PartOrItsName
                            ):
        otherPartName = otherPart
        if isinstance(otherPartName, CodeToCADInterface.Part):
            otherPartName = otherPartName.name

        if otherPartName == self.name:
            raise NameError(
                "Collision must be checked between different Parts.")

        return BlenderActions.isCollisionBetweenTwoObjects(self.name, otherPartName)

    def filletAllEdges(self, radius: DimensionOrItsFloatOrStringValue, useWidth: bool = False
                       ):
        return self.bevel(
            radius,
            chamfer=False,
            useWidth=useWidth
        )

    def filletEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        return self.bevel(
            radius,
            bevelEdgesNearlandmarkNames=landmarksNearEdges,
            chamfer=False,
            useWidth=useWidth
        )

    def filletFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        return self.bevel(
            radius,
            bevelFacesNearlandmarkNames=landmarksNearFaces,
            chamfer=False,
            useWidth=useWidth
        )

    def chamferAllEdges(self, radius: DimensionOrItsFloatOrStringValue
                        ):
        return self.bevel(
            radius,
            chamfer=True,
            useWidth=False
        )

    def chamferEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName]
                     ):
        return self.bevel(
            radius,
            bevelEdgesNearlandmarkNames=landmarksNearEdges,
            chamfer=True,
            useWidth=False
        )

    def chamferFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName]
                     ):
        return self.bevel(
            radius,
            bevelFacesNearlandmarkNames=landmarksNearFaces,
            chamfer=True,
            useWidth=False
        )

    def _addEdgesNearLandmarksToVertexGroup(self, bevelEdgesNearlandmarkNames: list[LandmarkOrItsName], vertexGroupName):

        kdTree = BlenderActions.createKdTreeForObject(self.name)
        vertexGroupObject = BlenderActions.createObjectVertexGroup(
            self.name, vertexGroupName)

        for landmarkOrItsName in bevelEdgesNearlandmarkNames:
            landmark = self.getLandmark(landmarkOrItsName) if isinstance(
                landmarkOrItsName, str) else landmarkOrItsName
            vertexIndecies = [index for (_, index, _) in BlenderActions.getClosestPointsToVertex(self.name, [
                dimension.value for dimension in landmark.getLocationWorld().toList()], numberOfPoints=2, objectKdTree=kdTree)]

            assert len(
                vertexIndecies) == 2, f"Could not find edges near landmark {landmark.getLandmarkEntityName()}"

            BlenderActions.addVerticiesToVertexGroup(
                vertexGroupObject, vertexIndecies)

    def _addFacesNearLandmarksToVertexGroup(self, bevelFacesNearlandmarkNames: list[LandmarkOrItsName], vertexGroupName):
        vertexGroupObject = BlenderActions.createObjectVertexGroup(
            self.name, vertexGroupName)

        for landmarkOrItsName in bevelFacesNearlandmarkNames:
            landmark = self.getLandmark(landmarkOrItsName) if isinstance(
                landmarkOrItsName, str) else landmarkOrItsName

            blenderPolygon = BlenderActions.getClosestFaceToVertex(
                self.name, [dimension.value for dimension in landmark.getLocationWorld().toList()])

            faceIndecies: list[int] = blenderPolygon.vertices  # type: ignore

            BlenderActions.addVerticiesToVertexGroup(
                vertexGroupObject, faceIndecies)

    def bevel(self,
              radius: DimensionOrItsFloatOrStringValue,
              bevelEdgesNearlandmarkNames: Optional[list[LandmarkOrItsName]] = None,
              bevelFacesNearlandmarkNames: Optional[list[LandmarkOrItsName]] = None,
              useWidth=False,
              chamfer=False,
              keywordArguments: Optional[dict] = None
              ):
        vertexGroupName = None

        if bevelEdgesNearlandmarkNames is not None:
            vertexGroupName = createUUIDLikeId()
            self._addEdgesNearLandmarksToVertexGroup(
                bevelEdgesNearlandmarkNames, vertexGroupName)

        if bevelFacesNearlandmarkNames is not None:
            vertexGroupName = vertexGroupName or createUUIDLikeId()
            self._addFacesNearLandmarksToVertexGroup(
                bevelFacesNearlandmarkNames, vertexGroupName)

        radiusDimension = Dimension.fromString(radius)

        radiusDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            radiusDimension)

        BlenderActions.applyBevelModifier(
            self.name,
            radiusDimension,
            vertexGroupName=vertexGroupName,
            useEdges=True,
            useWidth=useWidth,
            chamfer=chamfer,
            **(keywordArguments or {})
        )

        return self._applyModifiersOnly()

    def selectVertexNearLandmark(self, landmarkName: Optional[LandmarkOrItsName] = None
                                 ):

        raise NotImplementedError()
        return self

    def selectEdgeNearLandmark(self, landmarkName: Optional[LandmarkOrItsName] = None
                               ):

        raise NotImplementedError()
        return self

    def selectFaceNearLandmark(self, landmarkName: Optional[LandmarkOrItsName] = None
                               ):

        raise NotImplementedError()
        return self


class Sketch(Entity, CodeToCADInterface.Sketch):

    name: str
    curveType: Optional['CurveTypes'] = None
    description: Optional[str] = None

    def __init__(self, name: str, curveType: Optional['CurveTypes'] = None, description: Optional[str] = None):
        self.name = name
        self.curveType = curveType
        self.description = description

    def clone(self, newName: str, copyLandmarks: bool = True
              ) -> 'Sketch':

        assert Entity(
            newName).isExists() == False, f"{newName} already exists."

        BlenderActions.duplicateObject(self.name, newName, copyLandmarks)

        return Sketch(newName, self.curveType, self.description)

    def revolve(self, angle: AngleOrItsFloatOrStringValue, aboutEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName = "z") -> 'Part':

        if isinstance(aboutEntityOrLandmark, Entity):
            aboutEntityOrLandmark = aboutEntityOrLandmark.name

        axis = Axis.fromString(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        BlenderActions.applyScrewModifier(self.name, Angle.fromString(
            angle).toRadians(), axis, entityNameToDetermineAxis=aboutEntityOrLandmark)

        BlenderActions.createMeshFromCurve(
            self.name)

        return Part(self.name, self.description).apply()

    def offset(self, radius: DimensionOrItsFloatOrStringValue):

        radius = Dimension.fromString(radius)

        BlenderActions.offsetCurveGeometry(
            self.name, radius)

        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> 'Part':

        BlenderActions.extrudeCurve(
            self.name, Dimension.fromString(length))

        BlenderActions.createMeshFromCurve(
            self.name)

        return Part(self.name, self.description).apply()

    def sweep(self, profileNameOrInstance: SketchOrItsName, fillCap: bool = True) -> 'Part':
        profileCurveName = profileNameOrInstance
        if isinstance(profileCurveName, CodeToCADInterface.Sketch):
            profileCurveName = profileCurveName.name

        BlenderActions.addBevelObjectToCurve(
            self.name, profileCurveName, fillCap)

        BlenderActions.createMeshFromCurve(
            self.name)

        # Recalculate normals because they're usually wrong after sweeping.
        BlenderActions.recalculateNormals(self.name)

        return Part(self.name, self.description).apply()

    def profile(self,
                profileCurveName
                ):

        if isinstance(profileCurveName, Entity):
            profileCurveName = profileCurveName.name

        BlenderActions.applyCurveModifier(self.name, profileCurveName)

        return self

    def createText(self, text: str, fontSize: DimensionOrItsFloatOrStringValue = 1.0, bold: bool = False, italic: bool = False, underlined: bool = False, characterSpacing: 'int' = 1, wordSpacing: 'int' = 1, lineSpacing: 'int' = 1, fontFilePath: Optional[str] = None
                   ):
        size = Dimension.fromString(fontSize)

        BlenderActions.createText(self.name, text, size, bold, italic, underlined,
                                  characterSpacing, wordSpacing, lineSpacing, fontFilePath)
        return self

    def createFromVertices(self, coordinates: list[PointOrListOfFloatOrItsStringValue], interpolation: 'int' = 64
                           ):
        BlenderActions.create3DCurve(self.name, BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(
            self.curveType) if self.curveType is not None else BlenderDefinitions.BlenderCurveTypes.BEZIER, coordinates, interpolation)

        return self

    @staticmethod
    def _createPrimitiveDecorator(curvePrimitiveType: CurvePrimitiveTypes):
        def decorator(primitiveFunction):
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = BlenderDefinitions.BlenderCurvePrimitiveTypes.fromCurvePrimitiveTypes(
                    curvePrimitiveType)

                blenderPrimitiveFunction = BlenderActions.getBlenderCurvePrimitiveFunction(
                    blenderCurvePrimitiveType)

                keywordArgs = dict(
                    {
                        "curveType": BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType is not None else None},
                    **kwargs
                )

                blenderPrimitiveFunction(
                    *args[1:],
                    **keywordArgs
                )

                # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
                # therefore, we'll use the object's "expected" name and rename it to what it should be
                # note: this will fail if the "expected" name is incorrect
                curve = Sketch(
                    blenderCurvePrimitiveType.name).rename(self.name)

                BlenderActions.setCurveUsePath(self.name, False)

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Point)
    def createPoint(self, coordinate: PointOrListOfFloatOrItsStringValue
                    ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Line)
    def createLine(self, length: DimensionOrItsFloatOrStringValue, angleX: AngleOrItsFloatOrStringValue = 0.0, angleY: AngleOrItsFloatOrStringValue = 0.0, symmetric: bool = False
                   ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.LineTo)
    def createLineBetweenPoints(self, endAt: PointOrListOfFloatOrItsStringValue, startAt: Optional[PointOrListOfFloatOrItsStringValue] = None
                                ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Circle)
    def createCircle(self, radius: DimensionOrItsFloatOrStringValue
                     ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Ellipse)
    def createEllipse(self, radiusA: DimensionOrItsFloatOrStringValue, radiusB: DimensionOrItsFloatOrStringValue
                      ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Arc)
    def createArc(self, radius: DimensionOrItsFloatOrStringValue, angle: AngleOrItsFloatOrStringValue = "180d"
                  ):
        return self

    def createArcBetweenThreePoints(self, pointA: 'Point', pointB: 'Point', centerPoint: 'Point'
                                    ):
        raise NotImplementedError()
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Segment)
    def createSegment(self, innerRadius: DimensionOrItsFloatOrStringValue, outerRadius: DimensionOrItsFloatOrStringValue, angle: AngleOrItsFloatOrStringValue = "180d"
                      ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Rectangle)
    def createRectangle(self, length: DimensionOrItsFloatOrStringValue, width: DimensionOrItsFloatOrStringValue
                        ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Polygon_ab)
    def createPolygon(self, numberOfSides: 'int', length: DimensionOrItsFloatOrStringValue, width: DimensionOrItsFloatOrStringValue
                      ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Trapezoid)
    def createTrapezoid(self, lengthUpper: DimensionOrItsFloatOrStringValue, lengthLower: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue
                        ):
        return self

    @_createPrimitiveDecorator(CurvePrimitiveTypes.Spiral)
    def createSpiral(self, numberOfTurns: 'int', height: DimensionOrItsFloatOrStringValue, radius: DimensionOrItsFloatOrStringValue, isClockwise: bool = True, radiusEnd: Optional[DimensionOrItsFloatOrStringValue] = None):

        return self


class Landmark(CodeToCADInterface.Landmark):

    name: str
    parentEntity: EntityOrItsName
    description: Optional[str] = None

    def __init__(self, name: str, parentEntity: EntityOrItsName, description: Optional[str] = None):
        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    def getLandmarkEntityName(self
                              ) -> str:
        parentEntityName = self.parentEntity

        if isinstance(parentEntityName, CodeToCADInterface.Entity):
            parentEntityName = parentEntityName.name

        entityName = formatLandmarkEntityName(
            parentEntityName, self.name)

        return entityName

    def getParentEntity(self
                        ) -> 'CodeToCADInterface.Entity':

        if isinstance(self.parentEntity, str):
            return Entity(self.parentEntity)

        return self.parentEntity

    def isExists(self) -> bool:
        try:
            return BlenderActions.getObject(self.getLandmarkEntityName()) is not None
        except:
            return False

    def rename(self, newName: str
               ):

        assert Landmark(newName, self.parentEntity).isExists(
        ) == False, f"{newName} already exists."

        parentEntityName = self.parentEntity
        if isinstance(parentEntityName, CodeToCADInterface.Entity):
            parentEntityName = parentEntityName.name

        BlenderActions.updateObjectName(self.getLandmarkEntityName(
        ), formatLandmarkEntityName(parentEntityName, newName))

        self.name = newName

        return self

    def delete(self):
        BlenderActions.removeObject(self.getLandmarkEntityName())
        return self

    def isVisible(self
                  ) -> bool:
        return BlenderActions.getObjectVisibility(self.getLandmarkEntityName())

    def setVisible(self, isVisible: bool
                   ):

        BlenderActions.setObjectVisibility(
            self.getLandmarkEntityName(), isVisible)

        return self

    def getNativeInstance(self
                          ):

        return BlenderActions.getObject(self.getLandmarkEntityName())

    def getLocationWorld(self
                         ) -> 'Point':

        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectWorldLocation(self.getLandmarkEntityName())

    def getLocationLocal(self
                         ) -> 'Point':

        BlenderActions.updateViewLayer()
        return BlenderActions.getObjectLocalLocation(self.getLandmarkEntityName())

    def select(self
               ):
        BlenderActions.selectObject(self.getLandmarkEntityName())
        return self


class Joint(CodeToCADInterface.Joint):

    entity1: EntityOrItsNameOrLandmark
    entity2: EntityOrItsNameOrLandmark

    def __init__(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    def translateLandmarkOntoAnother(self
                                     ):
        if not isinstance(self.entity1, Landmark) or not isinstance(self.entity2, Landmark):
            raise TypeError("Entities 1 and 2 should be landmarks.")

        landmark1: Landmark = self.entity1
        landmark2: Landmark = self.entity2
        entityForLandmark2 = self.entity2.getParentEntity()

        translation = landmark1.getLocationWorld() - landmark2.getLocationWorld()

        entityForLandmark2.translateXYZ(
            translation.x, translation.y, translation.z)

        return self

    @staticmethod
    def _getEntityOrLandmarkName(entityOrLandmark) -> str:
        if isinstance(entityOrLandmark, str):
            return entityOrLandmark
        elif isinstance(entityOrLandmark, Entity):
            return entityOrLandmark.name
        elif isinstance(entityOrLandmark, Landmark):
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

        if isinstance(objectToLimitName, CodeToCADInterface.Entity):
            objectToLimitName = objectToLimitName.name
        elif isinstance(objectToLimitName, CodeToCADInterface.Landmark):

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
        if isinstance(objectToLimitName, CodeToCADInterface.Entity):
            objectToLimitName = objectToLimitName.name
        elif isinstance(objectToLimitName, CodeToCADInterface.Landmark):
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


class Material(CodeToCADInterface.Material):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

        try:
            BlenderActions.getMaterial(self.name)
        except:
            BlenderActions.createMaterial(self.name)

    def assignToPart(self, partName: PartOrItsName
                     ):
        if isinstance(partName, CodeToCADInterface.Part):
            partName = partName.name
        BlenderActions.setMaterialToObject(self.name, partName)
        return self

    def setColor(self, rValue: IntOrFloat, gValue: IntOrFloat, bValue: IntOrFloat, aValue: IntOrFloat = 1.0
                 ):
        BlenderActions.setMaterialColor(
            self.name, rValue, gValue, bValue, aValue)
        return self

    def setReflectivity(self, reflectivity: float):

        BlenderActions.setMaterialMetallicness(self.name, reflectivity)

        return self

    def setRoughness(self, roughness: float):

        BlenderActions.setMaterialRoughness(self.name, roughness)

        return self

    def addImageTexture(self, imageFilePath: str
                        ):
        absoluteFilePath = getAbsoluteFilepath(imageFilePath)

        BlenderActions.addTextureToMaterial(self.name, absoluteFilePath)
        return self


class Light(CodeToCADInterface.Light):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def createSun(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="SUN")
        return self

    def createPoint(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="POINT")
        return self

    def createSpot(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="SPOT")
        return self

    def createArea(self, energyLevel=100):
        BlenderActions.createLight(self.name, energyLevel, type="AREA")
        return self

    def setColor(self, rValue, gValue, bValue):
        BlenderActions.setLightColor(
            self.name, rValue, gValue, bValue)
        return self

    def translateXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                     ):

        Entity(self.name).translateXYZ(x, y, z)

        return self

    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):

        xAngle = Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Angle.fromAngleOrItsFloatOrStringValue(z)

        BlenderActions.rotateObject(
            self.name, [xAngle, yAngle, zAngle], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self

    def isExists(self
                 ) -> bool:

        return Entity(self.name).isExists()

    def rename(self, newName: str
               ):

        Entity(self.name).rename(newName, False)

        self.name = newName

        return self

    def delete(self):

        Entity(self.name).delete(False)

        return self

    def getNativeInstance(self
                          ):

        return Entity(self.name).getNativeInstance()

    def getLocationWorld(self
                         ) -> 'Point':

        return Entity(self.name).getLocationWorld()

    def getLocationLocal(self
                         ) -> 'Point':

        return Entity(self.name).getLocationLocal()

    def select(self
               ):

        Entity(self.name).select()

        return self


class Camera(CodeToCADInterface.Camera):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def createPerspective(self):
        BlenderActions.createCamera(self.name, type="PERSP")
        return self

    def createOrthogonal(self):
        BlenderActions.createCamera(self.name, type="ORTHO")
        return self

    def createPanoramic(self):
        BlenderActions.createCamera(self.name, type="PANO")
        return self

    def setFocalLength(self, length):
        BlenderActions.setFocalLength(self.name, length)
        return self

    def translateXYZ(self, x: DimensionOrItsFloatOrStringValue, y: DimensionOrItsFloatOrStringValue, z: DimensionOrItsFloatOrStringValue
                     ):

        Entity(self.name).translateXYZ(x, y, z)

        return self

    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):

        xAngle = Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Angle.fromAngleOrItsFloatOrStringValue(z)

        BlenderActions.rotateObject(
            self.name, [xAngle, yAngle, zAngle], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self

    def isExists(self
                 ) -> bool:

        return Entity(self.name).isExists()

    def rename(self, newName: str
               ):

        Entity(self.name).rename(newName, False)

        self.name = newName

        return self

    def delete(self):

        Entity(self.name).delete(False)

        return self

    def getNativeInstance(self
                          ):

        return Entity(self.name).getNativeInstance()

    def getLocationWorld(self
                         ) -> 'Point':

        return Entity(self.name).getLocationWorld()

    def getLocationLocal(self
                         ) -> 'Point':

        return Entity(self.name).getLocationLocal()

    def select(self
               ):

        Entity(self.name).select()

        return self


class Animation(CodeToCADInterface.Animation):

    def __init__(self):
        pass

    @staticmethod
    def default(
    ) -> 'Animation':
        return Animation()

    def setFrameStart(self, frameNumber: 'int'
                      ):

        BlenderActions.setFrameStart(frameNumber, None)

        return self

    def setFrameEnd(self, frameNumber: 'int'
                    ):

        BlenderActions.setFrameEnd(frameNumber, None)

        return self

    def setFrameCurrent(self, frameNumber: 'int'
                        ):

        BlenderActions.setFrameCurrent(frameNumber, None)

        return self

    def createKeyFrameLocation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):
        partName = entity

        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name

        BlenderActions.addKeyframeToObject(
            partName, frameNumber, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE.value)

        return self

    def createKeyFrameRotation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):
        partName = entity

        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name

        BlenderActions.addKeyframeToObject(
            partName, frameNumber, BlenderDefinitions.BlenderRotationTypes.EULER.value)

        return self


class Render(CodeToCADInterface.Render):

    @staticmethod
    def _setFileFormat(outputFilePath: str):
        fileFormat = BlenderDefinitions.FileFormat.fromUtilitiesFileFormat(
            FileFormats.fromString(getFileExtension(outputFilePath)))
        BlenderActions.setRenderFileFormat(fileFormat)

    def renderImage(self, outputFilePath: str, overwrite: bool = True, fileType: Optional[str] = None):

        absoluteFilePath = getAbsoluteFilepath(outputFilePath)

        Render._setFileFormat(absoluteFilePath)

        BlenderActions.renderImage(absoluteFilePath, overwrite or True)

        return self

    def renderVideoMp4(self, outputFilePath: str, startFrameNumber: 'int' = 1, endFrameNumber: 'int' = 100, stepFrames: 'int' = 1, overwrite: bool = True):

        absoluteFilePath = getAbsoluteFilepath(outputFilePath)

        Render._setFileFormat(absoluteFilePath)

        BlenderActions.renderAnimation(absoluteFilePath, overwrite or True)
        return self

    def renderVideoFrames(self, outputFolderPath: str, fileNamePrefix: str, startFrameNumber: 'int' = 1, endFrameNumber: 'int' = 100, stepFrames: 'int' = 1, overwrite: bool = True, fileType: Optional[str] = None):

        absoluteFilePath = getAbsoluteFilepath(outputFolderPath)

        raise NotImplementedError()
        return self

    def setFrameRate(self, frameRate: int):

        BlenderActions.setRenderFrameRate(int(frameRate))

        return self

    def setResolution(self, x: 'int', y: 'int'):
        BlenderActions.setRenderResolution(x, y)
        return self

    def setRenderQuality(self, quality: int):

        percentage = quality * 100 if quality < 1.0 else quality
        percentage = int(percentage)
        BlenderActions.setRenderQuality(percentage)

        return self

    def setRenderEngine(self, name: str):

        BlenderActions.setRenderEngine(
            BlenderDefinitions.RenderEngines.fromString(name))

        return self

    def setCamera(self, cameraNameOrInstance: CameraOrItsName):

        cameraName = cameraNameOrInstance
        if isinstance(cameraName, CodeToCADInterface.Camera):
            cameraName = cameraName.name

        BlenderActions.setSceneCamera(cameraName)

        return self


class Scene(CodeToCADInterface.Scene):

    # Blender's default Scene name is "Scene"
    name: str = "Scene"
    description: Optional[str] = None

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.name
        self.description = description

    @staticmethod
    def default(
    ) -> 'Scene':
        return Scene()

    def create(self
               ):
        raise NotImplementedError()
        return self

    def delete(self
               ):
        raise NotImplementedError()
        return self

    def getSelectedEntity(self) -> 'Entity':

        return Entity(BlenderActions.getSelectedObjectName())

    def export(self, filePath: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        for entity in entities:
            part = entity
            if isinstance(part, str):
                part = Part(part)
            part.export(filePath, overwrite, scale)
        return self

    def setDefaultUnit(self, unit: LengthUnitOrItsName
                       ):
        if isinstance(unit, str):
            unit = LengthUnit.fromString(unit)

        blenderUnit = BlenderDefinitions.BlenderLength.fromLengthUnit(unit)

        BlenderActions.setDefaultUnit(blenderUnit, self.name)
        return self

    def createGroup(self, name: str
                    ):
        BlenderActions.createCollection(name, self.name)
        return self

    def deleteGroup(self, name: str, removeChildren: bool
                    ):
        BlenderActions.removeCollection(
            name=name,
            sceneName=self.name,
            removeChildren=removeChildren
        )
        return self

    def removeFromGroup(self, entityName: str, groupName: str
                        ):
        if isinstance(entityName, Entity):
            entityName = entityName.name

        BlenderActions.removeObjectFromCollection(
            existingObjectName=entityName,
            collectionName=groupName,
            sceneName=self.name
        )
        return self

    def assignToGroup(self, entities: list[EntityOrItsName], groupName: str, removeFromOtherGroups: Optional[bool] = True
                      ):
        for entity in entities:
            entityName = entity
            if isinstance(entityName, CodeToCADInterface.Entity):
                entityName = entityName.name

            BlenderActions.assignObjectToCollection(
                entityName, groupName, self.name, removeFromOtherGroups or True)

        return self

    def setVisible(self, entities: list[EntityOrItsName], isVisible: bool
                   ):

        for entity in entities:
            if isinstance(entity, CodeToCADInterface.Entity):
                entity = entity.name

            BlenderActions.setObjectVisibility(entity, isVisible)

        return self

    def setBackgroundImage(self, filePath: str, locationX: Optional[DimensionOrItsFloatOrStringValue] = 0, locationY: Optional[DimensionOrItsFloatOrStringValue] = 0):

        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.addHDRTexture(self.name, absoluteFilePath)

        x = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(locationX or 0)).value
        y = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            Dimension.fromString(locationY or 0)).value

        BlenderActions.setBackgroundLocation(self.name, x, y)

        return self


class Analytics(CodeToCADInterface.Analytics):

    def __init__(self):
        pass

    @staticmethod
    def _getEntityFromNameOrLandmark(entityOrLandmark: EntityOrItsNameOrLandmark) -> Union[CodeToCADInterface.Entity, CodeToCADInterface.Landmark]:
        if isinstance(entityOrLandmark, str):
            return Entity(entityOrLandmark)
        return entityOrLandmark

    def measureDistance(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark
                        ) -> 'Dimensions':
        distance = Analytics._getEntityFromNameOrLandmark(entity2).getLocationWorld(
        ) - Analytics._getEntityFromNameOrLandmark(entity1).getLocationWorld()
        return Dimensions.fromPoint(distance)

    def measureAngle(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark, pivot: Optional[EntityOrItsNameOrLandmark] = None
                     ) -> 'list[Angle]':
        raise NotImplementedError()

    def getWorldPose(self, entity: EntityOrItsName
                     ) -> 'list[float]':
        partName = entity
        if isinstance(partName, CodeToCADInterface.Entity):
            partName = partName.name
        return BlenderActions.getObjectWorldPose(partName)

    def getBoundingBox(self, entityName: EntityOrItsName
                       ) -> 'BoundaryBox':
        entity = entityName
        if isinstance(entity, str):
            entity = Entity(entity)

        return entity.getBoundingBox()

    def getDimensions(self, entityName: EntityOrItsName
                      ) -> 'Dimensions':
        if isinstance(entityName, Entity):
            return entityName.getDimensions()
        if isinstance(entityName, str):
            return Entity(entityName).getDimensions()
        raise TypeError("entityName must be a string or an Entity")

    def log(self, message):
        BlenderActions.logMessage(message)
        return self
