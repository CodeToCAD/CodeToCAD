# This file was forked from core/CodeToCADProvider.py

import math
from typing import Optional, Union

import BlenderActions
import BlenderDefinitions

import core.CodeToCADInterface as CodeToCADInterface
import core.utilities as Utilities
from core.CodeToCADInterface import FloatOrItsStringValue, IntOrFloat, MaterialOrItsName, PartOrItsName, EntityOrItsName, LandmarkOrItsName, AxisOrItsIndexOrItsName, DimensionOrItsFloatOrStringValue, AngleOrItsFloatOrStringValue, EntityOrItsNameOrLandmark, PointOrListOfFloatOrItsStringValue, LengthUnitOrItsName
from core.utilities import (Angle, BoundaryBox, CurveTypes, Dimension,
                            Dimensions, Point, center, createUUIDLikeId,
                            getAbsoluteFilepath, getFilename, max, min)


if BlenderActions.getBlenderVersion() and BlenderActions.getBlenderVersion() < BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value:
    print(
        f"CodeToCAD BlenderProvider only supports Blender versions {'.'.join(tuple, BlenderDefinitions.BlenderVersions.TWO_DOT_EIGHTY.value)}+. You are running version {'.'.join(BlenderActions.getBlenderVersion())}")  # type: ignore


def injectBlenderProvider() -> None:
    from CodeToCAD import setPartProvider, setSketchProvider, setMaterialProvider, setLandmarkProvider, setJointProvider, setAnimationProvider, setSceneProvider, setAnalyticsProvider

    setPartProvider(Part)
    setSketchProvider(Sketch)
    setMaterialProvider(Material)
    setLandmarkProvider(Landmark)
    setJointProvider(Joint)
    setAnimationProvider(Animation)
    setSceneProvider(Scene)
    setAnalyticsProvider(Analytics)


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

    def select(self, landmarkName: Optional[LandmarkOrItsName] = None, selectionType: str = "vertex"
               ):
        raise NotImplementedError()
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

    def mirror(self, mirrorAcrossEntity: EntityOrItsName, axis: AxisOrItsIndexOrItsName, resultingMirroredEntityName: Optional[str]
               ):

        if resultingMirroredEntityName != None:
            raise NotImplementedError("Not yet supported. COD-113")

        mirrorAcrossEntityName = mirrorAcrossEntity
        if isinstance(mirrorAcrossEntity, Landmark):
            mirrorAcrossEntityName = mirrorAcrossEntity.getLandmarkEntityName()
        elif isinstance(mirrorAcrossEntity, Entity):
            mirrorAcrossEntityName = mirrorAcrossEntity.name

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

        angles = [Utilities.Angle(0) for _ in range(3)]
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

    def translateX(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Dimension.fromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.x)

        dimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            dimension)

        BlenderActions.translateObject(
            self.name, [dimension, Dimension(0), Dimension(0)], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateY(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Dimension.fromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.y)

        dimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            dimension)

        BlenderActions.translateObject(
            self.name, [Dimension(0), dimension, Dimension(0)], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def translateZ(self, amount: DimensionOrItsFloatOrStringValue
                   ):

        boundingBox = BlenderActions.getBoundingBox(self.name)

        dimension = Dimension.fromDimensionOrItsFloatOrStringValue(
            amount, boundingBox.z)

        dimension = BlenderDefinitions.BlenderLength.convertDimensionToBlenderUnit(
            dimension)

        BlenderActions.translateObject(
            self.name, [Dimension(0), Dimension(0), dimension], BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE)

        return self

    def scaleX(self, scale: DimensionOrItsFloatOrStringValue
               ):
        return self

    def scaleY(self, scale: DimensionOrItsFloatOrStringValue
               ):
        return self

    def scaleZ(self, scale: DimensionOrItsFloatOrStringValue
               ):
        return self

    def scaleKeepAspectRatio(self, scale: DimensionOrItsFloatOrStringValue, axis: AxisOrItsIndexOrItsName
                             ):
        return self

    def rotateX(self, rotation: AngleOrItsFloatOrStringValue
                ):
        return self

    def rotateY(self, rotation: AngleOrItsFloatOrStringValue
                ):
        return self

    def rotateZ(self, rotation: AngleOrItsFloatOrStringValue
                ):
        return self

    def twist(self, angle: AngleOrItsFloatOrStringValue, screwPitch: DimensionOrItsFloatOrStringValue, interations: 'int' = 1, axis: AxisOrItsIndexOrItsName = "z"
              ):
        return self

    def remesh(self, strategy: str, amount: float
               ):
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
        raise NotImplementedError()

    def getDimensions(self
                      ) -> 'Dimensions':
        raise NotImplementedError()

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
        return self

    def createPrimitive(self, primitiveName: str, dimensions: str, keywordArguments: Optional[dict] = None
                        ):

        assert self.isExists() == False, f"{self.name} already exists."

        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType: BlenderDefinitions.BlenderObjectPrimitiveTypes = getattr(
            BlenderDefinitions.BlenderObjectPrimitiveTypes, primitiveName.lower(), None)
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
        return self

    def createCylinder(self, radius: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                       ):
        return self

    def createTorus(self, innerRadius: DimensionOrItsFloatOrStringValue, outerRadius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                    ):
        return self

    def createSphere(self, radius: DimensionOrItsFloatOrStringValue, keywordArguments: Optional[dict] = None
                     ):
        return self

    def createGear(self, outerRadius: DimensionOrItsFloatOrStringValue, addendum: DimensionOrItsFloatOrStringValue, innerRadius: DimensionOrItsFloatOrStringValue, dedendum: DimensionOrItsFloatOrStringValue, height: DimensionOrItsFloatOrStringValue, pressureAngle: AngleOrItsFloatOrStringValue = "20d", numberOfTeeth: 'int' = 12, skewAngle: AngleOrItsFloatOrStringValue = 0, conicalAngle: AngleOrItsFloatOrStringValue = 0, crownAngle: AngleOrItsFloatOrStringValue = 0, keywordArguments: Optional[dict] = None
                   ):
        return self

    def loft(self, Landmark1: 'Landmark', Landmark2: 'Landmark'
             ):
        return self

    def union(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
              ):
        return self

    def subtract(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
                 ):
        return self

    def intersect(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
                  ):
        return self

    def hollow(self, thicknessX: DimensionOrItsFloatOrStringValue, thicknessY: DimensionOrItsFloatOrStringValue, thicknessZ: DimensionOrItsFloatOrStringValue, startAxis: AxisOrItsIndexOrItsName = "z", flipAxis: bool = False
               ):
        return self

    def hole(self, holeLandmark: LandmarkOrItsName, radius: DimensionOrItsFloatOrStringValue, depth: DimensionOrItsFloatOrStringValue, normalAxis: AxisOrItsIndexOrItsName = "z", flip: bool = False, instanceCount: 'int' = 1, instanceSeparation: DimensionOrItsFloatOrStringValue = 0.0, aboutEntityOrLandmark: Optional[EntityOrItsNameOrLandmark] = None, mirror: bool = False, instanceAxis: Optional[AxisOrItsIndexOrItsName] = None, initialRotationX: AngleOrItsFloatOrStringValue = 0.0, initialRotationY: AngleOrItsFloatOrStringValue = 0.0, initialRotationZ: AngleOrItsFloatOrStringValue = 0.0, leaveHoleEntity: bool = False
             ):
        return self

    def assignMaterial(self, materialName: MaterialOrItsName
                       ):
        return self

    def isCollidingWithPart(self, otherPart: PartOrItsName
                            ):
        raise NotImplementedError()

    def filletAllEdges(self, radius: DimensionOrItsFloatOrStringValue, useWidth: bool = False
                       ):
        return self

    def filletEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        return self

    def filletFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName], useWidth: bool = False
                    ):
        return self

    def chamferAllEdges(self, radius: DimensionOrItsFloatOrStringValue
                        ):
        return self

    def chamferEdges(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearEdges: list[LandmarkOrItsName]
                     ):
        return self

    def chamferFaces(self, radius: DimensionOrItsFloatOrStringValue, landmarksNearFaces: list[LandmarkOrItsName]
                     ):
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
        return self

    def extrude(self, length: DimensionOrItsFloatOrStringValue, convertToMesh: bool = True
                ):
        return self

    def sweep(self, profileCurveName: str, fillCap: bool = False
              ):
        return self

    def createText(self, text: str, fontSize: DimensionOrItsFloatOrStringValue = 1.0, bold: bool = False, italic: bool = False, underlined: bool = False, characterSpacing: 'int' = 1, wordSpacing: 'int' = 1, lineSpacing: 'int' = 1, fontFilePath: Optional[str] = None
                   ):
        return self

    def createFromVertices(self, coordinates: list[PointOrListOfFloatOrItsStringValue], interpolation: 'int' = 64
                           ):
        return self

    def createPoint(self, coordinate: PointOrListOfFloatOrItsStringValue
                    ):
        return self

    def createLine(self, length: DimensionOrItsFloatOrStringValue, angleX: AngleOrItsFloatOrStringValue = 0.0, angleY: AngleOrItsFloatOrStringValue = 0.0, symmetric: bool = False
                   ):
        return self

    def createLineBetweenPoints(self, endAt: PointOrListOfFloatOrItsStringValue, startAt: Optional[PointOrListOfFloatOrItsStringValue] = None
                                ):
        return self

    def createCircle(self, radius: 'Dimension'
                     ):
        return self

    def createEllipse(self, radiusA: 'Dimension', radiusB: 'Dimension'
                      ):
        return self

    def createArc(self, radius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                  ):
        return self

    def createArcBetweenThreePoints(self, pointA: 'Point', pointB: 'Point', centerPoint: 'Point'
                                    ):
        return self

    def createSegment(self, innerRadius: 'Dimension', outerRadius: 'Dimension', angle: AngleOrItsFloatOrStringValue = "180d"
                      ):
        return self

    def createRectangle(self, length: 'Dimension', width: 'Dimension'
                        ):
        return self

    def createPolygon(self, numberOfSides: 'int', length: 'Dimension', width: 'Dimension'
                      ):
        return self

    def createTrapezoid(self, lengthUpper: 'Dimension', lengthLower: 'Dimension', height: 'Dimension'
                        ):
        return self


class Landmark(Entity, CodeToCADInterface.Landmark):

    name: str
    parentEntity: EntityOrItsName
    description: Optional[str] = None

    def __init__(self, name: str, parentEntity: EntityOrItsName, description: Optional[str] = None):
        self.name = name
        self.parentEntity = parentEntity
        self.description = description

    def isExists(self) -> bool:
        try:
            return BlenderActions.getObject(self.getLandmarkEntityName()) != None
        except:
            return False

    def getLandmarkEntityName(self
                              ) -> str:
        parentEntityName: str = self.parentEntity  # type: ignore
        if isinstance(self.parentEntity, Entity):
            parentEntityName = self.parentEntity.name

        return Utilities.formatLandmarkEntityName(parentEntityName, self.name)


class Joint(CodeToCADInterface.Joint):

    entity1: EntityOrItsNameOrLandmark
    entity2: EntityOrItsNameOrLandmark

    def __init__(self, entity1: EntityOrItsNameOrLandmark, entity2: EntityOrItsNameOrLandmark):
        self.entity1 = entity1
        self.entity2 = entity2

    def translateLandmarkOntoAnother(self
                                     ):
        return self

    def pivot(self
              ):
        return self

    def gearRatio(self, ratio: float
                  ):
        return self

    def limitXLocation(self, min: Optional[PointOrListOfFloatOrItsStringValue] = None, max: Optional[PointOrListOfFloatOrItsStringValue] = None
                       ):
        return self

    def limitYLocation(self, min: Optional[PointOrListOfFloatOrItsStringValue] = None, max: Optional[PointOrListOfFloatOrItsStringValue] = None
                       ):
        return self

    def limitZLocation(self, min: Optional[PointOrListOfFloatOrItsStringValue] = None, max: Optional[PointOrListOfFloatOrItsStringValue] = None
                       ):
        return self

    def limitXRotation(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        return self

    def limitYRotation(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        return self

    def limitZRotation(self, min: Optional[AngleOrItsFloatOrStringValue] = None, max: Optional[AngleOrItsFloatOrStringValue] = None
                       ):
        return self


class Material(CodeToCADInterface.Material):

    name: str
    description: Optional[str] = None

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def assignToPart(self, partName: PartOrItsName
                     ):
        return self

    def setColor(self, rValue: IntOrFloat, gValue: IntOrFloat, bValue: IntOrFloat, aValue: IntOrFloat = 1.0
                 ):
        return self

    def addImageTexture(self, imageFilePath: str
                        ):
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
        return self

    def delete(self
               ):
        return self

    def export(self, filePath: str, entities: list[EntityOrItsName], overwrite: bool = True, scale: float = 1.0
               ):
        return self

    def setDefaultUnit(self, unit: LengthUnitOrItsName
                       ):
        return self

    def createGroup(self, name: str
                    ):
        return self

    def deleteGroup(self, name: str, removeChildren: bool
                    ):
        return self

    def removeFromGroup(self, entityName: str, groupName: str
                        ):
        return self

    def assignToGroup(self, entities: list[EntityOrItsName], groupName: str, removeFromOtherGroups: Optional[bool] = True
                      ):
        return self

    def setVisible(self, entities: list[EntityOrItsName], isVisible: bool
                   ):
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
