# This file was forked from core/CodeToCADProvider.py

import math
from typing import Optional, Union

import BlenderActions
import BlenderDefinitions

import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities
from core.CodeToCADInterface import FloatOrItsStringValue, IntOrFloat, MaterialOrItsName, PartOrItsName, EntityOrItsName, LandmarkOrItsName, AxisOrItsIndexOrItsName, DimensionOrItsFloatOrStringValue, AngleOrItsFloatOrStringValue, EntityOrItsNameOrLandmark, PointOrListOfFloatOrItsStringValue, LengthUnitOrItsName
from core.utilities import (Angle, BoundaryAxis, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, Point, center, createUUIDLikeId,
                            getAbsoluteFilepath, getFilename, max, min)


if BlenderActions.getBlenderVersion() and BlenderActions.getBlenderVersion() < BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value:
    print(
        f"CodeToCAD BlenderProvider only supports Blender versions {'.'.join(tuple, BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value)}+. You are running version {'.'.join(BlenderActions.getBlenderVersion())}")  # type: ignore


def injectBlenderProvider(globalContext: Optional[dict]) -> None:
    from CodeToCAD import setPartProvider, setSketchProvider, setMaterialProvider, setLandmarkProvider, setJointProvider, setAnimationProvider, setSceneProvider, setAnalyticsProvider

    setPartProvider(Part, globalContext)
    setSketchProvider(Sketch, globalContext)
    setMaterialProvider(Material, globalContext)
    setLandmarkProvider(Landmark, globalContext)
    setJointProvider(Joint, globalContext)
    setAnimationProvider(Animation, globalContext)
    setSceneProvider(Scene, globalContext)
    setAnalyticsProvider(Analytics, globalContext)


class Entity(CodeToCADInterface.Entity):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def isExists(self
                 ) -> bool:
        try:
            return BlenderActions.getObject(self.name) != None
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

    def apply(self
              ):

        BlenderActions.updateViewLayer()

        BlenderActions.applyDependencyGraph(self.name)

        BlenderActions.removeMesh(self.name)

        BlenderActions.updateObjectDataName(self.name, self.name)

        BlenderActions.clearModifiers(self.name)

        return self

    def getNativeInstance(self
                          ):
        return BlenderActions.getObject(self.name)

    def getLocationWorld(self
                         ) -> 'Point':
        BlenderActions.updateViewLayer()
        return Utilities.Point.fromList(
            [Dimension(value, BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)  # type: ignore
             for value in BlenderActions.getObjectWorldLocation(self.name)]
        )

    def getLocationLocal(self
                         ) -> 'Point':
        BlenderActions.updateViewLayer()
        return Utilities.Point.fromList(
            [Dimension(value, BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)  # type: ignore
             for value in BlenderActions.getObjectLocalLocation(self.name)]
        )

    def select(self):
        BlenderActions.selectObject(self.name)
        return self

    def export(self, filePath: str, overwrite: bool = True, scale: float = 1.0
               ):
        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.exportObject(
            self.name, absoluteFilePath, overwrite, scale)
        return self

    def clone(self, newName: str, copyLandmarks: bool = True
              ):

        assert Entity(
            newName).isExists() == False, f"{newName} already exists."

        BlenderActions.duplicateObject(self.name, newName, copyLandmarks)

        return self

    def mirror(self, mirrorAcrossEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName, resultingMirroredEntityName: Optional[str]
               ):

        if resultingMirroredEntityName != None:
            raise NotImplementedError("Not yet supported. COD-113")

        mirrorAcrossEntityName = mirrorAcrossEntityOrLandmark
        if isinstance(mirrorAcrossEntityOrLandmark, Landmark):
            mirrorAcrossEntityName = mirrorAcrossEntityOrLandmark.getLandmarkEntityName()
        elif isinstance(mirrorAcrossEntityOrLandmark, Entity):
            mirrorAcrossEntityName = mirrorAcrossEntityOrLandmark.name

        axis = Utilities.Axis.fromString(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        BlenderActions.applyMirrorModifier(
            self.name, mirrorAcrossEntityName, axis)

        return self

    def linearPattern(self, instanceCount: 'int', offset: DimensionOrItsFloatOrStringValue, directionAxis: AxisOrItsIndexOrItsName = "z"):

        axis = Utilities.Axis.fromString(directionAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        offsetAmount: float = offset  # type: ignore
        if isinstance(offset, str):
            offset = Utilities.Dimension.fromString(offset)

        if isinstance(offset, Utilities.Dimension):
            offset = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
                offset)
            offsetAmount = offset.value

        BlenderActions.applyLinearPattern(
            self.name, instanceCount, axis, offsetAmount)

        return self

    def circularPattern(self, instanceCount: 'int', separationAngle: AngleOrItsFloatOrStringValue, centerEntityOrLandmark: EntityOrItsNameOrLandmark, normalDirectionAxis: AxisOrItsIndexOrItsName = "z"):
        centerEntityOrLandmarkName = centerEntityOrLandmark
        if isinstance(centerEntityOrLandmark, Landmark):
            centerEntityOrLandmarkName = centerEntityOrLandmark.getLandmarkEntityName()
        elif isinstance(centerEntityOrLandmark, Entity):
            centerEntityOrLandmarkName = centerEntityOrLandmark.name

        pivotLandmarkName = createUUIDLikeId()

        self.createLandmark(pivotLandmarkName, 0, 0, 0)

        pivotLandmarkEntityName = self.getLandmark(
            pivotLandmarkName).getLandmarkEntityName()

        BlenderActions.applyPivotConstraint(
            pivotLandmarkEntityName, centerEntityOrLandmarkName)

        axis = Utilities.Axis.fromString(normalDirectionAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        angles: list[Optional[Angle]] = [Utilities.Angle(0) for _ in range(3)]
        angle: Angle = separationAngle  # type: ignore
        if isinstance(separationAngle, str):
            angle = Utilities.Angle.fromString(separationAngle)
        elif isinstance(separationAngle, (float, int)):
            angle = Utilities.Angle(separationAngle)

        angles[axis.value] = angle

        BlenderActions.rotateObject(
            pivotLandmarkEntityName, angles, BlenderDefinitions.BlenderRotationTypes.EULER)

        BlenderActions.applyCircularPattern(
            self.name, instanceCount, pivotLandmarkEntityName)

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

        xDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            x, boundingBox.x)  # type: ignore
        yDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            y, boundingBox.y)  # type: ignore
        zDimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            z, boundingBox.z)  # type: ignore

        BlenderActions.translateObject(
            self.name, [xDimension, yDimension, zDimension], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateX(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.x)  # type: ignore

        BlenderActions.translateObject(
            self.name, [dimension, Dimension(0), Dimension(0)], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateY(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.y)  # type: ignore

        BlenderActions.translateObject(
            self.name, [Dimension(0), dimension, Dimension(0)], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateZ(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Entity._translationDimensionFromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.z)  # type: ignore

        BlenderActions.translateObject(
            self.name, [Dimension(0), Dimension(0), dimension], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

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
        return self

    def scaleX(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().x.value)
        BlenderActions.scaleObject(self.name, scaleFactor, None, None)
        return self

    def scaleY(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().y.value)
        BlenderActions.scaleObject(self.name, None, scaleFactor, None)
        return self

    def scaleZ(self, scale: DimensionOrItsFloatOrStringValue
               ):
        scaleFactor = Entity._scaleFactorFromDimensionOrItsFloatOrStringValue(
            scale, self.getDimensions().z.value)
        BlenderActions.scaleObject(self.name, None, None, scaleFactor)
        return self

    def scaleXByFactor(self, scaleFactor: float
                       ):
        return self.scaleX(scaleFactor)

    def scaleYByFactor(self, scaleFactor: float
                       ):
        return self.scaleY(scaleFactor)

    def scaleZByFactor(self, scaleFactor: float
                       ):
        return self.scaleZ(scaleFactor)

    def scaleKeepAspectRatio(self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
                             ):
        scale = Utilities.Dimension.fromDimensionOrItsFloatOrStringValue(
            scale, None)
        valueInBlenderDefaultLength = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            scale)

        dimensionInAxis = self.getDimensions(
        )[Utilities.Axis.fromString(axis).value]
        scaleFactor: float = (
            valueInBlenderDefaultLength / dimensionInAxis).value

        BlenderActions.scaleObject(
            self.name, scaleFactor, scaleFactor, scaleFactor)
        return self

    def rotateXYZ(self, x: AngleOrItsFloatOrStringValue, y: AngleOrItsFloatOrStringValue, z: AngleOrItsFloatOrStringValue
                  ):

        xAngle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(x)
        yAngle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(y)
        zAngle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(z)

        BlenderActions.rotateObject(
            self.name, [xAngle, yAngle, zAngle], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self

    def rotateX(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [angle, None, None], BlenderDefinitions.BlenderRotationTypes.EULER)

        return self

    def rotateY(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [None, angle, None], BlenderDefinitions.BlenderRotationTypes.EULER)
        return self

    def rotateZ(self, rotation: AngleOrItsFloatOrStringValue
                ):
        angle = Utilities.Angle.fromAngleOrItsFloatOrStringValue(rotation)

        BlenderActions.rotateObject(
            self.name, [None, None, angle], BlenderDefinitions.BlenderRotationTypes.EULER)
        return self

    def twist(self, angle: AngleOrItsFloatOrStringValue, screwPitch: DimensionOrItsFloatOrStringValue, interations: 'int' = 1, axis: AxisOrItsIndexOrItsName = "z"
              ):

        axis = Utilities.Axis.fromString(axis)

        angleParsed = Utilities.Angle.fromString(angle)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        BlenderActions.applyScrewModifier(
            self.name, angleParsed.toRadians(), axis)

        return self

    def remesh(self, strategy: str, amount: float
               ):

        if strategy == "crease":
            BlenderActions.setEdgesMeanCrease(self.name, 1.0)
        if strategy == "edgesplit":
            BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.EDGE_SPLIT, {
                                         "name": "EdgeDiv", "split_angle": math.radians(30)})

        BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.SUBSURF, {
                                     "name": "Subdivision", "levels": amount})
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
        _ = Part(landmarkObjectName).createPrimitive("Empty", "0")

        # Assign the landmark to the parent's collection
        BlenderActions.assignObjectToCollection(
            landmarkObjectName, BlenderActions.getObjectCollectionName(self.name))

        # Parent the landmark to the object
        BlenderActions.makeParent(landmarkObjectName, self.name)

        BlenderActions.translateObject(
            landmarkObjectName, localPositions, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)
        return self

    def getBoundingBox(self
                       ) -> 'BoundaryBox':
        return BlenderActions.getBoundingBox(self.name)

    def getDimensions(self
                      ) -> 'Dimensions':
        dimensions = BlenderActions.getObject(self.name).dimensions
        dimensions = [
            Utilities.Dimension.fromString(
                dimension,
                BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value  # type: ignore
            )
            for dimension in dimensions
        ]
        return Utilities.Dimensions(dimensions[0], dimensions[1], dimensions[2])

    def getLandmark(self, landmarkName: str
                    ) -> 'Landmark':
        if isinstance(landmarkName, Landmark):
            landmarkName = landmarkName.name

        landmark = Landmark(landmarkName, self.name)

        assert BlenderActions.getObject(
            landmark.getLandmarkEntityName()) != None, f"Landmark {landmarkName} does not exist for {self.name}."
        return landmark


class Part(Entity, CodeToCADInterface.Part):

    def createFromFile(self, filePath: str, fileType: Optional[str] = None
                       ):
        assert self.isExists() == False, f"{self.name} already exists."

        fileName = getFilename(filePath)

        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.importFile(absoluteFilePath, fileType)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != fileName:
            Part(fileName).rename(self.name)

        return self

    def createPrimitive(self, primitiveName: str, dimensions: str, keywordArguments: Optional[dict] = None
                        ):

        assert self.isExists() == False, f"{self.name} already exists."

        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType: BlenderDefinitions.BlenderObjectPrimitiveTypes = getattr(
            BlenderDefinitions.BlenderObjectPrimitiveTypes, primitiveName.lower())
        expectedNameOfObjectInBlender = primitiveType.defaultNameInBlender(
        ) if primitiveType else None

        assert expectedNameOfObjectInBlender != None, \
            f"Primitive type with name {primitiveName} is not supported."

        BlenderActions.addPrimitive(
            primitiveType, dimensions, keywordArguments)

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        if self.name != expectedNameOfObjectInBlender:
            Part(expectedNameOfObjectInBlender).rename(
                self.name, primitiveType.hasData())

        return self

    def createCube(self, width: DimensionOrItsFloatOrStringValue, length: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                   ):
        return self.createPrimitive("cube", "{},{},{}".format(width, length, height), keywordArguments)

    def createCone(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, draftRadius: DimensionOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        return self.createPrimitive("cone", "{},{},{}".format(radius, height, draftRadius), keywordArguments)

    def createCylinder(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                       ):
        return self.createPrimitive("cylinder", "{},{}".format(radius, height), keywordArguments)

    def createTorus(self, innerRadius: DimensionOrItsFloatOrStringValue, outerRadius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                    ):
        return self.createPrimitive("torus", "{},{}".format(innerRadius, outerRadius), keywordArguments)

    def createSphere(self, radius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                     ):
        return self.createPrimitive("uvsphere", "{}".format(radius), keywordArguments)

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

    def loft(self, Landmark1: 'Landmark', Landmark2: 'Landmark'
             ):
        raise NotImplementedError()
        return self

    def union(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
              ):
        if isinstance(withPart, Entity):
            withPart = withPart.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.UNION,
            withPart
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(withPart, self.name)

        if deleteAfterUnion:
            self.apply()
            BlenderActions.removeObject(withPart, removeChildren=True)
        return self

    def subtract(self, withPart: PartOrItsName, deleteAfterSubtract: bool = True, isTransferLandmarks: bool = False
                 ):
        if isinstance(withPart, Entity):
            withPart = withPart.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.DIFFERENCE,
            withPart
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(withPart, self.name)

        if deleteAfterSubtract:
            self.apply()
            BlenderActions.removeObject(withPart, removeChildren=True)
        return self

    def intersect(self, withPart: PartOrItsName, deleteAfterIntersect: bool = True, isTransferLandmarks: bool = False
                  ):
        if isinstance(withPart, Entity):
            withPart = withPart.name

        BlenderActions.applyBooleanModifier(
            self.name,
            BlenderDefinitions.BlenderBooleanTypes.INTERSECT,
            withPart
        )

        if isTransferLandmarks:
            BlenderActions.transferLandmarks(withPart, self.name)

        if deleteAfterIntersect:
            self.apply()
            BlenderActions.removeObject(withPart, removeChildren=True)

        return self

    def hollow(self, thicknessX: DimensionOrItsFloatOrStringValue, thicknessY: DimensionOrItsFloatOrStringValue, thicknessZ: DimensionOrItsFloatOrStringValue, startAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False
               ):
        blenderObject = self.getNativeInstance()

        axis = Utilities.Axis.fromString(startAxis)
        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        startLandmarkLocation = [center, center, center]
        startLandmarkLocation[axis.value] = min if flipAxis else max

        startAxisLandmark = self.createLandmark(
            createUUIDLikeId(), startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        insidePart = self.clone(createUUIDLikeId(), copyLandmarks=False)
        insidePart_start = insidePart.createLandmark(
            "start", startLandmarkLocation[0], startLandmarkLocation[1], startLandmarkLocation[2])

        thicknessXYZ: list[Dimension] = [dimension.value for dimension in BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit([
            Utilities.Dimension.fromString(thicknessX),
            Utilities.Dimension.fromString(thicknessY),
            Utilities.Dimension.fromString(thicknessZ),
        ])]

        dimensions: list[float] = blenderObject.dimensions

        def scaleValue(mainDimension: float, thickness: float, axis: Utilities.Axis) -> float:
            axisSubtraction = (1 if axis.value == 0 else 2)
            return (mainDimension-thickness * axisSubtraction) / mainDimension

        scaleX: float = scaleValue(dimensions[0], thicknessXYZ[0].value, axis)
        scaleY = scaleValue(dimensions[1], thicknessXYZ[1].value, axis)
        scaleZ = scaleValue(dimensions[2], thicknessXYZ[2].value, axis)

        insidePart.scaleXYZ(scaleX, scaleY, scaleZ)

        Joint(startAxisLandmark, insidePart_start).limitLocationX(0, 0)
        Joint(startAxisLandmark, insidePart_start).limitLocationY(0, 0)
        Joint(startAxisLandmark, insidePart_start).limitLocationZ(0, 0)

        self.subtract(insidePart, isTransferLandmarks=False)

        startAxisLandmark.delete(removeChildren=True)

        return self

    def hole(self, holeLandmark: LandmarkOrItsName, radius: DimensionOrItsFloatOrStringValue, depth: DimensionOrItsFloatOrStringValue, normalAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False, initialRotationX: AngleOrItsFloatOrStringValue = 0.0, initialRotationY: AngleOrItsFloatOrStringValue = 0.0, initialRotationZ: AngleOrItsFloatOrStringValue = 0.0, mirrorAboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, mirrorAxis: AxisOrItsIndexOrItsName = "x", mirror: bool = False, circularPatternInstanceCount: 'int' = 1, circularPatternInstanceSeparation: AngleOrItsFloatOrStringValue = 0.0, circularPatternInstanceAxis: AxisOrItsIndexOrItsName = "z", circularPatternAboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, linearPatternInstanceCount: 'int' = 1, linearPatternInstanceSeparation: DimensionOrItsFloatOrStringValue = 0.0, linearPatternInstanceAxis: AxisOrItsIndexOrItsName = "x"):

        axis = Utilities.Axis.fromString(normalAxis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        hole = Part(createUUIDLikeId()).createCylinder(radius, depth)
        hole_head = hole.createLandmark(
            "hole", center, center, min if flipAxis else max)

        axisRotation = Utilities.Angle(-90, Utilities.AngleUnit.DEGREES)

        if axis is Utilities.Axis.X:
            initialRotationY = (axisRotation+initialRotationY).value
        elif axis is Utilities.Axis.Y:
            initialRotationX = (axisRotation+initialRotationX).value
        hole.rotateXYZ(initialRotationX, initialRotationY, initialRotationZ)

        Joint(holeLandmark, hole_head).limitLocationX(0, 0)
        Joint(holeLandmark, hole_head).limitLocationY(0, 0)
        Joint(holeLandmark, hole_head).limitLocationZ(0, 0)

        if mirror and mirrorAboutEntityOrLandmark:
            hole.mirror(mirrorAboutEntityOrLandmark, mirrorAxis,
                        resultingMirroredEntityName=None).apply()

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

        self.subtract(hole, deleteAfterSubtract=True,
                      isTransferLandmarks=False)
        return self

    def assignMaterial(self, materialName: MaterialOrItsName
                       ):
        material = materialName

        if isinstance(material, str):
            material = Material(material)

        material.assignToPart(self.name)
        return self

    def isCollidingWithPart(self, otherPart: PartOrItsName
                            ):
        otherPartName = otherPart
        if isinstance(otherPart, Part):
            otherPartName = otherPart.name

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

            BlenderActions.addVerticiesToVertexGroup(
                vertexGroupObject, blenderPolygon.vertices)

    def bevel(self,
              radius: DimensionOrItsFloatOrStringValue,
              bevelEdgesNearlandmarkNames: Optional[list[LandmarkOrItsName]] = None,
              bevelFacesNearlandmarkNames: Optional[list[LandmarkOrItsName]] = None,
              useWidth=False,
              chamfer=False,
              keywordArguments: Optional[dict] = None
              ):
        vertexGroupName = None

        if bevelEdgesNearlandmarkNames != None:
            vertexGroupName = createUUIDLikeId()
            self._addEdgesNearLandmarksToVertexGroup(
                bevelEdgesNearlandmarkNames, vertexGroupName)

        if bevelFacesNearlandmarkNames != None:
            vertexGroupName = vertexGroupName or createUUIDLikeId()
            self._addFacesNearLandmarksToVertexGroup(
                bevelFacesNearlandmarkNames, vertexGroupName)

        radiusDimension = Utilities.Dimension.fromString(radius)

        radiusDimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            radiusDimension)

        BlenderActions.applyBevelModifier(
            self.name,
            radiusDimension,
            vertexGroupName=vertexGroupName,
            useEdges=True,
            useWidth=useWidth,
            chamfer=chamfer,
            keywordArguments=keywordArguments or None
        )

        return self

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

    def revolve(self, angle: AngleOrItsFloatOrStringValue, aboutEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName = "z"
                ):

        if isinstance(aboutEntityOrLandmark, Entity):
            aboutEntityOrLandmark = aboutEntityOrLandmark.name

        axis = Utilities.Axis.fromString(axis)

        assert axis, f"Unknown axis {axis}. Please use 'x', 'y', or 'z'"

        BlenderActions.applyScrewModifier(self.name, Utilities.Angle.fromString(
            angle).toRadians(), axis, entityNameToDetermineAxis=aboutEntityOrLandmark)

        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue, convertToMesh: bool = True
                ):

        BlenderActions.extrude(
            self.name, Utilities.Dimension.fromString(length))

        if not convertToMesh:
            return self

        BlenderActions.createMeshFromCurve(self.name)

        return self

    def sweep(self, profileCurveName: str, fillCap: bool = False
              ):
        if isinstance(profileCurveName, Entity):
            profileCurveName = profileCurveName.name

        BlenderActions.addBevelObjectToCurve(
            self.name, profileCurveName, fillCap)

        return self

    def createText(self, text: str, fontSize: DimensionOrItsFloatOrStringValue = 1.0, bold: bool = False, italic: bool = False, underlined: bool = False, characterSpacing: 'int' = 1, wordSpacing: 'int' = 1, lineSpacing: 'int' = 1, fontFilePath: Optional[str] = None
                   ):
        size = Utilities.Dimension.fromString(fontSize)

        BlenderActions.createText(self.name, text, size, bold, italic, underlined,
                                  characterSpacing, wordSpacing, lineSpacing, fontFilePath)
        return self

    def createFromVertices(self, coordinates: list[PointOrListOfFloatOrItsStringValue], interpolation: 'int' = 64
                           ):
        BlenderActions.create3DCurve(self.name, BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(
            self.curveType) if self.curveType != None else BlenderDefinitions.BlenderCurveTypes.BEZIER, coordinates, interpolation)

        return self

    @staticmethod
    def _createPrimitiveDecorator(curvePrimitiveType: Utilities.CurvePrimitiveTypes):
        def decorator(primitiveFunction):
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = BlenderDefinitions.BlenderCurvePrimitiveTypes.fromCurvePrimitiveTypes(
                    curvePrimitiveType)

                blenderPrimitiveFunction = BlenderActions.getBlenderCurvePrimitiveFunction(
                    blenderCurvePrimitiveType)

                keywordArgs = dict(
                    {
                        "curveType": BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else None},
                    **kwargs
                )

                blenderPrimitiveFunction(
                    *args[1:],
                    keywordArguments=keywordArgs
                )

                # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
                # therefore, we'll use the object's "expected" name and rename it to what it should be
                # note: this will fail if the "expected" name is incorrect
                curve = Sketch(
                    blenderCurvePrimitiveType.name).rename(self.name)

                curve.getNativeInstance().data.use_path = False

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Point)
    def createPoint(self, coordinate: PointOrListOfFloatOrItsStringValue
                    ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Line)
    def createLine(self, length: DimensionOrItsFloatOrStringValue, angleX: AngleOrItsFloatOrStringValue = 0.0, angleY: AngleOrItsFloatOrStringValue = 0.0, symmetric: bool = False
                   ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.LineTo)
    def createLineBetweenPoints(self, endAt: PointOrListOfFloatOrItsStringValue, startAt: Optional[PointOrListOfFloatOrItsStringValue] = None
                                ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Circle)
    def createCircle(self, radius: 'Dimension'
                     ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Ellipse)
    def createEllipse(self, radiusA: 'Dimension', radiusB: 'Dimension'
                      ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Arc)
    def createArc(self, radius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                  ):
        return self

    def createArcBetweenThreePoints(self, pointA: 'Point', pointB: 'Point', centerPoint: 'Point'
                                    ):
        raise NotImplementedError()
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Segment)
    def createSegment(self, innerRadius: 'Dimension', outerRadius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                      ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Rectangle)
    def createRectangle(self, length: 'Dimension', width: 'Dimension'
                        ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Polygon)
    def createPolygon(self, numberOfSides: 'int', length: 'Dimension', width: 'Dimension'
                      ):
        return self

    @_createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Trapezoid)
    def createTrapezoid(self, lengthUpper: 'Dimension', lengthLower: 'Dimension', height: 'Dimension'
                        ):
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
        parentEntityName: str = self.parentEntity  # type: ignore
        if isinstance(self.parentEntity, Entity):
            parentEntityName = self.parentEntity.name

        return Utilities.formatLandmarkEntityName(parentEntityName, self.name)

    def getParentEntity(self
                        ) -> 'Entity':

        raise NotImplementedError()

    def isExists(self) -> bool:
        try:
            return BlenderActions.getObject(self.getLandmarkEntityName()) != None
        except:
            return False

    def rename(self, newName: str
               ):

        assert Landmark(newName, self.parentEntity).isExists(
        ) == False, f"{newName} already exists."

        parentEntityName: str = self.parentEntity  # type: ignore
        if isinstance(self.parentEntity, Entity):
            parentEntityName = self.parentEntity.name

        BlenderActions.updateObjectName(self.getLandmarkEntityName(
        ), Utilities.formatLandmarkEntityName(parentEntityName, newName))

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
        return Utilities.Point.fromList(
            [Dimension(value, BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)  # type: ignore
             for value in BlenderActions.getObjectWorldLocation(self.getLandmarkEntityName())]
        )

    def getLocationLocal(self
                         ) -> 'Point':

        BlenderActions.updateViewLayer()
        return Utilities.Point.fromList(
            [Dimension(value, BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value)  # type: ignore
             for value in BlenderActions.getObjectLocalLocation(self.getLandmarkEntityName())]
        )

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

        BlenderActions.translateLandmarkOntoAnother(
            landmark1.parentEntity,  landmark1.getLandmarkEntityName(), landmark2.getLandmarkEntityName())

        return self

    def pivot(self
              ):

        # BlenderActions.applyPivotConstraint(
        #     self.part2.name, self.part1Landmark.entityName, keywordArguments)
        raise NotImplementedError()
        return self

    def gearRatio(self, ratio: float
                  ):
        raise NotImplementedError()
        return self

    def limitLocationX(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self

    def limitLocationY(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self

    def limitLocationZ(self, min: Optional[DimensionOrItsFloatOrStringValue] = None, max: Optional[DimensionOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self

    def limitRotationX(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self

    def limitRotationY(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self

    def limitRotationZ(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        raise NotImplementedError()
        return self


class Material(CodeToCADInterface.Material):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def assignToPart(self, partName: PartOrItsName
                     ):
        raise NotImplementedError()
        return self

    def setColor(self, rValue: IntOrFloat, gValue: IntOrFloat, bValue: IntOrFloat, aValue: IntOrFloat = 1.0
                 ):
        raise NotImplementedError()
        return self

    def addImageTexture(self, imageFilePath: str
                        ):
        raise NotImplementedError()
        return self


class Light(Entity):

    def __init__(self, lightName):
        self.name = lightName

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


class Camera(Entity):

    def __init__(self, cameraName):
        self.name = cameraName

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


class Animation(CodeToCADInterface.Animation):

    def __init__(self):
        pass

    @staticmethod
    def default(
    ) -> 'Animation':
        return Animation()

    def createKeyFrameLocation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):
        raise NotImplementedError()

    def createKeyFrameRotation(self, entity: EntityOrItsName, frameNumber: 'int'
                               ):
        raise NotImplementedError()


class Scene(CodeToCADInterface.Scene):

    name: Optional[str] = None
    description: Optional[str] = None
    light = Light

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name
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

    def export(self, filePath: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        raise NotImplementedError()
        return self

    def setDefaultUnit(self, unit: LengthUnitOrItsName
                       ):
        raise NotImplementedError()
        return self

    def createGroup(self, name: str
                    ):
        raise NotImplementedError()
        return self

    def deleteGroup(self, name: str, removeChildren: bool
                    ):
        raise NotImplementedError()
        return self

    def removeFromGroup(self, entityName: str, groupName: str
                        ):
        raise NotImplementedError()
        return self

    def assignToGroup(self, entities: list[EntityOrItsName], groupName: str, removeFromOtherGroups: Optional[bool] = True
                      ):
        raise NotImplementedError()
        return self

    def setVisible(self, entities: list[EntityOrItsName], isVisible: bool
                   ):
        raise NotImplementedError()
        return self

    def setHDRIBackground(self,
                          filePath, x=0, y=0):

        absoluteFilePath = getAbsoluteFilepath(filePath)

        BlenderActions.addHDRTexture(self.name, absoluteFilePath)

        BlenderActions.setBackgroundLocation(self.name, x, y)

        return self


class Analytics(CodeToCADInterface.Analytics):

    def __init__(self):
        pass

    def measureDistance(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark
                        ) -> 'Dimensions':
        raise NotImplementedError()

    def measureAngle(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark, pivot: Optional[EntityOrItsNameOrLandmark] = None
                     ) -> 'list[Angle]':
        raise NotImplementedError()

    def getWorldPose(self, entity: EntityOrItsName
                     ) -> 'list[float]':
        raise NotImplementedError()

    def getBoundingBox(self, entityName: EntityOrItsName
                       ) -> 'BoundaryBox':
        raise NotImplementedError()

    def getDimensions(self, entityName: EntityOrItsName
                      ) -> 'Dimensions':
        if isinstance(entityName, Entity):
            return entityName.getDimensions()
        if isinstance(entityName, str):
            return Entity(entityName).getDimensions()
        raise TypeError("entityName must be a string or an Entity")

    def log(self, message):
        return BlenderActions.logMessage(message)
