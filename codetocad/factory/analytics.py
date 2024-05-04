# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.analytics_interface import AnalyticsInterface

from codetocad.providers import get_provider


from codetocad.interfaces.entity_interface import EntityInterface


def create_analytics() -> AnalyticsInterface:
    """
    Tools for collecting data about the entities and scene.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(AnalyticsInterface)()  # type: ignore
