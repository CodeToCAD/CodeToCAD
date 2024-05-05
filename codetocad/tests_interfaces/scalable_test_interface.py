# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class ScalableTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_scale_xyz(self):

        pass

    @abstractmethod
    def test_scale_x(self):

        pass

    @abstractmethod
    def test_scale_y(self):

        pass

    @abstractmethod
    def test_scale_z(self):

        pass

    @abstractmethod
    def test_scale_x_by_factor(self):

        pass

    @abstractmethod
    def test_scale_y_by_factor(self):

        pass

    @abstractmethod
    def test_scale_z_by_factor(self):

        pass

    @abstractmethod
    def test_scale_keep_aspect_ratio(self):

        pass
