# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.entity_interface import EntityInterface


class WireInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    ProjectableInterface,
    LandmarkableInterface,
    BooleanableInterface,
    SubdividableInterface,
    metaclass=ABCMeta,
):
    """
    A collection of connected edges.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        edges: "list[EdgeInterface]",
        description: "str| None" = None,
        native_instance=None,
        parent_entity: "str|EntityInterface| None" = None,
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
    def get_edges(
        self,
    ) -> "list[EdgeInterface]":
        """
        Return references to all the edges making up this wire.
        """

        print("get_edges is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def get_vertices(
        self,
    ) -> "list[VertexInterface]":
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

    @abstractmethod
    def revolve(
        self,
        angle: "str|float|Angle",
        about_entity_or_landmark: "str|EntityInterface",
        axis: "str|int|Axis" = "z",
    ) -> "PartInterface":
        """
        Revolve a Wire around another Entity or Landmark
        """

        print("revolve is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def twist(
        self,
        angle: "str|float|Angle",
        screw_pitch: "str|float|Dimension",
        iterations: "int" = 1,
        axis: "str|int|Axis" = "z",
    ) -> Self:
        """
        AKA Helix, Screw.
        """

        print("twist is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def extrude(self, length: "str|float|Dimension") -> "PartInterface":
        """
        Extrude a curve by a specified length. Returns a Part type.
        """

        print("extrude is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def sweep(
        self, profile_name_or_instance: "str|WireInterface", fill_cap: "bool" = True
    ) -> "PartInterface":
        """
        Extrude this Wire along the path of another Wire
        """

        print("sweep is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def offset(self, radius: "str|float|Dimension") -> "WireInterface":
        """
        Uniformly add a wall around a Wire. This returns a new wire in the same sketch.
        """

        print("offset is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def profile(self, profile_curve_name: "str") -> Self:
        """
        Bend this curve along the path of another
        """

        print("profile is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
    ) -> Self:
        """
        Create a curve from 2D/3D points.
        """

        print(
            "create_from_vertices is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_point(
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> Self:
        """
        Create a point
        """

        print(
            "create_point is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_line(
        self,
        length: "str|float|Dimension",
        angle: "str|float|Angle",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        """
        Create a line between two points
        """

        print(
            "create_line is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_line_to(
        self,
        to: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        options: "SketchOptions| None" = None,
    ) -> Self:
        """
        Create a line between two points
        """

        print(
            "create_line_to is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_arc(
        self,
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
    ) -> Self:
        """
        Create an arc. The radius is the distance from the center of the circle that forms the arc, to the chord tying start_at and end_at.
        """

        print(
            "create_arc is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
