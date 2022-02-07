from threading import Event, Thread
import bpy
from utilities import *


def blenderAddPrimitive(
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

def blenderUpdateObjectName( object, newName):
    object.name = newName
def blenderUpdateMeshName(mesh, newName):
    mesh.name = newName


def scaleBlenderObject(
    name:str,
    dimensions:str \
):
    dimensions:list[Dimension] = getDimensionsFromString(dimensions) or []
    
    dimensions = convertDimensionsToBlenderUnit(dimensions)

    while len(dimensions) < 3:
        dimensions.append(Dimension("1"))

    [x,y,z] = dimensions

    sceneDimensions = bpy.data.objects[name].dimensions

    #calculate scale factors if a unit is passed into the dimension
    if sceneDimensions:
        x.value = x.value/sceneDimensions.x if x.unit != None else x.value
        y.value = y.value/sceneDimensions.y if y.unit != None else y.value
        z.value = z.value/sceneDimensions.z if z.unit != None else z.value
    
    bpy.data.objects[name].scale = (x.value,y.value,z.value)