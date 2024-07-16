# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from typing import Self


from codetocad.providers import get_provider

from codetocad.interfaces.render_interface import RenderInterface


from codetocad.interfaces.camera_interface import CameraInterface


class Render(
    RenderInterface,
):
    """
    Render the scene and export images or videos.

    NOTE: This is a proxy - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    # References OBJECT PROXYING (PYTHON RECIPE) https://code.activestate.com/recipes/496741-object-proxying/

    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "__proxied"), name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "__proxied"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "__proxied"), name, value)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, "__proxied"))

    def __str__(self):
        return str(object.__getattribute__(self, "__proxied"))

    def __repr__(self):
        return repr(object.__getattribute__(self, "__proxied"))

    __slots__ = [
        "__proxied",
    ]

    def __init__(
        self,
    ):
        object.__setattr__(
            self, "__proxied", get_provider(RenderInterface)()  # type: ignore
        )

    def render_image(
        self,
        output_file_path: "str",
        overwrite: "bool" = True,
        file_type: "str| None" = None,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").render_image(
            output_file_path, overwrite, file_type
        )

    def render_video_mp4(
        self,
        output_file_path: "str",
        start_frame_number: "int" = 1,
        end_frame_number: "int" = 100,
        step_frames: "int" = 1,
        overwrite: "bool" = True,
    ) -> Self:
        return object.__getattribute__(self, "__proxied").render_video_mp4(
            output_file_path,
            start_frame_number,
            end_frame_number,
            step_frames,
            overwrite,
        )

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
        return object.__getattribute__(self, "__proxied").render_video_frames(
            output_folder_path,
            file_name_prefix,
            start_frame_number,
            end_frame_number,
            step_frames,
            overwrite,
            file_type,
        )

    def set_frame_rate(self, frame_rate: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_frame_rate(frame_rate)

    def set_resolution(self, x: "int", y: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_resolution(x, y)

    def set_render_quality(self, quality: "int") -> Self:
        return object.__getattribute__(self, "__proxied").set_render_quality(quality)

    def set_render_engine(self, name: "str") -> Self:
        return object.__getattribute__(self, "__proxied").set_render_engine(name)

    def set_camera(self, camera_name_or_instance: "str|CameraInterface") -> Self:
        return object.__getattribute__(self, "__proxied").set_camera(
            camera_name_or_instance
        )
