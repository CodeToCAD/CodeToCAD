from enum import Enum
import bpy
from utilities import *

# an enum of Blender modifiers and an instance method to add that modifier to an object in Blender.
class BlenderModifiers(Enum):
    EDGE_SPLIT = 0
    SUBSURF = 1
    BOOLEAN = 2

    def blenderAddModifier(self, shapeName:str, keywordArguments:dict):

        blenderObject = bpy.data.objects.get(shapeName)
        
        assert \
            blenderObject != None, \
            "Object {} does not exist".format(shapeName)

        modifier = blenderObject.modifiers.new(type=self.name, name=self.name)

        for key,value in keywordArguments.items():
            setattr(modifier, key, value)

class BlenderBooleanTypes(Enum):
    UNION = 0
    DIFFERENCE = 1
    INTERSECT = 2

def blenderApplyBooleanModifier(shapeName, type:BlenderBooleanTypes, withShapeName):

    blenderObject = bpy.data.objects.get(shapeName)
        
    blenderBooleanObject = bpy.data.objects.get(withShapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)

    assert \
        blenderBooleanObject != None, \
        "Object {} does not exist".format(withShapeName)

    BlenderModifiers.BOOLEAN.blenderAddModifier(
        shapeName, 
        {
            "operation": type.name,
            "object": blenderBooleanObject
        }
    )

# An enum of Blender Primitives, and an instance method to add the primitive to Blender.
class BlenderPrimitives(Enum):
    cube = 0
    cone = 1
    cylinder = 2
    torus = 3
    sphere = 4
    uvsphere = 5
    circle = 6
    grid = 7
    monkey = 8

    def blenderAddPrimitive(self, dimensions, keywordArguments):
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
        return switch[self.name]()

# Extracts dimensions from a string, then passes them as arguments to the BlenderPrimitives class
# TODO: if object already exists, merge objects
def blenderAddPrimitive(
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None
    ):

    dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []

    dimensions = convertDimensionsToBlenderUnit(dimensions)

    while len(dimensions) < 3:
        dimensions.append(Dimension(1))
    
    BlenderPrimitives[primitiveName].blenderAddPrimitive(dimensions, keywordArguments or {})

def blenderUpdateObjectName(oldName, newName):

    blenderObject = bpy.data.objects.get(oldName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(oldName)
    
    
    blenderObject.name = newName


def blenderUpdateObjectMeshName(parentObjectName, newName):
    
    blenderObject = bpy.data.objects.get(parentObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(parentObjectName)

    meshName = blenderObject.data.name

    blenderMesh = bpy.data.meshes.get(meshName)

    assert \
        blenderMesh != None, \
        "Mesh {} does not exist".format(meshName)

    blenderMesh.name = newName


# locks the scene interface
def blenderSceneLockInterface(isLocked):
    bpy.context.scene.render.use_lock_interface = isLocked

def blenderCreateCollection(name, sceneName = "Scene"):

    assert \
        name not in bpy.data.collections, \
        "Collection {} already exists".format(name)

    assert \
        sceneName in bpy.data.scenes, \
        "Scene {} does not exist".format(sceneName)

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[sceneName].collection.children.link(collection)

def blenderRemoveCollection(name, removeNestedObjects):
    
    assert \
        name in bpy.data.collections, \
        "Collection {} does not exist".format({name})

    if removeNestedObjects:
        for obj in bpy.data.collections[name].objects:
            bpy.data.objects.remove(obj)

    bpy.data.collections.remove(bpy.data.collections[name])

def blenderSetDefaultUnit(unitSystem, unitName, sceneName = "Scene"):

    
    blenderScene = bpy.data.scenes.get(sceneName)
    
    assert \
        blenderScene != None, \
        "Scene {} does not exist".format(sceneName)

    blenderScene.unit_settings.system = unitSystem
    blenderScene.unit_settings.length_unit = unitName


class BlenderRotationTypes(Enum):
    EULER = "rotation_euler"
    DELTA_EULER = "delta_rotation_euler"
    QUATERNION = "rotation_quaternion"
    DELTA_QUATERNION = "delta_rotation_quaternion"

def blenderRotateObject(shapeName, 
rotationAngles:list[Angle],
rotationType:BlenderRotationTypes):

    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
        
    
    assert \
        len(rotationAngles) == 3, \
        "rotationAngles must be length 3"

    rotationTuple = (rotationAngles[0].value, rotationAngles[1].value, rotationAngles[2].value)

    setattr(blenderObject, rotationType.value, rotationTuple)


class BlenderTranslationTypes(Enum):
    ABSOLUTE = "location"
    RELATIVE = "delta_location"

def blenderTranslationObject(shapeName, translationDimensions:list[Dimension], translationType:BlenderTranslationTypes):
    
    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
    
    assert \
        len(translationDimensions) == 3, \
        "translationDimensions must be length 3"

    translationTuple = (translationDimensions[0].value, translationDimensions[1].value, translationDimensions[2].value)

    setattr(blenderObject, translationType.value, translationTuple)


def blenderScaleObject(
    shapeName:str,
    scalingDimensions:list[Dimension] \
):
    blenderObject = bpy.data.objects.get(shapeName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(shapeName)
    
    assert \
        len(scalingDimensions) == 3, \
        "scalingDimensions must be length 3"

    [x,y,z] = scalingDimensions

    sceneDimensions = blenderObject.dimensions

    #calculate scale factors if a unit is passed into the dimension
    if sceneDimensions:
        x.value = x.value/sceneDimensions.x if x.unit != None else x.value
        y.value = y.value/sceneDimensions.y if y.unit != None else y.value
        z.value = z.value/sceneDimensions.z if z.unit != None else z.value
    
    blenderObject.scale = (x.value,y.value,z.value)


# TODO: if object already exists, merge objects
def blenderDuplicateObject(existingObjectName, newObjectName):

    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
    
    clonedObject = blenderObject.copy()
    clonedObject.name = newObjectName
    
    # Link clonedObject to a collection. Might want to make this optional.
    [currentCollection] = blenderObject.users_collection

    defaultCollection = currentCollection.name

    blenderAssignObjectToCollection(newObjectName, defaultCollection)


def blenderRemoveObjectFromCollection(existingObjectName, collectionName):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)

    collection = bpy.data.collections.get(collectionName)
    
    
    assert \
        collection != None, \
        "Collection {} does not exist".format(collectionName)
    
    assert \
        existingObjectName in collection.objects, \
        "Object {} does not exist in collection {}".format(existingObjectName, collectionName)
        
    collection.objects.unlink(blenderObject)


def blenderSetObjectVisibility(existingObjectName, isVisible):
    
    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
    
    blenderObject.hide_set(isVisible)

def blenderAssignObjectToCollection(existingObjectName, collectionName = "Scene Collection", sceneName = "Scene", removeFromOtherGroups = True):

    blenderObject = bpy.data.objects.get(existingObjectName)
    
    assert \
        blenderObject != None, \
        "Object {} does not exist".format(existingObjectName)
        
    currentCollections = blenderObject.users_collection

    assert \
        collectionName not in currentCollections, \
        "Object {} is already in collection {}.".format(existingObjectName, collectionName)

    
    collection = bpy.data.collections.get(collectionName)

    if collection == None and collectionName == "Scene Collection":
        scene = bpy.data.scenes.get(sceneName)

        assert \
            scene != None, \
            "Scene {} does not exist".format(sceneName)

        collection = scene.collection

    
    assert \
        collection != None, \
        "Collection {} does not exist".format(collectionName)

    if removeFromOtherGroups:
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blenderObject)
    
    
    collection.objects.link(blenderObject)