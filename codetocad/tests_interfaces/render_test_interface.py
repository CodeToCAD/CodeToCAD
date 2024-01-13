# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class RenderTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_render_image(self):
        pass

    @abstractmethod
    def test_render_video_mp4(self):
        pass

    @abstractmethod
    def test_render_video_frames(self):
        pass

    @abstractmethod
    def test_set_frame_rate(self):
        pass

    @abstractmethod
    def test_set_resolution(self):
        pass

    @abstractmethod
    def test_set_render_quality(self):
        pass

    @abstractmethod
    def test_set_render_engine(self):
        pass

    @abstractmethod
    def test_set_camera(self):
        pass
