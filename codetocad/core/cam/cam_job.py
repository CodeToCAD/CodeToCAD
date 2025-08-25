"""
Concrete implementation of CAM Job interface.
"""

import json
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime
import logging

from codetocad.interfaces.cam.cam_job_interface import CAMJobInterface, JobStatus
from codetocad.interfaces.cam.toolpath_interface import CuttingParameters

if TYPE_CHECKING:
    from codetocad.interfaces.cam.toolpath_interface import ToolpathInterface

logger = logging.getLogger(__name__)


class CAMJob(CAMJobInterface):
    """Concrete implementation of CAMJobInterface."""

    def __init__(self):
        super().__init__()
        self.created_date = datetime.now().isoformat()
        self.modified_date = self.created_date

    def generate_toolpaths(self) -> "CAMJob":
        """Generate all toolpaths based on job setup."""
        try:
            if not self.setup or not self.workpiece:
                raise ValueError("Job setup and workpiece must be defined")

            # This is a simplified implementation
            # Real implementation would analyze geometry and generate appropriate toolpaths

            from codetocad.integrations.cam_integration import cam_integration

            # Get suggested operations
            suggested_ops = cam_integration.suggest_machining_operations(self.workpiece)

            # Create toolpaths for each suggested operation
            for op_info in suggested_ops:
                toolpath = self._create_toolpath_from_operation(op_info)
                if toolpath:
                    self.add_toolpath(toolpath)

            self.status = JobStatus.TOOLPATHS_GENERATED
            self.modified_date = datetime.now().isoformat()

            logger.info(
                f"Generated {len(self.toolpaths)} toolpaths for job: {self.name}"
            )
            return self

        except Exception as e:
            logger.error(f"Failed to generate toolpaths: {e}")
            self.status = JobStatus.ERROR
            raise

    def optimize_toolpaths(self) -> "CAMJob":
        """Optimize toolpaths for efficiency and quality."""
        try:
            if not self.toolpaths:
                logger.warning("No toolpaths to optimize")
                return self

            from codetocad.integrations.cam_integration import cam_integration

            # Optimize toolpath sequence
            self.toolpaths = cam_integration.optimize_tool_sequence(self.toolpaths)

            # Optimize individual toolpaths
            for toolpath in self.toolpaths:
                toolpath.optimize_toolpath()

            self.modified_date = datetime.now().isoformat()
            logger.info(f"Optimized {len(self.toolpaths)} toolpaths")

            return self

        except Exception as e:
            logger.error(f"Failed to optimize toolpaths: {e}")
            raise

    def simulate_job(self) -> "CAMJob":
        """Run simulation and verification."""
        try:
            if not self.simulator:
                logger.warning("No simulator configured, skipping simulation")
                return self

            if not self.toolpaths:
                logger.warning("No toolpaths to simulate")
                return self

            # Run collision detection
            collisions = self.simulator.check_multiple_toolpaths(self.toolpaths)

            # Run material removal simulation
            material_preview = self.simulator.simulate_material_removal(self.toolpaths)

            # Store simulation results
            self.simulation_results = {
                "collisions": len(collisions),
                "collision_details": [
                    {
                        "type": (
                            c.collision_type.value if c.collision_type else "unknown"
                        ),
                        "severity": c.severity,
                        "description": c.description,
                    }
                    for c in collisions
                ],
                "material_removal": {
                    "volume_removed": material_preview.volume_removed,
                    "surface_area": material_preview.surface_area,
                    "roughness_estimate": material_preview.roughness_estimate,
                    "machining_time": material_preview.machining_time,
                    "tool_wear_estimate": material_preview.tool_wear_estimate,
                },
                "simulation_date": datetime.now().isoformat(),
            }

            self.status = JobStatus.SIMULATED
            self.modified_date = datetime.now().isoformat()

            logger.info(
                f"Simulation completed: {len(collisions)} collisions, "
                f"{material_preview.volume_removed:.2f}mm³ removed"
            )

            return self

        except Exception as e:
            logger.error(f"Failed to simulate job: {e}")
            self.status = JobStatus.ERROR
            raise

    def post_process(self) -> "CAMJob":
        """Generate G-code from toolpaths."""
        try:
            if not self.post_processor:
                logger.warning(
                    "No post processor configured, skipping G-code generation"
                )
                return self

            if not self.toolpaths:
                logger.warning("No toolpaths to post-process")
                return self

            # Generate G-code
            gcode_lines = self.post_processor.process_multiple_toolpaths(self.toolpaths)
            self.gcode_output = "\n".join(gcode_lines)

            self.status = JobStatus.POST_PROCESSED
            self.modified_date = datetime.now().isoformat()

            logger.info(f"Generated G-code: {len(gcode_lines)} lines")
            return self

        except Exception as e:
            logger.error(f"Failed to post-process job: {e}")
            self.status = JobStatus.ERROR
            raise

    def save_job(self, file_path: str | Path) -> None:
        """Save the complete job to file."""
        try:
            file_path = Path(file_path)

            # Create job data structure
            job_data = {
                "job_info": {
                    "name": self.name,
                    "status": self.status.value,
                    "created_date": self.created_date,
                    "modified_date": self.modified_date,
                    "custom_properties": self.custom_properties,
                },
                "setup": self._serialize_setup(),
                "toolpaths": self._serialize_toolpaths(),
                "simulation_results": self.simulation_results,
                "gcode_output": self.gcode_output,
                "job_report": self.job_report,
            }

            # Write to file
            with open(file_path, "w") as f:
                json.dump(job_data, f, indent=2)

            logger.info(f"Saved CAM job to: {file_path}")

        except Exception as e:
            logger.error(f"Failed to save job to {file_path}: {e}")
            raise

    def load_job(self, file_path: str | Path) -> "CAMJob":
        """Load a job from file."""
        try:
            file_path = Path(file_path)

            with open(file_path, "r") as f:
                job_data = json.load(f)

            # Load job info
            job_info = job_data.get("job_info", {})
            self.name = job_info.get("name", "Loaded Job")
            self.status = JobStatus(job_info.get("status", "created"))
            self.created_date = job_info.get("created_date")
            self.modified_date = job_info.get("modified_date")
            self.custom_properties = job_info.get("custom_properties", {})

            # Load other data
            self.simulation_results = job_data.get("simulation_results", {})
            self.gcode_output = job_data.get("gcode_output")
            self.job_report = job_data.get("job_report", {})

            logger.info(f"Loaded CAM job from: {file_path}")
            return self

        except Exception as e:
            logger.error(f"Failed to load job from {file_path}: {e}")
            raise

    def export_gcode(self, file_path: str | Path) -> None:
        """Export G-code to file."""
        try:
            if not self.gcode_output:
                raise ValueError("No G-code generated. Run post_process() first.")

            file_path = Path(file_path)

            with open(file_path, "w") as f:
                f.write(self.gcode_output)

            logger.info(f"Exported G-code to: {file_path}")

        except Exception as e:
            logger.error(f"Failed to export G-code to {file_path}: {e}")
            raise

    def _create_toolpath_from_operation(
        self, operation_info: dict[str, Any]
    ) -> "ToolpathInterface":
        """Create a toolpath from operation information."""
        try:
            from codetocad.core.cam.toolpath import Toolpath
            from codetocad.interfaces.cam.toolpath_interface import (
                ToolpathOperation,
                ToolpathStrategy,
                CuttingParameters,
            )

            toolpath = Toolpath()
            toolpath.set_name(operation_info["name"])
            toolpath.set_operation(ToolpathOperation(operation_info["operation"]))
            toolpath.set_strategy(ToolpathStrategy(operation_info["strategy"]))
            toolpath.set_description(operation_info.get("description", ""))

            # Assign tool if tool library is available
            if self.tool_library:
                # Simple tool assignment based on operation
                suitable_tools = self._find_suitable_tools(operation_info)
                if suitable_tools:
                    toolpath.set_tool(suitable_tools[0])

            # Set default cutting parameters
            cutting_params = self._create_default_cutting_parameters(operation_info)
            toolpath.set_cutting_parameters(cutting_params)

            return toolpath

        except Exception as e:
            logger.error(f"Failed to create toolpath from operation: {e}")
            return None

    def _find_suitable_tools(self, operation_info: dict[str, Any]) -> list:
        """Find suitable tools for an operation."""
        if not self.tool_library:
            return []

        operation = operation_info["operation"]

        # Simple tool selection logic
        if operation == "ROUGHING":
            return self.tool_library.get_tools_by_type("ROUGHING_MILL")
        elif operation == "FINISHING":
            return self.tool_library.get_tools_by_type("FINISHING_MILL")
        elif operation == "DRILLING":
            return self.tool_library.get_tools_by_type("DRILL")
        else:
            return self.tool_library.get_tools_by_type("FLAT_END_MILL")

    def _create_default_cutting_parameters(
        self, operation_info: dict[str, Any]
    ) -> "CuttingParameters":
        """Create default cutting parameters for an operation."""
        from codetocad.interfaces.cam.toolpath_interface import CuttingParameters

        operation = operation_info["operation"]

        # Default parameters based on operation type
        if operation == "ROUGHING":
            return CuttingParameters(
                depth_of_cut=10.0,
                step_down=2.0,
                step_over=0.6,
                feed_rate=2000,
                spindle_speed=12000,
                plunge_rate=500,
            )
        elif operation == "FINISHING":
            return CuttingParameters(
                depth_of_cut=0.5,
                step_down=0.5,
                step_over=0.3,
                feed_rate=1200,
                spindle_speed=18000,
                plunge_rate=300,
            )
        elif operation == "DRILLING":
            return CuttingParameters(
                depth_of_cut=20.0,
                step_down=3.0,
                step_over=1.0,
                feed_rate=200,
                spindle_speed=3000,
                plunge_rate=200,
            )
        else:
            return CuttingParameters(
                depth_of_cut=5.0,
                step_down=1.0,
                step_over=0.5,
                feed_rate=1000,
                spindle_speed=15000,
                plunge_rate=250,
            )

    def _serialize_setup(self) -> dict[str, Any]:
        """Serialize job setup to dictionary."""
        if not self.setup:
            return {}

        return {
            "name": self.setup.name,
            "description": self.setup.description,
            "strategy": self.setup.strategy.value,
            "material": self.setup.material.name if self.setup.material else None,
            "stock_dimensions": self.setup.stock_dimensions,
            "stock_to_leave": self.setup.stock_to_leave,
            "surface_finish_requirement": self.setup.surface_finish_requirement,
            "tolerance": self.setup.tolerance,
        }

    def _serialize_toolpaths(self) -> list:
        """Serialize toolpaths to list of dictionaries."""
        toolpath_data = []

        for toolpath in self.toolpaths:
            tp_data = {
                "name": toolpath.name,
                "operation": toolpath.operation.value,
                "strategy": toolpath.strategy.value,
                "enabled": toolpath.enabled,
                "description": toolpath.description,
                "tool_number": toolpath.tool.tool_number if toolpath.tool else None,
                "point_count": len(toolpath.points),
                "total_length": toolpath.get_total_length(),
                "machining_time": toolpath.get_machining_time_estimate(),
            }
            toolpath_data.append(tp_data)

        return toolpath_data
