# This file was forked from codetocad/TestCodeToCADProvider.py

import unittest

from mock.modeling.mock_modeling_provider import (
    reset_mock_modeling_provider,
    inject_mock_modeling_provider,
)

from codetocad import *
from codetocad.utilities import Dimension, center, max, min
from providers.blender.blender_provider import *


def injectMockProvider():
    reset_mock_modeling_provider()
    inject_mock_modeling_provider(globals())


class TestProviderCase(unittest.TestCase):
    def setUp(self) -> None:
        injectMockProvider()
        super().setUp()


class TestEntity(TestProviderCase):
    def test_is_exists(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.is_exists()

        assert value, "Get method failed."

    def test_rename(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.rename("newName", True)

        renamedPart = Part("newName")

        assert value.name == renamedPart.name, "Modify method failed."

        # TODO: test for renamelinkedEntitiesAndLandmarks = False. This is blocked by landmarking implementation

    def test_delete(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.is_exists()

        assert value, "Expected True, got False"

        value = instance.delete(False)

        value = instance.is_exists()

        assert not value, "Expected False, got True"

        # TODO: test for remove_children = True

    def test_is_visible(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.is_visible()

        assert value, "Get method failed."

    def test_set_visible(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.set_visible(True)

        assert value.is_visible() is True, "Expected False, got True"

        value = instance.set_visible(False)

        assert value.is_visible() is False, "Expected True, got False"

    @unittest.skip(
        "Blocked by understanding the consequences of implementating this capability."
    )
    def test_apply(self):
        instance = Part("name", "description")

        value = instance.apply()

        assert value, "Modify method failed."

    def test_get_native_instance(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.get_native_instance()

        assert value, "Get method failed."

    def test_get_location_world(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.get_location_world()

        assert (
            value.x == "0m" and value.y == "0m" and value.z == "0m"
        ), "Get method failed."

        # TODO: get location world after translating

    def test_get_location_local(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.get_location_world()

        assert (
            value.x == "0m" and value.y == "0m" and value.z == "0m"
        ), "Get method failed."

        # TODO: get location world after translating

    @unittest.skip("Not yet implemented")
    def test_select(self):
        instance = Part("name", "description")

        instance.select()

    def test_export(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.export("filePath.stl", True, 1.0)

        # no extension:
        self.assertRaises(
            AssertionError, lambda: instance.export("filePath", True, 1.0)
        )

        # bad extension:
        self.assertRaises(
            AssertionError,
            lambda: instance.export("filePath.NotARealExtension", True, 1.0),
        )

        # TODO: Test file absolute path resolution
        # TODO: Test export scale
        # TODO: Test overwriting

    def test_clone(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.clone("newName", False)

        assert instance.is_exists(), "The original object should still exist."

        assert instance.name != value.name, "Clone should return the cloned Entity."

        assert Part("newName").is_exists(), "Clone method failed."

        # TODO: test copyLandmarks parameter

    def test_mirror(self):
        partToMirror = (
            Part("partToMirror", "description").create_cube(1, 1, 1).translate_x(-5)
        )
        partToMirrorAcross = Part("partToMirrorAcross", "description").create_cube(
            1, 1, 1
        )

        value = partToMirror.mirror(partToMirrorAcross, "x", None)

        assert value.is_exists(), "Create method failed."

        # TODO: add test for bad mirrorAcrossEntity name
        # TODO: add test for bad axis name
        # TODO: add test for supplying resulting_mirrored_entity_name
        # TODO: add test to make sure mirrored object is really mirrored across the intended axis and distance

    def test_linear_pattern(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.linear_pattern(2, "2m")

        assert value.is_exists(), "Modify method failed."

        # TODO: make sure patterning works on all axes correctly

    def test_circular_pattern(self):
        partToPattern = (
            Part("partToPattern", "description").create_cube(1, 1, 1).translate_x(-5)
        )
        centerPart = Part("centerPart", "description").create_cube(1, 1, 1)

        value = partToPattern.circular_pattern(4, 90, centerPart)

        assert value.is_exists(), "Modify method failed."

        # TODO: make sure Entity, Landmark and string name all work correctly.
        # TODO: make sure patterning works on all axes correctly

    def test_translate_xyz(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.translate_xyz(5, 7, 9)

        assert value, "Modify method failed."

        assert instance.get_location_world() == Point(
            Dimension(5, "m"), Dimension(7, "m"), Dimension(9, "m")
        ), "Translation is not correct"

    def test_translate_x(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.translate_x(5)

        assert value, "Modify method failed."

        assert instance.get_location_world() == Point(
            Dimension(5, "m"), Dimension(0, "m"), Dimension(0, "m")
        ), "Translation is not correct"

    def test_translate_y(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.translate_y(5)

        assert value, "Modify method failed."

        assert instance.get_location_world() == Point(
            Dimension(0, "m"), Dimension(5, "m"), Dimension(0, "m")
        ), "Translation is not correct"

    def test_translate_z(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.translate_z(5)

        assert value, "Modify method failed."

        assert instance.get_location_world() == Point(
            Dimension(0, "m"), Dimension(0, "m"), Dimension(5, "m")
        ), "Translation is not correct"

    def test_scale_xyz(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_xyz(5, 7, 9)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 5
            and dimensions.y.value == 7
            and dimensions.z.value == 9
        ), "Modify method failed."

    def test_scale_x(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_x(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 5
            and dimensions.y.value == 1
            and dimensions.z.value == 1
        ), "Modify method failed."

    def test_scale_y(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_y(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 1
            and dimensions.y.value == 5
            and dimensions.z.value == 1
        ), "Modify method failed."

    def test_scale_z(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_z(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 1
            and dimensions.y.value == 1
            and dimensions.z.value == 5
        ), "Modify method failed."

    def test_scale_x_by_factor(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_x_by_factor(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 5
            and dimensions.y.value == 1
            and dimensions.z.value == 1
        ), "Modify method failed."

    def test_scale_y_by_factor(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_y_by_factor(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 1
            and dimensions.y.value == 5
            and dimensions.z.value == 1
        ), "Modify method failed."

    def test_scale_z_by_factor(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_z_by_factor(5)

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 1
            and dimensions.y.value == 1
            and dimensions.z.value == 5
        ), "Modify method failed."

    def test_scale_keep_aspect_ratio(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        instance.scale_keep_aspect_ratio(5, "x")

        dimensions = instance.get_dimensions()

        assert (
            dimensions.x.value == 5
            and dimensions.y.value == 5
            and dimensions.z.value == 5
        ), "Modify method failed."

    def test_rotate_xyz(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.rotate_xyz(45, 45, 45)

        assert value, "Modify method failed."
        # TODO: check the rotation value

    def test_rotate_x(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.rotate_x(45)

        assert value, "Modify method failed."

    def test_rotate_y(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.rotate_y(45)

        assert value, "Modify method failed."

    def test_rotate_z(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.rotate_z(45)

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_twist(self):
        instance = Part("name", "description")

        value = instance.twist("angle", "screwPitch", "iterations", "axis")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_remesh(self):
        instance = Part("name", "description")

        value = instance.remesh("strategy", "amount")

        assert value, "Modify method failed."

    def test_create_landmark(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.create_landmark("landmarkName", 0, 0, 0)

        assert value, "Modify method failed."

        landmark = instance.get_landmark("landmarkName")

        assert landmark.is_exists(), "Landmark was not created."

    def test_get_bounding_box(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.get_bounding_box()

        assert value, "Get method failed."
        assert value.x.center == 0.0
        assert value.y.center == 0.0
        assert value.z.center == 0.0
        assert value.x.min == -0.5
        assert value.x.max == 0.5
        assert value.y.min == -0.5
        assert value.y.max == 0.5
        assert value.z.min == -0.5
        assert value.z.max == 0.5

    def test_get_dimensions(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        value = instance.get_dimensions()

        assert value, "Get method failed."
        assert value.height == "1m"
        assert value.width == "1m"
        assert value.length == "1m"

    def test_get_landmark(self):
        instance = Part("name", "description").create_cube(1, 1, 1)

        # test creating and getting a landmark
        instance.create_landmark("landmarkName", max, max, max)
        value = instance.get_landmark("landmarkName")
        assert value, "Get method failed."
        valueLocation = value.get_location_world()
        assert valueLocation.x == "0.5m"
        assert valueLocation.y == "0.5m"
        assert valueLocation.z == "0.5m"

        # test landmark that doesn't exist
        try:
            value = instance.get_landmark("landmarkThatDoesNotExist")
            assert value is None, "Got a ghost landmark."
        except:  # noqa:E722
            pass

        # test preset landmark from_string
        value = instance.get_landmark("leftTop")
        assert value, "Get method failed."
        valueLocation = value.get_location_world()
        assert valueLocation.x == "-0.5m"
        assert valueLocation.y == "0.0m"
        assert valueLocation.z == "0.5m"

        # test preset landmark PresetLandmarks
        value = instance.get_landmark(PresetLandmark.leftTop)
        assert value, "Get method failed."
        valueLocation = value.get_location_world()
        assert valueLocation.x == "-0.5m"
        assert valueLocation.y == "0.0m"
        assert valueLocation.z == "0.5m"


class TestPart(TestProviderCase):
    @unittest.skip("")
    def test_create_from_file(self):
        instance = Part("TestPart")

        import pathlib

        value = instance.create_from_file(
            f"{pathlib.Path(__file__).parent}/../examples/importableCube.stl"
        )

        assert value.is_exists(), "Create method failed."

    def test_create_cube(self):
        instance = Part("TestPart")

        value = instance.create_cube(1, 1, 1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createCone(self):
        instance = Part("TestPart")

        value = instance.createCone(1, 1, 1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_cylinder(self):
        instance = Part("TestPart")

        value = instance.create_cylinder(1, 1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_torus(self):
        instance = Part("TestPart")

        value = instance.create_torus(0.5, 1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_sphere(self):
        instance = Part("TestPart")

        value = instance.create_sphere(1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_gear(self):
        instance = Part("TestPart")

        value = instance.create_gear(1, 1, 1, 1, 1)

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_loft(self):
        instance = Part("TestPart")

        value = instance.loft("Landmark1", "Landmark2")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_union(self):
        instance = Part("TestPart")

        value = instance.union(
            "withPart", "delete_after_union", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_subtract(self):
        instance = Part("TestPart")

        value = instance.subtract(
            "withPart", "delete_after_subtract", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_intersect(self):
        instance = Part("TestPart")

        value = instance.intersect(
            "withPart", "delete_after_intersect", "is_transfer_landmarks"
        )

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_hollow(self):
        instance = Part("TestPart").create_cube(1, 1, 1)

        value = instance.hollow("20cm", 0.2, 0.2, "z", False)

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_thicken(self):
        instance = Part("")

        value = instance.thicken("radius")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_hole(self):
        instance = Part("TestPart")

        value = instance.hole(
            "holeLandmark",
            "radius",
            "depth",
            "normal_axis",
            False,
            "initialRotationX",
            "initialRotationY",
            "initialRotationZ",
            "mirrorAboutEntityOrLandmark",
            "mirrorAxis",
            False,
            1,
            "circular_patternInstanceSeparation",
            "circular_patternInstanceAxis",
            "circular_patternAboutEntityOrLandmark",
            1,
            "linear_patternInstanceSeparation",
            "linear_patternInstanceAxis",
        )

        assert value, "Modify method failed."

    def test_set_material(self):
        instance = Part("TestPart").create_cube(1, 1, 1)

        value = instance.set_material("materialName")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_isCollidingWithPart(self):
        instance = Part("TestPart")

        value = instance.isCollidingWithPart("otherPart")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_fillet_all_edges(self):
        instance = Part("TestPart")

        value = instance.fillet_all_edges("radius", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_fillet_edges(self):
        instance = Part("TestPart")

        value = instance.fillet_edges("radius", "landmarksNearEdges", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_fillet_faces(self):
        instance = Part("TestPart")

        value = instance.fillet_faces("radius", "landmarksNearFaces", "useWidth")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_chamfer_all_edges(self):
        instance = Part("TestPart")

        value = instance.chamfer_all_edges("radius")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_chamfer_edges(self):
        instance = Part("TestPart")

        value = instance.chamfer_edges("radius", "landmarksNearEdges")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_chamfer_faces(self):
        instance = Part("TestPart")

        value = instance.chamfer_faces("radius", "landmarksNearFaces")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_selectVertexNearLandmark(self):
        instance = Part("TestPart")

        instance.selectVertexNearLandmark("landmarkName")

    @unittest.skip("")
    def test_selectEdgeNearLandmark(self):
        instance = Part("TestPart")

        instance.selectEdgeNearLandmark("landmarkName")

    @unittest.skip("")
    def test_selectFaceNearLandmark(self):
        instance = Part("TestPart")

        instance.selectFaceNearLandmark("landmarkName")


class TestSketch(TestProviderCase):
    @unittest.skip("")
    def test_revolve(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.revolve("angle", "aboutEntityOrLandmark", "axis")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_offset(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.offset("radius")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_extrude(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.extrude("length", "convertToMesh")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_sweep(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.sweep("profileNameOrInstance", "fillCap")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_create_text(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_text(
            "text",
            "font_size",
            "bold",
            "italic",
            "underlined",
            "characterSpacing",
            "wordSpacing",
            "lineSpacing",
            "font_file_path",
        )

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_from_vertices(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_from_vertices("points", "interpolation")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_point(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_point("point")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_line(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_line("length", "angleX", "angleY", "symmetric")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_lineBetweenPoints(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_lineBetweenPoints("endAt", "startAt")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_circle(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_circle("radius")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_ellipse(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_ellipse("radiusA", "radiusB")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_arc(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_arc("radius", "angle")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_arcBetweenThreePoints(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_arcBetweenThreePoints("pointA", "pointB", "centerPoint")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createSegment(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createSegment("innerRadius", "outerRadius", "angle")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createRectangle(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createRectangle("length", "width")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_polygon(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_polygon("numberOfSides", "length", "width")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createTrapezoid(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.createTrapezoid("lengthUpper", "lengthLower", "height")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_spiral(self):
        instance = Sketch("name", "curveType", "description")

        value = instance.create_spiral(
            "numberOfTurns", "height", "radius", "isClockwise", "radiusEnd"
        )

        assert value.is_exists(), "Create method failed."


class TestLandmark(TestProviderCase):
    @unittest.skip("")
    def test_get_landmark_entity_name(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.get_landmark_entity_name("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_parent_entity(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.get_parent_entity("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_is_exists(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.is_exists("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_rename(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.rename("newName", "renamelinkedEntitiesAndLandmarks")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_delete(self):
        instance = Landmark("name", "parentEntity", "description")

        instance.delete("remove_children")

    @unittest.skip("")
    def test_is_visible(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.is_visible("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_set_visible(self):
        instance = Landmark("name", "parentEntity", "description")

        instance.set_visible("is_visible")

    @unittest.skip("")
    def test_get_native_instance(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_world(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_local(self):
        instance = Landmark("name", "parentEntity", "description")

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_select(self):
        instance = Landmark("name", "parentEntity", "description")

        instance.select("landmarkName", "selectionType")


class TestJoint(TestProviderCase):
    @unittest.skip("")
    def test_translate_landmark_onto_another(self):
        instance = Joint("entity1", "entity2")

        value = instance.translate_landmark_onto_another("")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_pivot(self):
        instance = Joint("entity1", "entity2")

        value = instance.pivot("")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_gearRatio(self):
        instance = Joint("entity1", "entity2")

        value = instance.gearRatio("ratio")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_location_xyz(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_location_xyz("x", "y", "z")

        assert value, "Modify method failed."

    def test_limit_location_x(self):
        partA = (
            Part("A").create_cube(1, 1, 1).create_landmark("top", center, center, max)
        )
        partB = (
            Part("B")
            .create_cube(1, 1, 1)
            .create_landmark("bottom", center, center, min)
        )

        joint = Joint(partA, partB)

        value = joint.limit_location_x(0, 0)

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_location_y(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_location_y("min", "max")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_location_z(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_location_z("min", "max")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_rotation_xyz(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_rotation_xyz("x", "y", "z")

        assert value, "Modify method failed."

    def test_limit_rotation_x(self):
        partA = (
            Part("A").create_cube(1, 1, 1).create_landmark("top", center, center, max)
        )
        partB = (
            Part("B")
            .create_cube(1, 1, 1)
            .create_landmark("bottom", center, center, min)
        )

        joint = Joint(partA, partB)

        value = joint.limit_rotation_x(0, 0)

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_rotation_y(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_rotation_y("min", "max")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_limit_rotation_z(self):
        instance = Joint("entity1", "entity2")

        value = instance.limit_rotation_z("min", "max")

        assert value, "Modify method failed."


class TestMaterial(TestProviderCase):
    @unittest.skip("")
    def test_assign_to_part(self):
        instance = Material("name", "description")

        value = instance.assign_to_part("partName")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_set_color(self):
        instance = Material("name", "description")

        value = instance.set_color("rValue", "gValue", "bValue", "aValue")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_set_reflectivity(self):
        instance = Material("name", "description")

        value = instance.set_reflectivity("reflectivity")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setRoughness(self):
        instance = Material("name", "description")

        value = instance.setRoughness("roughness")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_set_image_texture(self):
        instance = Material("name", "description")

        value = instance.set_image_texture("imageFilePath")

        assert value, "Modify method failed."


class TestAnimation(TestProviderCase):
    @unittest.skip("")
    def test_setFrameStart(self):
        instance = Animation("")

        value = instance.setFrameStart("frameNumber")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setFrameEnd(self):
        instance = Animation("")

        value = instance.setFrameEnd("frameNumber")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setFrameCurrent(self):
        instance = Animation("")

        value = instance.setFrameCurrent("frameNumber")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_createKeyFrameLocation(self):
        instance = Animation("")

        instance.createKeyFrameLocation("entity", "frameNumber")

    @unittest.skip("")
    def test_createKeyFrameRotation(self):
        instance = Animation("")

        instance.createKeyFrameRotation("entity", "frameNumber")


class TestLight(TestProviderCase):
    @unittest.skip("")
    def test_set_color(self):
        instance = Light("name", "description")

        value = instance.set_color("rValue", "gValue", "bValue")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_create_sun(self):
        instance = Light("name", "description")

        value = instance.create_sun("energyLevel")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createSpot(self):
        instance = Light("name", "description")

        value = instance.createSpot("energyLevel")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_create_point(self):
        instance = Light("name", "description")

        value = instance.create_point("energyLevel")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createArea(self):
        instance = Light("name", "description")

        value = instance.createArea("energyLevel")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_translate_xyz(self):
        instance = Light("name", "description")

        value = instance.translate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_rotate_xyz(self):
        instance = Light("name", "description")

        value = instance.rotate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_is_exists(self):
        instance = Light("name", "description")

        value = instance.is_exists("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_rename(self):
        instance = Light("name", "description")

        value = instance.rename("newName", "renamelinkedEntitiesAndLandmarks")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_delete(self):
        instance = Light("name", "description")

        instance.delete("remove_children")

    @unittest.skip("")
    def test_get_native_instance(self):
        instance = Light("name", "description")

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_world(self):
        instance = Light("name", "description")

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_local(self):
        instance = Light("name", "description")

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_select(self):
        instance = Light("name", "description")

        instance.select("")


class TestCamera(TestProviderCase):
    @unittest.skip("")
    def test_create_perspective(self):
        instance = Camera("name", "description")

        value = instance.create_perspective("")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_createOrthogonal(self):
        instance = Camera("name", "description")

        value = instance.createOrthogonal("")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_set_focal_length(self):
        instance = Camera("name", "description")

        value = instance.set_focal_length("length")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_translate_xyz(self):
        instance = Camera("name", "description")

        value = instance.translate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_rotate_xyz(self):
        instance = Camera("name", "description")

        value = instance.rotate_xyz("x", "y", "z")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_is_exists(self):
        instance = Camera("name", "description")

        value = instance.is_exists("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_rename(self):
        instance = Camera("name", "description")

        value = instance.rename("newName", "renamelinkedEntitiesAndLandmarks")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_delete(self):
        instance = Camera("name", "description")

        instance.delete("remove_children")

    @unittest.skip("")
    def test_get_native_instance(self):
        instance = Camera("name", "description")

        value = instance.get_native_instance("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_world(self):
        instance = Camera("name", "description")

        value = instance.get_location_world("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_location_local(self):
        instance = Camera("name", "description")

        value = instance.get_location_local("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_select(self):
        instance = Camera("name", "description")

        instance.select("")


class TestRender(TestProviderCase):
    @unittest.skip("")
    def test_renderImage(self):
        instance = Render("")

        instance.renderImage("outputFilePath", "overwrite", "fileType")

    @unittest.skip("")
    def test_renderVideoMp4(self):
        instance = Render("")

        instance.renderVideoMp4(
            "outputFilePath",
            "startFrameNumber",
            "endFrameNumber",
            "stepFrames",
            "overwrite",
        )

    @unittest.skip("")
    def test_renderVideoFrames(self):
        instance = Render("")

        instance.renderVideoFrames(
            "outputFolderPath",
            "fileNamePrefix",
            "startFrameNumber",
            "endFrameNumber",
            "stepFrames",
            "overwrite",
            "fileType",
        )

    @unittest.skip("")
    def test_setFrameRate(self):
        instance = Render("")

        value = instance.setFrameRate("frameRate")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setResolution(self):
        instance = Render("")

        value = instance.setResolution("x", "y")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setRenderQuality(self):
        instance = Render("")

        value = instance.setRenderQuality("quality")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setRenderEngine(self):
        instance = Render("")

        value = instance.setRenderEngine("name")

        assert value, "Modify method failed."

    @unittest.skip("")
    def test_setCamera(self):
        instance = Render("")

        value = instance.setCamera("cameraNameOrInstance")

        assert value, "Modify method failed."


class TestScene(TestProviderCase):
    @unittest.skip("")
    def test_create(self):
        instance = Scene("name", "description")

        value = instance.create("")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_delete(self):
        instance = Scene("name", "description")

        instance.delete("")

    @unittest.skip("")
    def test_getSelectedEntity(self):
        instance = Scene("name", "description")

        value = instance.get_selected_entity("")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_export(self):
        instance = Scene("name", "description")

        instance.export("filePath", "entities", "overwrite", "scale")

    @unittest.skip("")
    def test_set_default_unit(self):
        instance = Scene("name", "description")

        instance.set_default_unit("unit")

    @unittest.skip("")
    def test_create_group(self):
        instance = Scene("name", "description")

        instance.create_group("name")

        assert value.is_exists(), "Create method failed."

    @unittest.skip("")
    def test_deleteGroup(self):
        instance = Scene("name", "description")

        instance.deleteGroup("name", "remove_children")

    @unittest.skip("")
    def test_removeFromGroup(self):
        instance = Scene("name", "description")

        instance.removeFromGroup("entityName", "groupName")

    @unittest.skip("")
    def test_assign_to_group(self):
        instance = Scene("name", "description")

        instance.assign_to_group("entities", "groupName", "removeFromOtherGroups")

    @unittest.skip("")
    def test_set_visible(self):
        instance = Scene("name", "description")

        instance.set_visible("entities", "is_visible")


class TestAnalytics(TestProviderCase):
    @unittest.skip("")
    def test_measureDistance(self):
        instance = Analytics("")

        value = instance.measureDistance("entity1", "entity2")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_measureAngle(self):
        instance = Analytics("")

        value = instance.measureAngle("entity1", "entity2", "pivot")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_getWorldPose(self):
        instance = Analytics("")

        value = instance.getWorldPose("entity")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_bounding_box(self):
        instance = Analytics("")

        value = instance.get_bounding_box("entityName")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_get_dimensions(self):
        instance = Analytics("")

        value = instance.get_dimensions("entityName")

        assert value, "Get method failed."

    @unittest.skip("")
    def test_log(self):
        instance = Analytics("")

        value = instance.log("message")

        assert value, "Get method failed."
