# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.landmark_interface import LandmarkInterface


from codetocad.interfaces.entity_interface import EntityInterface


class Landmark:
    """
    Landmarks are named positions on an entity.

    NOTE: This is a proxy-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
        name: "str",
        parent_entity: "str|Entity",
        description: "str| None" = None,
        native_instance=None,
    ) -> LandmarkInterface:
        return get_provider(LandmarkInterface)(
            name, parent_entity, description, native_instance
        )  # type: ignore
