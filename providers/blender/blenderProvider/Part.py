from typing import Optional
from . import BlenderActions
from . import BlenderDefinitions

from codetocad.interfaces import PartInterface, LandmarkInterface, EntityInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *

from .Material import Material
from .Entity import Entity
from .Joint import Joint


class Part(Entity, PartInterface):

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
              ) -> 'PartInterface':

        assert Entity(
            newName).isExists() == False, f"{newName} already exists."

        BlenderActions.duplicateObject(self.name, newName, copyLandmarks)

        return Part(newName, self.description)

    def loft(self, Landmark1: 'LandmarkInterface', Landmark2: 'LandmarkInterface'
             ):
        raise NotImplementedError()
        return self

    def union(self, withPart: PartOrItsName, deleteAfterUnion: bool = True, isTransferLandmarks: bool = False
              ):
        partName = withPart
        if isinstance(partName, EntityInterface):
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
        if isinstance(partName, EntityInterface):
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
        if isinstance(partName, EntityInterface):
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

    def thicken(self, radius: DimensionOrItsFloatOrStringValue) -> 'PartInterface':

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
        if isinstance(otherPartName, PartInterface):
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
