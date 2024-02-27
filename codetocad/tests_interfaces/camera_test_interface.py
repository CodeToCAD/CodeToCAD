# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class CameraTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_create_perspective(self):
        pass

    @abstractmethod
    def test_create_orthogonal(self):
        pass

    @abstractmethod
    def test_create_panoramic(self):
        pass

    @abstractmethod
    def test_set_focal_length(self):
        pass
