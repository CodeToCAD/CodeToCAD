"""
FreeCAD-specific Toolpath implementation.
"""

from typing import TYPE_CHECKING, Tuple
import logging

from codetocad.core.cam.toolpath import Toolpath as BaseToolpath
from codetocad.interfaces.cam.toolpath_interface import ToolpathPoint
from codetocad.adapters.freecad.freecad_actions.path_operations import (
    create_profile_operation,
    create_pocket_operation,
    create_drilling_operation,
    create_adaptive_operation,
    create_surface_operation,
    get_toolpath_points,
    calculate_toolpath,
)

if TYPE_CHECKING:
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.interfaces.cad.sketch.sketch_interface import SketchInterface

logger = logging.getLogger(__name__)


class Toolpath(BaseToolpath):
    """FreeCAD-specific implementation of ToolpathInterface."""

    def __init__(self):
        super().__init__()
        self.freecad_operation = None  # Reference to FreeCAD Path operation
        self.freecad_job = None  # Reference to parent FreeCAD job

    def set_freecad_operation(self, operation) -> "Toolpath":
        """Set the underlying FreeCAD Path operation."""
        self.freecad_operation = operation
        return self

    def set_freecad_job(self, job) -> "Toolpath":
        """Set the parent FreeCAD job."""
        self.freecad_job = job
        return self

    def generate_from_sketch(self, sketch: "SketchInterface") -> "Toolpath":
        """Generate toolpath from a 2D sketch using FreeCAD Path."""
        try:
            if not self.freecad_job:
                raise ValueError("FreeCAD job must be set before generating toolpath")

            if not self.tool:
                raise ValueError("Tool must be assigned before generating toolpath")

            # Get the native FreeCAD object from the sketch
            if hasattr(sketch, "native_instance"):
                base_geometry = sketch.native_instance
            else:
                raise ValueError("Sketch must have a native FreeCAD instance")

            # Create FreeCAD tool controller if needed
            tool_controller = self._get_or_create_tool_controller()

            # Generate operation based on strategy
            if self.strategy.value == "profile":
                self.freecad_operation = create_profile_operation(
                    self.freecad_job,
                    self.name,
                    base_geometry,
                    tool_controller,
                    **self._get_operation_parameters(),
                )
            elif self.strategy.value == "pocket":
                self.freecad_operation = create_pocket_operation(
                    self.freecad_job,
                    self.name,
                    base_geometry,
                    tool_controller,
                    **self._get_operation_parameters(),
                )
            else:
                # Default to profile for unsupported strategies
                logger.warning(
                    f"Strategy {self.strategy.value} not fully supported, using profile"
                )
                self.freecad_operation = create_profile_operation(
                    self.freecad_job, self.name, base_geometry, tool_controller
                )

            # Calculate toolpath
            if calculate_toolpath(self.freecad_operation):
                self._extract_toolpath_points()

            logger.info(f"Generated toolpath from sketch: {len(self.points)} points")
            return self

        except Exception as e:
            logger.error(f"Failed to generate toolpath from sketch: {e}")
            raise

    def generate_from_part(self, part: "PartInterface") -> "Toolpath":
        """Generate toolpath from a 3D part using FreeCAD Path."""
        try:
            if not self.freecad_job:
                raise ValueError("FreeCAD job must be set before generating toolpath")

            if not self.tool:
                raise ValueError("Tool must be assigned before generating toolpath")

            # Get the native FreeCAD object from the part
            if hasattr(part, "native_instance"):
                base_geometry = part.native_instance
            else:
                raise ValueError("Part must have a native FreeCAD instance")

            # Create FreeCAD tool controller if needed
            tool_controller = self._get_or_create_tool_controller()

            # Generate operation based on strategy
            if self.strategy.value in ["waterline", "surface_finishing"]:
                self.freecad_operation = create_surface_operation(
                    self.freecad_job,
                    self.name,
                    base_geometry,
                    tool_controller,
                    **self._get_operation_parameters(),
                )
            elif self.strategy.value == "adaptive_clearing":
                self.freecad_operation = create_adaptive_operation(
                    self.freecad_job,
                    self.name,
                    base_geometry,
                    tool_controller,
                    **self._get_operation_parameters(),
                )
            else:
                # Default to pocket for 3D operations
                logger.warning(
                    f"Strategy {self.strategy.value} not fully supported for 3D, using pocket"
                )
                self.freecad_operation = create_pocket_operation(
                    self.freecad_job,
                    self.name,
                    base_geometry,
                    tool_controller,
                    **self._get_operation_parameters(),
                )

            # Calculate toolpath
            if calculate_toolpath(self.freecad_operation):
                self._extract_toolpath_points()

            logger.info(f"Generated toolpath from part: {len(self.points)} points")
            return self

        except Exception as e:
            logger.error(f"Failed to generate toolpath from part: {e}")
            raise

    def generate_drilling_pattern(
        self, points: list[tuple[float, float]], depth: float
    ) -> "Toolpath":
        """Generate drilling toolpath using FreeCAD Path."""
        try:
            if not self.freecad_job:
                raise ValueError("FreeCAD job must be set before generating toolpath")

            if not self.tool:
                raise ValueError("Tool must be assigned before generating toolpath")

            # Create FreeCAD tool controller if needed
            tool_controller = self._get_or_create_tool_controller()

            # Convert 2D points to 3D for FreeCAD
            drill_points_3d = [(x, y, 0.0) for x, y in points]

            # Create drilling operation
            self.freecad_operation = create_drilling_operation(
                self.freecad_job,
                self.name,
                drill_points_3d,
                tool_controller,
                **self._get_drilling_parameters(depth),
            )

            # Calculate toolpath
            if calculate_toolpath(self.freecad_operation):
                self._extract_toolpath_points()

            logger.info(
                f"Generated drilling pattern: {len(points)} holes, {len(self.points)} points"
            )
            return self

        except Exception as e:
            logger.error(f"Failed to generate drilling pattern: {e}")
            # Fall back to base implementation
            return super().generate_drilling_pattern(points, depth)

    def optimize_toolpath(self) -> "Toolpath":
        """Optimize the toolpath using FreeCAD's optimization features."""
        try:
            # First run base optimization
            super().optimize_toolpath()

            # If we have a FreeCAD operation, we could apply additional optimizations
            if self.freecad_operation:
                # FreeCAD operations are typically already optimized
                # Additional optimization could be implemented here
                pass

            return self

        except Exception as e:
            logger.error(f"Failed to optimize toolpath: {e}")
            return self

    def _get_or_create_tool_controller(self):
        """Get or create a FreeCAD tool controller for this toolpath's tool."""
        from codetocad.adapters.freecad.freecad_actions.tool_operations import (
            create_tool,
            create_tool_controller,
        )

        if not self.tool or not self.freecad_job:
            raise ValueError("Tool and FreeCAD job must be set")

        # Check if tool controller already exists
        if hasattr(self.freecad_job, "ToolController"):
            for tc in self.freecad_job.ToolController:
                if hasattr(tc, "Tool") and tc.Tool and tc.Tool.Name == self.tool.name:
                    return tc

        # Create new FreeCAD tool
        freecad_tool = create_tool(
            name=self.tool.name,
            tool_type=self.tool.tool_type.value,
            diameter=self.tool.geometry.diameter if self.tool.geometry else 6.0,
            length=self.tool.geometry.length if self.tool.geometry else 50.0,
            cutting_edge_height=(
                self.tool.geometry.cutting_length if self.tool.geometry else 20.0
            ),
            flute_count=self.tool.geometry.flute_count if self.tool.geometry else 2,
        )

        # Create tool controller
        cutting_data = self.tool.cutting_data
        tool_controller = create_tool_controller(
            self.freecad_job,
            freecad_tool,
            f"TC_{self.tool.name}",
            horizontal_feed=cutting_data.feed_rate if cutting_data else 1000.0,
            vertical_feed=cutting_data.plunge_rate if cutting_data else 250.0,
            spindle_speed=cutting_data.spindle_speed if cutting_data else 12000.0,
        )

        return tool_controller

    def _get_operation_parameters(self) -> dict:
        """Get operation parameters from cutting parameters."""
        params = {}

        if self.cutting_parameters:
            params.update(
                {
                    "start_depth": 0.0,
                    "final_depth": -self.cutting_parameters.depth_of_cut,
                    "step_down": self.cutting_parameters.step_down,
                }
            )

            # Add strategy-specific parameters
            if self.strategy.value == "profile":
                params["side"] = "Outside"  # Default to outside profiling
                params["direction"] = "CW"
            elif self.strategy.value == "pocket":
                params["cut_mode"] = (
                    "Climb" if self.cutting_parameters else "Conventional"
                )
                params["pattern"] = "ZigZag"
                params["step_over"] = (
                    self.cutting_parameters.step_over * 100
                )  # Convert to percentage

        return params

    def _get_drilling_parameters(self, depth: float) -> dict:
        """Get drilling-specific parameters."""
        params = {
            "peck_enabled": True,
            "peck_depth": (
                self.cutting_parameters.step_down if self.cutting_parameters else 3.0
            ),
            "retract_height": (
                self.cutting_parameters.clearance_height
                if self.cutting_parameters
                else 2.0
            ),
        }
        return params

    def _extract_toolpath_points(self):
        """Extract toolpath points from FreeCAD operation."""
        if not self.freecad_operation:
            return

        try:
            # Get points from FreeCAD operation
            freecad_points = get_toolpath_points(self.freecad_operation)

            # Convert to ToolpathPoint objects
            self.points.clear()
            for x, y, z in freecad_points:
                point = ToolpathPoint(x=x, y=y, z=z)
                # TODO: Determine if point is rapid move based on G-code command
                self.points.append(point)

            logger.info(f"Extracted {len(self.points)} points from FreeCAD operation")

        except Exception as e:
            logger.error(f"Failed to extract toolpath points: {e}")

    def copy(self) -> "Toolpath":
        """Create a copy of the FreeCAD toolpath."""
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

        # Copy FreeCAD-specific properties
        new_toolpath.freecad_job = self.freecad_job
        # Note: Don't copy freecad_operation as it should be unique

        return new_toolpath
