# THIS IS AN AUTO-GENERATE FILE.
# DO NOT EDIT MANUALLY.
# Please run development/capabilities_json_to_python/capabilities_to_py.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from abc import ABCMeta, abstractmethod


class PartTestInterface(metaclass=ABCMeta):

    @abstractmethod
    def test_create_cube(self):

        pass

    @abstractmethod
    def test_create_cone(self):

        pass

    @abstractmethod
    def test_create_cylinder(self):

        pass

    @abstractmethod
    def test_create_torus(self):

        pass

    @abstractmethod
    def test_create_sphere(self):

        pass

    @abstractmethod
    def test_create_gear(self):

        pass

    @abstractmethod
    def test_create_text(self):

        pass

    @abstractmethod
    def test_clone(self):

        pass

    @abstractmethod
    def test_hollow(self):

        pass

    @abstractmethod
    def test_thicken(self):

        pass

    @abstractmethod
    def test_hole(self):

        pass

    @abstractmethod
    def test_twist(self):

        pass

    @abstractmethod
    def test_set_material(self):

        pass

    @abstractmethod
    def test_is_colliding_with_part(self):

        pass

    @abstractmethod
    def test_fillet_all_edges(self):

        pass

    @abstractmethod
    def test_fillet_edges(self):

        pass

    @abstractmethod
    def test_fillet_faces(self):

        pass

    @abstractmethod
    def test_chamfer_all_edges(self):

        pass

    @abstractmethod
    def test_chamfer_edges(self):

        pass

    @abstractmethod
    def test_chamfer_faces(self):

        pass

    @abstractmethod
    def test_select_vertex_near_landmark(self):

        pass

    @abstractmethod
    def test_select_edge_near_landmark(self):

        pass

    @abstractmethod
    def test_select_face_near_landmark(self):

        pass
