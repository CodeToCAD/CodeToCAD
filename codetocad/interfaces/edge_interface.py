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
    SubdividableInterface,
    ProjectableInterface,
)

from . import EntityInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import VertexInterface
    from . import SketchInterface


class EdgeInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    SubdividableInterface,
    ProjectableInterface,
    metaclass=ABCMeta,
):
    """A curve bounded by two Vertices."""

    v1: "Vertex"
    v2: "Vertex"
    parent_sketch: Optional[SketchOrItsName] = None

    @abstractmethod
    def __init__(
        self,
        v1: "VertexInterface",
        v2: "VertexInterface",
        name: str,
        parent_sketch: Optional[SketchOrItsName] = None,
        description: Optional[str] = None,
        native_instance=None,
    ):
        super().__init__(
            name=name, description=description, native_instance=native_instance
        )
        self.v1 = v1
        self.v2 = v2
        self.parent_sketch = parent_sketch
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def offset(self, distance: DimensionOrItsFloatOrStringValue) -> "EdgeInterface":
        """
        Clone and offset this edge a distance away from this one.
        """

        print("offset is called in an abstract method. Please override this method.")
        raise NotImplementedError()

    @abstractmethod
    def fillet(self, other_edge: "EdgeInterface", amount: AngleOrItsFloatOrStringValue):
        """
        Fillet this and another edge.
        """

        print("fillet is called in an abstract method. Please override this method.")
        return self

    @abstractmethod
    def set_is_construction(self, is_construction: bool):
        """
        Mark this edge for construction only.
        """

        print(
            "set_is_construction is called in an abstract method. Please override this method."
        )
        return self

    @abstractmethod
    def get_is_construction(self) -> bool:
        """
        Check if this edge is for construction only.
        """

        print(
            "get_is_construction is called in an abstract method. Please override this method."
        )
        raise NotImplementedError()
