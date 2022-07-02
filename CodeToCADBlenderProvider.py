import math
import CodeToCAD.utilities as Utilities
import BlenderDefinitions
import BlenderActions

from pathlib import Path
from types import LambdaType

from BlenderEvents import BlenderEvents

def debugOnReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {} Type: {}".format(update.id.name, type(update.id)))

def setup(blenderEvents):

    # start the updateEventThread
    blenderEvents.isWaitForAssertionsEnabled = False
    BlenderActions.addTimer(blenderEvents.blenderEventsHandler.processEventsAndOperations)

    # tell Blender to notify onReceiveBlenderDependencyGraphUpdateEvent when its dependency graph is updated. https://docs.blender.org/api/current/bpy.app.handlers.html 
    BlenderActions.addDependencyGraphUpdateListener(blenderEvents.onReceiveBlenderDependencyGraphUpdateEvent)

    BlenderActions.addDependencyGraphUpdateListener(debugOnReceiveBlenderDependencyGraphUpdateEvent)

# TODO: move this to a main function
blenderEvents = BlenderEvents()
setup(blenderEvents)

class shape: 
    # Text to 3D Modeling Automation Capabilities.

    name = None
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
    
        path = Path(filePath)

        fileName = path.stem
        
        blenderEvents.addToBlenderOperationsQueue(
            "Importing {}".format(fileName),
            lambda: BlenderActions.blenderImportFile(filePath, fileType),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == fileName
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(fileName),
            lambda: True,
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.MESH.value and update.id.name == fileName
        )
        
        self.rename(self.name, fileName)
        
        return self

    def cloneShape(self,
    shapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Cloning object {} to create {}".format(shapeName, self.name),
            lambda: BlenderActions.duplicateObject(shapeName, self.name),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self


    def createPrimitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        # TODO: account for blender auto-renaming with sequential numbers
        expectedNameOfObjectInBlender = primitiveName[0].upper() + primitiveName[1:]
        
        blenderEvents.addToBlenderOperationsQueue(
            "Creating primitive {}".format(primitiveName),
            lambda: BlenderActions.addPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(primitiveName),
            lambda: True,
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.MESH.value and update.id.name == expectedNameOfObjectInBlender
        )

        self.rename(self.name, expectedNameOfObjectInBlender)

        return self


    def createCube(self,
    width:str,  \
    length:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cube", "{},{},{}".format(width,length,height), keywordArguments)

    def createCone(self,
    radius:str,  \
    height:str,  \
    draftRadius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cone", "{},{},{}".format(radius,height,draftRadius), keywordArguments)

    def createCylinder(self,
    radius:str,  \
    height:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("cylinder", "{},{}".format(radius,height), keywordArguments)

    def createTorus(self,
    innerRadius:str,  \
    outerRadius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("torus", "{},{}".format(innerRadius,outerRadius), keywordArguments)

    def createSphere(self,
    radius:str,  \
    keywordArguments:dict=None \
    ):
        return self.createPrimitive("sphere", "{}".format(radius), keywordArguments)


    def verticies(self,
    landmarkName:str \
    ):
        print("verticies is not implemented") # implement 
        return self

    def loft(self,
    shape1Name:str,  \
    shape2Name:str \
    ):
        print("loft is not implemented") # implement 
        return self

    def mirror(self,
    mirrorAcrossShapeName:str, \
    axis = (True, True, True)
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Mirror modifier to {}".format(self.name),
            lambda: BlenderActions.applyMirrorModifier(self.name, mirrorAcrossShapeName, axis),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        
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

    def translate(self,
    dimensions:str\
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Translating {}".format(self.name),
            lambda: BlenderActions.translateObject(self.name, dimensionsList, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def setPosition(self,
    dimensions:str\
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))

        blenderEvents.addToBlenderOperationsQueue(
            "Setting position of {}".format(self.name),
            lambda: BlenderActions.translateObject(self.name, dimensionsList, BlenderDefinitions.BlenderTranslationTypes.ABSOLUTE),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self
        
    def scale(self,
    dimensions:str
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Scaling {}".format(self.name),
            lambda: BlenderActions.scaleObject(self.name, dimensionsList),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        
        return self

    def rotate(self,
    rotation:str \
    ):
        angleList:list[Utilities.Angle] = Utilities.getAnglesFromString(rotation) or []

        while len(angleList) < 3:
            angleList.append(Utilities.Angle("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Rotating {}".format(self.name),
            lambda: BlenderActions.rotateObject(self.name, angleList, BlenderDefinitions.BlenderRotationTypes.EULER),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def rename(self,
    newName:str, \
    expectedNameOfObjectInBlender:str = None
    ):
        expectedNameOfObjectInBlender = expectedNameOfObjectInBlender or self.name
        self.name = newName if expectedNameOfObjectInBlender else self.name
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming object {} to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: BlenderActions.updateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming mesh {} to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: BlenderActions.updateObjectDataName(self.name, self.name)
            ,
            lambda update: update.id.name == self.name
        )
        return self

    def union(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Union modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.UNION,
                        withShapeName
                    ),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def subtract(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Difference modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                    self.name,
                    BlenderDefinitions.BlenderBooleanTypes.DIFFERENCE,
                    withShapeName
                ),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def intersect(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Intersect modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.INTERSECT,
                        withShapeName
                    ),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
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
        
    def revolve(self,
    angle:str,
    axis:Utilities.Axis,
    shapeNameToDetermineAxis = None
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying revolve (screw) modifier to {}".format(self.name),
            lambda: BlenderActions.applyScrewModifier(self.name, Utilities.Angle(angle).toRadians(), axis, shapeNameToDetermineAxis=shapeNameToDetermineAxis),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def thicken(self,
    thickness:int
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying solidify modifier to {}".format(self.name),
            lambda: BlenderActions.applySolidifyModifier(self.name, Utilities.Dimension(thickness)),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self
        
    def screw(self,
    angle:str,
    axis:Utilities.Axis,
    screwPitch:str = 0,
    iterations:int = 1
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying screw modifier to {}".format(self.name),
            lambda: BlenderActions.applyScrewModifier(self.name, Utilities.Angle(angle).toRadians(), axis, screwPitch=Utilities.Dimension(screwPitch), iterations=iterations),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def remesh(self,
    strategy:str = None,  \
    amount:float = None \
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Applying EdgeSplit modifier to {}".format(self.name),
            lambda: BlenderActions.addModifier(self.name, BlenderDefinitions.BlenderModifiers.EDGE_SPLIT, {"name": "EdgeDiv", "split_angle": math.radians(30)}),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Subdivision Surface modifier to {}".format(self.name),
            lambda: BlenderActions.addModifier(self.name, BlenderDefinitions.BlenderModifiers.SUBSURF, {"name": "Subdivision", "levels": 2}),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

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
    
    # This is a blender specific action to apply the dependency graph modifiers onto a mesh
    def apply(self):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Dependency Graph changes to {}. This permanently changes the mesh.".format(self.name),
            lambda: BlenderActions.applyDependencyGraph(self.name),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def landmark(self, landmarkName, localPosition):

        landmarkObject = landmark(landmarkName, self.name)
        
        blenderEvents.addToBlenderOperationsQueue(
            "Creating landmark {} on {}.".format(landmarkName, self.name),
            lambda: BlenderActions.createLandmark(self.name, landmarkObject.landmarkName, localPosition),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == landmarkObject.landmarkName
        )
        

        return self
        

    def isVisible(self,
    isVisible:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" setting isVisible {}".format(self.name, isVisible),
            lambda: BlenderActions.setObjectVisibility(self.name, isVisible),
            None
        ) 
        return self

    def getNativeInstance(self
    ): 
        return BlenderActions.getObject(self.name)
        
    def select(self,
    landmarkName:str,  \
    selectionType:str = "face" \
    ):
        landmarkObject = landmark(landmarkName, self.name)
        landmarkLocation = BlenderActions.getObjectWorldLocation(landmarkObject.landmarkName)
        [closestPoint, normal, blenderPolygon, blenderVertices] = BlenderActions.getClosestPointsToVertex(self.name, landmarkLocation)

        if blenderVertices != None:
            for vertex in blenderVertices:
                vertex.select = True

        return self

class curve(shape):
    
    name = None
    curveType = None
    description = None

    def __init__(self,
    name:str, \
    curveType:Utilities.CurveTypes=None, \
    description:str=None \
    ):
        self.name = name
        self.curveType = curveType
        self.description = description


    def sweep(self,
        profileCurveName,
        fillCap = False
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: BlenderActions.addBevelObjectToCurve(self.name, profileCurveName, fillCap),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self
        
    def curve(self,
        profileCurveName
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: BlenderActions.applyCurveModifier(self.name, profileCurveName),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def createText(self,
        text,
        size = "1m",
        bold = False,
        italic = False,
        underlined = False,
        characterSpacing = 1,
        wordSpacing = 1,
        lineSpacing = 1,
        fontFilePath = None
        ):

        size = Utilities.Dimension(size)

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: BlenderActions.createText(self.name, text, size, bold, italic, underlined, characterSpacing, wordSpacing, lineSpacing, fontFilePath),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def createFromVerticies(self,
        coordinates, \
        interpolation = 64 \
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: BlenderActions.createCurve(self.name, BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else BlenderDefinitions.BlenderCurveTypes.BEZIER, coordinates, interpolation),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self


    def createPrimitiveDecorator(curvePrimitiveType:Utilities.CurvePrimitiveTypes):
        def decorator(primitiveFunction):
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = BlenderDefinitions.BlenderCurvePrimitiveTypes.fromCurvePrimitiveTypes(curvePrimitiveType)

                blenderPrimitiveFunction = BlenderActions.getBlenderCurvePrimitiveFunction(blenderCurvePrimitiveType)

                blenderEvents.addToBlenderOperationsQueue(
                    "Creating curve primitive {}".format(self.name),
                    lambda: blenderPrimitiveFunction(
                        *args[1:],
                        dict(
                                {"curveType": BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else None}
                                , **kwargs
                            )
                        ),
                    lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == blenderCurvePrimitiveType.name
                )
                
                self.rename(self.name, blenderCurvePrimitiveType.name)

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Point)
    def createPoint(self, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.LineTo)
    def createLineTo(self, endLocation, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Line)
    def createLine(self, length, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Angle)
    def createAngle(self, length, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Circle)
    def createCircle(self, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Ellipse)
    def createEllipse(self, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Arc)
    def createArc(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Sector)
    def createSector(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Segment)
    def createSegment(self, outter_radius, inner_radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Rectangle)        
    def createRectangle(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Rhomb)
    def createRhomb(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Polygon)
    def createPolygon(self, numberOfSides, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Polygon_ab)
    def createPolygon_ab(self, numberOfSides, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(Utilities.CurvePrimitiveTypes.Trapezoid)
    def createTrapezoid(self, length_upper, length_lower, height, keywordArguments = {}):
        return self

class landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToShapeWithName = None
    landmarkName = None

    def __init__(self,
    landmarkName:str,
    localToShapeWithName:str=None \
    ):
        self.localToShapeWithName = localToShapeWithName
        
        if localToShapeWithName:
            self.landmarkName = "{}_{}".format(localToShapeWithName, landmarkName)
        else:
            self.landmarkName = landmarkName

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
        print("linearPattern is not implemented") #      implement 
        return self

    def circularPattern(self
    ):
        print("circularPattern is not implemented") # implement 
        return self

    def contourPattern(self
    ):
        print("contourPattern is not implemented") # implement 
        return self

class joint: 
    # Text to 3D Modeling Automation Capabilities.

    shape1Name = None
    shape2Name = None
    shape1Landmark:landmark = None
    shape2Landmark:landmark = None
    jointType = None
    initialRotation = None
    limitRotation = None
    limitTranslation = None

    def __init__(self,
    shape1Name:str, \
    shape2Name:str, \
    shape1LandmarkName:str, \
    shape2LandmarkName:str, \
    jointType:str = None, \
    initialRotation:str = None, \
    limitRotation:str = None, \
    limitTranslation:str = None \
    ):
        self.shape1Name = shape1Name
        self.shape2Name = shape2Name
        self.shape1Landmark = landmark(shape1LandmarkName, shape1Name)
        self.shape2Landmark = landmark(shape2LandmarkName, shape2Name)
        self.jointType = jointType
        self.initialRotation = initialRotation
        self.limitRotation = limitRotation
        self.limitTranslation = limitTranslation

        
    def transformLandmarkOntoAnother(self):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Transforming {} landmark {} onto {} landmark {}".format(self.shape1Name, self.shape1Landmark.landmarkName, self.shape2Name, self.shape2Landmark.landmarkName),
            lambda: BlenderActions.transformLandmarkOntoAnother(self.shape1Name, self.shape2Name, self.shape1Landmark.landmarkName, self.shape2Landmark.landmarkName),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.shape2Landmark.landmarkName,
        )

        return self

class material: 
    # Text to 3D Modeling Automation Capabilities.


    def __init__(self
    ):
        pass


class scene: 
    # Text to 3D Modeling Automation Capabilities.

    name = None
    description = None

    # Names a scene
    def __init__(self,
    name:str = "Scene", # Uses Blender's default Scene
    description:str=None \
    ):
        self.name = name
        self.description = description

    def create(self):
        print("create is not implemented") # implement 
        return self

    def delete(self):
        print("delete is not implemented") # implement 
        return self

    def export(self
    ):
        print("export is not implemented") # implement 
        return self

    def setDefaultUnit(self,
    unit:Utilities.LengthUnit \
    ):

        if type(unit) == str:
            unit = Utilities.LengthUnit.fromString(unit)
            
        unit = BlenderDefinitions.BlenderLength.fromLengthUnit(unit)

        blenderEvents.addToBlenderOperationsQueue(
            f"Setting document units to {unit.name}",
            lambda: BlenderActions.setDefaultUnit(unit, self.name), 
            lambda update: update.id.name == "Scene"
        )

        return self

    def createGroup(self,
    name:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Creating a {} collection".format(name),
            lambda: BlenderActions.createCollection(name, self.name), 
            lambda update: update.id.name == name
        )

        return self

    def deleteGroup(self,
    name:str,  \
    removeNestedShapes:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Removing the {} collection".format(name),
            lambda: BlenderActions.removeCollection(name, removeNestedShapes), 
            lambda update: update.id.name == "Scene"
        )

        return self
        
    def removeShapeFromGroup(self,
    shapeName:str, \
    groupName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Removing {} from collection {}".format(shapeName, groupName),
            lambda: BlenderActions.removeObjectFromCollection(shapeName, groupName), 
            lambda update: update.id.name == groupName
            )

        return self

        
    def assignShapeToGroup(self,
    shapeName:str, \
    groupName:str, \
    removeFromOtherGroups:bool = True \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Assigning object {} to collection {}".format(shapeName, groupName),
            lambda: BlenderActions.assignObjectToCollection(shapeName, groupName, self.name, removeFromOtherGroups), 
            lambda update: update.id.name == groupName
        )

        return self
        

    def setShapeVisibility(self,
    shapeName:str, \
    isVisible:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" setting isVisible {}".format(shapeName, isVisible),
            lambda: BlenderActions.setObjectVisibility(shapeName, isVisible),
            lambda update: update.id.name == self.name
        ) 

        return self

class analytics: 
    # Text to 3D Modeling Automation Capabilities.

    def execute(self, callback: LambdaType, description = ""):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Running analytics execute. {}".format(description),
            callback,
            None
        )

    def measureLandmarks(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        print("measure is not implemented") # implement 
        return None

    def getWorldPose(self,
    shapeName:str \
    ):
        return BlenderActions.getObjectWorldPose(shapeName)

    def getBoundingBox(self,
    shapeName:str \
    ):
        return BlenderActions.getBoundingBox(shapeName)

    def getDimensions(self,
    shapeName:str \
    ):
        
        dimensions = BlenderActions.getObject(shapeName).dimensions
        return [
            Utilities.Dimension(
                dimension,
                BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value
            ) 
            for dimension in dimensions
            ]
