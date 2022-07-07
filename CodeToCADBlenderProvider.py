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

class Entity:
    def translate(self,
    dimensions:str\
    ):
        dimensionsList:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimensions) or []
        
        dimensionsList = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Utilities.Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Translating {}".format(self.name),
            lambda: BlenderActions.translateObject(self.name, dimensionsList, BlenderDefinitions.BlenderTranslationTypes.RELATIVE),
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
    newName:str,
    renameData = True
    ):

        blenderEvents.addToBlenderOperationsQueue(
            "Renaming object {} to {}".format(self.name, newName),
            lambda: BlenderActions.updateObjectName(self.name, newName)
            ,
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        if renameData:
            blenderEvents.addToBlenderOperationsQueue(
                "Renaming mesh {} to {}".format(self.name, newName),
                lambda: BlenderActions.updateObjectDataName(newName, newName)
                ,
                lambda update: update.id.name == self.name
            )

        return self


    def clone(self,
    partName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Cloning object {} to create {}".format(partName, self.name),
            lambda: BlenderActions.duplicateObject(partName, self.name),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
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
    entityNameToDetermineAxis = None
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying revolve (screw) modifier to {}".format(self.name),
            lambda: BlenderActions.applyScrewModifier(self.name, Utilities.Angle(angle).toRadians(), axis, entityNameToDetermineAxis=entityNameToDetermineAxis),
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
            lambda: BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.EDGE_SPLIT, {"name": "EdgeDiv", "split_angle": math.radians(30)}),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Subdivision Surface modifier to {}".format(self.name),
            lambda: BlenderActions.applyModifier(self.name, BlenderDefinitions.BlenderModifiers.SUBSURF, {"name": "Subdivision", "levels": 2}),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def mirror(self,
    mirrorAcrossEntityName:str, \
    axis = (True, True, True)
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Mirror modifier to {}".format(self.name),
            lambda: BlenderActions.applyMirrorModifier(self.name, mirrorAcrossEntityName, axis),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        
        return self

    def pattern(self,
    partName:str,  \
    landmarkName:str \
    ):
        print("pattern is not implemented") # implement 
        return self


    def delete(self,
        removeChildren = True
    ):
        blenderEvents.addToBlenderOperationsQueue(
            f"Removing entity {self.name}. Removing children: {removeChildren}",
            lambda: BlenderActions.removeObject(self.name, removeChildren),
            lambda update: update.id.name == self.name
        )
        return self
    
    # This is a blender specific action to apply the dependency graph modifiers onto a mesh
    def apply(self):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Dependency Graph changes to {}. This permanently changes the mesh.".format(self.name),
            lambda: BlenderActions.applyDependencyGraph(self.name),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        
        blenderEvents.addToBlenderOperationsQueue(
            f"Removing old mesh with name {self.name}",
            lambda: BlenderActions.removeMesh(self.name)
            ,
            lambda update: update.id.name == self.name
        )

        
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming new mesh name to {}".format(self.name, self.name),
            lambda: BlenderActions.updateObjectDataName(self.name, self.name)
            ,
            lambda update: update.id.name == self.name
        )
        
        
        blenderEvents.addToBlenderOperationsQueue(
            f"Removing modifiers for object {self.name}",
            lambda: BlenderActions.clearModifiers(self.name)
            ,
            lambda update: update.id.name == self.name
        )

        return self

    def landmark(self, landmarkName, localPosition):

        landmarkObjectName = Landmark(landmarkName, self.name).landmarkName
        
        # Create an Empty object to represent the landmark
        # Using an Empty object allows us to parent the object to this Empty.
        # Parenting inherently transforms the landmark whenever the object is translated/rotated/scaled.
        # This might not work in other CodeToCAD implementations, but it does in Blender
        Part(landmarkObjectName).createPrimitive("Empty", "0")

        # Assign the landmark to the parent's collection
        blenderEvents.addToBlenderOperationsQueue(
            "Assigning landmark {} to the {} object's collection.".format(landmarkName, self.name),
            lambda: BlenderActions.assignObjectToCollection(landmarkObjectName, BlenderActions.getObjectCollection(self.name)),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == landmarkObjectName
        )

        # Parent the landmark to the object
        blenderEvents.addToBlenderOperationsQueue(
            "Make object {} the parent of landmark {}.".format(self.name, landmarkName),
            lambda: BlenderActions.makeParent(landmarkObjectName, self.name),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == landmarkObjectName
        )

        blenderEvents.addToBlenderOperationsQueue(
            "Setting position of landmark {}".format(landmarkName),
            lambda: BlenderActions.transformLandmarkInsideParent(self.name, landmarkObjectName, localPosition),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == landmarkObjectName
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
        landmarkObject = Landmark(landmarkName, self.name)
        landmarkLocation = BlenderActions.getObjectWorldLocation(landmarkObject.landmarkName)
        [closestPoint, normal, blenderPolygon, blenderVertices] = BlenderActions.getClosestPointsToVertex(self.name, landmarkLocation)

        if blenderVertices != None:
            for vertex in blenderVertices:
                vertex.select = True

        return self

class Part(Entity):

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
            lambda: BlenderActions.importFile(filePath, fileType),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == fileName
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(fileName),
            lambda: True,
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.MESH.value and update.id.name == fileName
        )
        
        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part(fileName).rename(self.name)
        
        return self

    def createPrimitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        # TODO: account for blender auto-renaming with sequential numbers
        primitiveType = getattr(BlenderDefinitions.BlenderObjectPrimitiveTypes, primitiveName.lower(), None)
        expectedNameOfObjectInBlender = primitiveType.defaultNameInBlender() if primitiveType else None

        assert expectedNameOfObjectInBlender != None, \
            f"Primitive type with name {primitiveName} is not supported."
        
        blenderEvents.addToBlenderOperationsQueue(
            "Creating primitive {}".format(expectedNameOfObjectInBlender),
            lambda: BlenderActions.addPrimitive(primitiveType, dimensions, keywordArguments),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == expectedNameOfObjectInBlender
        )

        # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
        # therefore, we'll use the object's "expected" name and rename it to what it should be
        # note: this will fail if the "expected" name is incorrect
        Part(expectedNameOfObjectInBlender).rename(self.name, primitiveType.hasData())

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
    part1Name:str,  \
    part2Name:str \
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
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Union modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.UNION,
                        withPartName
                    ),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def subtract(self,
    withPartName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Difference modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                    self.name,
                    BlenderDefinitions.BlenderBooleanTypes.DIFFERENCE,
                    withPartName
                ),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )
        return self

    def intersect(self,
    withPartName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Applying Boolean Intersect modifier to {}".format(self.name),
            lambda: BlenderActions.applyBooleanModifier(
                        self.name,
                        BlenderDefinitions.BlenderBooleanTypes.INTERSECT,
                        withPartName
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

    def hollow(self,
    wallThickness:float \
    ):
        print("hollow is not implemented") # implement 
        return self

# alias for Part
Shape = Part

class Sketch(Entity):
    
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
            "Adding sweep to sketch {}.".format(self.name),
            lambda: BlenderActions.addBevelObjectToCurve(self.name, profileCurveName, fillCap),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self
        
    def profile(self,
        profileCurveName
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Adding profile to sketch {}.".format(self.name),
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
            "Creating text {}.".format(self.name),
            lambda: BlenderActions.createText(self.name, text, size, bold, italic, underlined, characterSpacing, wordSpacing, lineSpacing, fontFilePath),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.name
        )

        return self

    def createFromVerticies(self,
        coordinates, \
        interpolation = 64 \
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Creating sketch {} from vertices.".format(self.name),
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
                    "Creating sketch primitive {}".format(self.name),
                    lambda: blenderPrimitiveFunction(
                        *args[1:],
                        dict(
                                {"curveType": BlenderDefinitions.BlenderCurveTypes.fromCurveTypes(self.curveType) if self.curveType != None else None}
                                , **kwargs
                            )
                        ),
                    lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == blenderCurvePrimitiveType.name
                )

                
                # Since we're using Blender's bpy.ops API, we cannot provide a name for the newly created object,
                # therefore, we'll use the object's "expected" name and rename it to what it should be
                # note: this will fail if the "expected" name is incorrect
                Part(blenderCurvePrimitiveType.name).rename(self.name)

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

# alias for Sketch
Curve = Sketch

class Landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToEntityWithName = None
    landmarkName = None

    def __init__(self,
    landmarkName:str,
    localToEntityWithName:str=None \
    ):
        self.localToEntityWithName = localToEntityWithName
        
        if localToEntityWithName:
            self.landmarkName = "{}_{}".format(localToEntityWithName, landmarkName)
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

class Joint: 
    # Text to 3D Modeling Automation Capabilities.

    part1Name = None
    part2Name = None
    part1Landmark:Landmark = None
    part2Landmark:Landmark = None

    def __init__(self,
    part1Name:str, \
    part2Name:str, \
    part1LandmarkName:str, \
    part2LandmarkName:str
    ):
        self.part1Name = part1Name
        self.part2Name = part2Name
        self.part1Landmark = Landmark(part1LandmarkName, part1Name)
        self.part2Landmark = Landmark(part2LandmarkName, part2Name) if part2LandmarkName else None

        
    def transformLandmarkOntoAnother(self):
        
        blenderEvents.addToBlenderOperationsQueue(
            "Transforming {} landmark {} onto {} landmark {}".format(self.part1Name, self.part1Landmark.landmarkName, self.part2Name, self.part2Landmark.landmarkName),
            lambda: BlenderActions.transformLandmarkOntoAnother(self.part1Name, self.part2Name, self.part1Landmark.landmarkName, self.part2Landmark.landmarkName),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value and update.id.name == self.part2Landmark.landmarkName,
        )

        return self

    @staticmethod
    def _getLimitLocationDimensions(dimension:str):
        dimensionsArray = None

        if dimension != None:
            dimensionsArray:list[Utilities.Dimension] = Utilities.getDimensionsFromString(dimension) or []
            
            dimensionsArray = BlenderDefinitions.BlenderLength.convertDimensionsToBlenderUnit(dimensionsArray)

            assert len(dimensionsArray) > 0,\
                f"Limit Location joint must contain at least one value"
            
            if len(dimensionsArray) == 1:
                dimensionsArray.append(Utilities.Dimension(dimensionsArray[0].value, dimensionsArray[0].unit))

        return dimensionsArray

    @staticmethod
    def _limitLocationOffsetFromLandmark(objectName, objectLandmarkName, relativeToLandmarkName, xDimensions, yDimensions, zDimensions, keywordArguments):

        [x,y,z] = BlenderActions.getObjectWorldLocation(objectName) - BlenderActions.getObjectWorldLocation(objectLandmarkName)
        

        if xDimensions:
            for index in range(0,len(xDimensions)):
                xDimensions[index].value = xDimensions[index].value + x
        if yDimensions:
            for index in range(0,len(yDimensions)):
                yDimensions[index].value = yDimensions[index].value + y
        if zDimensions:
            for index in range(0,len(zDimensions)):
                zDimensions[index].value = zDimensions[index].value + z

        BlenderActions.applyLimitLocationConstraint(objectName, xDimensions, yDimensions, zDimensions, relativeToLandmarkName, keywordArguments)

    def limitLocation(
        self,
        x:str = None,
        y:str = None,
        z:str = None,
        keywordArguments = {}
        ):
        
        xDimensions = Joint._getLimitLocationDimensions(x)
        yDimensions = Joint._getLimitLocationDimensions(y)
        zDimensions = Joint._getLimitLocationDimensions(z)

        
        blenderEvents.addToBlenderOperationsQueue(
            "Adding location constraint on {} landmark {} onto {} landmark {}".format(self.part1Name, self.part1Landmark.landmarkName, self.part2Name, self.part2Landmark.landmarkName),
            lambda: Joint._limitLocationOffsetFromLandmark(self.part2Name, self.part2Landmark.landmarkName, self.part1Landmark.landmarkName, xDimensions, yDimensions, zDimensions, keywordArguments),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value
        )

        return self
        

    @staticmethod
    def _getLimitRotationAngles(angles:str):
        angleList = None

        if angles and len(angles) > 0:
            
            angleList:list[Utilities.Angle] = Utilities.getAnglesFromString(angles) or []

            assert len(angleList) > 0,\
                f"Limit Rotation joint angle must contain at least one value"
            
            if len(angleList) == 1:

                angleList.append(Utilities.Angle(angleList[0].value, angleList[0].unit))

        return angleList

    def limitRotation(
        self,
        x:str = None,
        y:str = None,
        z:str = None,
        keywordArguments = {}
        ):

        xAngles = Joint._getLimitRotationAngles(x)
        yAngles = Joint._getLimitRotationAngles(y)
        zAngles = Joint._getLimitRotationAngles(z)
        
        blenderEvents.addToBlenderOperationsQueue(
            "Adding rotation constraint on {} landmark {} onto {} landmark {}".format(self.part1Name, self.part1Landmark.landmarkName, self.part2Name, self.part2Landmark.landmarkName),
            lambda: BlenderActions.applyLimitRotationConstraint(self.part2Name, xAngles, yAngles, zAngles, self.part1Landmark.landmarkName, keywordArguments),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value
        )

        return self
        
    def pivot(
        self,
        keywordArguments = {}
        ):

        blenderEvents.addToBlenderOperationsQueue(
            "Adding pivot constraint on {} landmark {} onto {}".format(self.part1Name, self.part1Landmark.landmarkName, self.part2Name),
            lambda: BlenderActions.applyPivotConstraint(self.part2Name, self.part1Landmark.landmarkName, keywordArguments),
            lambda update: type(update.id) == BlenderDefinitions.BlenderTypes.OBJECT.value
        )

        return self

class Material: 
    # Text to 3D Modeling Automation Capabilities.


    def __init__(self
    ):
        pass


class Scene: 
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
    removeChildren:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Removing the {} collection".format(name),
            lambda: BlenderActions.removeCollection(name, removeChildren), 
            lambda update: update.id.name == "Scene"
        )

        return self
        
    def removeFromGroup(self,
    entityName:str, \
    groupName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Removing {} from collection {}".format(entityName, groupName),
            lambda: BlenderActions.removeObjectFromCollection(entityName, groupName), 
            lambda update: update.id.name == groupName
            )

        return self

        
    def assignToGroup(self,
    entityName:str, \
    groupName:str, \
    removeFromOtherGroups:bool = True \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Assigning object {} to collection {}".format(entityName, groupName),
            lambda: BlenderActions.assignObjectToCollection(entityName, groupName, self.name, removeFromOtherGroups), 
            lambda update: update.id.name == groupName
        )

        return self
        

    def setVisibility(self,
    entityName:str, \
    isVisible:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" setting isVisible {}".format(entityName, isVisible),
            lambda: BlenderActions.setObjectVisibility(entityName, isVisible),
            lambda update: update.id.name == self.name
        ) 

        return self

class Analytics: 
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
    partName:str \
    ):
        return BlenderActions.getObjectWorldPose(partName)

    def getBoundingBox(self,
    partName:str \
    ):
        return BlenderActions.getBoundingBox(partName)

    def getDimensions(self,
    partName:str \
    ):
        
        dimensions = BlenderActions.getObject(partName).dimensions
        return [
            Utilities.Dimension(
                dimension,
                BlenderDefinitions.BlenderLength.DEFAULT_BLENDER_UNIT.value
            ) 
            for dimension in dimensions
            ]
