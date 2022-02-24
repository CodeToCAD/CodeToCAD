from threading import Event, Thread
from enum import Enum
import bpy
from utilities import *

# an enum of Blender modifiers and an instance method to add that modifier to an object in Blender.
class BlenderModifiers(Enum):
    EDGE_SPLIT = 0
    SUBSURF = 1
    BOOLEAN = 2

    def blenderAddModifier(self, shapeName:str, keywordArguments:dict):
        if not (shapeName in bpy.data.objects):
            print("blenderAddModifier: error: {} is not an object".format(shapeName))
            return False

        modifier = bpy.data.objects[shapeName].modifiers.new(type=self.name)
        for key,value in keywordArguments.items():
            setattr(modifier, key, value)

        return True

class BlenderBooleanTypes(Enum):
    UNION = 0
    DIFFERENCE = 1
    INTERSECT = 2

def blenderApplyBooleanModifier(shapeName, type:BlenderBooleanTypes, withShapeName):

    if not (withShapeName in bpy.data.objects):
        print("blenderApplyBooleanModifier: error: {} is not an object".format(withShapeName))
        return False

    return BlenderModifiers.BOOLEAN.applyBlenderModifier(shapeName, {"operation": type.name, "object": bpy.data.objects[withShapeName]})

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

    def blenderAddFunction(self, dimensions, keywordArguments):
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
def blenderAddPrimitive(
    primitiveName:str,  \
    dimensions:str,  \
    keywordArguments:dict=None
    ):

    dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []

    dimensions = convertDimensionsToBlenderUnit(dimensions)

    while len(dimensions) < 3:
        dimensions.append(Dimension(1))
    
    BlenderPrimitives[primitiveName].blenderAddFunction(dimensions, keywordArguments or {})

    return True

def blenderUpdateObjectName(oldName, newName):

    if not (oldName in bpy.data.objects):
        return False

    bpy.data.objects[oldName].name = newName

    return True

def blenderUpdateObjectMeshName(parentObjectName, newName):
    
    if not (parentObjectName in bpy.data.objects):
        return False

    meshName = bpy.data.objects[parentObjectName].data.name

    if not (meshName in bpy.data.meshes):
        return False

    bpy.data.meshes[meshName].name = newName

    return True

# updates the name of the active object in Blender.
# NOTE: Use with caution
def blenderUpdateActiveObjectName(newName):
    bpy.context.view_layer.objects.active.name = newName
    return True

# updates the name of the active object in Blender.
# NOTE: Use with caution
def blenderUpdateActiveMeshName(newName):
    meshName = bpy.context.view_layer.objects.active.data.name

    if not (meshName in bpy.data.meshes):
        return False

    bpy.data.meshes[meshName].name = newName
    return True

# locks the scene interface
def blenderSceneLockInterface(isLocked):
    bpy.context.scene.render.use_lock_interface = isLocked
    return True

def blenderCreateCollection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[name]
    return True

def blenderRemoveCollection(name, removeNestedObjects):
    if name in bpy.data.collections:
        if removeNestedObjects:
            for obj in bpy.data.collections[name].objects:
                bpy.data.objects.remove(obj)
        bpy.data.collections.remove(bpy.data.collections[name])

        return True
    return False

def blenderSetDefaultUnit(system, name):
    bpy.context.scene.unit_settings.system = system
    bpy.context.scene.unit_settings.length_unit = name
    return True


class BlenderRotationTypes(Enum):
    EULER = "rotation_euler"
    DELTA_EULER = "delta_rotation_euler"
    QUATERNION = "rotation_quaternion"
    DELTA_QUATERNION = "delta_rotation_quaternion"

def blenderRotateObject(shapeName, rotationTuple, rotationType:BlenderRotationTypes):
    if not (shapeName in bpy.data.objects):
        return False

    setattr(bpy.data.objects[shapeName], rotationType.value, rotationTuple)

    return True

class BlenderTranslationTypes(Enum):
    ABSOLUTE = "location"
    RELATIVE = "delta_location"

def blenderTranslationObject(shapeName, translationTuple, translationType:BlenderTranslationTypes):
    
    if not (shapeName in bpy.data.objects):
        return False

    setattr(bpy.data.objects[shapeName], translationType.value, translationTuple)

    return True

def blenderScaleObject(
    name:str,
    dimensions:list[Dimension] \
):
    if not (name in bpy.data.objects):
        return False

    [x,y,z] = dimensions

    sceneDimensions = bpy.data.objects[name].dimensions

    #calculate scale factors if a unit is passed into the dimension
    if sceneDimensions:
        x.value = x.value/sceneDimensions.x if x.unit != None else x.value
        y.value = y.value/sceneDimensions.y if y.unit != None else y.value
        z.value = z.value/sceneDimensions.z if z.unit != None else z.value
    
    bpy.data.objects[name].scale = (x.value,y.value,z.value)

    return True