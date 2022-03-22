import math
from pathlib import Path
from utilities import *
from blenderExecute import *
from BlenderEvents import BlenderEvents

def debugOnReceiveBlenderDependencyGraphUpdateEvent(scene, depsgraph):
    for update in depsgraph.updates:
        print("Received Event: {} Type: {}".format(update.id.name, type(update.id)))

def setup(blenderEvents):

    # start the updateEventThread
    # blenderEvents.startBlenderEventThread()
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

    def fromFile(self,
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
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming object {} to {}".format(fileName, self.name),
            lambda: blenderUpdateObjectName(fileName, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming mesh {} to {}".format(fileName, self.name),
            lambda: blenderUpdateObjectMeshName(self.name, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == self.name
        )
        
        

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
            "Creating primitive {}".format(primitiveName),
            lambda: blenderAddPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Waiting for mesh {} to be created".format(primitiveName),
            lambda: True,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == expectedNameOfObjectInBlender
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming object {} to {}".format(primitiveName, self.name),
            lambda: blenderUpdateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming mesh {} to {}".format(primitiveName, self.name),
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

        # convert all the values to radians
        angleListRadians = [angle.toRadians() for angle in angleList]
    
        blenderEvents.addToBlenderOperationsQueue(
            "Rotating {}".format(self.name),
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
            "Renaming object {} to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: blenderUpdateObjectName(expectedNameOfObjectInBlender, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Renaming mesh {} to {}".format(expectedNameOfObjectInBlender, self.name),
            lambda: blenderUpdateObjectMeshName(self.name, self.name)
            ,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name == self.name
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
        
        blenderEvents.addToBlenderOperationsQueue(
            "Creating landmark {} on {}.".format(landmarkName, self.name),
            lambda: blenderAddLandmark(self.name, landmarkName, localPosition),
            lambda update: type(update.id) == bpy.types.Object and update.id.name == self.name
        )

        return self

        

class landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToShapeWithName = None
    landmarkName = None

    def __init__(self,
    landmarkName:str,
    localToShapeWithName:str=None \
    ):
        self.landmarkName = landmarkName
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
    shape1Landmark = None
    shape2Landmark = None
    jointType = None
    initialRotation = None
    limitRotation = None
    limitTranslation = None

    def __init__(self,
    shape1Name:str, \
    shape2Name:str, \
    shape1Landmark:str, \
    shape2Landmark:str, \
    jointType:str, \
    initialRotation:str, \
    limitRotation:str, \
    limitTranslation:str \
    ):
        self.shape1Name = shape1Name
        self.shape2Name = shape2Name
        self.shape1Landmark = shape1Landmark
        self.shape2Landmark = shape2Landmark
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
