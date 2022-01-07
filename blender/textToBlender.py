import bpy
from utilities import *

class shape: 
    # Text to 3D Modeling Automation Capabilities.

    name= None
    description= None

    def __init__(self,
    name, \
    description=None \
    ):
        self.name = name
        self.description = description

    def fromFile(self,
    fileName,  \
    fileType=None \
    ):
        print("fromFile is not implemented") # implement 
        return self

    def cloneShape(self,
    shapeName \
    ):
        print("cloneShape is not implemented") # implement 
        return self

    def primitive(self,
    primitiveName,  \
    initialDimensions \
    ):
        import bmesh

        switch = {
            "cube": bmesh.ops.create_cube,
            "cone": bmesh.ops.create_cone,
            "cylinder": bmesh.ops.create_cone,
            "torus": bmesh.ops.create_torus,
            "sphere": bmesh.ops.create_uvsphere,
            "uvsphere": bmesh.ops.create_uvsphere,
            "icosphere": bmesh.ops.create_icosphere,
            "circle": bmesh.ops.create_circle,
            "grid": bmesh.ops.create_grid,
            "vertex": bmesh.ops.create_vert,
            "monkey": bmesh.ops.create_monkey,
        }

        objectMesh = bpy.data.meshes.new(primitiveName)
        
        createMeshFunction = switch[primitiveName]

        bmeshMesh = bmesh.new()
        createMeshFunction(bmeshMesh)
        bmeshMesh.to_mesh(objectMesh)
        bmeshMesh.free()

        object = bpy.data.objects.new(self.name, objectMesh)

        print('dimemnsions:', getDimensionsFromString(initialDimensions))
        
        object.scale = tuple(getDimensionsFromString(initialDimensions))

        collection = bpy.data.collections.get("Collection")
        collection.objects.link(object)

        return self

    def verticies(self,
    landmarkName \
    ):
        print("verticies is not implemented") # implement 
        return self

    def loft(self,
    shape1Name,  \
    shape2Name \
    ):
        print("loft is not implemented") # implement 
        return self

    def mirror(self,
    shapeName,  \
    landmarkName \
    ):
        print("mirror is not implemented") # implement 
        return self

    def pattern(self,
    shapeName,  \
    landmarkName \
    ):
        print("pattern is not implemented") # implement 
        return self

    def mask(self,
    shapeName,  \
    landmarkName \
    ):
        print("mask is not implemented") # implement 
        return self

    def scale(self,
    dimensions \
    ):
        print("scale is not implemented") # implement 
        return self

    def rotate(self,
    rotation \
    ):
        print("rotate is not implemented") # implement 
        return self

    def rename(self,
    name \
    ):
        print("rename is not implemented") # implement 
        return self

    def union(self,
    withShapeName \
    ):
        print("union is not implemented") # implement 
        return self

    def subtract(self,
    withShapeName \
    ):
        print("subtract is not implemented") # implement 
        return self

    def intersect(self,
    withShapeName \
    ):
        print("intersect is not implemented") # implement 
        return self

    def bevel(self,
    landmarkName,  \
    angle,  \
    roundedness \
    ):
        print("bevel is not implemented") # implement 
        return self

    def extrude(self,
    landmarkName,  \
    dimensions \
    ):
        print("extrude is not implemented") # implement 
        return self

    def remesh(self,
    strategy,  \
    amount \
    ):
        print("remesh is not implemented") # implement 
        return self

    def hollow(self,
    wallThickness \
    ):
        print("hollow is not implemented") # implement 
        return self

    def visibility(self,
    isVisible \
    ):
        print("visibility is not implemented") # implement 
        return self

    def delete(self
    ):
        print("delete is not implemented") # implement 
        return self

class landmark: 
    # Text to 3D Modeling Automation Capabilities.

    localToShapeWithName= None

    def __init__(self,
    localToShapeWithName=None \
    ):
        self.localToShapeWithName = localToShapeWithName

    def vertices(self,
    locations \
    ):
        print("vertices is not implemented") # implement 
        return self

    def rectangle(self,
    dimensions \
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

    shape1Name= None
    shape2Name= None
    shape1LandmarkName= None
    shape2LandmarkName= None
    jointType= None
    initialRotation= None
    limitRotation= None
    limitTranslation= None

    def __init__(self,
    shape1Name, \
    shape2Name, \
    shape1LandmarkName, \
    shape2LandmarkName, \
    jointType, \
    initialRotation, \
    limitRotation, \
    limitTranslation \
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

class analytics: 
    # Text to 3D Modeling Automation Capabilities.

    def constructor(self
    ):
        print("constructor is not implemented") # implement 
        return self

    def measure(self,
    landmark1Name,  \
    landmark2Name=None \
    ):
        print("measure is not implemented") # implement 
        return self

    def worldPose(self,
    shapeName \
    ):
        print("worldPose is not implemented") # implement 
        return self

    def boundingBox(self,
    shapeName \
    ):
        print("boundingBox is not implemented") # implement 
        return self
