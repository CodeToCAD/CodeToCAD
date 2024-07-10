from codetocad.interfaces.render_interface import RenderInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface
from codetocad.codetocad_types import *
from codetocad.utilities import get_absolute_filepath, get_file_extension
from providers.blender.blender_provider.blender_actions.camera import set_scene_camera
from providers.blender.blender_provider.blender_actions.render import (
    render_animation,
    render_image,
    set_render_engine,
    set_render_file_format,
    set_render_frame_rate,
    set_render_quality,
    set_render_resolution,
)
from providers.blender.blender_provider.blender_definitions import (
    FileFormat,
    RenderEngines,
)


class Render(RenderInterface):

    @staticmethod
    def _set_file_format(output_file_path: str):
        fileFormat = FileFormat.from_utilities_file_format(
            FileFormats.from_string(get_file_extension(output_file_path))
        )
        set_render_file_format(fileFormat)

    @supported(SupportLevel.UNSUPPORTED)
    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ):
        absoluteFilePath = get_absolute_filepath(output_file_path)
        Render._set_file_format(absoluteFilePath)
        render_image(absoluteFilePath, overwrite or True)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def render_video_mp4(
        self,
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ):
        absoluteFilePath = get_absolute_filepath(output_file_path)
        Render._set_file_format(absoluteFilePath)
        render_animation(absoluteFilePath, overwrite or True)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def render_video_frames(
        self,
        output_folder_path: "str",
        file_name_prefix: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ):
        absoluteFilePath = get_absolute_filepath(output_folder_path)
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_frame_rate(self, frame_rate: "int"):
        set_render_frame_rate(int(frame_rate))
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_resolution(self, x: "int", y: "int"):
        set_render_resolution(x, y)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_render_quality(self, quality: "int"):
        percentage = quality * 100 if quality < 1.0 else quality
        percentage = int(percentage)
        set_render_quality(percentage)
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_render_engine(self, name: "str"):
        set_render_engine(RenderEngines.from_string(name))
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_camera(self, camera_name_or_instance: "str|CameraInterface"):
        cameraName = camera_name_or_instance
        if isinstance(cameraName, CameraInterface):
            cameraName = cameraName.name
        set_scene_camera(cameraName)
        return self
