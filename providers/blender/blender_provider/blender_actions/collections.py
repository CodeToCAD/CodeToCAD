import bpy

from providers.blender.blender_provider.blender_actions.objects import (
    remove_object,
)

default_scene_name = "Scene"
default_collection_name = "Scene Collection"


def get_collection(name: str, scene_name="Scene") -> bpy.types.Collection:
    collection = bpy.data.scenes[scene_name].collection.children.get(name)

    assert (
        collection is not None
    ), f"Collection {name} does not exists in scene {scene_name}"

    return collection


def create_collection(name: str, scene_name="Scene"):
    assert (
        bpy.data.scenes.get(scene_name) is not None
    ), f"Scene {scene_name} does not exist"

    existing_collection = bpy.data.scenes[scene_name].collection.children.get(name)

    assert existing_collection is None, f"Collection {name} already exists"

    collection = bpy.data.collections.new(name)

    bpy.data.scenes[scene_name].collection.children.link(collection)


def remove_collection(blender_collection: bpy.types.Collection, remove_children: bool):
    if remove_children:
        for obj in blender_collection.objects:
            try:
                remove_object(obj, True)
            except Exception as e:
                print(f"Could not remove {obj.name}. {e}")

    bpy.data.collections.remove(blender_collection)


def remove_object_from_collection(
    blender_object: bpy.types.Object,
    blender_collection: bpy.types.Collection,
):
    assert (
        blender_collection.objects.get(blender_object.name) is not None
    ), f"Object {blender_object.name} does not exist in collection {blender_collection.name}"

    blender_collection.objects.unlink(blender_object)


def assign_object_to_collection(
    blender_object: bpy.types.Object,
    blender_collection: bpy.types.Collection | None = None,
    remove_from_other_groups=True,
    move_children=True,
):
    """
    Assigns the existing_object_name to a collection.
    Defaults to using Scene Collection under the default Scene scene.
    """
    if blender_collection is None:
        scene = bpy.data.scenes.get(default_scene_name)

        assert scene is not None, f"Scene {default_scene_name} does not exist"

        blender_collection = scene.collection

    assert (
        blender_collection is not None
    ), f"Collection {default_collection_name} does not exist"

    if remove_from_other_groups:
        currentCollections: tuple[bpy.types.Collection, ...] = (
            blender_object.users_collection
        )
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blender_object)

    blender_collection.objects.link(blender_object)

    if move_children:
        for child in blender_object.children:
            assign_object_to_collection(child, blender_collection, True, True)
