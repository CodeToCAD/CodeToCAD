# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class MirrorableTestInterface(metaclass=ABCMeta):
    @abstractmethod
    def test_mirror(self):
        instance = Mirrorable()

        value = instance.mirror(
            "mirror_across_entity", "axis", "resulting_mirrored_entity_name"
        )

        assert value.is_exists(), "Create method failed."
