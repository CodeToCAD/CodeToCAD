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
    get_object_collection,
    get_object_world_location,
    remove_object,
    update_object_name,
)
from providers.blender.blender_provider.blender_definitions import (
    BlenderLength,
    BlenderTypes,
)


def create_mesh_from_curve(
    curve_object: bpy.types.Object,
    new_object_name: Optional[str] = None,
):
    if new_object_name is None:
        update_object_name(curve_object, str(uuid4()))
        new_object_name = curve_object.name

    dependencyGraph = bpy.context.evaluated_depsgraph_get()
    evaluatedObject: bpy.types.Object = curve_object.evaluated_get(dependencyGraph)
    mesh: bpy.types.Mesh = bpy.data.meshes.new_from_object(
        evaluatedObject, depsgraph=dependencyGraph
    )

    blender_object = create_object(new_object_name, mesh)

    blender_object.matrix_world = curve_object.matrix_world

    assign_object_to_collection(blender_object)

    existingCurveObjectChildren = curve_object.children
    for child in existingCurveObjectChildren:
        if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
            child.parent = blender_object

    # twisted logic here, but if we renamed this above, we want to nuke it because we're done with it.
    if curve_object.name != new_object_name:
        remove_object(curve_object, remove_children=True)


def transfer_landmarks(
    from_blender_object: bpy.types.Object,
    to_blender_object: bpy.types.Object,
):
    update_view_layer()

    translation = (
        get_object_world_location(from_blender_object)
        - get_object_world_location(to_blender_object)
    ).to_list()

    translation = [
        axisValue.value
        for axisValue in BlenderLength.convert_dimensions_to_blender_unit(translation)
    ]

    defaultCollection = get_object_collection(to_blender_object)

    from_blender_object_children = from_blender_object.children
    for child in from_blender_object_children:
        if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
            child.name = f"{to_blender_object.name}_{child.name}"
            isAlreadyExists = bpy.data.objects.get(child.name) is None
            if isAlreadyExists:
                print(f"{child.name} already exists. Skipping landmark transfer.")
                continue
            child.parent = to_blender_object
            child.location = child.location + mathutils.Vector(translation)
            assign_object_to_collection(child, defaultCollection)


def duplicate_object(
    existing_blender_object: bpy.types.Object,
    new_object_name: str,
    copy_landmarks: bool = True,
):

    assert (
        get_object_or_none(new_object_name) is None
    ), f"Object with name {new_object_name} already exists."

    cloned_object: bpy.types.Object = existing_blender_object.copy()
    cloned_object.name = new_object_name

    if existing_blender_object.data:
        cloned_object.data = existing_blender_object.data.copy()
        cloned_object.data.name = new_object_name

    # Link clonedObject to the original object's collection.
    defaultCollection = get_object_collection(existing_blender_object)

    assign_object_to_collection(cloned_object, defaultCollection)

    if copy_landmarks:
        blender_object_children: tuple = existing_blender_object.children
        for child in blender_object_children:
            if isinstance(child, BlenderTypes.OBJECT.value) and child.type == "EMPTY":
                newChild: bpy.types.Object = child.copy()
                newChild.name = child.name.replace(
                    existing_blender_object.name, new_object_name
                )
                newChild.parent = cloned_object
                assign_object_to_collection(newChild, defaultCollection)
