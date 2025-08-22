"""
Unit tests for KiCad PCB Board implementation.

These tests validate the board management operations including
board creation, layer management, and design rule handling.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from codetocad.interfaces.cad.pcb import (
    BoardDimensions,
    BoardShape,
    DrillSpecs,
    LayerProperties,
    LayerType,
    LayerSide,
)


class TestPCBBoard(unittest.TestCase):
    """Test cases for PCB Board operations."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock KiCad availability
        self.mock_pcbnew = Mock()
        self.mock_board = Mock()
        self.mock_pcbnew.BOARD.return_value = self.mock_board

        # Patch KiCad imports
        self.kicad_patcher = patch.dict("sys.modules", {"pcbnew": self.mock_pcbnew})
        self.kicad_patcher.start()

        # Patch KICAD_AVAILABLE
        self.available_patcher = patch("codetocad.adapters.kicad.KICAD_AVAILABLE", True)
        self.available_patcher.start()

        # Import after patching
        from codetocad.adapters.kicad.pcb import PCBBoard

        self.PCBBoard = PCBBoard

    def tearDown(self):
        """Clean up test fixtures."""
        self.kicad_patcher.stop()
        self.available_patcher.stop()

    def test_board_creation(self):
        """Test basic board creation."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(
            width=50.0, height=40.0, thickness=1.6, shape=BoardShape.RECTANGLE
        )

        result = board.create_board("test_board", dimensions, layer_count=2)

        # Verify board was created
        self.assertIsNotNone(board._kicad_board)
        self.assertEqual(board.name, "test_board")
        self.assertEqual(board.dimensions, dimensions)
        self.assertIs(result, board)  # Method chaining

        # Verify KiCad calls
        self.mock_pcbnew.BOARD.assert_called_once()

    def test_board_dimensions_rectangle(self):
        """Test rectangular board dimensions."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(
            width=100.0, height=80.0, shape=BoardShape.RECTANGLE
        )

        board.create_board("rect_board", dimensions)

        # Check area calculation
        expected_area = 100.0 * 80.0
        self.assertEqual(board.get_board_area(), expected_area)

    def test_board_dimensions_circle(self):
        """Test circular board dimensions."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(
            width=50.0, height=50.0, shape=BoardShape.CIRCLE  # Diameter
        )

        board.create_board("circle_board", dimensions)

        # Check area calculation (π * r²)
        import math

        radius = 50.0 / 2
        expected_area = math.pi * radius * radius
        self.assertAlmostEqual(board.get_board_area(), expected_area, places=2)

    def test_custom_board_outline(self):
        """Test custom board outline."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("custom_board", dimensions)

        # Define custom outline points (triangle)
        outline_points = [
            (0, 20),  # Top
            (-25, -20),  # Bottom left
            (25, -20),  # Bottom right
            (0, 20),  # Close triangle
        ]

        result = board.set_board_outline(outline_points)

        # Verify method chaining
        self.assertIs(result, board)

    def test_design_rules(self):
        """Test design rule setting."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("rules_board", dimensions)

        # Set design rules
        rules = {
            "min_trace_width": 0.15,
            "min_via_size": 0.3,
            "min_drill_size": 0.15,
            "min_spacing": 0.1,
        }

        result = board.set_design_rules(rules)

        # Verify rules were stored
        for key, value in rules.items():
            self.assertEqual(board.design_rules[key], value)

        # Verify method chaining
        self.assertIs(result, board)

    def test_mounting_hole(self):
        """Test mounting hole addition."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("hole_board", dimensions)

        # Add mounting hole
        drill_specs = DrillSpecs(
            drill_diameter=3.2, finished_hole_diameter=3.2, plated=False
        )

        result = board.add_mounting_hole(20, 15, drill_specs)

        # Verify method chaining
        self.assertIs(result, board)

    def test_layer_management(self):
        """Test layer addition and removal."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("layer_board", dimensions)

        # Create a test layer
        from codetocad.adapters.kicad.pcb import PCBLayer

        layer_props = LayerProperties(
            name="Signal1",
            layer_type=LayerType.SIGNAL,
            side=LayerSide.INNER,
            thickness=0.035,
        )

        layer = PCBLayer(layer_props)

        # Add layer
        result = board.add_layer(layer)
        self.assertIs(result, board)
        self.assertIn(layer, board.layers)

        # Get layer
        retrieved_layer = board.get_layer("Signal1")
        self.assertIs(retrieved_layer, layer)

        # Remove layer
        result = board.remove_layer("Signal1")
        self.assertIs(result, board)
        self.assertNotIn(layer, board.layers)

        # Get non-existent layer
        missing_layer = board.get_layer("NonExistent")
        self.assertIsNone(missing_layer)

    def test_validation(self):
        """Test board validation."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("valid_board", dimensions)

        # Mock validation response
        self.mock_board.GetNetCount.return_value = 5
        self.mock_board.GetFootprints.return_value = [Mock(), Mock()]  # 2 components

        violations = board.validate_design_rules()

        # Should be a list (empty or with violations)
        self.assertIsInstance(violations, list)

    def test_board_info(self):
        """Test board information retrieval."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("info_board", dimensions)

        # Mock board info
        mock_bbox = Mock()
        mock_bbox.GetX.return_value = 0
        mock_bbox.GetY.return_value = 0
        mock_bbox.GetWidth.return_value = 50000000  # 50mm in nm
        mock_bbox.GetHeight.return_value = 40000000  # 40mm in nm

        self.mock_board.ComputeBoundingBox.return_value = mock_bbox
        self.mock_board.GetFileName.return_value = "info_board.kicad_pcb"
        self.mock_board.GetCopperLayerCount.return_value = 2
        self.mock_board.GetFootprints.return_value = []
        self.mock_board.GetNetCount.return_value = 0

        info = board.get_info()

        # Verify info structure
        self.assertIsInstance(info, dict)
        self.assertIn("name", info)
        self.assertIn("component_count", info)
        self.assertIn("net_count", info)

    def test_component_and_net_management(self):
        """Test component and net addition."""
        board = self.PCBBoard()

        dimensions = BoardDimensions(width=50.0, height=40.0)
        board.create_board("mgmt_board", dimensions)

        # Mock component and net
        mock_component = Mock()
        mock_net = Mock()

        # Add component
        result = board.add_component(mock_component)
        self.assertIs(result, board)
        self.assertIn(mock_component, board.components)

        # Add net
        result = board.add_net(mock_net)
        self.assertIs(result, board)
        self.assertIn(mock_net, board.nets)

    def test_error_handling(self):
        """Test error handling for invalid operations."""
        board = self.PCBBoard()

        # Test operations without creating board first
        with self.assertRaises(RuntimeError):
            board.set_board_outline([(0, 0), (10, 10)])

        with self.assertRaises(RuntimeError):
            board.set_design_rules({"min_trace_width": 0.1})

        with self.assertRaises(RuntimeError):
            board.add_mounting_hole(0, 0, DrillSpecs(3.2, 3.2))

    @patch("codetocad.adapters.kicad.KICAD_AVAILABLE", False)
    def test_kicad_not_available(self):
        """Test behavior when KiCad is not available."""
        # Re-import with KiCad unavailable
        from codetocad.adapters.kicad.pcb import PCBBoard

        board = PCBBoard()
        dimensions = BoardDimensions(width=50.0, height=40.0)

        # Should raise ImportError
        with self.assertRaises(ImportError):
            board.create_board("no_kicad_board", dimensions)


class TestBoardDimensions(unittest.TestCase):
    """Test cases for BoardDimensions dataclass."""

    def test_default_values(self):
        """Test default dimension values."""
        dims = BoardDimensions(width=50.0, height=40.0)

        self.assertEqual(dims.width, 50.0)
        self.assertEqual(dims.height, 40.0)
        self.assertEqual(dims.thickness, 1.6)  # Default
        self.assertEqual(dims.shape, BoardShape.RECTANGLE)  # Default
        self.assertEqual(dims.corner_radius, 0.0)  # Default

    def test_custom_values(self):
        """Test custom dimension values."""
        dims = BoardDimensions(
            width=100.0,
            height=80.0,
            thickness=2.0,
            shape=BoardShape.CIRCLE,
            corner_radius=2.5,
        )

        self.assertEqual(dims.width, 100.0)
        self.assertEqual(dims.height, 80.0)
        self.assertEqual(dims.thickness, 2.0)
        self.assertEqual(dims.shape, BoardShape.CIRCLE)
        self.assertEqual(dims.corner_radius, 2.5)


if __name__ == "__main__":
    unittest.main()
