# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.providers import get_provider


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface


def create_edge(
    name: "str",
    v1: "VertexInterface",
    v2: "VertexInterface",
    description: "str| None" = None,
    native_instance=None,
    parent_entity: "str|EntityInterface| None" = None,
) -> EdgeInterface:
    """
    A curve bounded by two Vertices.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(EdgeInterface)(
        name, v1, v2, description, native_instance, parent_entity
    )  # type: ignore
