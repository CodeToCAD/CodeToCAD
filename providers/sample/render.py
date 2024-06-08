# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self

from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel


from codetocad.interfaces.render_interface import RenderInterface


from codetocad.interfaces.camera_interface import CameraInterface


class Render(
    RenderInterface,
):

    @supported(SupportLevel.SUPPORTED, notes="")
    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ) -> Self:

        print("render_image called", f": {output_file_path}, {overwrite}, {file_type}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def render_video_mp4(
        self,
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ) -> Self:

        print(
            "render_video_mp4 called",
            f": {output_file_path}, {start_frame_number}, {end_frame_number}, {step_frames}, {overwrite}",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def render_video_frames(
        self,
        output_folder_path: "str",
        file_name_prefix: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ) -> Self:

        print(
            "render_video_frames called",
            f": {output_folder_path}, {file_name_prefix}, {start_frame_number}, {end_frame_number}, {step_frames}, {overwrite}, {file_type}",
        )

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_rate(self, frame_rate: "int") -> Self:

        print("set_frame_rate called", f": {frame_rate}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_resolution(self, x: "int", y: "int") -> Self:

        print("set_resolution called", f": {x}, {y}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_render_quality(self, quality: "int") -> Self:

        print("set_render_quality called", f": {quality}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_render_engine(self, name: "str") -> Self:

        print("set_render_engine called", f": {name}")

        return self

    @supported(SupportLevel.SUPPORTED, notes="")
    def set_camera(self, camera_name_or_instance: "str|CameraInterface") -> Self:

        print("set_camera called", f": {camera_name_or_instance}")

        return self
