import math
from utilities import *
from blenderExecute import *
from BlenderEvents import BlenderEvents

def setup(blenderEvents):

    # start the updateEventThread
    blenderEvents.startUpdateEventThread()

    # tell Blender to notify onReceiveBlenderDependencyGraphUpdate when its dependency graph is updated. https://docs.blender.org/api/current/bpy.app.handlers.html 
    bpy.app.handlers.depsgraph_update_post.append(blenderEvents.onReceiveBlenderDependencyGraphUpdate)

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
        print("cloneShape is not implemented") # implement 
        return self


    def primitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        blenderEvents.addToBlenderOperationsQueue(
            "Object of type {} created".format(primitiveName),
            lambda: blenderAddPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == primitiveName
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Mesh of type {} created".format(primitiveName),
            lambda:None,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name.lower() == primitiveName
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Object of type {} renamed to {}".format(primitiveName, self.name),
            lambda: blenderUpdateObjectName(bpy.data.objects[-1], self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Mesh of type {} renamed to {}".format(primitiveName, self.name),
            lambda: blenderUpdateMeshName(bpy.data.meshes[-1], self.name)
            ,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name.lower() == self.name
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


    def scale(self,
    dimensions:str \
    ):
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object with name {} scale transformed".format(self.name),
            lambda: scaleBlenderObject(self.name, dimensions),
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == self.name
        )
        
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
    
        blenderEvents.addToBlenderOperationsQueue(
            "Object with name {} applying EDGE_SPLIT modifier".format(self.name),
            lambda: BlenderModifiers.EDGE_SPLIT.applyBlenderModifier(self.name, {"name": "EdgeDiv", "split_angle": math.radians(60)}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == self.name
        )
        blenderEvents.addToBlenderOperationsQueue(
            "Object with name {} applying SUBSURF modifier".format(self.name),
            lambda: BlenderModifiers.SUBSURF.applyBlenderModifier(self.name, {"name": "Subdivision", "levels": 3}),
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == self.name
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

    def __init__(self
    ):
        pass

    def export(self
    ):
        print("export is not implemented") # implement 
        return self

    def setDefaultUnit(self,
    unit:BlenderLength \
    ):
        bpy.context.scene.unit_settings.system = unit.getSystem()
        bpy.context.scene.unit_settings.length_unit = unit.name
        return self

    def createGroup(self,
    name:str \
    ):
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[name]
        return self

    def deleteGroup(self,
    name:str,  \
    removeNestedShapes:bool \
    ):
        if name in bpy.data.collections:
            if removeNestedShapes:
                for obj in bpy.data.collections[name].objects:
                    bpy.data.objects.remove(obj)
            bpy.data.collections.remove(bpy.data.collections[name])
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
