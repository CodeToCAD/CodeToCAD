from tests.test_providers import *
from codetocad.tests_interfaces.render_test_interface import RenderTestInterface
import os


class RenderTest(TestProviderCase, RenderTestInterface):
    def test_render_image(self):
        instance = Part.create_cube(1, 1, 1)

        instance = Render.render_image(
            output_file_path=f"{os.getcwd()}/test-render-image-blender.png",
            overwrite=True,
        )  # "file_type")

    def test_render_video_mp4(self):
        instance = Part.create_cube(1, 1, 1)

        instance = Render.render_video_mp4(
            output_file_path="test-render.mp4",
            start_frame_number=10,
            end_frame_number=200,
            step_frames=10,
            # "overwrite",
        )

    def test_render_video_frames(self):
        instance = Part.create_cube(1, 1, 1)

        instance = Render.render_video_frames(
            output_folder_path="test-renders",
            file_name_prefix="test-blender-vids",
            start_frame_number=10,
            end_frame_number=200,
            step_frames=10,
            # "overwrite",
            # "file_type",
        )

    def test_set_frame_rate(self):
        instance = Render.set_frame_rate(frame_rate=10)

        assert instance is None, "Modify method failed."

    def test_set_resolution(self):
        instance = Render.set_resolution(x=600, y=800)

        assert instance is None, "Modify method failed."

    def test_set_render_quality(self):
        instance = Render.set_render_quality(quality=100)

        assert instance is None, "Modify method failed."

    def test_set_render_engine(self):
        instance = Render.set_render_engine(name="cycles")

        assert instance is None, "Modify method failed."

    def test_set_camera(self):
        camera = Camera.create_orthogonal()

        instance = Render.set_camera(camera_instance=camera)

        assert instance is None, "Modify method failed."
