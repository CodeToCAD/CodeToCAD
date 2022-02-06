from threading import Event, Thread
from time import sleep
import bpy
from utilities import *

blenderOperationsComplete = Event()
blenderOperations = []

def addBlenderOperation(description, operation, assertion):
    global blenderOperations,blenderOperationsComplete

    blenderOperationsComplete.clear()

    blenderOperations.append(
        {
            "started": False,
            "description": description,
            "operation": operation,
            "assertion": assertion
        }
    )

    if len(blenderOperations) == 1:
        operation()

updateEventQueue = []

def updateEventHandler():
    global blenderOperations,blenderOperationsComplete, updateEventQueue
    while 1:
        sleep(0.5)
        if len(updateEventQueue) == 0:
            return
        
        update = updateEventQueue.pop(0)

        if len(blenderOperations) == 0:
            return
        
        operation = blenderOperations[0]

        print("update:", update.id.name, type(update.id), "transformOperation:", update.is_updated_transform,"geometryOperation:", update.is_updated_geometry, "currentOperation:", operation["description"], "Operations left:", len(blenderOperations))
        
        if operation["assertion"](update):
            print("assertion complete:", operation["description"])
            blenderOperations.pop(0)
            if len(blenderOperations) == 0:
                print("All operations complete")
                blenderOperationsComplete.set()
            else:    
                operation = blenderOperations[0]
                operation["operation"]()
                
Thread(target=updateEventHandler).start()

def on_depsgraph_update(scene, depsgraph):

    global updateEventQueue
    
    for update in depsgraph.updates:
        updateEventQueue.append(update)
  
bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

class BlenderLength(Units):
    #metric
    KILOMETERS = Length.kilometer
    METERS = Length.meter
    CENTIMETERS = Length.centimeter
    MILLIMETERS = Length.millimeter
    MICROMETERS = Length.micrometer
    #imperial
    MILES = Length.mile
    FEET = Length.foot
    INCHES = Length.inch
    THOU = Length.thousandthInch

    def getSystem(self):
        if self == self.KILOMETERS or self == self.METERS or self == self.CENTIMETERS or self == self.MILLIMETERS or self == self.MICROMETERS:
            return'METRIC'
        else:
            return'IMPERIAL'

# Use this value to scale any number operations done throughout this implementation
defaultBlenderUnit = BlenderLength.METERS

def convertDimensionsToBlenderUnit(dimensions:list[Dimension]):
    return [
        Dimension(
            float(
                convertToUnit(
                    defaultBlenderUnit.value, dimension.value,
                    dimension.unit or defaultBlenderUnit.value
                )
            ),
            defaultBlenderUnit.value
        )
        
            if (dimension.unit != None and dimension.unit != defaultBlenderUnit.value)

            else dimension

                for dimension in dimensions 
    ]

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

    def blenderAddPrimitive(
        self,
        primitiveName:str,  \
        dimensions:str,  \
        keywordArguments:dict=None
        ):

        dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []

        dimensions = convertDimensionsToBlenderUnit(dimensions)

        while len(dimensions) < 3:
            dimensions.append(Dimension("1"))


        keywordArguments = keywordArguments or {}
        
        switch = {
            "cube": lambda:bpy.ops.mesh.primitive_cube_add(size=1, scale=tuple(dimensions), **keywordArguments),
            "cone": lambda:bpy.ops.mesh.primitive_cone_add(radius1=dimensions[0].value, radius2=dimensions[1].value, depth=dimensions[2].value, **keywordArguments),
            "cylinder": lambda:bpy.ops.mesh.primitive_cylinder_add(radius=dimensions[0].value, depth=dimensions[1].value, **keywordArguments),
            "torus": lambda:bpy.ops.mesh.primitive_torus_add(mode='EXT_INT', abso_minor_rad=dimensions[0].value, abso_major_rad=dimensions[1].value, **keywordArguments),
            "sphere": lambda:bpy.ops.mesh.primitive_ico_sphere_add(radius=dimensions[0].value, **keywordArguments),
            "uvsphere": lambda:bpy.ops.mesh.primitive_uv_sphere_add(radius=dimensions[0].value, **keywordArguments),
            "circle": lambda:bpy.ops.mesh.primitive_circle_add(radius=dimensions[0].value, **keywordArguments),
            "grid": lambda:bpy.ops.mesh.primitive_grid_add(size=dimensions[0].value, **keywordArguments),
            "monkey": lambda:bpy.ops.mesh.primitive_monkey_add(size=dimensions[0].value, **keywordArguments),
        }

        switch[primitiveName]()
    
    def blenderUpdateObjectName(self, object, newName):
        object.name = newName
    def blenderUpdateMeshName(self, mesh, newName):
        mesh.name = newName

    def primitive(self,
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None \
    ):
        addBlenderOperation(
            "Object of type {} created".format(primitiveName),
            lambda: self.blenderAddPrimitive(primitiveName, dimensions, keywordArguments),
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == primitiveName
        )
        addBlenderOperation(
            "Mesh of type {} created".format(primitiveName),
            lambda:None,
            lambda update: type(update.id) == bpy.types.Mesh and update.id.name.lower() == primitiveName
        )
        addBlenderOperation(
            "Object of type {} renamed to {}".format(primitiveName, self.name),
            lambda: self.blenderUpdateObjectName(bpy.data.objects[-1], self.name)
            ,
            lambda update: type(update.id) == bpy.types.Object and update.id.name.lower() == self.name
        )
        addBlenderOperation(
            "Mesh of type {} renamed to {}".format(primitiveName, self.name),
            lambda: self.blenderUpdateMeshName(bpy.data.meshes[-1], self.name)
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

    def scaleBlenderObject(self,
    dimensions:str \
    ):
        dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []
        
        dimensions = convertDimensionsToBlenderUnit(dimensions)

        while len(dimensions) < 3:
            dimensions.append(Dimension("1"))

        [x,y,z] = dimensions

        sceneDimensions = bpy.data.objects[self.name].dimensions

        #calculate scale factors if a unit is passed into the dimension
        if sceneDimensions:
            x.value = x.value/sceneDimensions.x if x.unit != None else x.value
            y.value = y.value/sceneDimensions.y if y.unit != None else y.value
            z.value = z.value/sceneDimensions.z if z.unit != None else z.value
        
        bpy.data.objects[self.name].scale = (x.value,y.value,z.value)

    def scale(self,
    dimensions:str \
    ):
    
        addBlenderOperation(
            "Object with name {} scale transformed".format(self.name),
            lambda: self.scaleBlenderObject(dimensions),
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
        print("remesh is not implemented") # implement 
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
