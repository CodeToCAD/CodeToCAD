import bpy
from utilities import *

class BlenderLength(Enum):
    KILOMETERS = Length.kilometer
    METERS = Length.meter
    CENTIMETERS = Length.centimeter
    MILLIMETERS = Length.millimeter
    MICROMETERS = Length.micrometer

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
        
        dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []

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
        
        object = bpy.data.objects[-1]

        object.name = self.name

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
    
        dimensions:list[Dimension] = getDimensionsFromString(dimensions)

        while len(dimensions) < 3:
            dimensions.append(Dimension("1"))

        [x,y,z] = dimensions

        currentDimensions = bpy.data.objects[self.name].dimensions

        #calculate scale factors if a unit is passed into the dimension
        if currentDimensions:
            x.value = x.value/currentDimensions.x if x.unit != None else x.value
            y.value = y.value/currentDimensions.y if y.unit != None else y.value
            z.value = z.value/currentDimensions.z if z.unit != None else z.value
        
        bpy.data.objects[self.name].scale = (x.value,y.value,z.value)
        
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

    def constructor(self
    ):
        print("constructor is not implemented") # implement 
        return self

class scene: 
    # Text to 3D Modeling Automation Capabilities.

    def constructor(self
    ):
        print("constructor is not implemented") # implement 
        return self

    def export(self
    ):
        print("export is not implemented") # implement 
        return self

    def setDefaultUnit(self,
    unit:BlenderLength \
    ):
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

    def measure(self,
    landmark1Name:str,  \
    landmark2Name:str=None \
    ):
        print("measure is not implemented") # implement 
        return self

    def worldPose(self,
    shapeName:str \
    ):
        print("worldPose is not implemented") # implement 
        return self

    def boundingBox(self,
    shapeName:str \
    ):
        print("boundingBox is not implemented") # implement 
        return self
