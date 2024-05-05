# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class JointTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_translate_landmark_onto_another(self):

        pass

    @abstractmethod
    def test_pivot(self):

        pass

    @abstractmethod
    def test_gear_ratio(self):

        pass

    @abstractmethod
    def test_limit_location_xyz(self):

        pass

    @abstractmethod
    def test_limit_location_x(self):

        pass

    @abstractmethod
    def test_limit_location_y(self):

        pass

    @abstractmethod
    def test_limit_location_z(self):

        pass

    @abstractmethod
    def test_limit_rotation_xyz(self):

        pass

    @abstractmethod
    def test_limit_rotation_x(self):

        pass

    @abstractmethod
    def test_limit_rotation_y(self):

        pass

    @abstractmethod
    def test_limit_rotation_z(self):

        pass
