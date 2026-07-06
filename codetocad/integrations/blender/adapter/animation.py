from codetocad.integrations.blender.adapter.scene import get_scene

try:
    import bpy
except ImportError:
    pass


def add_keyframe_to_object(
    blender_object: "bpy.types.Object", frame_number: int, data_path: str
):
    # Acts on https://docs.blender.org/api/current/bpy.types.Keyframe.html
    blender_object.keyframe_insert(data_path=data_path, frame=frame_number)


def set_frame_start(frame_number: int, scene_name: str | None):
    scene = get_scene(scene_name)
    scene.frame_start = frame_number


def set_frame_end(frame_number: int, scene_name: str | None):
    scene = get_scene(scene_name)
    scene.frame_end = frame_number


def set_frame_step(step: int, scene_name: str | None):
    scene = get_scene(scene_name)
    scene.frame_step = step


def set_frame_current(frame_number: int, scene_name: str | None):
    scene = get_scene(scene_name)
    scene.frame_set(frame_number)
