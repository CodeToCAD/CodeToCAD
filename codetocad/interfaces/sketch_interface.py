# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.edge_interface import EdgeInterface

from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.part_interface import PartInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.importable_interface import ImportableInterface

from codetocad.interfaces.scalable_interface import ScalableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.exportable_interface import ExportableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface


class SketchInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    ImportableInterface,
    ExportableInterface,
    ScalableInterface,
    ProjectableInterface,
    LandmarkableInterface,
    metaclass=ABCMeta,
):

    """
    Capabilities related to creating and manipulating 2D sketches, composed of vertices, edges and wires.
    """

    @abstractmethod
    def __init__(
        self,
        name: "str",
        description: "str| None" = None,
        native_instance=None,
        curve_type: "CurveTypes| None" = None,
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance
        self.curve_type = curve_type

    @abstractmethod
    def clone(
        self, new_name: "str", copy_landmarks: "bool" = True
    ) -> "SketchInterface":
        """
        Clone an existing sketch with its geometry and properties. Returns the new Sketch.
        """

        print("clone is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def revolve(
        self,
        angle: "AngleOrItsFloatOrStringValue",
        about_entity_or_landmark: "EntityOrItsName",
        axis: "AxisOrItsIndexOrItsName" = "z",
    ) -> "PartInterface":
        """
        Revolve a Sketch around another Entity or Landmark
        """

        print("revolve is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def twist(
        self,
        angle: "AngleOrItsFloatOrStringValue",
        screw_pitch: "DimensionOrItsFloatOrStringValue",
        iterations: "int" = 1,
        axis: "AxisOrItsIndexOrItsName" = "z",
    ):
        """
        AKA Helix, Screw.
        """

        print("twist is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def extrude(self, length: "DimensionOrItsFloatOrStringValue") -> "PartInterface":
        """
        Extrude a curve by a specified length. Returns a Part type.
        """

        print("extrude is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def sweep(
        self, profile_name_or_instance: "SketchOrItsName", fill_cap: "bool" = True
    ) -> "PartInterface":
        """
        Extrude this Sketch along the path of another Sketch
        """

        print("sweep is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def offset(self, radius: "DimensionOrItsFloatOrStringValue"):
        """
        Uniformly add a wall around a Sketch.
        """

        print("offset is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def profile(self, profile_curve_name: "str"):
        """
        Bend this curve along the path of another
        """

        print("profile is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def create_text(
        self,
        text: "str",
        font_size: "DimensionOrItsFloatOrStringValue" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
    ):
        """
        Adds text to a sketch.
        """

        print(
            "create_text is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_from_vertices(
        self, points: "list[PointOrListOfFloatOrItsStringValueOrVertex]"
    ) -> "WireInterface":
        """
        Create a curve from 2D/3D points.
        """

        print(
            "create_from_vertices is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_point(
        self, point: "PointOrListOfFloatOrItsStringValue"
    ) -> "VertexInterface":
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
        start_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        end_at: "PointOrListOfFloatOrItsStringValueOrVertex",
    ) -> "EdgeInterface":
        """
        Create a line between two points
        """

        print(
            "create_line is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_circle(
        self, radius: "DimensionOrItsFloatOrStringValue"
    ) -> "WireInterface":
        """
        Create a circle
        """

        print(
            "create_circle is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_ellipse(
        self,
        radius_minor: "DimensionOrItsFloatOrStringValue",
        radius_major: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        """
        Create an ellipse
        """

        print(
            "create_ellipse is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_arc(
        self,
        start_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        end_at: "PointOrListOfFloatOrItsStringValueOrVertex",
        radius: "DimensionOrItsFloatOrStringValue",
        flip: "bool| None" = False,
    ) -> "WireInterface":
        """
        Create an arc. The radius is the distance from the center of the circle that forms the arc, to the chord tying start_at and end_at.
        """

        print(
            "create_arc is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_rectangle(
        self,
        length: "DimensionOrItsFloatOrStringValue",
        width: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        """
        Create a rectangle
        """

        print(
            "create_rectangle is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_polygon(
        self,
        number_of_sides: "int",
        length: "DimensionOrItsFloatOrStringValue",
        width: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        """
        Create an n-gon
        """

        print(
            "create_polygon is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_trapezoid(
        self,
        length_upper: "DimensionOrItsFloatOrStringValue",
        length_lower: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
    ) -> "WireInterface":
        """
        Create a trapezoid
        """

        print(
            "create_trapezoid is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_spiral(
        self,
        number_of_turns: "int",
        height: "DimensionOrItsFloatOrStringValue",
        radius: "DimensionOrItsFloatOrStringValue",
        is_clockwise: "bool" = True,
        radius_end: "DimensionOrItsFloatOrStringValue| None" = None,
    ) -> "WireInterface":
        """
        Create a spiral or helix
        """

        print(
            "create_spiral is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
