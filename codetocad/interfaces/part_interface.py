# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *
from codetocad.utilities import *
from codetocad.core import *
from codetocad.enums import *


from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.entity_interface import EntityInterface

from codetocad.interfaces.scalable_interface import ScalableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.importable_interface import ImportableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.exportable_interface import ExportableInterface


class PartInterface(
    EntityInterface,
    MirrorableInterface,
    PatternableInterface,
    SubdividableInterface,
    ImportableInterface,
    ExportableInterface,
    ScalableInterface,
    LandmarkableInterface,
    BooleanableInterface,
    metaclass=ABCMeta,
):

    """
    Capabilities related to creating and manipulating 3D shapes.
    """

    @abstractmethod
    def __init__(
        self, name: "str", description: "str| None" = None, native_instance=None
    ):
        self.name = name
        self.description = description
        self.native_instance = native_instance

    @abstractmethod
    def create_cube(
        self,
        width: "DimensionOrItsFloatOrStringValue",
        length: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds cuboid geometry to a part.
        """

        print(
            "create_cube is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_cone(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        draft_radius: "DimensionOrItsFloatOrStringValue" = 0,
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds cone geometry to a part.
        """

        print(
            "create_cone is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_cylinder(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds cylinder geometry to a part.
        """

        print(
            "create_cylinder is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_torus(
        self,
        inner_radius: "DimensionOrItsFloatOrStringValue",
        outer_radius: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds torus geometry to a part.
        """

        print(
            "create_torus is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_sphere(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds sphere geometry to a part.
        """

        print(
            "create_sphere is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_gear(
        self,
        outer_radius: "DimensionOrItsFloatOrStringValue",
        addendum: "DimensionOrItsFloatOrStringValue",
        inner_radius: "DimensionOrItsFloatOrStringValue",
        dedendum: "DimensionOrItsFloatOrStringValue",
        height: "DimensionOrItsFloatOrStringValue",
        pressure_angle: "AngleOrItsFloatOrStringValue" = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: "AngleOrItsFloatOrStringValue" = 0,
        conical_angle: "AngleOrItsFloatOrStringValue" = 0,
        crown_angle: "AngleOrItsFloatOrStringValue" = 0,
        keyword_arguments: "dict| None" = None,
    ):
        """
        Adds gear geometry to a part.
        """

        print(
            "create_gear is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def clone(self, new_name: "str", copy_landmarks: "bool" = True) -> "PartInterface":
        """
        Clone an existing Part with its geometry and properties. Returns the new Part.
        """

        print("clone is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def hollow(
        self,
        thickness_x: "DimensionOrItsFloatOrStringValue",
        thickness_y: "DimensionOrItsFloatOrStringValue",
        thickness_z: "DimensionOrItsFloatOrStringValue",
        start_axis: "AxisOrItsIndexOrItsName" = "z",
        flip_axis: "bool" = False,
    ):
        """
        Remove vertices, if necessary, until the part has a specified wall thickness.
        """

        print("hollow is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def thicken(self, radius: "DimensionOrItsFloatOrStringValue"):
        """
        Uniformly add a wall around a Part.
        """

        print("thicken is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def hole(
        self,
        hole_landmark: "LandmarkOrItsName",
        radius: "DimensionOrItsFloatOrStringValue",
        depth: "DimensionOrItsFloatOrStringValue",
        normal_axis: "AxisOrItsIndexOrItsName" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "AngleOrItsFloatOrStringValue" = 0.0,
        initial_rotation_y: "AngleOrItsFloatOrStringValue" = 0.0,
        initial_rotation_z: "AngleOrItsFloatOrStringValue" = 0.0,
        mirror_about_entity_or_landmark: "EntityOrItsName| None" = None,
        mirror_axis: "AxisOrItsIndexOrItsName" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "AngleOrItsFloatOrStringValue" = 0.0,
        circular_pattern_instance_axis: "AxisOrItsIndexOrItsName" = "z",
        circular_pattern_about_entity_or_landmark: "EntityOrItsName| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "DimensionOrItsFloatOrStringValue" = 0.0,
        linear_pattern_instance_axis: "AxisOrItsIndexOrItsName" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "DimensionOrItsFloatOrStringValue" = 0.0,
        linear_pattern2nd_instance_axis: "AxisOrItsIndexOrItsName" = "y",
    ):
        """
        Create a hole.
        """

        print("hole is called in an abstract method. Please override this method.")

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
        AKA Helix, Screw. Revolve an entity
        """

        print("twist is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_material(self, material_name: "MaterialOrItsName"):
        """
        Assign a known material to this part.
        """

        print(
            "set_material is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def is_colliding_with_part(self, other_part: "PartOrItsName") -> "bool":
        """
        Check if this part is colliding with another.
        """

        print(
            "is_colliding_with_part is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def fillet_all_edges(
        self, radius: "DimensionOrItsFloatOrStringValue", use_width: "bool" = False
    ):
        """
        Fillet all edges.
        """

        print(
            "fillet_all_edges is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def fillet_edges(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_edges: "list[LandmarkOrItsName]",
        use_width: "bool" = False,
    ):
        """
        Fillet specific edges.
        """

        print(
            "fillet_edges is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def fillet_faces(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_faces: "list[LandmarkOrItsName]",
        use_width: "bool" = False,
    ):
        """
        Fillet specific faces.
        """

        print(
            "fillet_faces is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def chamfer_all_edges(self, radius: "DimensionOrItsFloatOrStringValue"):
        """
        Chamfer all edges.
        """

        print(
            "chamfer_all_edges is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def chamfer_edges(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_edges: "list[LandmarkOrItsName]",
    ):
        """
        Chamfer specific edges.
        """

        print(
            "chamfer_edges is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def chamfer_faces(
        self,
        radius: "DimensionOrItsFloatOrStringValue",
        landmarks_near_faces: "list[LandmarkOrItsName]",
    ):
        """
        Chamfer specific faces.
        """

        print(
            "chamfer_faces is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_vertex_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        """
        Select the vertex closest to a Landmark on the entity (in UI).
        """

        print(
            "select_vertex_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_edge_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        """
        Select an edge closest to a landmark on the entity (in UI).
        """

        print(
            "select_edge_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_face_near_landmark(
        self, landmark_name: "LandmarkOrItsName| None" = None
    ):
        """
        Select a face closest to a landmark on the entity (in UI).
        """

        print(
            "select_face_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
