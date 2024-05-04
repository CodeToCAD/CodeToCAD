# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.providers import get_provider


from codetocad.interfaces.entity_interface import EntityInterface


def create_landmark(
    name: "str",
    parent_entity: "str|Entity",
    description: "str| None" = None,
    native_instance=None,
) -> LandmarkInterface:
    """
    Landmarks are named positions on an entity.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(LandmarkInterface)(
        name, parent_entity, description, native_instance
    )  # type: ignore
