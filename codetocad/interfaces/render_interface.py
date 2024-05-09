# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from typing import Self


from codetocad.interfaces.camera_interface import CameraInterface


class RenderInterface(metaclass=ABCMeta):
    """
    Render the scene and export images or videos.
    """

    @abstractmethod
    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ) -> Self:
        """
        Render a still image.
        """

        print(
            "render_image is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def render_video_mp4(
        self,
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ) -> Self:
        """
        Render an MP4 video.
        """

        print(
            "render_video_mp4 is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
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
        """
        Render a video as image frame stills.
        """

        print(
            "render_video_frames is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_frame_rate(self, frame_rate: "int") -> Self:
        """
        Set rendering framerate.
        """

        print(
            "set_frame_rate is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_resolution(self, x: "int", y: "int") -> Self:
        """
        Set rendering resolution
        """

        print(
            "set_resolution is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_render_quality(self, quality: "int") -> Self:
        """
        Set rendering quality.
        """

        print(
            "set_render_quality is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_render_engine(self, name: "str") -> Self:
        """
        Set rendering engine name.
        """

        print(
            "set_render_engine is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def set_camera(self, camera_name_or_instance: "str|CameraInterface") -> Self:
        """
        Set the rendering camera.
        """

        print(
            "set_camera is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
