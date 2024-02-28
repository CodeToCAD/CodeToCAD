# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface


class WireInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    ProjectableInterface,
    LandmarkableInterface,
    BooleanableInterface,
    metaclass=ABCMeta,
):

    """
    A collection of connected edges.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        edges: "list[Edge]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "EntityOrItsName| None" = None,
    ):
        self.name = name
        self.edges = edges
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    @abstractmethod
    def get_normal(self, flip: "bool| None" = False) -> "Point":
        """
        Get the normal created by this wire. Must be a closed wire.
        """

        print(
            "get_normal is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_vertices(
        self,
    ) -> "list[Vertex]":
        """
        Collapse all edges' vertices into one list.
        """

        print(
            "get_vertices is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_is_closed(
        self,
    ) -> "bool":
        """
        Checks if a wire is closed. Note: A closed wire is a Face or Surface.
        """

        print(
            "get_is_closed is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def loft(
        self, other: "WireInterface", new_part_name: "str| None" = None
    ) -> "PartInterface":
        """
        Create a surface between two Wires (Faces). If new_part_name is not provided, the two Wires' parents and the surface will be boolean union'ed, and the resulting Part will take the name of the first wire.
        """

        print("loft is called in an abstract method. Please override this method.")

        raise NotImplementedError()
