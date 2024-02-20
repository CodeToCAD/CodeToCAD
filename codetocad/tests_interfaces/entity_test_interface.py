# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class EntityTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_is_exists(self):
        pass

    @abstractmethod
    def test_rename(self):
        pass

    @abstractmethod
    def test_delete(self):
        pass

    @abstractmethod
    def test_is_visible(self):
        pass

    @abstractmethod
    def test_set_visible(self):
        pass

    @abstractmethod
    def test_apply(self):
        pass

    @abstractmethod
    def test_get_native_instance(self):
        pass

    @abstractmethod
    def test_get_location_world(self):
        pass

    @abstractmethod
    def test_get_location_local(self):
        pass

    @abstractmethod
    def test_select(self):
        pass

    @abstractmethod
    def test_translate_xyz(self):
        pass

    @abstractmethod
    def test_translate_x(self):
        pass

    @abstractmethod
    def test_translate_y(self):
        pass

    @abstractmethod
    def test_translate_z(self):
        pass

    @abstractmethod
    def test_rotate_xyz(self):
        pass

    @abstractmethod
    def test_rotate_x(self):
        pass

    @abstractmethod
    def test_rotate_y(self):
        pass

    @abstractmethod
    def test_rotate_z(self):
        pass

    @abstractmethod
    def test_get_bounding_box(self):
        pass

    @abstractmethod
    def test_get_dimensions(self):
        pass
