# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *


from codetocad.providers import get_provider

from codetocad.interfaces.vertex_interface import VertexInterface


class Vertex:
    """
    A single point in space, or a control point.

    NOTE: This is a proxy-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
        name: "str",
        location: "Point",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ) -> VertexInterface:
        return get_provider(VertexInterface)(
            name, location, description, native_instance, parent_entity
        )  # type: ignore
