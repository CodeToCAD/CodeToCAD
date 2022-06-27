import math
from pathlib import Path
from types import LambdaType
from CodeToCAD.utilities import *
from BlenderExecute import *
from BlenderEvents import BlenderEvents

def debugOnReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {} Type: {}".format(update.id.name, type(update.id)))

def setup(blenderEvents):

    # start the updateEventThread
    # blenderEvents.startBlenderEventThread()
    blenderEvents.isWaitForAssertionsEnabled = False
    blenderEvents.startBlenderEventTimer(bpy)

    # tell Blender to notify onReceiveBlenderDependencyGraphUpdateEvent when its dependency graph is updated. https://docs.blender.org/api/current/bpy.app.handlers.html 
    bpy.app.handlers.depsgraph_update_post.append(blenderEvents.onReceiveBlenderDependencyGraphUpdateEvent)

    # blenderSceneLockInterface(True)
    
    bpy.app.handlers.depsgraph_update_post.append(debugOnReceiveBlenderDependencyGraphUpdateEvent)

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
            lambda: blenderImportFile(filePath, fileType),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == fileName
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(fileName),
            lambda: True,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == fileName
        )
        
        self.rename(self.name, fileName)
        
        return self

    def cloneShape(self,
    shapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Cloning object {} to create {}".format(shapeName, self.name),
            lambda: blenderDuplicateObject(shapeName, self.name),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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
            lambda: blenderAddPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(primitiveName),
            lambda: True,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == expectedNameOfObjectInBlender
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
            lambda: blenderApplyMirrorModifier(self.name, mirrorAcrossShapeName, axis),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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
        dimensionsList:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensionsList = convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Translating {}".format(self.name),
            lambda: blenderTranslationObject(self.name, dimensionsList, BlenderTranslationTypes.RELATIVE),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

    def setPosition(self,
    dimensions:str\
    ):
        dimensionsList:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensionsList = convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Dimension("1"))

        blenderEvents.addToBlenderOperationsQueue(
            "Setting position of {}".format(self.name),
            lambda: blenderTranslationObject(self.name, dimensionsList, BlenderTranslationTypes.ABSOLUTE),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self
        
    def scale(self,
    dimensions:str
    ):
        dimensionsList:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensionsList = convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Scaling {}".format(self.name),
            lambda: blenderScaleObject(self.name, dimensionsList),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        
        return self

    def rotate(self,
    rotation:str \
    ):
        angleList:list[Angle] = getAnglesFromString(rotation) or []

        while len(angleList) < 3:
            angleList.append(Angle("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Rotating {}".format(self.name),
            lambda: blenderRotateObject(self.name, angleList, BlenderRotationTypes.EULER),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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
            lambda: blenderUpdateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming mesh {} to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: blenderUpdateObjectDataName(self.name, self.name)
            ,
            lambda update: update.id.name == self.name
        )
        return self

    def union(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Union modifier to {}".format(self.name),
            lambda: blenderApplyBooleanModifier(self.name, BlenderBooleanTypes.UNION, withShapeName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def subtract(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Difference modifier to {}".format(self.name),
            lambda: blenderApplyBooleanModifier(self.name, BlenderBooleanTypes.DIFFERENCE, withShapeName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def intersect(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Intersect modifier to {}".format(self.name),
            lambda: blenderApplyBooleanModifier(self.name, BlenderBooleanTypes.INTERSECT, withShapeName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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
    axis:Axis,
    shapeNameToDetermineAxis = None
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying revolve (screw) modifier to {}".format(self.name),
            lambda: blenderApplyScrewModifier(self.name, Angle(angle).toRadians(), axis, shapeNameToDetermineAxis=shapeNameToDetermineAxis),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def thicken(self,
    thickness:int
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying solidify modifier to {}".format(self.name),
            lambda: blenderApplySolidifyModifier(self.name, Dimension(thickness)),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self
        
    def screw(self,
    angle:str,
    axis:Axis,
    screwPitch:str = 0,
    iterations:int = 1
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying screw modifier to {}".format(self.name),
            lambda: blenderApplyScrewModifier(self.name, Angle(angle).toRadians(), axis, screwPitch=Dimension(screwPitch), iterations=iterations),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def remesh(self,
    strategy:str = None,  \
    amount:float = None \
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Applying EdgeSplit modifier to {}".format(self.name),
            lambda: BlenderModifiers.EDGE_SPLIT.blenderAddModifier(self.name, {"name": "EdgeDiv", "split_angle": math.radians(30)}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Subdivision Surface modifier to {}".format(self.name),
            lambda: BlenderModifiers.SUBSURF.blenderAddModifier(self.name, {"name": "Subdivision", "levels": 2}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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
            lambda: blenderApplyDependencyGraph(self.name),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

    def landmark(self, landmarkName, localPosition):

        landmarkObject = landmark(landmarkName, self.name)
        
        blenderEvents.addToBlenderOperationsQueue(
            "Creating landmark {} on {}.".format(landmarkName, self.name),
            lambda: blenderCreateLandmark(self.name, landmarkObject.landmarkName, localPosition),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == landmarkObject.landmarkName
        )
        

        return self
        

    def isVisible(self,
    isVisible:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" setting isVisible {}".format(self.name, isVisible),
            lambda: blenderSetObjectVisibility(self.name, isVisible),
            None
        ) 
        return self

    def getNativeInstance(self
    ): 
        return blenderGetObject(self.name)
        
    def select(self,
    landmarkName:str,  \
    selectionType:str = "face" \
    ):
        landmarkObject = landmark(landmarkName, self.name)
        landmarkLocation = blenderGetObjectWorldLocation(landmarkObject.landmarkName)
        [closestPoint, normal, blenderPolygon, blenderVertices] = blenderGetClosestPointsToVertex(self.name, landmarkLocation)

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
    curveType:CurveTypes=None, \
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
            lambda: blenderAddBevelObjectToCurve(self.name, profileCurveName, fillCap),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self
        
    def curve(self,
        profileCurveName
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: blenderApplyCurveModifier(self.name, profileCurveName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
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

        size = Dimension(size)

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: blenderCreateText(self.name, text, size, bold, italic, underlined, characterSpacing, wordSpacing, lineSpacing, fontFilePath),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

    def createFromVerticies(self,
        coordinates, \
        interpolation = 64 \
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating curve {} from vertices.".format(self.name),
            lambda: blenderCreateCurve(self.name, BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else BlenderCurveTypes.BEZIER, coordinates, interpolation),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self


    def createPrimitiveDecorator(curvePrimitiveType:CurvePrimitiveTypes):
        def decorator(primitiveFunction):
            def wrapper(*args, **kwargs):

                self = args[0]

                blenderCurvePrimitiveType = BlenderCurvePrimitiveTypes.fromCurvePrimitiveTypes(curvePrimitiveType)

                blenderPrimitiveFunction = blenderCurvePrimitiveType.getBlenderCurvePrimitiveFunction()

                blenderEvents.addToBlenderOperationsQueue(
                    "Creating curve primitive {}".format(self.name),
                    lambda: blenderPrimitiveFunction(
                        *args[1:],
                        dict(
                                {"curveType": BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else None}
                                , **kwargs
                            )
                        ),
                    lambda update: type(update.id) == bpy.types.Object and update.id.name == blenderCurvePrimitiveType.name
                )
                
                self.rename(self.name, blenderCurvePrimitiveType.name)

                return primitiveFunction(*args, **kwargs)
            return wrapper
        return decorator

    @createPrimitiveDecorator(CurvePrimitiveTypes.Point)
    def createPoint(self, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.LineTo)
    def createLineTo(self, endLocation, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Line)
    def createLine(self, length, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Angle)
    def createAngle(self, length, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Circle)
    def createCircle(self, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Ellipse)
    def createEllipse(self, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Arc)
    def createArc(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Sector)
    def createSector(self, radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Segment)
    def createSegment(self, outter_radius, inner_radius, angle, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Rectangle)        
    def createRectangle(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Rhomb)
    def createRhomb(self, length, width, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Polygon)
    def createPolygon(self, numberOfSides, radius, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Polygon_ab)
    def createPolygon_ab(self, numberOfSides, radius_x, radius_y, keywordArguments = {}):
        return self
    @createPrimitiveDecorator(CurvePrimitiveTypes.Trapezoid)
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
            lambda: blenderTransformLandmarkOntoAnother(self.shape1Name, self.shape2Name, self.shape1Landmark.landmarkName, self.shape2Landmark.landmarkName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.shape2Landmark.landmarkName,
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
    unit:BlenderLength \
    ):
        unitSystem =  unit.getSystem()
        unitName =  unit.name
        blenderEvents.addToBlenderOperationsQueue("Setting document units to {} {}".format(unitSystem, unitName), lambda: blenderSetDefaultUnit(unitSystem, unitName, self.name), 
        lambda update: update.id.name == "Scene")
        return self

    def createGroup(self,
    name:str \
    ):
        blenderEvents.addToBlenderOperationsQueue("Creating a {} collection".format(name), lambda: blenderCreateCollection(name, self.name), 
        lambda update: update.id.name == name)
        return self

    def deleteGroup(self,
    name:str,  \
    removeNestedShapes:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue("Removing the {} collection".format(name), lambda: blenderRemoveCollection(name, removeNestedShapes), 
        lambda update: update.id.name == "Scene")
        return self
        
    def removeShapeFromGroup(self,
    shapeName:str, \
    groupName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Removing {} from collection {}".format(shapeName, groupName),
            lambda: blenderRemoveObjectFromCollection(shapeName, groupName), 
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
            lambda: blenderAssignObjectToCollection(shapeName, groupName, self.name, removeFromOtherGroups), 
            lambda update: update.id.name == groupName
            )
        return self
        

    def setShapeVisibility(self,
    shapeName:str, \
    isVisible:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" setting isVisible {}".format(shapeName, isVisible),
            lambda: blenderSetObjectVisibility(shapeName, isVisible),
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
        return blenderGetObjectWorldPose(shapeName)

    def getBoundingBox(self,
    shapeName:str \
    ):
        return blenderGetBoundingBox(shapeName)

    def getDimensions(self,
    shapeName:str \
    ):
        dimensions = bpy.data.objects[shapeName].dimensions
        return [
            Dimension(
                dimension,
                defaultBlenderUnit.value
            ) 
            for dimension in dimensions
            ]
