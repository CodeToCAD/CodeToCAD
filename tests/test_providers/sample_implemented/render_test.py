from tests.test_providers import *
from codetocad.tests_interfaces.render_test_interface import RenderTestInterface
import os


class RenderTest(TestProviderCase, RenderTestInterface):
    def test_render_image(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance = Render()

        value = instance.render_image(
            output_file_path=f"{os.getcwd()}/test-render-image-blender.png",
            overwrite=True,
        )  # "file_type")

    def test_render_video_mp4(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance = Render()

        value = instance.render_video_mp4(
            output_file_path="test-render.mp4",
            start_frame_number=10,
            end_frame_number=200,
            step_frames=10,
            # "overwrite",
        )

    def test_render_video_frames(self):
        instance = Part("myCube")

        instance.create_cube(1, 1, 1)

        instance = Render()

        value = instance.render_video_frames(
            output_folder_path="test-renders",
            file_name_prefix="test-blender-vids",
            start_frame_number=10,
            end_frame_number=200,
            step_frames=10,
            # "overwrite",
            # "file_type",
        )

    def test_set_frame_rate(self):
        instance = Render()

        value = instance.set_frame_rate(frame_rate=10)

        assert value, "Modify method failed."

    def test_set_resolution(self):
        instance = Render()

        value = instance.set_resolution(x=600, y=800)

        assert value, "Modify method failed."

    def test_set_render_quality(self):
        instance = Render()

        value = instance.set_render_quality(quality=100)

        assert value, "Modify method failed."

    def test_set_render_engine(self):
        instance = Render()

        value = instance.set_render_engine(name="cycles")

        assert value, "Modify method failed."

    def test_set_camera(self):
        instance = Render()

        value = instance.set_camera(camera_name_or_instance="myCamera")

        assert value, "Modify method failed."
