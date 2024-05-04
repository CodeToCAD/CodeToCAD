from providers.blender.blender_provider.blender_actions.collections import (
    assign_object_to_collection,
)
from uuid import uuid4
import mathutils
from typing import Optional
import bpy

from providers.blender.blender_provider.blender_actions.context import (
    update_view_layer,
)
from providers.blender.blender_provider.blender_actions.objects import (
    create_object,
    get_object,
    get_object_collection_name,
    get_object_world_location,
    remove_object,
    update_object_name,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderTypes,
)


def create_mesh_from_curve(
    existing_curve_object_name: str,
    new_object_name: Optional[str] = None,
):
    existingCurveObject = get_object(existing_curve_object_name)

    if new_object_name is None:
        update_object_name(existing_curve_object_name, str(uuid4()))
        new_object_name = existing_curve_object_name

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    evaluatedObject: bpy.types.Object = existingCurveObject.evaluated_get(
        dependencyGraph
    )
    mesh: bpy.types.Mesh = bpy.data.meshes.new_from_object(
        evaluatedObject, depsgraph=dependencyGraph
    )

    blenderObject = create_object(new_object_name, mesh)

    blenderObject.matrix_world = existingCurveObject.matrix_world

    assign_object_to_collection(new_object_name)

    existingCurveObjectChildren: list[bpy.types.Object] = existingCurveObject.children
    for child in existingCurveObjectChildren:
        if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
            child.parent = blenderObject

    # twisted logic here, but if we renamed this above, we want to nuke it because we're done with it.
    if existingCurveObject.name != existing_curve_object_name:
        remove_object(existingCurveObject.name, remove_children=True)


def transfer_landmarks(
    from_object_name: str,
    to_object_name: str,
):
    update_view_layer()

    fromBlenderObject = get_object(from_object_name)
    toBlenderObject = get_object(to_object_name)

    translation = (
        get_object_world_location(from_object_name)
        - get_object_world_location(to_object_name)
    ).to_list()

    translation = [
        axisValue.value
        for axisValue in BlenderLength.convert_dimensions_to_blender_unit(translation)
    ]

    defaultCollection = get_object_collection_name(to_object_name)

    fromBlenderObjectChildren: list[bpy.types.Object] = fromBlenderObject.children
    for child in fromBlenderObjectChildren:
        if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
            child.name = f"{to_object_name}_{child.name}"
            isAlreadyExists = bpy.data.objects.get(child.name) is None
            if isAlreadyExists:
                print(f"{child.name} already exists. Skipping landmark transfer.")
                continue
            child.parent = toBlenderObject
            child.location = child.location + mathutils.Vector(translation)
            assign_object_to_collection(child.name, defaultCollection)


def duplicate_object(
    existing_object_name: str, new_object_name: str, copy_landmarks: bool = True
):
    clonedObject = bpy.data.objects.get(new_object_name)

    assert clonedObject is None, f"Object with name {new_object_name} already exists."

    blenderObject = get_object(existing_object_name)

    clonedObject: bpy.types.Object = blenderObject.copy()
    clonedObject.name = new_object_name
    clonedObject.data = blenderObject.data.copy()
    clonedObject.data.name = new_object_name

    # Link clonedObject to the original object's collection.
    defaultCollection = get_object_collection_name(existing_object_name)

    assign_object_to_collection(new_object_name, defaultCollection)

    if copy_landmarks:
        blenderObjectChildren: list[bpy.types.Object] = blenderObject.children
        for child in blenderObjectChildren:
            if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
                newChild: bpy.types.Object = child.copy()
                newChild.name = child.name.replace(
                    existing_object_name, new_object_name
                )
                newChild.parent = clonedObject
                assign_object_to_collection(newChild.name, defaultCollection)
