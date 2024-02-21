from typing import Optional

from providers.blender.blender_provider.blender_actions.objects import get_object
from providers.blender.blender_provider.blender_actions.scene import get_scene


def add_keyframe_to_object(object_name: str, frame_number: int, data_path: str):
    blenderObject = get_object(object_name)

    # Acts on https://docs.blender.org/api/current/bpy.types.Keyframe.html
    blenderObject.keyframe_insert(data_path=data_path, frame=frame_number)


def set_frame_start(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_start = frame_number


def set_frame_end(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_end = frame_number


def set_frame_step(step: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_step = step


def set_frame_current(frame_number: int, scene_name: Optional[str]):
    scene = get_scene(scene_name)
    scene.frame_set(frame_number)
