# THIS IS AN AUTO-GENERATE FILE. 
# DO NOT EDIT MANUALLY.
# Please run development/capabilitiesJsonToPython/capabilitiesToPy.sh to generate this file.

# testsSample will implement these interfaces - this ensures that as capabilities.json is updated, tests are up to date as well.

from unittest import skip

from .test_helper import *
from codetocad.tests_interfaces import SketchTestInterface

class SketchTest(TestProviderCase, SketchTestInterface):
    
    
    @skip("TODO")
    def test_clone(self):
        instance = Sketch("name","curve_type","description")

        value = instance.clone("new_name","copy_landmarks")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_revolve(self):
        instance = Sketch("name","curve_type","description")

        value = instance.revolve("angle","about_entity_or_landmark","axis")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_extrude(self):
        instance = Sketch("name","curve_type","description")

        value = instance.extrude("length")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_sweep(self):
        instance = Sketch("name","curve_type","description")

        value = instance.sweep("profile_name_or_instance","fill_cap")

        
        assert value, "Get method failed."
        
    @skip("TODO")
    def test_offset(self):
        instance = Sketch("name","curve_type","description")

        value = instance.offset("radius")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_profile(self):
        instance = Sketch("name","curve_type","description")

        value = instance.profile("profile_curve_name")

        
        assert value, "Modify method failed."
        
    @skip("TODO")
    def test_create_text(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_text("text","font_size","bold","italic","underlined","character_spacing","word_spacing","line_spacing","font_file_path")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_from_vertices(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_from_vertices("coordinates","interpolation")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_point(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_point("coordinate")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_line(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_line("length","angle_x","angle_y","symmetric")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_line_between_points(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_line_between_points("end_at","start_at")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_circle(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_circle("radius")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_ellipse(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_ellipse("radius_a","radius_b")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_arc(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_arc("radius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_arc_between_three_points(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_arc_between_three_points("point_a","point_b","center_point")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_segment(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_segment("inner_radius","outer_radius","angle")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_rectangle(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_rectangle("length","width")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_polygon(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_polygon("number_of_sides","length","width")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_trapezoid(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_trapezoid("length_upper","length_lower","height")

        
        assert value.isExists(), "Create method failed."
        
    @skip("TODO")
    def test_create_spiral(self):
        instance = Sketch("name","curve_type","description")

        value = instance.create_spiral("number_of_turns","height","radius","is_clockwise","radius_end")

        
        assert value.isExists(), "Create method failed."
        