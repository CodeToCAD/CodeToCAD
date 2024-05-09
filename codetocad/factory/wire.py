# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.


from codetocad.interfaces.wire_interface import WireInterface

from codetocad.providers import get_provider


from codetocad.interfaces.edge_interface import EdgeInterface


def create_wire(
    name: "str",
    edges: "list[EdgeInterface]",
    description: "str| None" = None,
    native_instance=None,
    parent_entity: "str|EntityInterface| None" = None,
) -> WireInterface:
    """
    A collection of connected edges.

    NOTE: This is a factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """
    return get_provider(WireInterface)(
        name, edges, description, native_instance, parent_entity
    )  # type: ignore
