import math
from utilities import *
from blenderExecute import *
from BlenderEvents import BlenderEvents

def setup(blenderEvents):

    # start the updateEventThread
    # blenderEvents.startBlenderEventThread()
    blenderEvents.startBlenderEventTimer(bpy)

    # tell Blender to notify onReceiveBlenderDependencyGraphUpdateEvent when its dependency graph is updated. https://docs.blender.org/api/current/bpy.app.handlers.html 
    bpy.app.handlers.depsgraph_update_post.append(blenderEvents.onReceiveBlenderDependencyGraphUpdateEvent)

    # blenderSceneLockInterface(True)

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

    def fromFile(self,
    fileName:str,  \
    fileType:str=None \
    ):
        print("fromFile is not implemented") # implement 
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


    def primitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        # TODO: account for blender auto-renaming with sequential numbers
        expectedNameOfObjectInBlender = primitiveName[0].upper() + primitiveName[1:]
        
        blenderEvents.addToBlenderOperationsQueue(
            "Object of type {} created".format(primitiveName),
            lambda: blenderAddPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Mesh of type {} created".format(primitiveName),
            lambda: True,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Object of type {} renamed to {}".format(primitiveName, self.name),
            lambda: blenderUpdateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Mesh of type {} renamed to {}".format(primitiveName, self.name),
            lambda: blenderUpdateObjectMeshName(self.name, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == self.name
        )

        return self

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

    def translate(self,
    dimensions:str\
    ):
        dimensionsList:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensionsList = convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" scale transformed".format(self.name),
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
            "Object \"{}\" scale transformed".format(self.name),
            lambda: blenderTranslationObject(self.name, dimensionsList, BlenderTranslationTypes.ABSOLUTE),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

    def scale(self,
    dimensions:str \
    ):
        dimensionsList:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensionsList = convertDimensionsToBlenderUnit(dimensionsList)

        while len(dimensionsList) < 3:
            dimensionsList.append(Dimension("1"))
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" scale transformed".format(self.name),
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

        # convert all the values to radians
        angleListRadians = [angle.toRadians() for angle in angleList]
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" scale transformed".format(self.name),
            lambda: blenderRotateObject(self.name, angleListRadians, BlenderRotationTypes.EULER),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def rename(self,
    name:str \
    ):
        expectedNameOfObjectInBlender = self.name
        self.name = name
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" renamed to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: blenderUpdateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Mesh with name {} renamed to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: blenderUpdateObjectMeshName(self.name, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == self.name
        )
        return self

    def union(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" applying BOOLEAN UNION modifier".format(self.name),
            lambda: blenderApplyBooleanModifier(self.name, BlenderBooleanTypes.UNION, withShapeName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def subtract(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" applying BOOLEAN DIFFERENCE modifier".format(self.name),
            lambda: blenderApplyBooleanModifier(self.name, BlenderBooleanTypes.DIFFERENCE, withShapeName),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        return self

    def intersect(self,
    withShapeName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" applying BOOLEAN INTERSECT modifier".format(self.name),
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

    def remesh(self,
    strategy:str,  \
    amount:float \
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" applying EDGE_SPLIT modifier".format(self.name),
            lambda: BlenderModifiers.EDGE_SPLIT.applyBlenderModifier(self.name, {"name": "EdgeDiv", "split_angle": math.radians(60)}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Object \"{}\" applying SUBSURF modifier".format(self.name),
            lambda: BlenderModifiers.SUBSURF.applyBlenderModifier(self.name, {"name": "Subdivision", "levels": 3}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

    def hollow(self,
    wallThickness:float \
    ):
        print("hollow is not implemented") # implement 
        return self

    def visibility(self,
    isVisible:bool \
    ):
        print("visibility is not implemented") # implement 
        return self

    def delete(self
    ):
        print("delete is not implemented") # implement 
        return self

class landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToShapeWithName = None

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
        blenderEvents.addToBlenderOperationsQueue("Set document units to {} {}".format(unitSystem, unitName), lambda: blenderSetDefaultUnit(unitSystem, unitName, self.name), 
        lambda update: update.id.name == "Scene")
        return self

    def createGroup(self,
    name:str \
    ):
        blenderEvents.addToBlenderOperationsQueue("Create a {} collection".format(name), lambda: blenderCreateCollection(name, self.name), 
        lambda update: update.id.name == name)
        return self

    def deleteGroup(self,
    name:str,  \
    removeNestedShapes:bool \
    ):
        blenderEvents.addToBlenderOperationsQueue("Remove the {} collection".format(name), lambda: blenderRemoveCollection(name, removeNestedShapes), 
        lambda update: update.id.name == "Scene")
        return self
        
    def removeShapeFromGroup(self,
    shapeName:str, \
    groupName:str \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Assign object {} to {} collection".format(shapeName, groupName),
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
            "Assign object {} to {} collection".format(shapeName, groupName),
            lambda: blenderAssignObjectToCollection(shapeName, groupName, removeFromOtherGroups), 
            lambda update: update.id.name == groupName
            )
        return self

class analytics: 
    # Text to 3D Modeling Automation Capabilities.

    def constructor(self
    ):
        print("constructor is not implemented") # implement 
        return self

    def measureLandmarks(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        print("measure is not implemented") # implement 
        return self

    def getWorldPose(self,
    shapeName:str \
    ):
        print("worldPose is not implemented") # implement 
        return self

    def getBoundingBox(self,
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

    def getDimensions(self,
    shapeName:str \
    ):
        return self.boundingBox(shapeName)
