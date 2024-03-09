# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.
from tests.test_providers import *

from codetocad.tests_interfaces.render_test_interface import RenderTestInterface


class RenderTest(TestProviderCase, RenderTestInterface):
    def test_render_image(self):
        instance = Render()

        value = instance.render_image(
            output_file_path="String", overwrite=True, file_type="String"
        )

    def test_render_video_mp4(self):
        instance = Render()

        value = instance.render_video_mp4(
            output_file_path="String",
            start_frame_number=1,
            end_frame_number=100,
            step_frames=1,
            overwrite=True,
        )

    def test_render_video_frames(self):
        instance = Render()

        value = instance.render_video_frames(
            output_folder_path="String",
            file_name_prefix="String",
            start_frame_number=1,
            end_frame_number=100,
            step_frames=1,
            overwrite=True,
            file_type="String",
        )

    def test_set_frame_rate(self):
        instance = Render()

        value = instance.set_frame_rate(frame_rate=0)

        assert value, "Modify method failed."

    def test_set_resolution(self):
        instance = Render()

        value = instance.set_resolution(x=0, y=0)

        assert value, "Modify method failed."

    def test_set_render_quality(self):
        instance = Render()

        value = instance.set_render_quality(quality=0)

        assert value, "Modify method failed."

    def test_set_render_engine(self):
        instance = Render()

        value = instance.set_render_engine(name="String")

        assert value, "Modify method failed."

    def test_set_camera(self):
        instance = Render()

        value = instance.set_camera(camera_name_or_instance=Camera("a camera"))

        assert value, "Modify method failed."
