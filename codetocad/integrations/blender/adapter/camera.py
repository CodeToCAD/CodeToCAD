from codetocad.integrations.blender.adapter.collections import (
    assign_object_to_collection,
)

try:
    import bpy
except ImportError:
    pass


from codetocad.integrations.blender.adapter.objects import (
    create_object,
)
from codetocad.integrations.blender.adapter.scene import get_scene


def create_camera(camera_object_name: str, type):
    camera_data = bpy.data.cameras.new(name=camera_object_name)

    blender_object = create_object(camera_object_name, data=camera_data)

    assign_object_to_collection(blender_object)


def get_camera(
    camera_name: str,
):
    blender_camera = bpy.data.cameras.get(camera_name)

    assert blender_camera is not None, f"Camera {camera_name} does not exist."

    return blender_camera


def set_scene_camera(blender_camera: "bpy.types.Object", scene_name: str | None = None):
    scene = get_scene(scene_name)

    scene.camera = blender_camera


def set_focal_length(blender_camera: "bpy.types.Camera", length=50.0):
    assert length >= 1, "Length needs to be greater than or equal to 1."

    blender_camera.lens = length
