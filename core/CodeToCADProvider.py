import core.utilities as Utilities
import core.CodeToCADInterface as CodeToCADInterface

from core.CodeToCADInterface import createUUID, getAbsoluteFilepath
from core.utilities import Point, Dimension, CurveTypes, Angle, min, max, center

class Entity(CodeToCADInterface.Entity): 
    # Capabilities for CodeToCAD.

    def clone(self,
    entityName:str \
    ):
        print("clone is not implemented") # implement 
        return self

    def mirror(self,
    entityName:str,  \
    landmarkName:str \
    ):
        print("mirror is not implemented") # implement 
        return self

    def pattern(self,
    entityName:str,  \
    landmarkName:str \
    ):
        print("pattern is not implemented") # implement 
        return self

    def scale(self,
    dimensions:str \
    ):
        print("scale is not implemented") # implement 
        return self

    def rotate(self,
    rotation:str \
    ):
        print("rotate is not implemented") # implement 
        return self

    def rename(self,
    name:str \
    ):
        print("rename is not implemented") # implement 
        return self

    def remesh(self,
    strategy:str,  \
    amount:float \
    ):
        print("remesh is not implemented") # implement 
        return self

    def delete(self,
    removeChildren:bool \
    ):
        print("delete is not implemented") # implement 
        return self

    def setVisible(self,
    isVisible:bool \
    ):
        print("setVisible is not implemented") # implement 
        return self

    def apply(self
    ):
        print("apply is not implemented") # implement 
        return self

    def getNativeInstance(self
    ):
        print("getNativeInstance is not implemented") # implement 
        return "return value here"

    def select(self,
    landmarkName:str,  \
    selectionType:str \
    ):
        print("select is not implemented") # implement 
        return self

class Part(CodeToCADInterface.Part): 
    # Capabilities for CodeToCAD.name = None
    description = None

    def __init__(self,
    name:str, \
    description:str=None \
    ):
        self.name = name
        self.description = description

    def createFromFile(self,
    filePath:str,  \
    fileType:str=None \
    ):
        print("createFromFile is not implemented") # implement 
        return self

    def createPrimitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        print("createPrimitive is not implemented") # implement 
        return self

    def createCube(self,
    width:str,  \
    length:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        print("createCube is not implemented") # implement 
        return self

    def createCone(self,
    radius:str,  \
    height:str,  \
    draftRadius:str,  \
    keywordArguments:dict=None \
    ):
        print("createCone is not implemented") # implement 
        return self

    def createCylinder(self,
    radius:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        print("createCylinder is not implemented") # implement 
        return self

    def createTorus(self,
    innerRadius:str,  \
    outerRadius:str,  \
    keywordArguments:dict=None \
    ):
        print("createTorus is not implemented") # implement 
        return self

    def createSphere(self,
    radius:str,  \
    keywordArguments:dict=None \
    ):
        print("createSphere is not implemented") # implement 
        return self

    def verticies(self,
    verticies:list \
    ):
        print("verticies is not implemented") # implement 
        return self

    def loft(self,
    part1Name:str,  \
    part1LandmarkName:str,  \
    part2Name:str,  \
    part2LandmarkName:str \
    ):
        print("loft is not implemented") # implement 
        return self

    def mask(self,
    partName:str,  \
    landmarkName:str \
    ):
        print("mask is not implemented") # implement 
        return self

    def union(self,
    withPartName:str \
    ):
        print("union is not implemented") # implement 
        return self

    def subtract(self,
    withPartName:str \
    ):
        print("subtract is not implemented") # implement 
        return self

    def intersect(self,
    withPartName:str \
    ):
        print("intersect is not implemented") # implement 
        return self

    def bevel(self,
    landmarkName:str,  \
    angle:float,  \
    roundedness:int \
    ):
        print("bevel is not implemented") # implement 
        return self

    def hollow(self,
    wallThickness:float \
    ):
        print("hollow is not implemented") # implement 
        return self

class Sketch(CodeToCADInterface.Sketch): 
    # Capabilities for CodeToCAD.name = None
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

    def extrude(self,
    length:str \
    ):
        print("extrude is not implemented") # implement 
        return self

    def sweep(self,
    profileCurveName:str,  \
    fillCap:bool \
    ):
        print("sweep is not implemented") # implement 
        return self

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
        print("createText is not implemented") # implement 
        return self

    def createFromVertices(self,
    verticesArray:list[Point],  \
    interpolation:int \
    ):
        print("createFromVertices is not implemented") # implement 
        return self

    def createPoint(self
    ):
        print("createPoint is not implemented") # implement 
        return self

    def createLine(self,
    length:Dimension,  \
    symmetric:bool \
    ):
        print("createLine is not implemented") # implement 
        return self

    def createLineBetweenPoints(self,
    pointA:Point,  \
    pointB:Point \
    ):
        print("createLineBetweenPoints is not implemented") # implement 
        return self

    def createCircle(self,
    radius:Dimension \
    ):
        print("createCircle is not implemented") # implement 
        return self

    def createEllipse(self,
    radiusA:Dimension,  \
    radiusB:Dimension \
    ):
        print("createEllipse is not implemented") # implement 
        return self

    def createArc(self,
    radius:Dimension,  \
    angle:Angle \
    ):
        print("createArc is not implemented") # implement 
        return self

    def createArcBetweenThreePoints(self,
    pointA:Point,  \
    pointB:Point,  \
    centerPoint:Point \
    ):
        print("createArcBetweenThreePoints is not implemented") # implement 
        return self

    def createSegment(self,
    innerRadius:Dimension,  \
    outerRadius:Dimension,  \
    angle:Angle \
    ):
        print("createSegment is not implemented") # implement 
        return self

    def createRectangle(self,
    length:Dimension,  \
    width:Dimension \
    ):
        print("createRectangle is not implemented") # implement 
        return self

    def createPolygon(self,
    numberOfSides:int,  \
    length:Dimension,  \
    width:Dimension \
    ):
        print("createPolygon is not implemented") # implement 
        return self

    def createTrapezoid(self,
    lengthUpper:Dimension,  \
    lengthLower:Dimension,  \
    height:Dimension \
    ):
        print("createTrapezoid is not implemented") # implement 
        return self

class Landmark(CodeToCADInterface.Landmark): 
    # Capabilities for CodeToCAD.landmarkName = None
    localToEntityWithName = None

    def __init__(self,
    landmarkName:str, \
    localToEntityWithName:str \
    ):
        self.landmarkName = landmarkName
        self.localToEntityWithName = localToEntityWithName

class Joint(CodeToCADInterface.Joint): 
    # Capabilities for CodeToCAD.entity1Name = None
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

    def translateLandmarkOntoAnother(self
    ):
        print("translateLandmarkOntoAnother is not implemented") # implement 
        return self

    def pivot(self
    ):
        print("pivot is not implemented") # implement 
        return self

    def gear(self,
    ratio:float \
    ):
        print("gear is not implemented") # implement 
        return self

    def limitLocation(self,
    x:str,  \
    y:str,  \
    z:str \
    ):
        print("limitLocation is not implemented") # implement 
        return self

    def limitRotation(self,
    x:str,  \
    y:str,  \
    z:str \
    ):
        print("limitRotation is not implemented") # implement 
        return self

class Material(CodeToCADInterface.Material): 
    # Capabilities for CodeToCAD.

    def __init__(self
    ):
        pass

class Scene(CodeToCADInterface.Scene): 
    # Capabilities for CodeToCAD.name = None
    description = None

    def __init__(self,
    name:str, \
    description:str=None \
    ):
        self.name = name
        self.description = description

    def create(self
    ):
        print("create is not implemented") # implement 
        return "return value here"

    def delete(self
    ):
        print("delete is not implemented") # implement 
        return "return value here"

    def export(self
    ):
        print("export is not implemented") # implement 
        return "return value here"

    def setDefaultUnit(self,
    unit:str \
    ):
        print("setDefaultUnit is not implemented") # implement 
        return self

    def createGroup(self,
    name:str \
    ):
        print("createGroup is not implemented") # implement 
        return self

    def deleteGroup(self,
    name:str,  \
    removeChildren:bool \
    ):
        print("deleteGroup is not implemented") # implement 
        return self

    def removeFromGroup(self,
    entityName:str,  \
    groupName:str \
    ):
        print("removeFromGroup is not implemented") # implement 
        return self

    def assignToGroup(self,
    entityName:str,  \
    groupName:str,  \
    removeFromOtherGroups:bool=None \
    ):
        print("assignToGroup is not implemented") # implement 
        return self

    def setVisible(self,
    entityName:str,  \
    isVisible:bool \
    ):
        print("setVisible is not implemented") # implement 
        return self

class Analytics(CodeToCADInterface.Analytics): 
    # Capabilities for CodeToCAD.

    def __init__(self
    ):
        pass

    def measureLandmarks(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        print("measureLandmarks is not implemented") # implement 
        return "return value here"

    def getWorldPose(self,
    entityName:str \
    ):
        print("getWorldPose is not implemented") # implement 
        return "return value here"

    def getBoundingBox(self,
    entityName:str \
    ):
        print("getBoundingBox is not implemented") # implement 
        return "return value here"

    def getDimensions(self,
    entityName:str \
    ):
        print("getDimensions is not implemented") # implement 
        return "return value here"

