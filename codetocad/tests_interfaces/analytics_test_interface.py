# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class AnalyticsTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_measure_distance(self):

        pass

    @abstractmethod
    def test_measure_angle(self):

        pass

    @abstractmethod
    def test_get_world_pose(self):

        pass

    @abstractmethod
    def test_get_bounding_box(self):

        pass

    @abstractmethod
    def test_get_dimensions(self):

        pass

    @abstractmethod
    def test_log(self):

        pass
