from utilities import Dimension, CurveTypes, Point, Angle

class shape: 
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

    def cloneShape(self,
    shapeName:str \
    ):
        print("cloneShape is not implemented") # implement 
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
    shape1Name:str,  \
    shape1LandmarkName:str,  \
    shape2Name:str,  \
    shape2LandmarkName:str \
    ):
        print("loft is not implemented") # implement 
        return self

    def mirror(self,
    shapeName:str,  \
    landmarkName:str \
    ):
        print("mirror is not implemented") # implement 
        return self

    def pattern(self,
    shapeName:str,  \
    landmarkName:str \
    ):
        print("pattern is not implemented") # implement 
        return self

    def mask(self,
    shapeName:str,  \
    landmarkName:str \
    ):
        print("mask is not implemented") # implement 
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

    def union(self,
    withShapeName:str \
    ):
        print("union is not implemented") # implement 
        return self

    def subtract(self,
    withShapeName:str \
    ):
        print("subtract is not implemented") # implement 
        return self

    def intersect(self,
    withShapeName:str \
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

    def extrude(self,
    landmarkName:str,  \
    dimensions:str \
    ):
        print("extrude is not implemented") # implement 
        return self

    def remesh(self,
    strategy:str,  \
    amount:float \
    ):
        print("remesh is not implemented") # implement 
        return self

    def hollow(self,
    wallThickness:float \
    ):
        print("hollow is not implemented") # implement 
        return self

    def delete(self
    ):
        print("delete is not implemented") # implement 
        return self

    def isVisible(self,
    isVisible:bool \
    ):
        print("isVisible is not implemented") # implement 
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

class curve: 
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

class landmark: 
    # Capabilities for CodeToCAD.localToShapeWithName = None

    def __init__(self,
    localToShapeWithName:str=None \
    ):
        self.localToShapeWithName = localToShapeWithName

    def vertices(self,
    locations:str \
    ):
        print("vertices is not implemented") # implement 
        return self

    def rectangle(self,
    dimensions:str \
    ):
        print("rectangle is not implemented") # implement 
        return self

    def linearPattern(self
    ):
        print("linearPattern is not implemented") # implement 
        return "return value here"

    def circularPattern(self
    ):
        print("circularPattern is not implemented") # implement 
        return "return value here"

    def contourPattern(self
    ):
        print("contourPattern is not implemented") # implement 
        return "return value here"

class joint: 
    # Capabilities for CodeToCAD.shape1Name = None
    shape2Name = None
    shape1LandmarkName = None
    shape2LandmarkName = None
    jointType = None
    initialRotation = None
    limitRotation = None
    limitTranslation = None

    def __init__(self,
    shape1Name:str, \
    shape2Name:str, \
    shape1LandmarkName:str, \
    shape2LandmarkName:str, \
    jointType:str, \
    initialRotation:str, \
    limitRotation:str, \
    limitTranslation:str \
    ):
        self.shape1Name = shape1Name
        self.shape2Name = shape2Name
        self.shape1LandmarkName = shape1LandmarkName
        self.shape2LandmarkName = shape2LandmarkName
        self.jointType = jointType
        self.initialRotation = initialRotation
        self.limitRotation = limitRotation
        self.limitTranslation = limitTranslation

    def curve(self
    ):
        print("curve is not implemented") # implement 
        return "return value here"

class material: 
    # Capabilities for CodeToCAD.

    def __init__(self
    ):
        pass

class scene: 
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
    removeNestedShapes:bool \
    ):
        print("deleteGroup is not implemented") # implement 
        return self

    def removeShapeFromGroup(self,
    shapeName:str,  \
    groupName:str \
    ):
        print("removeShapeFromGroup is not implemented") # implement 
        return self

    def assignShapeToGroup(self,
    shapeName:str,  \
    groupName:str,  \
    removeFromOtherGroups:bool=None \
    ):
        print("assignShapeToGroup is not implemented") # implement 
        return self

    def setShapeVisibility(self,
    shapeName:str,  \
    isVisible:bool \
    ):
        print("setShapeVisibility is not implemented") # implement 
        return self

class analytics: 
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
    shapeName:str \
    ):
        print("getWorldPose is not implemented") # implement 
        return "return value here"

    def getBoundingBox(self,
    shapeName:str \
    ):
        print("getBoundingBox is not implemented") # implement 
        return "return value here"

    def getDimensions(self,
    shapeName:str \
    ):
        print("getDimensions is not implemented") # implement 
        return "return value here"

