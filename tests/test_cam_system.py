"""
Comprehensive tests for the CAM system.

This test suite validates the CAM interfaces, tool presets, and adapter implementations.
"""

import unittest
import tempfile
import os
from pathlib import Path

# Core CAM imports
from codetocad.core.cam.tool import Tool
from codetocad.core.cam.toolpath import Toolpath
from codetocad.core.cam.tool_library import ToolLibrary

# Interface imports
from codetocad.interfaces.cam.tool_interface import (
    ToolType,
    ToolMaterial,
    ToolGeometry,
    CuttingData,
)
from codetocad.interfaces.cam.toolpath_interface import (
    ToolpathStrategy,
    ToolpathOperation,
    CuttingParameters,
    ToolpathPoint,
)
from codetocad.interfaces.cam.work_coordinate_system_interface import (
    WCSOrigin,
    CoordinateSystem,
    WorkpieceSetup,
)


class TestCAMToolSystem(unittest.TestCase):
    """Test the CAM tool system including presets."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = Tool()

    def test_tool_creation(self):
        """Test basic tool creation and configuration."""
        self.tool.set_name("Test End Mill")
        self.tool.set_tool_number(1)
        self.tool.tool_type = ToolType.FLAT_END_MILL
        self.tool.material = ToolMaterial.CARBIDE

        # Set geometry
        geometry = ToolGeometry(
            diameter=6.0,
            length=60.0,
            cutting_length=20.0,
            shank_diameter=6.0,
            flute_count=2,
        )
        self.tool.set_geometry(geometry)

        # Set cutting data
        cutting_data = CuttingData(
            spindle_speed=18000,
            feed_rate=1800,
            plunge_rate=450,
            step_over=0.5,
            step_down=1.5,
        )
        self.tool.set_cutting_data(cutting_data)

        # Validate tool
        issues = self.tool.validate()
        self.assertEqual(len(issues), 0, f"Tool validation failed: {issues}")

        # Test calculations
        chip_load = self.tool.calculate_chip_load()
        self.assertIsNotNone(chip_load)
        self.assertGreater(chip_load, 0)

        surface_speed = self.tool.calculate_surface_speed()
        self.assertIsNotNone(surface_speed)
        self.assertGreater(surface_speed, 0)

    def test_tool_presets(self):
        """Test tool preset system."""
        # Test end mill presets
        end_mill = Tool.preset.end_mill.flat_carbide_6mm()
        self.assertEqual(end_mill.name, "6mm Carbide Flat End Mill")
        self.assertEqual(end_mill.tool_type, ToolType.FLAT_END_MILL)
        self.assertEqual(end_mill.material, ToolMaterial.CARBIDE)
        self.assertIsNotNone(end_mill.geometry)
        self.assertEqual(end_mill.geometry.diameter, 6.0)

        # Test drill presets
        drill = Tool.preset.drill.twist_drill_hss_5mm()
        self.assertEqual(drill.tool_type, ToolType.DRILL)
        self.assertEqual(drill.material, ToolMaterial.HSS)
        self.assertEqual(drill.geometry.diameter, 5.0)

        # Test ball mill presets
        ball_mill = Tool.preset.ball_mill.ball_mill_carbide_3mm()
        self.assertEqual(ball_mill.tool_type, ToolType.BALL_END_MILL)
        self.assertEqual(ball_mill.geometry.diameter, 3.0)

        # Test V-bit presets
        v_bit = Tool.preset.v_bit.engraving_90_degree()
        self.assertEqual(v_bit.tool_type, ToolType.V_BIT)
        self.assertIsNotNone(v_bit.geometry.tip_angle)
        self.assertEqual(v_bit.geometry.tip_angle, 90.0)

    def test_tool_serialization(self):
        """Test tool serialization to/from dictionary."""
        # Create and configure tool
        tool = Tool.preset.end_mill.flat_carbide_6mm()

        # Serialize to dictionary
        tool_dict = tool.to_dict()
        self.assertIn("name", tool_dict)
        self.assertIn("tool_type", tool_dict)
        self.assertIn("geometry", tool_dict)
        self.assertIn("cutting_data", tool_dict)

        # Create new tool from dictionary
        new_tool = Tool()
        new_tool.from_dict(tool_dict)

        # Verify properties match
        self.assertEqual(new_tool.name, tool.name)
        self.assertEqual(new_tool.tool_type, tool.tool_type)
        self.assertEqual(new_tool.geometry.diameter, tool.geometry.diameter)
        self.assertEqual(
            new_tool.cutting_data.spindle_speed, tool.cutting_data.spindle_speed
        )


class TestCAMToolpathSystem(unittest.TestCase):
    """Test the CAM toolpath system."""

    def setUp(self):
        """Set up test fixtures."""
        self.toolpath = Toolpath()
        self.tool = Tool.preset.end_mill.flat_carbide_6mm()

    def test_toolpath_creation(self):
        """Test basic toolpath creation and configuration."""
        self.toolpath.set_name("Test Profile")
        self.toolpath.set_operation(ToolpathOperation.FINISHING)
        self.toolpath.set_strategy(ToolpathStrategy.PROFILE)
        self.toolpath.set_tool(self.tool)

        # Set cutting parameters
        cutting_params = CuttingParameters(
            depth_of_cut=5.0,
            step_down=1.0,
            step_over=0.5,
            feed_rate=1200,
            spindle_speed=18000,
            plunge_rate=300,
        )
        self.toolpath.set_cutting_parameters(cutting_params)

        # Validate toolpath (should pass basic validation even without points)
        issues = self.toolpath.validate()
        # Filter out "no points" issue for basic configuration test
        filtered_issues = [
            issue for issue in issues if "no points" not in issue.lower()
        ]
        self.assertEqual(
            len(filtered_issues), 0, f"Toolpath validation failed: {filtered_issues}"
        )

    def test_drilling_pattern_generation(self):
        """Test drilling pattern generation."""
        drill_tool = Tool.preset.drill.twist_drill_hss_5mm()
        self.toolpath.set_tool(drill_tool)
        self.toolpath.set_operation(ToolpathOperation.DRILLING)
        self.toolpath.set_strategy(ToolpathStrategy.DRILLING)

        # Set cutting parameters
        cutting_params = CuttingParameters(
            depth_of_cut=10.0,
            step_down=3.0,
            step_over=1.0,
            feed_rate=200,
            spindle_speed=3000,
            plunge_rate=200,
            safe_height=5.0,
            clearance_height=2.0,
        )
        self.toolpath.set_cutting_parameters(cutting_params)

        # Generate drilling pattern
        drill_points = [(0, 0), (10, 0), (10, 10), (0, 10)]
        self.toolpath.generate_drilling_pattern(drill_points, 10.0)

        # Verify toolpath was generated
        self.assertGreater(len(self.toolpath.points), 0)

        # Check that we have rapid moves to safe height
        rapid_moves = [p for p in self.toolpath.points if p.rapid_move]
        self.assertGreater(len(rapid_moves), 0)

        # Calculate statistics
        total_length = self.toolpath.get_total_length()
        self.assertGreater(total_length, 0)

        machining_time = self.toolpath.get_machining_time_estimate()
        self.assertGreater(machining_time, 0)

    def test_toolpath_optimization(self):
        """Test toolpath optimization."""
        # Create a simple toolpath with some points
        points = [
            ToolpathPoint(0, 0, 0),
            ToolpathPoint(0, 0, 0),  # Duplicate point
            ToolpathPoint(10, 0, 0),
            ToolpathPoint(10, 10, 0),
        ]
        self.toolpath.points = points

        original_count = len(self.toolpath.points)

        # Optimize toolpath
        self.toolpath.optimize_toolpath()

        # Should have removed duplicate point
        self.assertLess(len(self.toolpath.points), original_count)


class TestCAMToolLibrary(unittest.TestCase):
    """Test the CAM tool library system."""

    def setUp(self):
        """Set up test fixtures."""
        self.library = ToolLibrary()
        self.library.set_name("Test Library")

    def test_tool_library_operations(self):
        """Test basic tool library operations."""
        # Add tools to library
        tool1 = Tool.preset.end_mill.flat_carbide_6mm(tool_number=1)
        tool2 = Tool.preset.drill.twist_drill_hss_5mm(tool_number=2)
        tool3 = Tool.preset.ball_mill.ball_mill_carbide_3mm(tool_number=3)

        self.library.add_tool(tool1)
        self.library.add_tool(tool2)
        self.library.add_tool(tool3)

        # Test library statistics
        self.assertEqual(len(self.library), 3)
        self.assertIn(1, self.library)
        self.assertIn(2, self.library)
        self.assertIn(3, self.library)

        # Test tool retrieval
        retrieved_tool = self.library.get_tool(1)
        self.assertIsNotNone(retrieved_tool)
        self.assertEqual(retrieved_tool.name, tool1.name)

        # Test filtering
        end_mills = self.library.get_tools_by_type(ToolType.FLAT_END_MILL)
        self.assertEqual(len(end_mills), 1)

        drills = self.library.get_tools_by_type(ToolType.DRILL)
        self.assertEqual(len(drills), 1)

        # Test diameter range filtering
        small_tools = self.library.get_tools_by_diameter_range(0, 4)
        self.assertEqual(len(small_tools), 1)  # 3mm ball mill

        # Test library validation
        issues = self.library.validate_library()
        self.assertEqual(len(issues), 0, f"Library validation failed: {issues}")

    def test_tool_library_serialization(self):
        """Test tool library save/load functionality."""
        # Add some tools
        tool1 = Tool.preset.end_mill.flat_carbide_6mm(tool_number=1)
        tool2 = Tool.preset.drill.twist_drill_hss_5mm(tool_number=2)

        self.library.add_tool(tool1)
        self.library.add_tool(tool2)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp_file:
            tmp_path = tmp_file.name

        try:
            self.library.save_to_file(tmp_path)
            self.assertTrue(os.path.exists(tmp_path))

            # Load into new library
            new_library = ToolLibrary()
            new_library.load_from_file(tmp_path)

            # Verify loaded library
            self.assertEqual(len(new_library), 2)
            self.assertEqual(new_library.name, self.library.name)

            loaded_tool = new_library.get_tool(1)
            self.assertIsNotNone(loaded_tool)
            self.assertEqual(loaded_tool.name, tool1.name)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestCAMWorkCoordinateSystem(unittest.TestCase):
    """Test the work coordinate system functionality."""

    def test_wcs_creation(self):
        """Test WCS creation and configuration."""
        from codetocad.core.cam.work_coordinate_system import WorkCoordinateSystem

        wcs = WorkCoordinateSystem()
        wcs.set_name("Test WCS")

        # Set workpiece setup
        workpiece = WorkpieceSetup(
            length=100.0, width=50.0, height=20.0, fixture_height=5.0
        )
        wcs.set_workpiece_setup(workpiece)

        # Set origin from preset
        wcs.set_origin_from_preset(WCSOrigin.BOTTOM_LEFT_FRONT)

        # Test coordinate transformations
        test_point = (10, 10, -5)
        machine_point = wcs.transform_point_to_machine(test_point)
        back_to_wcs = wcs.transform_point_from_machine(machine_point)

        # Should be close to original (within floating point precision)
        self.assertAlmostEqual(back_to_wcs[0], test_point[0], places=6)
        self.assertAlmostEqual(back_to_wcs[1], test_point[1], places=6)
        self.assertAlmostEqual(back_to_wcs[2], test_point[2], places=6)

        # Test workpiece bounds
        bounds = wcs.get_workpiece_bounds()
        self.assertIsNotNone(bounds)

        # Validate WCS
        issues = wcs.validate()
        self.assertEqual(len(issues), 0, f"WCS validation failed: {issues}")


def run_cam_tests():
    """Run all CAM system tests."""
    print("🔧 Running CAM System Tests...")

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestCAMToolSystem))
    test_suite.addTest(unittest.makeSuite(TestCAMToolpathSystem))
    test_suite.addTest(unittest.makeSuite(TestCAMToolLibrary))
    test_suite.addTest(unittest.makeSuite(TestCAMWorkCoordinateSystem))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    if result.wasSuccessful():
        print("✅ All CAM tests passed!")
    else:
        print(
            f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)"
        )

        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)

        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)

    return result.wasSuccessful()


if __name__ == "__main__":
    run_cam_tests()
