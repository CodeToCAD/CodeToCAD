# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.wire_interface import WireInterface


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.edge_interface import EdgeInterface


class Wire:
    """
    A collection of connected edges.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
        name: "str",
        edges: "list[Edge]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ) -> WireInterface:
        return cls._provider(name, edges, description, native_instance, parent_entity)

    @classmethod
    def register(cls, provider: WireInterface):
        cls._provider = provider
