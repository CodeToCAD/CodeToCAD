from codetocad.interfaces.render_interface import RenderInterface
from codetocad.utilities.supported import supported
from codetocad.enums.support_level import SupportLevel
from codetocad.interfaces.camera_interface import CameraInterface


class Render(RenderInterface):

    @supported(SupportLevel.UNSUPPORTED)
    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ):
        raise NotImplementedError()
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
        raise NotImplementedError()
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
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_frame_rate(self, frame_rate: "int"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_resolution(self, x: "int", y: "int"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_render_quality(self, quality: "int"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_render_engine(self, name: "str"):
        raise NotImplementedError()
        return self

    @supported(SupportLevel.UNSUPPORTED)
    def set_camera(self, camera_instance: "CameraInterface"):
        raise NotImplementedError()
        return self
