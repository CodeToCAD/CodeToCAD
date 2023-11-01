from typing import Optional

from . import blender_actions
from . import blender_definitions

from codetocad.interfaces import RenderInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


class Render(RenderInterface):
    @staticmethod
    def _set_file_format(output_file_path: str):
        fileFormat = blender_definitions.FileFormat.from_utilities_file_format(
            FileFormats.from_string(get_file_extension(output_file_path))
        )
        blender_actions.set_render_file_format(fileFormat)

    def render_image(
        self,
        output_file_path: str,
        overwrite: bool = True,
        file_type: Optional[str] = None,
    ):
        absoluteFilePath = get_absolute_filepath(output_file_path)

        Render._set_file_format(absoluteFilePath)

        blender_actions.render_image(absoluteFilePath, overwrite or True)

        return self

    def render_video_mp4(
        self,
        output_file_path: str,
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: bool = True,
    ):
        absoluteFilePath = get_absolute_filepath(output_file_path)

        Render._set_file_format(absoluteFilePath)

        blender_actions.render_animation(absoluteFilePath, overwrite or True)
        return self

    def render_video_frames(
        self,
        output_folder_path: str,
        file_name_prefix: str,
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: bool = True,
        file_type: Optional[str] = None,
    ):
        absoluteFilePath = get_absolute_filepath(output_folder_path)

        raise NotImplementedError()
        return self

    def set_frame_rate(self, frame_rate: int):
        blender_actions.set_render_frame_rate(int(frame_rate))

        return self

    def set_resolution(self, x: "int", y: "int"):
        blender_actions.set_render_resolution(x, y)
        return self

    def set_render_quality(self, quality: int):
        percentage = quality * 100 if quality < 1.0 else quality
        percentage = int(percentage)
        blender_actions.set_render_quality(percentage)

        return self

    def set_render_engine(self, name: str):
        blender_actions.set_render_engine(
            blender_definitions.RenderEngines.from_string(name)
        )

        return self

    def set_camera(self, camera_name_or_instance: CameraOrItsName):
        cameraName = camera_name_or_instance
        if isinstance(cameraName, CameraInterface):
            cameraName = cameraName.name

        blender_actions.set_scene_camera(cameraName)

        return self
