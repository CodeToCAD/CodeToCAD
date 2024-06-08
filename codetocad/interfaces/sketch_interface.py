# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *


from codetocad.interfaces.vertex_interface import VertexInterface

from codetocad.interfaces.wire_interface import WireInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.scalable_interface import ScalableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.projectable_interface import ProjectableInterface

from codetocad.interfaces.importable_interface import ImportableInterface

from codetocad.interfaces.exportable_interface import ExportableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.entity_interface import EntityInterface


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
    def get_wires(
        self,
    ) -> "list[WireInterface]":
        """
        Get a list of Wires in this Sketch.
        """

        print("get_wires is called in an abstract method. Please override this method.")

        raise NotImplementedError()

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
    def create_text(
        self,
        text: "str",
        font_size: "str|float|Dimension" = 1.0,
        bold: "bool" = False,
        italic: "bool" = False,
        underlined: "bool" = False,
        character_spacing: "int" = 1,
        word_spacing: "int" = 1,
        line_spacing: "int" = 1,
        font_file_path: "str| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        """
        Adds text to a sketch.
        """

        print(
            "create_text is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_from_vertices(
        self,
        points: "list[str|list[str]|list[float]|list[Dimension]|Point|VertexInterface]",
        options: "SketchOptions| None" = None,
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
        self,
        point: "str|list[str]|list[float]|list[Dimension]|Point",
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
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
    ) -> "WireInterface":
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
    ) -> "WireInterface":
        """
        Create a line between two points
        """

        print(
            "create_line_to is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_circle(
        self,
        radius: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
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
        radius_minor: "str|float|Dimension",
        radius_major: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
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
        end_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface",
        radius: "str|float|Dimension",
        start_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = "PresetLandmark.end",
        flip: "bool| None" = False,
        options: "SketchOptions| None" = None,
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
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
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
        length: "str|float|Dimension",
        width: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
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
        length_upper: "str|float|Dimension",
        length_lower: "str|float|Dimension",
        height: "str|float|Dimension",
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
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
        height: "str|float|Dimension",
        radius: "str|float|Dimension",
        is_clockwise: "bool" = True,
        radius_end: "str|float|Dimension| None" = None,
        center_at: "str|list[str]|list[float]|list[Dimension]|Point|VertexInterface|LandmarkInterface|PresetLandmark| None" = None,
        options: "SketchOptions| None" = None,
    ) -> "WireInterface":
        """
        Create a spiral or helix
        """

        print(
            "create_spiral is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
