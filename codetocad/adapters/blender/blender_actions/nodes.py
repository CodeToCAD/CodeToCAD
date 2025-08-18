import bpy


def get_node_tree(
    scene: bpy.types.Scene,
) -> bpy.types.NodeTree:

    scene_world = scene.world
    if scene_world is None:
        raise Exception("Scene does not have a world")

    node_tree = scene_world.node_tree

    if node_tree is None:
        raise Exception("Scene does not have a node tree")

    return node_tree


def delete_nodes(
    scene: bpy.types.Scene,
):
    nodes = get_node_tree(scene).nodes
    nodes.clear()


def create_nodes(scene: bpy.types.Scene, type) -> bpy.types.Node:
    nodes = get_node_tree(scene).nodes.new(type=type)
    return nodes
