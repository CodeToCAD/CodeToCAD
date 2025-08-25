"""
CAM Job interface for managing complete machining workflows.

Coordinates toolpaths, tools, work coordinate systems, and post-processing
into a complete machining job.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from codetocad.interfaces.cam.toolpath_interface import ToolpathInterface
    from codetocad.interfaces.cam.tool_interface import ToolInterface
    from codetocad.interfaces.cam.tool_library_interface import ToolLibraryInterface
    from codetocad.interfaces.cam.work_coordinate_system_interface import (
        WorkCoordinateSystemInterface,
    )
    from codetocad.interfaces.cam.post_processor_interface import PostProcessorInterface
    from codetocad.interfaces.cam.simulation_interface import SimulationInterface
    from codetocad.interfaces.cad.part.part_interface import PartInterface
    from codetocad.core.material import Material


class JobStatus(Enum):
    """CAM job status states."""

    CREATED = "created"
    SETUP = "setup"
    TOOLPATHS_GENERATED = "toolpaths_generated"
    SIMULATED = "simulated"
    POST_PROCESSED = "post_processed"
    READY = "ready"
    ERROR = "error"


class MachiningStrategy(Enum):
    """Overall machining strategies."""

    ROUGHING_ONLY = "roughing_only"
    FINISHING_ONLY = "finishing_only"
    ROUGHING_FINISHING = "roughing_finishing"
    ADAPTIVE_MACHINING = "adaptive_machining"
    HIGH_SPEED_MACHINING = "high_speed_machining"
    CUSTOM = "custom"


@dataclass
class JobSetup:
    """Job setup configuration."""

    name: str
    description: str = ""
    strategy: MachiningStrategy = MachiningStrategy.ROUGHING_FINISHING

    # Material and stock
    material: "Material|None" = None
    stock_dimensions: tuple[float, float, float] | None = None  # X, Y, Z
    stock_to_leave: float = 0.0  # mm

    # Machine settings
    machine_name: str = "Generic CNC"
    max_spindle_speed: float = 24000.0  # RPM
    max_feed_rate: float = 10000.0  # mm/min

    # Quality settings
    surface_finish_requirement: str = (
        "standard"  # "rough", "standard", "fine", "mirror"
    )
    tolerance: float = 0.1  # mm

    # Safety settings
    safe_z_height: float = 5.0  # mm
    clearance_height: float = 2.0  # mm


@dataclass
class MachiningSequence:
    """Defines the sequence of machining operations."""

    operations: list[str]  # List of operation names in order
    dependencies: dict[str, list[str]]  # operation -> list of prerequisite operations
    parallel_operations: list[
        list[str]
    ]  # Groups of operations that can run in parallel

    def __post_init__(self):
        """Initialize empty collections if not provided."""
        if not self.dependencies:
            self.dependencies = {}
        if not self.parallel_operations:
            self.parallel_operations = []


class CAMJobInterface(ABC):
    """Abstract interface for CAM job management."""

    def __init__(self):
        self.name: str = "CAM Job"
        self.status: JobStatus = JobStatus.CREATED
        self.setup: JobSetup | None = None

        # Core components
        self.workpiece: "PartInterface" | None = None
        self.toolpaths: list["ToolpathInterface"] = []
        self.tool_library: "ToolLibraryInterface" | None = None
        self.work_coordinate_system: "WorkCoordinateSystemInterface" | None = None
        self.post_processor: "PostProcessorInterface" | None = None
        self.simulator: "SimulationInterface" | None = None

        # Sequencing
        self.machining_sequence: MachiningSequence | None = None

        # Results and outputs
        self.simulation_results: dict[str, Any] = {}
        self.gcode_output: str | None = None
        self.job_report: dict[str, Any] = {}

        # Metadata
        self.created_date: str | None = None
        self.modified_date: str | None = None
        self.custom_properties: dict[str, Any] = {}

    def set_name(self, name: str) -> "CAMJobInterface":
        """Set the job name."""
        self.name = name
        return self

    def set_setup(self, setup: JobSetup) -> "CAMJobInterface":
        """Set the job setup configuration."""
        self.setup = setup
        self.status = JobStatus.SETUP
        return self

    def set_workpiece(self, workpiece: "PartInterface") -> "CAMJobInterface":
        """Set the workpiece to be machined."""
        self.workpiece = workpiece
        return self

    def set_tool_library(self, library: "ToolLibraryInterface") -> "CAMJobInterface":
        """Set the tool library for the job."""
        self.tool_library = library
        return self

    def set_work_coordinate_system(
        self, wcs: "WorkCoordinateSystemInterface"
    ) -> "CAMJobInterface":
        """Set the work coordinate system."""
        self.work_coordinate_system = wcs
        return self

    def set_post_processor(
        self, post_processor: "PostProcessorInterface"
    ) -> "CAMJobInterface":
        """Set the post-processor for G-code generation."""
        self.post_processor = post_processor
        return self

    def set_simulator(self, simulator: "SimulationInterface") -> "CAMJobInterface":
        """Set the simulator for verification."""
        self.simulator = simulator
        return self

    def add_toolpath(self, toolpath: "ToolpathInterface") -> "CAMJobInterface":
        """Add a toolpath to the job."""
        self.toolpaths.append(toolpath)
        return self

    def remove_toolpath(self, toolpath: "ToolpathInterface") -> "CAMJobInterface":
        """Remove a toolpath from the job."""
        if toolpath in self.toolpaths:
            self.toolpaths.remove(toolpath)
        return self

    def get_toolpaths_by_operation(self, operation: str) -> list["ToolpathInterface"]:
        """Get toolpaths filtered by operation type."""
        return [tp for tp in self.toolpaths if tp.operation.value == operation]

    def get_toolpaths_by_tool(self, tool: "ToolInterface") -> list["ToolpathInterface"]:
        """Get toolpaths that use a specific tool."""
        return [tp for tp in self.toolpaths if tp.tool == tool]

    def get_enabled_toolpaths(self) -> list["ToolpathInterface"]:
        """Get only enabled toolpaths."""
        return [tp for tp in self.toolpaths if tp.enabled]

    def set_machining_sequence(self, sequence: MachiningSequence) -> "CAMJobInterface":
        """Set the machining operation sequence."""
        self.machining_sequence = sequence
        return self

    @abstractmethod
    def generate_toolpaths(self) -> "CAMJobInterface":
        """Generate all toolpaths based on job setup."""
        pass

    @abstractmethod
    def optimize_toolpaths(self) -> "CAMJobInterface":
        """Optimize toolpaths for efficiency and quality."""
        pass

    @abstractmethod
    def simulate_job(self) -> "CAMJobInterface":
        """Run simulation and verification."""
        pass

    @abstractmethod
    def post_process(self) -> "CAMJobInterface":
        """Generate G-code from toolpaths."""
        pass

    def validate_job(self) -> list[str]:
        """Validate the complete job setup."""
        issues = []

        if not self.name:
            issues.append("Job name is required")

        if not self.setup:
            issues.append("Job setup is required")

        if not self.workpiece:
            issues.append("Workpiece is required")

        if not self.tool_library:
            issues.append("Tool library is required")

        if not self.work_coordinate_system:
            issues.append("Work coordinate system is required")

        if not self.toolpaths:
            issues.append("At least one toolpath is required")

        # Validate individual components
        if self.tool_library:
            library_issues = self.tool_library.validate_library()
            issues.extend([f"Tool library: {issue}" for issue in library_issues])

        if self.work_coordinate_system:
            wcs_issues = self.work_coordinate_system.validate()
            issues.extend([f"WCS: {issue}" for issue in wcs_issues])

        for i, toolpath in enumerate(self.toolpaths):
            toolpath_issues = toolpath.validate()
            issues.extend([f"Toolpath {i}: {issue}" for issue in toolpath_issues])

        # Validate tool assignments
        for i, toolpath in enumerate(self.toolpaths):
            if toolpath.tool and self.tool_library:
                if toolpath.tool.tool_number not in self.tool_library:
                    issues.append(
                        f"Toolpath {i}: Tool {toolpath.tool.tool_number} not in library"
                    )

        return issues

    def get_job_statistics(self) -> dict[str, Any]:
        """Get comprehensive job statistics."""
        enabled_toolpaths = self.get_enabled_toolpaths()

        stats = {
            "job_name": self.name,
            "status": self.status.value,
            "toolpath_count": len(self.toolpaths),
            "enabled_toolpath_count": len(enabled_toolpaths),
            "total_length": sum(tp.get_total_length() for tp in enabled_toolpaths),
            "estimated_time": sum(
                tp.get_machining_time_estimate() for tp in enabled_toolpaths
            ),
            "tools_required": len(
                set(tp.tool.tool_number for tp in enabled_toolpaths if tp.tool)
            ),
            "operations": {},
        }

        # Count operations
        for toolpath in enabled_toolpaths:
            op = toolpath.operation.value
            stats["operations"][op] = stats["operations"].get(op, 0) + 1

        # Add setup information
        if self.setup:
            stats["setup"] = {
                "strategy": self.setup.strategy.value,
                "material": self.setup.material.name if self.setup.material else None,
                "surface_finish": self.setup.surface_finish_requirement,
                "tolerance": self.setup.tolerance,
            }

        return stats

    def generate_job_report(self) -> dict[str, Any]:
        """Generate comprehensive job report."""
        report = {
            "job_info": {
                "name": self.name,
                "status": self.status.value,
                "created_date": self.created_date,
                "modified_date": self.modified_date,
            },
            "statistics": self.get_job_statistics(),
            "validation": self.validate_job(),
            "simulation_results": self.simulation_results,
            "recommendations": [],
        }

        # Generate recommendations
        recommendations = []
        validation_issues = report["validation"]

        if validation_issues:
            recommendations.append("Resolve validation issues before proceeding")

        if report["statistics"]["estimated_time"] > 120:  # 2 hours
            recommendations.append("Consider breaking job into multiple setups")

        if report["statistics"]["tools_required"] > 10:
            recommendations.append("High tool count - verify tool changer capacity")

        report["recommendations"] = recommendations
        self.job_report = report

        return report

    @abstractmethod
    def save_job(self, file_path: str | Path) -> None:
        """Save the complete job to file."""
        pass

    @abstractmethod
    def load_job(self, file_path: str | Path) -> "CAMJobInterface":
        """Load a job from file."""
        pass

    @abstractmethod
    def export_gcode(self, file_path: str | Path) -> None:
        """Export G-code to file."""
        pass

    def clone_job(self, new_name: str) -> "CAMJobInterface":
        """Create a copy of the job with a new name."""
        # This would be implemented by concrete classes
        # to create a deep copy of the job
        raise NotImplementedError("clone_job must be implemented by concrete classes")

    def get_progress(self) -> dict[str, Any]:
        """Get job progress information."""
        progress = {
            "current_status": self.status.value,
            "completion_percentage": 0,
            "next_steps": [],
            "estimated_completion_time": None,
        }

        # Calculate completion percentage based on status
        status_progress = {
            JobStatus.CREATED: 10,
            JobStatus.SETUP: 25,
            JobStatus.TOOLPATHS_GENERATED: 50,
            JobStatus.SIMULATED: 75,
            JobStatus.POST_PROCESSED: 90,
            JobStatus.READY: 100,
            JobStatus.ERROR: 0,
        }

        progress["completion_percentage"] = status_progress.get(self.status, 0)

        # Determine next steps
        if self.status == JobStatus.CREATED:
            progress["next_steps"] = [
                "Configure job setup",
                "Set workpiece",
                "Configure tools",
            ]
        elif self.status == JobStatus.SETUP:
            progress["next_steps"] = ["Generate toolpaths", "Assign tools"]
        elif self.status == JobStatus.TOOLPATHS_GENERATED:
            progress["next_steps"] = ["Run simulation", "Verify toolpaths"]
        elif self.status == JobStatus.SIMULATED:
            progress["next_steps"] = ["Generate G-code", "Review post-processing"]
        elif self.status == JobStatus.POST_PROCESSED:
            progress["next_steps"] = ["Final review", "Export files"]
        elif self.status == JobStatus.READY:
            progress["next_steps"] = ["Job ready for machining"]

        return progress

    def __repr__(self) -> str:
        toolpath_count = len(self.toolpaths)
        return f"<CAMJob: {self.name}, {self.status.value}, {toolpath_count} toolpaths>"
