# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.vertex_interface import VertexInterface


from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.entity_interface import EntityInterface


class EdgeInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    SubdividableInterface,
    ProjectableInterface,
    LandmarkableInterface,
    metaclass=ABCMeta,
):
    """
    A curve bounded by two Vertices.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        v1: "VertexInterface",
        v2: "VertexInterface",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
    ):

        self.name = name
        self.v1 = v1
        self.v2 = v2
        self.description = description
        self.native_instance = native_instance
        self.parent_entity = parent_entity

    @abstractmethod
    def offset(self, distance: "str|float|Dimension") -> "EdgeInterface":
        """
        Clone and offset this edge a distance away from this one. This returns a new edge in the same sketch.
        """

        print("offset is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def fillet(self, other_edge: "EdgeInterface", amount: "str|float|Angle") -> Self:
        """
        Fillet this and another edge.
        """

        print("fillet is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_is_construction(self, is_construction: "bool") -> Self:
        """
        Mark this edge for construction only.
        """

        print(
            "set_is_construction is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def get_is_construction(
        self,
    ) -> "bool":
        """
        Check if this edge is for construction only.
        """

        print(
            "get_is_construction is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
