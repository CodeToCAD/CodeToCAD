# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from typing import Optional
from abc import ABCMeta, abstractmethod

from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces import (
    MirrorableInterface,
    PatternableInterface,
    ProjectableInterface,
)

from . import EntityInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import EdgeInterface
    from . import EntityInterface
    from . import VertexInterface
    from . import PartInterface


class WireInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    ProjectableInterface,
    metaclass=ABCMeta,
):
    """A collection of connected edges."""

    edges: "list[EdgeInterface]"
    parent_entity: Optional[EntityOrItsName] = None

    @abstractmethod
    def __init__(
        self,
        edges: "list[EdgeInterface]",
        name: str,
        parent_entity: Optional[EntityOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.edges = edges
        self.parent_entity = parent_entity
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def get_vertices(self) -> "list[VertexInterface]":
        """
        Collapse all edges' vertices into one list.
        """

        print(
            "get_vertices is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()

    @abstractmethod
    def is_closed(self) -> bool:
        """
        A closed wire is a Face.
        """

        print("is_closed is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def loft(
        self, other: "WireInterface", new_part_name: Optional[str] = None
    ) -> "PartInterface":
        """
        Create a surface between two Wires (Faces). If new_part_name is not provided, the two Wires' parents and the surface will be boolean union'ed, and the resulting Part will take the name of the first wire.
        """

        print("loft is called in an abstract method. Please override this method.")
        raise NotImplementedError()
