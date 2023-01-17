import core.utilities as Utilities
import core.CodeToCADInterface as CodeToCADInterface

from typing import Optional
from core.utilities import Point, Dimension, Dimensions, CurveTypes, Angle, BoundaryBox, min, max, center, createUUID, getAbsoluteFilepath, getFilename, StringOrFloat, StringNameOrPart, StringNameOrEntity, StringNameOrLandmark, IntOrFloat, StringNameOrMaterial


class Entity(CodeToCADInterface.Entity):
    # Capabilities shared between Parts and Sketches.

    def isExists(self
                 ) -> bool:
        print("isExists is not implemented")  # TODO: implement
        raise NotImplementedError

    def clone(self,
              entityName: str
              ):
        print("clone is not implemented")  # TODO: implement
        return self

    def mirror(self,
               entityName: str,
               landmarkName: str
               ):
        print("mirror is not implemented")  # TODO: implement
        return self

    def pattern(self,
                entityName: str,
                landmarkName: str
                ):
        print("pattern is not implemented")  # TODO: implement
        return self

    def scale(self,
              dimensions: str
              ):
        print("scale is not implemented")  # TODO: implement
        return self

    def rotate(self,
               rotation: str
               ):
        print("rotate is not implemented")  # TODO: implement
        return self

    def rename(self,
               name: str
               ):
        print("rename is not implemented")  # TODO: implement
        return self

    def remesh(self,
               strategy: str,
               amount: float
               ):
        print("remesh is not implemented")  # TODO: implement
        return self

    def delete(self,
               removeChildren: bool
               ):
        print("delete is not implemented")  # TODO: implement
        return self

    def setVisible(self,
                   isVisible: bool
                   ):
        print("setVisible is not implemented")  # TODO: implement
        return self

    def apply(self
              ):
        print("apply is not implemented")  # TODO: implement
        return self

    def getNativeInstance(self
                          ):
        print("getNativeInstance is not implemented")  # TODO: implement
        raise NotImplementedError

    def select(self,
               landmarkName: str,
               selectionType: str
               ):
        print("select is not implemented")  # TODO: implement
        return self


class Part(CodeToCADInterface.Part):
    # Capabilities Part CRUD.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    def createFromFile(self,
                       filePath: str,
                       fileType: Optional[str] = None
                       ):
        print("createFromFile is not implemented")  # TODO: implement
        return self

    def createPrimitive(self,
                        primitiveName: str,
                        dimensions: str,
                        keywordArguments: Optional[dict] = None
                        ):
        print("createPrimitive is not implemented")  # TODO: implement
        return self

    def createCube(self,
                   width: StringOrFloat,
                   length: StringOrFloat,
                   height: StringOrFloat,
                   keywordArguments: Optional[dict] = None
                   ):
        print("createCube is not implemented")  # TODO: implement
        return self

    def createCone(self,
                   radius: StringOrFloat,
                   height: StringOrFloat,
                   draftRadius: StringOrFloat,
                   keywordArguments: Optional[dict] = None
                   ):
        print("createCone is not implemented")  # TODO: implement
        return self

    def createCylinder(self,
                       radius: StringOrFloat,
                       height: StringOrFloat,
                       keywordArguments: Optional[dict] = None
                       ):
        print("createCylinder is not implemented")  # TODO: implement
        return self

    def createTorus(self,
                    innerRadius: StringOrFloat,
                    outerRadius: StringOrFloat,
                    keywordArguments: Optional[dict] = None
                    ):
        print("createTorus is not implemented")  # TODO: implement
        return self

    def createSphere(self,
                     radius: StringOrFloat,
                     keywordArguments: Optional[dict] = None
                     ):
        print("createSphere is not implemented")  # TODO: implement
        return self

    def verticies(self,
                  verticies: list
                  ):
        print("verticies is not implemented")  # TODO: implement
        return self

    def loft(self,
             part1Name: StringNameOrPart,
             part1LandmarkName: StringNameOrLandmark,
             part2Name: StringNameOrPart,
             part2LandmarkName: StringNameOrLandmark
             ):
        print("loft is not implemented")  # TODO: implement
        return self

    def mask(self,
             partName: str,
             landmarkName: str
             ):
        print("mask is not implemented")  # TODO: implement
        return self

    def union(self,
              withPartName: str
              ):
        print("union is not implemented")  # TODO: implement
        return self

    def subtract(self,
                 withPartName: str
                 ):
        print("subtract is not implemented")  # TODO: implement
        return self

    def intersect(self,
                  withPartName: str
                  ):
        print("intersect is not implemented")  # TODO: implement
        return self

    def bevel(self,
              landmarkName: str,
              angle: float,
              roundedness: int
              ):
        print("bevel is not implemented")  # TODO: implement
        return self

    def hollow(self,
               wallThickness: float
               ):
        print("hollow is not implemented")  # TODO: implement
        return self

    def assignMaterial(self,
                       materialName: StringNameOrMaterial
                       ):
        print("assignMaterial is not implemented")  # TODO: implement
        return self


class Sketch(CodeToCADInterface.Sketch):
    # Capabilities related to adding, multiplying, and/or modifying a curve.
    name: str
    curveType: CurveTypes
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 curveType: CurveTypes,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.curveType = curveType
        self.description = description

    def extrude(self,
                length: str
                ):
        print("extrude is not implemented")  # TODO: implement
        return self

    def sweep(self,
              profileCurveName: str,
              fillCap: bool
              ):
        print("sweep is not implemented")  # TODO: implement
        return self

    def createText(self,
                   text: str,
                   fontSize: Dimension,
                   bold: bool,
                   italic: bool,
                   underlined: bool,
                   characterSpacing: int,
                   wordSpacing: int,
                   lineSpacing: int,
                   fontFilePath: str
                   ):
        print("createText is not implemented")  # TODO: implement
        return self

    def createFromVertices(self,
                           verticesArray: list[Point],
                           interpolation: int
                           ):
        print("createFromVertices is not implemented")  # TODO: implement
        return self

    def createPoint(self
                    ):
        print("createPoint is not implemented")  # TODO: implement
        return self

    def createLine(self,
                   length: Dimension,
                   symmetric: bool
                   ):
        print("createLine is not implemented")  # TODO: implement
        return self

    def createLineBetweenPoints(self,
                                pointA: Point,
                                pointB: Point
                                ):
        print("createLineBetweenPoints is not implemented")  # TODO: implement
        return self

    def createCircle(self,
                     radius: Dimension
                     ):
        print("createCircle is not implemented")  # TODO: implement
        return self

    def createEllipse(self,
                      radiusA: Dimension,
                      radiusB: Dimension
                      ):
        print("createEllipse is not implemented")  # TODO: implement
        return self

    def createArc(self,
                  radius: Dimension,
                  angle: Angle
                  ):
        print("createArc is not implemented")  # TODO: implement
        return self

    def createArcBetweenThreePoints(self,
                                    pointA: Point,
                                    pointB: Point,
                                    centerPoint: Point
                                    ):
        print("createArcBetweenThreePoints is not implemented")  # TODO: implement
        return self

    def createSegment(self,
                      innerRadius: Dimension,
                      outerRadius: Dimension,
                      angle: Angle
                      ):
        print("createSegment is not implemented")  # TODO: implement
        return self

    def createRectangle(self,
                        length: Dimension,
                        width: Dimension
                        ):
        print("createRectangle is not implemented")  # TODO: implement
        return self

    def createPolygon(self,
                      numberOfSides: int,
                      length: Dimension,
                      width: Dimension
                      ):
        print("createPolygon is not implemented")  # TODO: implement
        return self

    def createTrapezoid(self,
                        lengthUpper: Dimension,
                        lengthLower: Dimension,
                        height: Dimension
                        ):
        print("createTrapezoid is not implemented")  # TODO: implement
        return self


class Landmark(CodeToCADInterface.Landmark):
    # Landmarks are named positions on an entity.
    landmarkName: str
    localToEntityWithName: str

    def __init__(self,
                 landmarkName: str,
                 localToEntityWithName: str
                 ):
        self.landmarkName = landmarkName
        self.localToEntityWithName = localToEntityWithName


class Joint(CodeToCADInterface.Joint):
    # Joints define the relationships and constraints between entities.
    entity1Name: str
    entity2Name: str
    entity1LandmarkName: str
    entity2LandmarkName: str

    def __init__(self,
                 entity1Name: str,
                 entity2Name: str,
                 entity1LandmarkName: str,
                 entity2LandmarkName: str
                 ):
        self.entity1Name = entity1Name
        self.entity2Name = entity2Name
        self.entity1LandmarkName = entity1LandmarkName
        self.entity2LandmarkName = entity2LandmarkName

    def translateLandmarkOntoAnother(self
                                     ):
        # TODO: implement
        print("translateLandmarkOntoAnother is not implemented")
        return self

    def pivot(self
              ):
        print("pivot is not implemented")  # TODO: implement
        return self

    def gear(self,
             ratio: float
             ):
        print("gear is not implemented")  # TODO: implement
        return self

    def limitLocation(self,
                      x: str,
                      y: str,
                      z: str
                      ):
        print("limitLocation is not implemented")  # TODO: implement
        return self

    def limitRotation(self,
                      x: str,
                      y: str,
                      z: str
                      ):
        print("limitRotation is not implemented")  # TODO: implement
        return self


class Material(CodeToCADInterface.Material):
    # Materials affect the appearance and simulation properties of the parts.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    def assignToPart(self,
                     partName: StringNameOrPart
                     ):
        print("assignToPart is not implemented")  # TODO: implement
        return self

    def setColor(self,
                 rValue: IntOrFloat,
                 gValue: IntOrFloat,
                 bValue: IntOrFloat,
                 aValue: IntOrFloat
                 ):
        print("setColor is not implemented")  # TODO: implement
        return self

    def addImageTexture(self,
                        imageFilePath: str
                        ):
        print("addImageTexture is not implemented")  # TODO: implement
        return self


class Scene(CodeToCADInterface.Scene):
    # Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    def create(self
               ):
        print("create is not implemented")  # TODO: implement
        raise NotImplementedError

    def delete(self
               ):
        print("delete is not implemented")  # TODO: implement
        raise NotImplementedError

    def export(self
               ):
        print("export is not implemented")  # TODO: implement
        raise NotImplementedError

    def setDefaultUnit(self,
                       unit: str
                       ):
        print("setDefaultUnit is not implemented")  # TODO: implement
        return self

    def createGroup(self,
                    name: str
                    ):
        print("createGroup is not implemented")  # TODO: implement
        return self

    def deleteGroup(self,
                    name: str,
                    removeChildren: bool
                    ):
        print("deleteGroup is not implemented")  # TODO: implement
        return self

    def removeFromGroup(self,
                        entityName: str,
                        groupName: str
                        ):
        print("removeFromGroup is not implemented")  # TODO: implement
        return self

    def assignToGroup(self,
                      entityName: str,
                      groupName: str,
                      removeFromOtherGroups: Optional[bool] = None
                      ):
        print("assignToGroup is not implemented")  # TODO: implement
        return self

    def setVisible(self,
                   entityName: str,
                   isVisible: bool
                   ):
        print("setVisible is not implemented")  # TODO: implement
        return self


class Analytics(CodeToCADInterface.Analytics):
    # Tools for collecting data about the entities and scene.

    def __init__(self
                 ):
        pass

    def measureLandmarks(self,
                         landmark1Name: str,
                         landmark2Name: Optional[str] = None
                         ) -> Dimension:
        print("measureLandmarks is not implemented")  # TODO: implement
        raise NotImplementedError

    def getWorldPose(self,
                     entityName: str
                     ):
        print("getWorldPose is not implemented")  # TODO: implement
        raise NotImplementedError

    def getBoundingBox(self,
                       entityName: str
                       ) -> BoundaryBox:
        print("getBoundingBox is not implemented")  # TODO: implement
        raise NotImplementedError

    def getDimensions(self,
                      entityName: str
                      ) -> Dimensions:
        print("getDimensions is not implemented")  # TODO: implement
        raise NotImplementedError
