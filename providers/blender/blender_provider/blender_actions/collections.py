import bpy

from providers.blender.blender_provider.blender_actions.objects import (
    get_object,
    remove_object,
)


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


def remove_collection(name: str, scene_name: str, remove_children: bool):
    collection = get_collection(name, scene_name)

    if remove_children:
        for obj in collection.objects:
            try:
                remove_object(obj.name, True)
            except Exception as e:
                print(f"Could not remove {obj.name}. {e}")

    bpy.data.collections.remove(collection)


def remove_object_from_collection(
    existing_object_name: str, collection_name: str, scene_name: str
):
    blender_object = get_object(existing_object_name)

    collection = get_collection(collection_name, scene_name)

    assert (
        collection.objects.get(existing_object_name) is not None
    ), f"Object {existing_object_name} does not exist in collection {collection_name}"

    collection.objects.unlink(blender_object)


def assign_object_to_collection(
    existing_object_name: str,
    collection_name="Scene Collection",
    scene_name="Scene",
    remove_from_other_groups=True,
    move_children=True,
):
    """
    Assigns the existing_object_name to a collection.
    Defaults to using Scene Collection under the default Scene scene.
    """
    blender_object = get_object(existing_object_name)

    collection = bpy.data.collections.get(collection_name)

    if collection is None and collection_name == "Scene Collection":
        scene = bpy.data.scenes.get(scene_name)

        assert scene is not None, f"Scene {scene_name} does not exist"

        collection = scene.collection

    assert collection is not None, f"Collection {collection_name} does not exist"

    if remove_from_other_groups:
        currentCollections: list[bpy.types.Collection] = blender_object.users_collection
        for currentCollection in currentCollections:
            currentCollection.objects.unlink(blender_object)

    collection.objects.link(blender_object)

    if move_children:
        for child in blender_object.children:
            assign_object_to_collection(
                child.name, collection_name, scene_name, True, True
            )
