# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import PartTestInterface

class PartTest(TestProviderCase, PartTestInterface):
    
    @skip("TODO")
    def test_create_cube(self):
        instance = Part("")

        value = instance.create_cube("width","length","height","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_cone(self):
        instance = Part("")

        value = instance.create_cone("radius","height","draft_radius","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_cylinder(self):
        instance = Part("")

        value = instance.create_cylinder("radius","height","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_torus(self):
        instance = Part("")

        value = instance.create_torus("inner_radius","outer_radius","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_sphere(self):
        instance = Part("")

        value = instance.create_sphere("radius","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_gear(self):
        instance = Part("")

        value = instance.create_gear("outer_radius","addendum","inner_radius","dedendum","height","pressure_angle","number_of_teeth","skew_angle","conical_angle","crown_angle","keyword_arguments")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_clone(self):
        instance = Part("")

        value = instance.clone("new_name","copy_landmarks")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_loft(self):
        instance = Part("")

        value = instance.loft("landmark1","landmark2")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_union(self):
        instance = Part("")

        value = instance.union("with_part","delete_after_union","is_transfer_landmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_subtract(self):
        instance = Part("")

        value = instance.subtract("with_part","delete_after_subtract","is_transfer_landmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_intersect(self):
        instance = Part("")

        value = instance.intersect("with_part","delete_after_intersect","is_transfer_landmarks")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_hollow(self):
        instance = Part("")

        value = instance.hollow("thickness_x","thickness_y","thickness_z","start_axis","flip_axis")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_thicken(self):
        instance = Part("")

        value = instance.thicken("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_hole(self):
        instance = Part("")

        value = instance.hole("hole_landmark","radius","depth","normal_axis","flip_axis","initial_rotation_x","initial_rotation_y","initial_rotation_z","mirror_about_entity_or_landmark","mirror_axis","mirror","circular_pattern_instance_count","circular_pattern_instance_separation","circular_pattern_instance_axis","circular_pattern_about_entity_or_landmark","linear_pattern_instance_count","linear_pattern_instance_separation","linear_pattern_instance_axis","linear_pattern2nd_instance_count","linear_pattern2nd_instance_separation","linear_pattern2nd_instance_axis")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_set_material(self):
        instance = Part("")

        value = instance.set_material("material_name")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_is_colliding_with_part(self):
        instance = Part("")

        value = instance.is_colliding_with_part("other_part")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_fillet_all_edges(self):
        instance = Part("")

        value = instance.fillet_all_edges("radius","use_width")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_fillet_edges(self):
        instance = Part("")

        value = instance.fillet_edges("radius","landmarks_near_edges","use_width")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_fillet_faces(self):
        instance = Part("")

        value = instance.fillet_faces("radius","landmarks_near_faces","use_width")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamfer_all_edges(self):
        instance = Part("")

        value = instance.chamfer_all_edges("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamfer_edges(self):
        instance = Part("")

        value = instance.chamfer_edges("radius","landmarks_near_edges")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_chamfer_faces(self):
        instance = Part("")

        value = instance.chamfer_faces("radius","landmarks_near_faces")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_select_vertex_near_landmark(self):
        instance = Part("")

        value = instance.select_vertex_near_landmark("landmark_name")

        
    @skip("TODO")
    def test_select_edge_near_landmark(self):
        instance = Part("")

        value = instance.select_edge_near_landmark("landmark_name")

        
    @skip("TODO")
    def test_select_face_near_landmark(self):
        instance = Part("")

        value = instance.select_face_near_landmark("landmark_name")

        