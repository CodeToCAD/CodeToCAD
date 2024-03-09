# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.
# Copy this file and remove this header to create a new CodeToCAD Provider.

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.edge_interface import EdgeInterface


from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface


class Edge:
    """
    A curve bounded by two Vertices.

    NOTE: This is a facade-factory - calling this returns an instance of a registered provider.
    Register a provider using the `register()` method.
    """

    def __new__(
        cls,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ) -> EdgeInterface:
        return cls._provider(name, v1, v2, description, native_instance, parent_entity)

    @classmethod
    def register(cls, provider: EdgeInterface):
        cls._provider = provider
