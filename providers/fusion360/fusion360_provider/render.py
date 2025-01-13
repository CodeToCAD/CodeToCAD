from codetocad.interfaces.render_interface import RenderInterface
from codetocad.codetocad_types import *
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface


class Render(RenderInterface):

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def render_image(
        output_file_path: "str", overwrite: "bool" = True, file_type: "str| None" = None
    ) -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def render_video_mp4(
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ) -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def render_video_frames(
        output_folder_path: "str",
        file_name_prefix: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ) -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def set_frame_rate(frame_rate: "int") -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def set_resolution(x: "int", y: "int") -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def set_render_quality(quality: "int") -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def set_render_engine(name: "str") -> None:
        raise NotImplementedError()
        return self

    @staticmethod
    @supported(SupportLevel.SUPPORTED, notes="")
    def set_camera(camera_instance: "CameraInterface") -> None:
        raise NotImplementedError()
        return self
