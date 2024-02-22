from typing import Optional
import bpy
import providers.blender.blender_provider.blender_definitions as blender_definitions

from providers.blender.blender_provider.blender_actions.nodes import (
    create_nodes,
    delete_nodes,
    get_node_tree,
)


def scene_lock_interface(is_locked: bool):
    bpy.context.scene.render.use_lock_interface = is_locked


def set_default_unit(
    blender_unit: blender_definitions.BlenderLength, scene_name="Scene"
):
    blenderScene = bpy.data.scenes.get(scene_name)

    assert blenderScene is not None, f"Scene {scene_name} does not exist"

    blenderScene.unit_settings.system = blender_unit.get_system()
    blenderScene.unit_settings.length_unit = blender_unit.name


def add_hdr_texture(
    scene_name: str,
    image_file_path: str,
):
    delete_nodes(scene_name)
    nodeBackground = create_nodes(scene_name, "ShaderNodeBackground")
    nodeEnvironment: bpy.types.ShaderNodeTexEnvironment = create_nodes(
        scene_name, "ShaderNodeTexEnvironment"
    )
    nodeEnvironment.image = bpy.data.images.load(image_file_path)
    nodeEnvironment.location = 0, 0
    nodeOutput = create_nodes(scene_name, "ShaderNodeOutputWorld")
    nodeOutput.location = 0, 0
    links = get_node_tree(scene_name).links
    links.new(nodeEnvironment.outputs["Color"], nodeBackground.inputs["Color"])
    links.new(nodeBackground.outputs["Background"], nodeOutput.inputs["Surface"])


def set_background_location(scene_name: str, x, y):
    envTexture: bpy.types.ShaderNodeTexEnvironment = get_node_tree(
        scene_name
    ).nodes.get("Environment Texture")
    envTexture.location = x, y


def get_scene(scene_name: Optional[str] = "Scene") -> bpy.types.Scene:
    blenderScene = bpy.data.scenes.get(scene_name or "Scene")

    assert blenderScene is not None, f"Scene{scene_name} does not exists"

    return blenderScene
