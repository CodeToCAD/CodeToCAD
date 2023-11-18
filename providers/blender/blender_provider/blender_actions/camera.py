from typing import Optional
import bpy

from . import get_object, create_object, assign_object_to_collection, get_scene


def create_camera(obj_name: str, type):
    camera_data = bpy.data.cameras.new(name=obj_name)
    create_object(obj_name, data=camera_data)
    assign_object_to_collection(obj_name)


def get_camera(
    camera_name: str,
):
    blenderCamera = bpy.data.cameras.get(camera_name)

    assert blenderCamera is not None, f"Camera {camera_name} does not exist."

    return blenderCamera


def set_scene_camera(camera_name: str, scene_name: Optional[str] = None):
    blenderCamera = get_object(camera_name)
    scene = get_scene(scene_name)

    scene.camera = blenderCamera


def set_focal_length(camera_name: str, length=50.0):
    camera = get_camera(camera_name)
    assert length >= 1, "Length needs to be greater than or equal to 1."

    camera.lens = length
