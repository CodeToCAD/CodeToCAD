# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class EdgeTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_offset(self):
        pass

    @abstractmethod
    def test_fillet(self):
        pass

    @abstractmethod
    def test_set_is_construction(self):
        pass

    @abstractmethod
    def test_get_is_construction(self):
        pass
