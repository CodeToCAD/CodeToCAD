from abc import ABCMeta, abstractmethod

from core.utilities import Point, Dimension, CurveTypes, Angle


class Entity(metaclass=ABCMeta): 
    # Capabilities shared between Parts and Sketches.

    @abstractmethod
    def clone(self,
    entityName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def mirror(self,
    entityName:str,  \
    landmarkName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def pattern(self,
    entityName:str,  \
    landmarkName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def scale(self,
    dimensions:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def rotate(self,
    rotation:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def rename(self,
    name:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def remesh(self,
    strategy:str,  \
    amount:float \
    ):
        raise NotImplementedError

    @abstractmethod
    def delete(self,
    removeChildren:bool \
    ):
        raise NotImplementedError

    @abstractmethod
    def setVisible(self,
    isVisible:bool \
    ):
        raise NotImplementedError

    @abstractmethod
    def apply(self
    ):
        raise NotImplementedError

    @abstractmethod
    def getNativeInstance(self
    ):
        raise NotImplementedError

    @abstractmethod
    def select(self,
    landmarkName:str,  \
    selectionType:str \
    ):
        raise NotImplementedError

class Part(metaclass=ABCMeta): 
    # Capabilities Part CRUD.

    name = None
    description = None

    def __init__(self,
    name:str, \
    description:str=None \
    ):
        self.name = name
        self.description = description

    @abstractmethod
    def createFromFile(self,
    filePath:str,  \
    fileType:str=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createPrimitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createCube(self,
    width:str,  \
    length:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createCone(self,
    radius:str,  \
    height:str,  \
    draftRadius:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createCylinder(self,
    radius:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createTorus(self,
    innerRadius:str,  \
    outerRadius:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def createSphere(self,
    radius:str,  \
    keywordArguments:dict=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def verticies(self,
    verticies:list \
    ):
        raise NotImplementedError

    @abstractmethod
    def loft(self,
    part1Name:str,  \
    part1LandmarkName:str,  \
    part2Name:str,  \
    part2LandmarkName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def mask(self,
    partName:str,  \
    landmarkName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def union(self,
    withPartName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def subtract(self,
    withPartName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def intersect(self,
    withPartName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def bevel(self,
    landmarkName:str,  \
    angle:float,  \
    roundedness:int \
    ):
        raise NotImplementedError

    @abstractmethod
    def hollow(self,
    wallThickness:float \
    ):
        raise NotImplementedError

class Sketch(metaclass=ABCMeta): 
    # Capabilities related to adding, multiplying, and/or modifying a curve.

    name = None
    curveType = None
    description = None

    def __init__(self,
    name:str, \
    curveType:CurveTypes, \
    description:str=None \
    ):
        self.name = name
        self.curveType = curveType
        self.description = description

    @abstractmethod
    def extrude(self,
    length:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def sweep(self,
    profileCurveName:str,  \
    fillCap:bool \
    ):
        raise NotImplementedError

    @abstractmethod
    def createText(self,
    text:str,  \
    fontSize:Dimension,  \
    bold:bool,  \
    italic:bool,  \
    underlined:bool,  \
    characterSpacing:int,  \
    wordSpacing:int,  \
    lineSpacing:int,  \
    fontFilePath:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def createFromVertices(self,
    verticesArray:list[Point],  \
    interpolation:int \
    ):
        raise NotImplementedError

    @abstractmethod
    def createPoint(self
    ):
        raise NotImplementedError

    @abstractmethod
    def createLine(self,
    length:Dimension,  \
    symmetric:bool \
    ):
        raise NotImplementedError

    @abstractmethod
    def createLineBetweenPoints(self,
    pointA:Point,  \
    pointB:Point \
    ):
        raise NotImplementedError

    @abstractmethod
    def createCircle(self,
    radius:Dimension \
    ):
        raise NotImplementedError

    @abstractmethod
    def createEllipse(self,
    radiusA:Dimension,  \
    radiusB:Dimension \
    ):
        raise NotImplementedError

    @abstractmethod
    def createArc(self,
    radius:Dimension,  \
    angle:Angle \
    ):
        raise NotImplementedError

    @abstractmethod
    def createArcBetweenThreePoints(self,
    pointA:Point,  \
    pointB:Point,  \
    centerPoint:Point \
    ):
        raise NotImplementedError

    @abstractmethod
    def createSegment(self,
    innerRadius:Dimension,  \
    outerRadius:Dimension,  \
    angle:Angle \
    ):
        raise NotImplementedError

    @abstractmethod
    def createRectangle(self,
    length:Dimension,  \
    width:Dimension \
    ):
        raise NotImplementedError

    @abstractmethod
    def createPolygon(self,
    numberOfSides:int,  \
    length:Dimension,  \
    width:Dimension \
    ):
        raise NotImplementedError

    @abstractmethod
    def createTrapezoid(self,
    lengthUpper:Dimension,  \
    lengthLower:Dimension,  \
    height:Dimension \
    ):
        raise NotImplementedError

class Landmark(metaclass=ABCMeta): 
    # Landmarks are named positions on an entity.

    landmarkName = None
    localToEntityWithName = None

    def __init__(self,
    landmarkName:str, \
    localToEntityWithName:str \
    ):
        self.landmarkName = landmarkName
        self.localToEntityWithName = localToEntityWithName

class Joint(metaclass=ABCMeta): 
    # Joints define the relationships and constraints between entities.

    entity1Name = None
    entity2Name = None
    entity1LandmarkName = None
    entity2LandmarkName = None

    def __init__(self,
    entity1Name:str, \
    entity2Name:str, \
    entity1LandmarkName:str, \
    entity2LandmarkName:str \
    ):
        self.entity1Name = entity1Name
        self.entity2Name = entity2Name
        self.entity1LandmarkName = entity1LandmarkName
        self.entity2LandmarkName = entity2LandmarkName

    @abstractmethod
    def translateLandmarkOntoAnother(self
    ):
        raise NotImplementedError

    @abstractmethod
    def pivot(self
    ):
        raise NotImplementedError

    @abstractmethod
    def gear(self,
    ratio:float \
    ):
        raise NotImplementedError

    @abstractmethod
    def limitLocation(self,
    x:str,  \
    y:str,  \
    z:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def limitRotation(self,
    x:str,  \
    y:str,  \
    z:str \
    ):
        raise NotImplementedError

class Material(metaclass=ABCMeta): 
    # Materials affect the appearance and simulation properties of the parts.

    

    def __init__(self
    ):
        pass

class Scene(metaclass=ABCMeta): 
    # Scene, camera, lighting, rendering, animation, simulation and GUI related functionality.

    name = None
    description = None

    def __init__(self,
    name:str, \
    description:str=None \
    ):
        self.name = name
        self.description = description

    @abstractmethod
    def create(self
    ):
        raise NotImplementedError

    @abstractmethod
    def delete(self
    ):
        raise NotImplementedError

    @abstractmethod
    def export(self
    ):
        raise NotImplementedError

    @abstractmethod
    def setDefaultUnit(self,
    unit:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def createGroup(self,
    name:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def deleteGroup(self,
    name:str,  \
    removeChildren:bool \
    ):
        raise NotImplementedError

    @abstractmethod
    def removeFromGroup(self,
    entityName:str,  \
    groupName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def assignToGroup(self,
    entityName:str,  \
    groupName:str,  \
    removeFromOtherGroups:bool=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def setVisible(self,
    entityName:str,  \
    isVisible:bool \
    ):
        raise NotImplementedError

class Analytics(metaclass=ABCMeta): 
    # Tools for collecting data about the entities and scene.

    

    def __init__(self
    ):
        pass

    @abstractmethod
    def measureLandmarks(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        raise NotImplementedError

    @abstractmethod
    def getWorldPose(self,
    entityName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def getBoundingBox(self,
    entityName:str \
    ):
        raise NotImplementedError

    @abstractmethod
    def getDimensions(self,
    entityName:str \
    ):
        raise NotImplementedError

