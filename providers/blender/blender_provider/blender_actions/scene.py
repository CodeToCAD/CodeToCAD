from typing import Optional
import bpy


from providers.blender.blender_provider.blender_actions.nodes import (
    create_nodes,
    delete_nodes,
    get_node_tree,
)
from providers.blender.blender_provider.blender_definitions import BlenderLength


def scene_lock_interface(is_locked: bool):
    bpy.context.scene.render.use_lock_interface = is_locked


def set_default_unit(blender_unit: BlenderLength, scene_name="Scene"):
    blenderScene = bpy.data.scenes.get(scene_name)

    assert blenderScene is not None, f"Scene {scene_name} does not exist"

    blenderScene.unit_settings.system = blender_unit.get_system()
    blenderScene.unit_settings.length_unit = blender_unit.name


def add_hdr_texture(
    scene: bpy.types.Scene,
    image_file_path: str,
):
    delete_nodes(scene)

    nodeBackground = create_nodes(scene, "ShaderNodeBackground")

    nodeEnvironment: bpy.types.ShaderNodeTexEnvironment = create_nodes(
        scene, "ShaderNodeTexEnvironment"
    )  # type: ignore

    nodeEnvironment.image = bpy.data.images.load(image_file_path)
    nodeEnvironment.location = 0, 0

    nodeOutput = create_nodes(scene, "ShaderNodeOutputWorld")
    nodeOutput.location = 0, 0

    links = get_node_tree(scene).links

    links.new(nodeEnvironment.outputs["Color"], nodeBackground.inputs["Color"])
    links.new(nodeBackground.outputs["Background"], nodeOutput.inputs["Surface"])


def set_background_location(scene: bpy.types.Scene, x, y):
    envTexture: bpy.types.ShaderNodeTexEnvironment | None = get_node_tree(
        scene
    ).nodes.get(
        "Environment Texture"
    )  # type: ignore

    if envTexture is None:
        raise Exception("Could not find an environment texture in the scene")

    envTexture.location = x, y


def get_scene(scene_name: Optional[str] = "Scene") -> bpy.types.Scene:
    blenderScene = bpy.data.scenes.get(scene_name or "Scene")

    assert blenderScene is not None, f"Scene{scene_name} does not exists"

    return blenderScene
