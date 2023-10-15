from functools import wraps
from typing import Optional

from codetocad.CodeToCADTypes import *
from codetocad.interfaces import SketchInterface
from codetocad.utilities import *

from . import BlenderActions, BlenderDefinitions
from .Entity import Entity
from .Part import Part


class Sketch(Entity, SketchInterface):

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

    def revolve(self, angle: AngleOrItsFloatOrStringValue, aboutEntityOrLandmark: EntityOrItsNameOrLandmark, axis: AxisOrItsIndexOrItsName = "z") -> 'PartInterface':

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

    def extrude(self, length: DimensionOrItsFloatOrStringValue) -> 'PartInterface':

        BlenderActions.extrudeCurve(
            self.name, Dimension.fromString(length))

        BlenderActions.createMeshFromCurve(
            self.name)

        return Part(self.name, self.description).apply()

    def sweep(self, profileNameOrInstance: SketchOrItsName, fillCap: bool = True) -> 'PartInterface':
        profileCurveName = profileNameOrInstance
        if isinstance(profileCurveName, SketchInterface):
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

            @wraps(primitiveFunction)
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
