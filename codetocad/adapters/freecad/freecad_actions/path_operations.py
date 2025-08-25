"""
FreeCAD Path operations for CAM functionality.

This module provides low-level operations for creating and managing
FreeCAD Path objects and operations.
"""

from typing import Dict, Any, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    pass

# Configure logging
logger = logging.getLogger(__name__)


def _ensure_freecad_available():
    """Ensure FreeCAD is available and import required modules."""
    try:
        import FreeCAD
        import Path
        import PathScripts

        return FreeCAD, Path, PathScripts
    except ImportError as e:
        logger.error(f"FreeCAD not available: {e}")
        raise ImportError("FreeCAD is required for this adapter") from e


def create_path_job(name: str, base_objects: list[Any] = None) -> Any:
    """Create a new FreeCAD Path Job."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        # Get active document or create new one
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument("CAM_Job")

        # Create Path Job
        job = doc.addObject("Path::FeaturePython", name)

        # Initialize job with PathScripts
        from PathScripts import PathJob

        PathJob.ObjectJob(job)

        # Set base objects if provided
        if base_objects:
            job.Base = base_objects

        # Set default properties
        job.PostProcessor = "grbl"
        job.PostProcessorArgs = ""
        job.PostProcessorOutputFile = ""

        doc.recompute()
        logger.info(f"Created Path Job: {name}")

        return job

    except Exception as e:
        logger.error(f"Failed to create Path Job {name}: {e}")
        raise


def create_profile_operation(
    job: Any, name: str, base_geometry: Any, tool_controller: Any, **kwargs
) -> Any:
    """Create a Profile operation in FreeCAD Path."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create Profile operation
        profile_op = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathProfile

        PathProfile.ObjectProfile(profile_op)

        # Set basic properties
        profile_op.Base = [(base_geometry, [])]
        profile_op.ToolController = tool_controller

        # Set operation parameters from kwargs
        if "side" in kwargs:
            profile_op.Side = kwargs["side"]  # 'Outside', 'Inside', 'On'
        if "direction" in kwargs:
            profile_op.Direction = kwargs["direction"]  # 'CW', 'CCW'
        if "offset_extra" in kwargs:
            profile_op.OffsetExtra = kwargs["offset_extra"]
        if "start_depth" in kwargs:
            profile_op.StartDepth = kwargs["start_depth"]
        if "final_depth" in kwargs:
            profile_op.FinalDepth = kwargs["final_depth"]
        if "step_down" in kwargs:
            profile_op.StepDown = kwargs["step_down"]

        # Add to job
        job.Operations = job.Operations + [profile_op]

        doc.recompute()
        logger.info(f"Created Profile operation: {name}")

        return profile_op

    except Exception as e:
        logger.error(f"Failed to create Profile operation {name}: {e}")
        raise


def create_pocket_operation(
    job: Any, name: str, base_geometry: Any, tool_controller: Any, **kwargs
) -> Any:
    """Create a Pocket operation in FreeCAD Path."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create Pocket operation
        pocket_op = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathPocket

        PathPocket.ObjectPocket(pocket_op)

        # Set basic properties
        pocket_op.Base = [(base_geometry, [])]
        pocket_op.ToolController = tool_controller

        # Set operation parameters
        if "cut_mode" in kwargs:
            pocket_op.CutMode = kwargs["cut_mode"]  # 'Climb', 'Conventional'
        if "pattern" in kwargs:
            pocket_op.Pattern = kwargs["pattern"]  # 'ZigZag', 'Offset', 'Spiral'
        if "step_over" in kwargs:
            pocket_op.StepOver = kwargs["step_over"]
        if "start_depth" in kwargs:
            pocket_op.StartDepth = kwargs["start_depth"]
        if "final_depth" in kwargs:
            pocket_op.FinalDepth = kwargs["final_depth"]
        if "step_down" in kwargs:
            pocket_op.StepDown = kwargs["step_down"]

        # Add to job
        job.Operations = job.Operations + [pocket_op]

        doc.recompute()
        logger.info(f"Created Pocket operation: {name}")

        return pocket_op

    except Exception as e:
        logger.error(f"Failed to create Pocket operation {name}: {e}")
        raise


def create_drilling_operation(
    job: Any, name: str, drill_points: list[tuple], tool_controller: Any, **kwargs
) -> Any:
    """Create a Drilling operation in FreeCAD Path."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create Drilling operation
        drill_op = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathDrilling

        PathDrilling.ObjectDrilling(drill_op)

        # Create drill points as FreeCAD objects
        drill_objects = []
        for i, (x, y, z) in enumerate(drill_points):
            point = doc.addObject("Part::Vertex", f"DrillPoint_{i}")
            point.X = x
            point.Y = y
            point.Z = z
            drill_objects.append(point)

        # Set basic properties
        drill_op.Base = [(obj, []) for obj in drill_objects]
        drill_op.ToolController = tool_controller

        # Set drilling parameters
        if "peck_depth" in kwargs:
            drill_op.PeckDepth = kwargs["peck_depth"]
        if "peck_enabled" in kwargs:
            drill_op.PeckEnabled = kwargs["peck_enabled"]
        if "dwell_enabled" in kwargs:
            drill_op.DwellEnabled = kwargs["dwell_enabled"]
        if "dwell_time" in kwargs:
            drill_op.DwellTime = kwargs["dwell_time"]
        if "retract_height" in kwargs:
            drill_op.RetractHeight = kwargs["retract_height"]

        # Add to job
        job.Operations = job.Operations + [drill_op]

        doc.recompute()
        logger.info(f"Created Drilling operation: {name}")

        return drill_op

    except Exception as e:
        logger.error(f"Failed to create Drilling operation {name}: {e}")
        raise


def create_adaptive_operation(
    job: Any, name: str, base_geometry: Any, tool_controller: Any, **kwargs
) -> Any:
    """Create an Adaptive operation in FreeCAD Path."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create Adaptive operation
        adaptive_op = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathAdaptive

        PathAdaptive.ObjectAdaptive(adaptive_op)

        # Set basic properties
        adaptive_op.Base = [(base_geometry, [])]
        adaptive_op.ToolController = tool_controller

        # Set adaptive parameters
        if "step_over" in kwargs:
            adaptive_op.StepOver = kwargs["step_over"]
        if "lift_distance" in kwargs:
            adaptive_op.LiftDistance = kwargs["lift_distance"]
        if "keep_tool_down_ratio" in kwargs:
            adaptive_op.KeepToolDownRatio = kwargs["keep_tool_down_ratio"]
        if "stock_to_leave" in kwargs:
            adaptive_op.StockToLeave = kwargs["stock_to_leave"]

        # Add to job
        job.Operations = job.Operations + [adaptive_op]

        doc.recompute()
        logger.info(f"Created Adaptive operation: {name}")

        return adaptive_op

    except Exception as e:
        logger.error(f"Failed to create Adaptive operation {name}: {e}")
        raise


def create_surface_operation(
    job: Any, name: str, base_geometry: Any, tool_controller: Any, **kwargs
) -> Any:
    """Create a 3D Surface operation in FreeCAD Path."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create Surface operation
        surface_op = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathSurface

        PathSurface.ObjectSurface(surface_op)

        # Set basic properties
        surface_op.Base = [(base_geometry, [])]
        surface_op.ToolController = tool_controller

        # Set surface parameters
        if "algorithm" in kwargs:
            surface_op.Algorithm = kwargs[
                "algorithm"
            ]  # 'OCL Dropcutter', 'OCL Waterline'
        if "cut_pattern" in kwargs:
            surface_op.CutPattern = kwargs[
                "cut_pattern"
            ]  # 'Line', 'ZigZag', 'Circular'
        if "step_over" in kwargs:
            surface_op.StepOver = kwargs["step_over"]
        if "sample_interval" in kwargs:
            surface_op.SampleInterval = kwargs["sample_interval"]

        # Add to job
        job.Operations = job.Operations + [surface_op]

        doc.recompute()
        logger.info(f"Created Surface operation: {name}")

        return surface_op

    except Exception as e:
        logger.error(f"Failed to create Surface operation {name}: {e}")
        raise


def calculate_toolpath(operation: Any) -> bool:
    """Calculate/regenerate toolpath for an operation."""
    try:
        operation.Proxy.execute(operation)
        operation.Document.recompute()
        logger.info(f"Calculated toolpath for operation: {operation.Label}")
        return True
    except Exception as e:
        logger.error(f"Failed to calculate toolpath for {operation.Label}: {e}")
        return False


def get_toolpath_points(operation: Any) -> list[tuple]:
    """Extract toolpath points from a FreeCAD Path operation."""
    try:
        if not hasattr(operation, "Path"):
            return []

        path = operation.Path
        points = []

        # Parse Path commands to extract coordinates
        for command in path.Commands:
            if hasattr(command, "Parameters"):
                params = command.Parameters
                x = params.get("X", 0.0)
                y = params.get("Y", 0.0)
                z = params.get("Z", 0.0)
                points.append((x, y, z))

        logger.info(f"Extracted {len(points)} points from {operation.Label}")
        return points

    except Exception as e:
        logger.error(f"Failed to extract toolpath points from {operation.Label}: {e}")
        return []
