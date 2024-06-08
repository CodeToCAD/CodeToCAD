# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

from abc import ABCMeta, abstractmethod


from codetocad.codetocad_types import *

from typing import Self


from codetocad.interfaces.landmark_interface import LandmarkInterface

from codetocad.interfaces.material_interface import MaterialInterface

from codetocad.interfaces.importable_interface import ImportableInterface

from codetocad.interfaces.exportable_interface import ExportableInterface

from codetocad.interfaces.subdividable_interface import SubdividableInterface

from codetocad.interfaces.scalable_interface import ScalableInterface

from codetocad.interfaces.landmarkable_interface import LandmarkableInterface

from codetocad.interfaces.mirrorable_interface import MirrorableInterface

from codetocad.interfaces.booleanable_interface import BooleanableInterface

from codetocad.interfaces.patternable_interface import PatternableInterface

from codetocad.interfaces.entity_interface import EntityInterface


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
        width: "str|float|Dimension",
        length: "str|float|Dimension",
        height: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
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
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        draft_radius: "str|float|Dimension" = 0,
        options: "PartOptions| None" = None,
    ) -> Self:
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
        radius: "str|float|Dimension",
        height: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
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
        inner_radius: "str|float|Dimension",
        outer_radius: "str|float|Dimension",
        options: "PartOptions| None" = None,
    ) -> Self:
        """
        Adds torus geometry to a part.
        """

        print(
            "create_torus is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def create_sphere(
        self, radius: "str|float|Dimension", options: "PartOptions| None" = None
    ) -> Self:
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
        outer_radius: "str|float|Dimension",
        addendum: "str|float|Dimension",
        inner_radius: "str|float|Dimension",
        dedendum: "str|float|Dimension",
        height: "str|float|Dimension",
        pressure_angle: "str|float|Angle" = "20d",
        number_of_teeth: "int" = 12,
        skew_angle: "str|float|Angle" = 0,
        conical_angle: "str|float|Angle" = 0,
        crown_angle: "str|float|Angle" = 0,
        options: "PartOptions| None" = None,
    ) -> Self:
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
        thickness_x: "str|float|Dimension",
        thickness_y: "str|float|Dimension",
        thickness_z: "str|float|Dimension",
        start_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
    ) -> Self:
        """
        Remove vertices, if necessary, until the part has a specified wall thickness.
        """

        print("hollow is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def thicken(self, radius: "str|float|Dimension") -> Self:
        """
        Uniformly add a wall around a Part.
        """

        print("thicken is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def hole(
        self,
        hole_landmark: "str|LandmarkInterface",
        radius: "str|float|Dimension",
        depth: "str|float|Dimension",
        normal_axis: "str|int|Axis" = "z",
        flip_axis: "bool" = False,
        initial_rotation_x: "str|float|Angle" = 0.0,
        initial_rotation_y: "str|float|Angle" = 0.0,
        initial_rotation_z: "str|float|Angle" = 0.0,
        mirror_about_entity_or_landmark: "str|EntityInterface| None" = None,
        mirror_axis: "str|int|Axis" = "x",
        mirror: "bool" = False,
        circular_pattern_instance_count: "int" = 1,
        circular_pattern_instance_separation: "str|float|Angle" = 0.0,
        circular_pattern_instance_axis: "str|int|Axis" = "z",
        circular_pattern_about_entity_or_landmark: "str|EntityInterface| None" = None,
        linear_pattern_instance_count: "int" = 1,
        linear_pattern_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern_instance_axis: "str|int|Axis" = "x",
        linear_pattern2nd_instance_count: "int" = 1,
        linear_pattern2nd_instance_separation: "str|float|Dimension" = 0.0,
        linear_pattern2nd_instance_axis: "str|int|Axis" = "y",
    ) -> Self:
        """
        Create a hole.
        """

        print("hole is called in an abstract method. Please override this method.")

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
        AKA Helix, Screw. Revolve an entity
        """

        print("twist is called in an abstract method. Please override this method.")

        raise NotImplementedError()

    @abstractmethod
    def set_material(self, material_name: "str|MaterialInterface") -> Self:
        """
        Assign a known material to this part.
        """

        print(
            "set_material is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def is_colliding_with_part(self, other_part: "str|PartInterface") -> "bool":
        """
        Check if this part is colliding with another.
        """

        print(
            "is_colliding_with_part is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def fillet_all_edges(
        self, radius: "str|float|Dimension", use_width: "bool" = False
    ) -> Self:
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
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ) -> Self:
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
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
        use_width: "bool" = False,
    ) -> Self:
        """
        Fillet specific faces.
        """

        print(
            "fillet_faces is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def chamfer_all_edges(self, radius: "str|float|Dimension") -> Self:
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
        radius: "str|float|Dimension",
        landmarks_near_edges: "list[str|LandmarkInterface]",
    ) -> Self:
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
        radius: "str|float|Dimension",
        landmarks_near_faces: "list[str|LandmarkInterface]",
    ) -> Self:
        """
        Chamfer specific faces.
        """

        print(
            "chamfer_faces is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_vertex_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        """
        Select the vertex closest to a Landmark on the entity (in UI).
        """

        print(
            "select_vertex_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_edge_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        """
        Select an edge closest to a landmark on the entity (in UI).
        """

        print(
            "select_edge_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()

    @abstractmethod
    def select_face_near_landmark(
        self, landmark_name: "str|LandmarkInterface| None" = None
    ) -> Self:
        """
        Select a face closest to a landmark on the entity (in UI).
        """

        print(
            "select_face_near_landmark is called in an abstract method. Please override this method."
        )

        raise NotImplementedError()
