import bpy


def get_node_tree(
    scene_name: str,
) -> bpy.types.NodeTree:
    from providers.blender.blender_provider.blender_actions.scene import get_scene

    scene = get_scene(scene_name)
    nodeTree = scene.world.node_tree
    return nodeTree


def delete_nodes(
    scene_name: str,
):
    nodes = get_node_tree(scene_name).nodes
    nodes.clear()


def create_nodes(scene_name: str, type) -> bpy.types.Node:
    nodes = get_node_tree(scene_name).nodes.new(type=type)
    return nodes
