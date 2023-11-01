# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod

from codetocad import Render


class RenderTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_render_image(self):
        instance = Render()

        value = instance.render_image("output_file_path", "overwrite", "file_type")

    @abstractmethod
    def test_render_video_mp4(self):
        instance = Render()

        value = instance.render_video_mp4(
            "output_file_path",
            "start_frame_number",
            "end_frame_number",
            "step_frames",
            "overwrite",
        )

    @abstractmethod
    def test_render_video_frames(self):
        instance = Render()

        value = instance.render_video_frames(
            "output_folder_path",
            "file_name_prefix",
            "start_frame_number",
            "end_frame_number",
            "step_frames",
            "overwrite",
            "file_type",
        )

    @abstractmethod
    def test_set_frame_rate(self):
        instance = Render()

        value = instance.set_frame_rate("frame_rate")

        assert value, "Modify method failed."

    @abstractmethod
    def test_set_resolution(self):
        instance = Render()

        value = instance.set_resolution("x", "y")

        assert value, "Modify method failed."

    @abstractmethod
    def test_set_render_quality(self):
        instance = Render()

        value = instance.set_render_quality("quality")

        assert value, "Modify method failed."

    @abstractmethod
    def test_set_render_engine(self):
        instance = Render()

        value = instance.set_render_engine("name")

        assert value, "Modify method failed."

    @abstractmethod
    def test_set_camera(self):
        instance = Render()

        value = instance.set_camera("camera_name_or_instance")

        assert value, "Modify method failed."
