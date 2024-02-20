# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class SceneTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_default(self):
        pass

    @abstractmethod
    def test_create(self):
        pass

    @abstractmethod
    def test_delete(self):
        pass

    @abstractmethod
    def test_is_exists(self):
        pass

    @abstractmethod
    def test_get_selected_entity(self):
        pass

    @abstractmethod
    def test_export(self):
        pass

    @abstractmethod
    def test_set_default_unit(self):
        pass

    @abstractmethod
    def test_create_group(self):
        pass

    @abstractmethod
    def test_delete_group(self):
        pass

    @abstractmethod
    def test_remove_from_group(self):
        pass

    @abstractmethod
    def test_assign_to_group(self):
        pass

    @abstractmethod
    def test_set_visible(self):
        pass

    @abstractmethod
    def test_set_background_image(self):
        pass
