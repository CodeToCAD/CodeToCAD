# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.providers import get_provider

from codetocad.interfaces.entity_interface import EntityInterface


class Entity:
    """
    Capabilities shared between scene objects.

    NOTE: This is a proxy-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls, name: "str", description: "str| None" = None, native_instance=None
    ) -> EntityInterface:
        return get_provider(EntityInterface)(
            name, description, native_instance
        )  # type: ignore
