from abc import ABCMeta, abstractmethod
from typing import Optional

from core.utilities import Point, Dimension, Dimensions, CurveTypes, Angle, BoundaryBox, StringOrFloat, StringNameOrPart, StringNameOrEntity, StringNameOrLandmark, IntOrFloat, StringNameOrMaterial


class Entity(metaclass=ABCMeta):
    # Capabilities shared between Parts and Sketches.

    @abstractmethod
    def isExists(self
                 ) -> bool:
        print("isExists is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def clone(self,
              entityName: str
              ):
        print("clone is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def mirror(self,
               entityName: str,
               landmarkName: str
               ):
        print("mirror is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def pattern(self,
                entityName: str,
                landmarkName: str
                ):
        print("pattern is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def scale(self,
              dimensions: str
              ):
        print("scale is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def rotate(self,
               rotation: str
               ):
        print("rotate is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def rename(self,
               name: str
               ):
        print("rename is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def remesh(self,
               strategy: str,
               amount: float
               ):
        print("remesh is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def delete(self,
               removeChildren: bool
               ):
        print("delete is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def setVisible(self,
                   isVisible: bool
                   ):
        print("setVisible is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def apply(self
              ):
        print("apply is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def getNativeInstance(self
                          ):
        print("getNativeInstance is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def select(self,
               landmarkName: str,
               selectionType: str
               ):
        print("select is called in the interface. Please override this method.")
        return self


class Part(Entity, metaclass=ABCMeta):
    # Capabilities Part CRUD.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    @abstractmethod
    def createFromFile(self,
                       filePath: str,
                       fileType: Optional[str] = None
                       ):
        print("createFromFile is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createPrimitive(self,
                        primitiveName: str,
                        dimensions: str,
                        keywordArguments: Optional[dict] = None
                        ):
        print("createPrimitive is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createCube(self,
                   width: StringOrFloat,
                   length: StringOrFloat,
                   height: StringOrFloat,
                   keywordArguments: Optional[dict] = None
                   ):
        print("createCube is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createCone(self,
                   radius: StringOrFloat,
                   height: StringOrFloat,
                   draftRadius: StringOrFloat,
                   keywordArguments: Optional[dict] = None
                   ):
        print("createCone is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createCylinder(self,
                       radius: StringOrFloat,
                       height: StringOrFloat,
                       keywordArguments: Optional[dict] = None
                       ):
        print("createCylinder is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createTorus(self,
                    innerRadius: StringOrFloat,
                    outerRadius: StringOrFloat,
                    keywordArguments: Optional[dict] = None
                    ):
        print("createTorus is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createSphere(self,
                     radius: StringOrFloat,
                     keywordArguments: Optional[dict] = None
                     ):
        print("createSphere is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def verticies(self,
                  verticies: list
                  ):
        print("verticies is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def loft(self,
             part1Name: StringNameOrPart,
             part1LandmarkName: StringNameOrLandmark,
             part2Name: StringNameOrPart,
             part2LandmarkName: StringNameOrLandmark
             ):
        print("loft is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def mask(self,
             partName: str,
             landmarkName: str
             ):
        print("mask is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def union(self,
              withPartName: str
              ):
        print("union is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def subtract(self,
                 withPartName: str
                 ):
        print("subtract is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def intersect(self,
                  withPartName: str
                  ):
        print("intersect is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def bevel(self,
              landmarkName: str,
              angle: float,
              roundedness: int
              ):
        print("bevel is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def hollow(self,
               wallThickness: float
               ):
        print("hollow is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def assignMaterial(self,
                       materialName: StringNameOrMaterial
                       ):
        print("assignMaterial is called in the interface. Please override this method.")
        return self


class Sketch(Entity, metaclass=ABCMeta):
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

    @abstractmethod
    def extrude(self,
                length: str
                ):
        print("extrude is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def sweep(self,
              profileCurveName: str,
              fillCap: bool
              ):
        print("sweep is called in the interface. Please override this method.")
        return self

    @abstractmethod
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
        print("createText is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createFromVertices(self,
                           verticesArray: list[Point],
                           interpolation: int
                           ):
        print("createFromVertices is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createPoint(self
                    ):
        print("createPoint is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createLine(self,
                   length: Dimension,
                   symmetric: bool
                   ):
        print("createLine is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createLineBetweenPoints(self,
                                pointA: Point,
                                pointB: Point
                                ):
        print("createLineBetweenPoints is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createCircle(self,
                     radius: Dimension
                     ):
        print("createCircle is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createEllipse(self,
                      radiusA: Dimension,
                      radiusB: Dimension
                      ):
        print("createEllipse is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createArc(self,
                  radius: Dimension,
                  angle: Angle
                  ):
        print("createArc is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createArcBetweenThreePoints(self,
                                    pointA: Point,
                                    pointB: Point,
                                    centerPoint: Point
                                    ):
        print("createArcBetweenThreePoints is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createSegment(self,
                      innerRadius: Dimension,
                      outerRadius: Dimension,
                      angle: Angle
                      ):
        print("createSegment is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createRectangle(self,
                        length: Dimension,
                        width: Dimension
                        ):
        print("createRectangle is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createPolygon(self,
                      numberOfSides: int,
                      length: Dimension,
                      width: Dimension
                      ):
        print("createPolygon is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createTrapezoid(self,
                        lengthUpper: Dimension,
                        lengthLower: Dimension,
                        height: Dimension
                        ):
        print("createTrapezoid is called in the interface. Please override this method.")
        return self


class Landmark(metaclass=ABCMeta):
    # Landmarks are named positions on an entity.
    landmarkName: str
    localToEntityWithName: str

    def __init__(self,
                 landmarkName: str,
                 localToEntityWithName: str
                 ):
        self.landmarkName = landmarkName
        self.localToEntityWithName = localToEntityWithName


class Joint(metaclass=ABCMeta):
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

    @abstractmethod
    def translateLandmarkOntoAnother(self
                                     ):
        print("translateLandmarkOntoAnother is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def pivot(self
              ):
        print("pivot is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def gear(self,
             ratio: float
             ):
        print("gear is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def limitLocation(self,
                      x: str,
                      y: str,
                      z: str
                      ):
        print("limitLocation is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def limitRotation(self,
                      x: str,
                      y: str,
                      z: str
                      ):
        print("limitRotation is called in the interface. Please override this method.")
        return self


class Material(metaclass=ABCMeta):
    # Materials affect the appearance and simulation properties of the parts.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    @abstractmethod
    def assignToPart(self,
                     partName: StringNameOrPart
                     ):
        print("assignToPart is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def setColor(self,
                 rValue: IntOrFloat,
                 gValue: IntOrFloat,
                 bValue: IntOrFloat,
                 aValue: IntOrFloat
                 ):
        print("setColor is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def addImageTexture(self,
                        imageFilePath: str
                        ):
        print("addImageTexture is called in the interface. Please override this method.")
        return self


class Scene(metaclass=ABCMeta):
    # Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.
    name: str
    description: Optional[str] = None

    def __init__(self,
                 name: str,
                 description: Optional[str] = None
                 ):
        self.name = name
        self.description = description

    @abstractmethod
    def create(self
               ):
        print("create is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def delete(self
               ):
        print("delete is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def export(self
               ):
        print("export is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def setDefaultUnit(self,
                       unit: str
                       ):
        print("setDefaultUnit is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def createGroup(self,
                    name: str
                    ):
        print("createGroup is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def deleteGroup(self,
                    name: str,
                    removeChildren: bool
                    ):
        print("deleteGroup is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def removeFromGroup(self,
                        entityName: str,
                        groupName: str
                        ):
        print("removeFromGroup is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def assignToGroup(self,
                      entityName: str,
                      groupName: str,
                      removeFromOtherGroups: Optional[bool] = None
                      ):
        print("assignToGroup is called in the interface. Please override this method.")
        return self

    @abstractmethod
    def setVisible(self,
                   entityName: str,
                   isVisible: bool
                   ):
        print("setVisible is called in the interface. Please override this method.")
        return self


class Analytics(metaclass=ABCMeta):
    # Tools for collecting data about the entities and scene.

    def __init__(self
                 ):
        pass

    @abstractmethod
    def measureLandmarks(self,
                         landmark1Name: str,
                         landmark2Name: Optional[str] = None
                         ) -> Dimension:
        print("measureLandmarks is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def getWorldPose(self,
                     entityName: str
                     ):
        print("getWorldPose is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def getBoundingBox(self,
                       entityName: str
                       ) -> BoundaryBox:
        print("getBoundingBox is called in the interface. Please override this method.")
        raise NotImplementedError

    @abstractmethod
    def getDimensions(self,
                      entityName: str
                      ) -> Dimensions:
        print("getDimensions is called in the interface. Please override this method.")
        raise NotImplementedError
