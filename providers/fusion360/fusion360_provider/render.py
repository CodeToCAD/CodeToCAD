from typing import Optional
from codetocad.interfaces.camera_interface import CameraInterface
from providers.fusion360.fusion360_provider.camera import Camera
from codetocad.interfaces import RenderInterface
from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Camera


class Render(RenderInterface):
    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ):
        print("render_image called:", output_file_path, overwrite, file_type)
        return self

    def render_video_mp4(
        self,
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ):
        print(
            "render_video_mp4 called:",
            output_file_path,
            start_frame_number,
            end_frame_number,
            step_frames,
            overwrite,
        )
        return self

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
        print(
            "render_video_frames called:",
            output_folder_path,
            file_name_prefix,
            start_frame_number,
            end_frame_number,
            step_frames,
            overwrite,
            file_type,
        )
        return self

    def set_frame_rate(self, frame_rate: "int"):
        print("set_frame_rate called:", frame_rate)
        return self

    def set_resolution(self, x: "int", y: "int"):
        print("set_resolution called:", x, y)
        return self

    def set_render_quality(self, quality: "int"):
        print("set_render_quality called:", quality)
        return self

    def set_render_engine(self, name: "str"):
        print("set_render_engine called:", name)
        return self

    def set_camera(self, camera_name_or_instance: "CameraOrItsName"):
        print("set_camera called:", camera_name_or_instance)
        return self
