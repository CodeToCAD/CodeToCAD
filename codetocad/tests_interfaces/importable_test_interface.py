# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class ImportableTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_create_from_file(self):
        instance = Importable()

        value = instance.create_from_file("file_path", "file_type")

        assert value.is_exists(), "Create method failed."
