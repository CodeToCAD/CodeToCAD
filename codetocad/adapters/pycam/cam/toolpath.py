"""
PyCAM-specific Toolpath implementation.
"""

from typing import TYPE_CHECKING, Tuple
import logging

from codetocad.core.cam.toolpath import Toolpath as BaseToolpath
from codetocad.interfaces.cam.toolpath_interface import ToolpathPoint
from codetocad.adapters.pycam.pycam_actions.toolpath_generation import (
    generate_contour_toolpath,
    generate_waterline_toolpath,
    generate_push_cutter_toolpath,
    generate_drop_cutter_toolpath,
    optimize_toolpath_order,
)

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

logger = logging.getLogger(__name__)


class Toolpath(BaseToolpath):
    """PyCAM-specific implementation of ToolpathInterface."""

    def __init__(self):
        super().__init__()
        self.pycam_model = None  # Reference to PyCAM model

    def set_pycam_model(self, model) -> "Toolpath":
        """Set the PyCAM model for toolpath generation."""
        self.pycam_model = model
        return self

    def generate_from_sketch(self, sketch: "SketchInterface") -> "Toolpath":
        """Generate toolpath from a 2D sketch using PyCAM."""
        try:
            if not self.tool:
                raise ValueError("Tool must be assigned before generating toolpath")

            # PyCAM works primarily with 3D models, so we need to extrude the sketch
            # or create a simple 2D operation

            # For 2D operations, we'll use contour following
            tool_settings = self._get_tool_settings()
            operation_settings = self._get_operation_settings()

            # Create a simple model from sketch bounds
            model = self._create_model_from_sketch(sketch)

            # Generate toolpath based on strategy
            if self.strategy.value == "profile":
                points = generate_contour_toolpath(
                    model, tool_settings, operation_settings
                )
            else:
                # Default to contour for unsupported strategies
                logger.warning(
                    f"Strategy {self.strategy.value} not supported in PyCAM, using contour"
                )
                points = generate_contour_toolpath(
                    model, tool_settings, operation_settings
                )

            # Convert to ToolpathPoint objects
            self._convert_points_to_toolpath(points)

            logger.info(f"Generated toolpath from sketch: {len(self.points)} points")
            return self

        except Exception as e:
            logger.error(f"Failed to generate toolpath from sketch: {e}")
            # Fall back to base implementation
            return super().generate_from_sketch(sketch)

    def generate_from_part(self, part: "PartInterface") -> "Toolpath":
        """Generate toolpath from a 3D part using PyCAM."""
        try:
            if not self.tool:
                raise ValueError("Tool must be assigned before generating toolpath")

            # Create PyCAM model from part
            model = self._create_model_from_part(part)
            if not model:
                raise ValueError("Failed to create PyCAM model from part")

            tool_settings = self._get_tool_settings()
            operation_settings = self._get_operation_settings()

            # Generate toolpath based on strategy
            if self.strategy.value == "waterline":
                points = generate_waterline_toolpath(
                    model, tool_settings, operation_settings
                )
            elif self.strategy.value == "surface_finishing":
                points = generate_drop_cutter_toolpath(
                    model, tool_settings, operation_settings
                )
            elif self.strategy.value in ["conventional_clearing", "adaptive_clearing"]:
                points = generate_push_cutter_toolpath(
                    model, tool_settings, operation_settings
                )
            else:
                # Default to waterline for 3D operations
                logger.warning(
                    f"Strategy {self.strategy.value} not fully supported, using waterline"
                )
                points = generate_waterline_toolpath(
                    model, tool_settings, operation_settings
                )

            # Convert to ToolpathPoint objects
            self._convert_points_to_toolpath(points)

            logger.info(f"Generated toolpath from part: {len(self.points)} points")
            return self

        except Exception as e:
            logger.error(f"Failed to generate toolpath from part: {e}")
            # Fall back to base implementation
            return super().generate_from_part(part)

    def generate_drilling_pattern(
        self, points: list[tuple[float, float]], depth: float
    ) -> "Toolpath":
        """Generate drilling toolpath (PyCAM doesn't have specific drilling, so use base implementation)."""
        logger.info(
            "Using base drilling implementation (PyCAM doesn't support drilling operations)"
        )
        return super().generate_drilling_pattern(points, depth)

    def optimize_toolpath(self) -> "Toolpath":
        """Optimize the toolpath using PyCAM optimization algorithms."""
        try:
            if not self.points:
                return self

            # Convert to coordinate tuples
            point_tuples = [(p.x, p.y, p.z) for p in self.points]

            # Optimize using PyCAM algorithms
            optimized_tuples = optimize_toolpath_order(point_tuples)

            # Convert back to ToolpathPoint objects
            self.points = []
            for x, y, z in optimized_tuples:
                point = ToolpathPoint(x=x, y=y, z=z)
                self.points.append(point)

            logger.info(f"Optimized toolpath: {len(self.points)} points")
            return self

        except Exception as e:
            logger.error(f"Failed to optimize toolpath: {e}")
            # Fall back to base optimization
            return super().optimize_toolpath()

    def _get_tool_settings(self) -> dict:
        """Get tool settings for PyCAM operations."""
        settings = {
            "radius": 3.0,  # Default radius
            "type": "cylindrical",
        }

        if self.tool and self.tool.geometry:
            settings["radius"] = self.tool.geometry.diameter / 2.0

            # Map tool types
            if self.tool.tool_type.value == "ball_end_mill":
                settings["type"] = "ball"
            elif self.tool.tool_type.value == "v_bit":
                settings["type"] = "v_bit"
                settings["angle"] = self.tool.geometry.tip_angle or 60.0

        return settings

    def _get_operation_settings(self) -> dict:
        """Get operation settings for PyCAM operations."""
        settings = {
            "step_down": 1.0,
            "step_over": 1.0,
            "start_z": 0.0,
            "end_z": -5.0,
            "direction": "x",
            "sample_distance": 0.1,
        }

        if self.cutting_parameters:
            settings.update(
                {
                    "step_down": self.cutting_parameters.step_down,
                    "start_z": self.cutting_parameters.safe_height,
                    "end_z": -self.cutting_parameters.depth_of_cut,
                }
            )

            # Calculate step over in mm from percentage
            if self.tool and self.tool.geometry:
                step_over_mm = (
                    self.tool.geometry.diameter * self.cutting_parameters.step_over
                )
                settings["step_over"] = step_over_mm

        return settings

    def _create_model_from_sketch(self, sketch: "SketchInterface") -> Any:
        """Create a simple PyCAM model from a sketch."""
        try:
            # For 2D sketches, create a simple rectangular model
            # This is a simplified approach - real implementation would
            # need to extract actual sketch geometry

            # Create a mock model with bounds
            class SimpleModel:
                def __init__(self):
                    self.bounds = {
                        "x_min": -25.0,
                        "x_max": 25.0,
                        "y_min": -25.0,
                        "y_max": 25.0,
                        "z_min": -5.0,
                        "z_max": 0.0,
                    }

            return SimpleModel()

        except Exception as e:
            logger.error(f"Failed to create model from sketch: {e}")
            return None

    def _create_model_from_part(self, part: "PartInterface") -> Any:
        """Create a PyCAM model from a 3D part."""
        try:
            # Check if part has STL export capability
            if hasattr(part, "export") and hasattr(part.export, "stl"):
                # Export to temporary STL file and load with PyCAM
                import tempfile
                import os

                with tempfile.NamedTemporaryFile(
                    suffix=".stl", delete=False
                ) as tmp_file:
                    tmp_path = tmp_file.name

                try:
                    # Export part to STL
                    part.export.stl(tmp_path)

                    # Load with PyCAM
                    from codetocad.adapters.pycam.pycam_actions.model_operations import (
                        load_stl_model,
                    )

                    model = load_stl_model(tmp_path)

                    return model

                finally:
                    # Clean up temporary file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

            else:
                # Create a simple model from part bounds
                logger.warning("Part doesn't support STL export, creating simple model")
                return self._create_simple_model_from_part(part)

        except Exception as e:
            logger.error(f"Failed to create PyCAM model from part: {e}")
            return None

    def _create_simple_model_from_part(self, part: "PartInterface") -> Any:
        """Create a simple model from part bounds."""
        try:
            # Get part bounding box if available
            bounds = getattr(part, "bounding_box", None)

            if bounds:
                min_point, max_point = bounds
                model_bounds = {
                    "x_min": min_point[0],
                    "x_max": max_point[0],
                    "y_min": min_point[1],
                    "y_max": max_point[1],
                    "z_min": min_point[2],
                    "z_max": max_point[2],
                }
            else:
                # Default bounds
                model_bounds = {
                    "x_min": -25.0,
                    "x_max": 25.0,
                    "y_min": -25.0,
                    "y_max": 25.0,
                    "z_min": -10.0,
                    "z_max": 0.0,
                }

            class SimpleModel:
                def __init__(self, bounds):
                    self.bounds = bounds

            return SimpleModel(model_bounds)

        except Exception as e:
            logger.error(f"Failed to create simple model: {e}")
            return None

    def _convert_points_to_toolpath(self, points: list[tuple[float, float, float]]):
        """Convert coordinate tuples to ToolpathPoint objects."""
        self.points.clear()

        for i, (x, y, z) in enumerate(points):
            # Determine if this is a rapid move
            # Simple heuristic: if Z changes significantly, it's likely a rapid move
            rapid_move = False
            if i > 0:
                prev_z = points[i - 1][2]
                if abs(z - prev_z) > 1.0:  # More than 1mm Z change
                    rapid_move = True

            point = ToolpathPoint(
                x=x,
                y=y,
                z=z,
                rapid_move=rapid_move,
                feed_rate=(
                    self.cutting_parameters.feed_rate
                    if self.cutting_parameters
                    else None
                ),
            )
            self.points.append(point)

    def copy(self) -> "Toolpath":
        """Create a copy of the PyCAM toolpath."""
        new_toolpath = Toolpath()

        # Copy base properties
        new_toolpath.name = self.name
        new_toolpath.operation = self.operation
        new_toolpath.strategy = self.strategy
        new_toolpath.description = self.description
        new_toolpath.enabled = self.enabled
        new_toolpath.tool = self.tool

        # Deep copy cutting parameters and points
        if self.cutting_parameters:
            import copy

            new_toolpath.cutting_parameters = copy.deepcopy(self.cutting_parameters)

        new_toolpath.points = [
            ToolpathPoint(
                x=p.x, y=p.y, z=p.z, feed_rate=p.feed_rate, rapid_move=p.rapid_move
            )
            for p in self.points
        ]

        # Copy PyCAM-specific properties
        new_toolpath.pycam_model = self.pycam_model

        return new_toolpath
