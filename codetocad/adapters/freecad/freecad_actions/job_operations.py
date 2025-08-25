"""
FreeCAD job operations for CAM functionality.

This module provides low-level operations for setting up and managing
FreeCAD Path jobs including geometry, stock, and fixtures.
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
        import Part

        return FreeCAD, Path, PathScripts, Part
    except ImportError as e:
        logger.error(f"FreeCAD not available: {e}")
        raise ImportError("FreeCAD is required for this adapter") from e


def setup_job_geometry(job: Any, base_objects: list[Any]) -> bool:
    """Setup the base geometry for a Path job."""
    try:
        job.Base = base_objects
        job.Document.recompute()

        logger.info(f"Setup job geometry with {len(base_objects)} objects")
        return True

    except Exception as e:
        logger.error(f"Failed to setup job geometry: {e}")
        return False


def setup_job_stock(job: Any, stock_type: str = "CreateBox", **kwargs) -> Any:
    """Setup stock material for a Path job."""
    FreeCAD, Path, PathScripts, Part = _ensure_freecad_available()

    try:
        doc = job.Document

        if stock_type == "CreateBox":
            # Create box stock
            length = kwargs.get("length", 100.0)
            width = kwargs.get("width", 100.0)
            height = kwargs.get("height", 20.0)

            stock = doc.addObject("Part::Box", "Stock")
            stock.Length = length
            stock.Width = width
            stock.Height = height

            # Position stock
            if "placement" in kwargs:
                stock.Placement = kwargs["placement"]

        elif stock_type == "CreateCylinder":
            # Create cylindrical stock
            radius = kwargs.get("radius", 50.0)
            height = kwargs.get("height", 20.0)

            stock = doc.addObject("Part::Cylinder", "Stock")
            stock.Radius = radius
            stock.Height = height

        elif stock_type == "FromBase":
            # Create stock from base geometry with offset
            if not job.Base:
                raise ValueError("No base geometry defined for job")

            # Get bounding box of base objects
            bbox = None
            for obj in job.Base:
                if bbox is None:
                    bbox = obj.Shape.BoundBox
                else:
                    bbox.add(obj.Shape.BoundBox)

            if bbox:
                # Add stock allowance
                stock_allowance = kwargs.get("stock_allowance", 5.0)

                stock = doc.addObject("Part::Box", "Stock")
                stock.Length = bbox.XLength + 2 * stock_allowance
                stock.Width = bbox.YLength + 2 * stock_allowance
                stock.Height = bbox.ZLength + stock_allowance

                # Position stock to encompass base geometry
                import FreeCAD

                placement = FreeCAD.Placement()
                placement.Base = FreeCAD.Vector(
                    bbox.XMin - stock_allowance, bbox.YMin - stock_allowance, bbox.ZMin
                )
                stock.Placement = placement

        else:
            raise ValueError(f"Unknown stock type: {stock_type}")

        # Assign stock to job
        job.Stock = stock
        doc.recompute()

        logger.info(f"Setup job stock: {stock_type}")
        return stock

    except Exception as e:
        logger.error(f"Failed to setup job stock: {e}")
        raise


def setup_job_fixtures(job: Any, fixtures: list[Any]) -> bool:
    """Setup fixtures/clamps for a Path job."""
    try:
        # Add fixtures to job
        if hasattr(job, "Fixtures"):
            job.Fixtures = fixtures
        else:
            # Store fixtures in custom property
            job.addProperty(
                "App::PropertyLinkList", "Fixtures", "Job", "Fixture objects"
            )
            job.Fixtures = fixtures

        job.Document.recompute()

        logger.info(f"Setup job fixtures: {len(fixtures)} objects")
        return True

    except Exception as e:
        logger.error(f"Failed to setup job fixtures: {e}")
        return False


def setup_job_coordinate_system(
    job: Any, origin: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0)
) -> bool:
    """Setup work coordinate system for a Path job."""
    FreeCAD, Path, PathScripts, Part = _ensure_freecad_available()

    try:
        import FreeCAD

        # Create placement for coordinate system
        placement = FreeCAD.Placement()
        placement.Base = FreeCAD.Vector(*origin)

        # Apply rotation if specified
        if any(angle != 0 for angle in rotation):
            import math

            rx, ry, rz = [math.radians(angle) for angle in rotation]
            placement.Rotation = FreeCAD.Rotation(rx, ry, rz)

        # Set job placement
        job.Placement = placement
        job.Document.recompute()

        logger.info(
            f"Setup job coordinate system: origin={origin}, rotation={rotation}"
        )
        return True

    except Exception as e:
        logger.error(f"Failed to setup job coordinate system: {e}")
        return False


def calculate_toolpaths(job: Any, operations: list[Any] = None) -> bool:
    """Calculate toolpaths for job operations."""
    try:
        # Get operations to calculate
        if operations is None:
            operations = job.Operations

        success_count = 0
        for operation in operations:
            try:
                # Execute operation to generate toolpath
                operation.Proxy.execute(operation)
                success_count += 1
                logger.info(f"Calculated toolpath for: {operation.Label}")
            except Exception as e:
                logger.error(f"Failed to calculate toolpath for {operation.Label}: {e}")

        job.Document.recompute()

        logger.info(
            f"Calculated toolpaths: {success_count}/{len(operations)} successful"
        )
        return success_count == len(operations)

    except Exception as e:
        logger.error(f"Failed to calculate toolpaths: {e}")
        return False


def post_process_job(
    job: Any, output_file: str = None, post_processor: str = None
) -> str:
    """Post-process a Path job to generate G-code."""
    FreeCAD, Path, PathScripts, Part = _ensure_freecad_available()

    try:
        # Set post processor if specified
        if post_processor:
            job.PostProcessor = post_processor

        # Set output file if specified
        if output_file:
            job.PostProcessorOutputFile = output_file

        # Import post processing functionality
        from PathScripts import PathPost

        # Generate G-code
        gcode = PathPost.export(job, output_file or "")

        logger.info(f"Post-processed job to G-code: {len(gcode.split())} lines")
        return gcode

    except Exception as e:
        logger.error(f"Failed to post-process job: {e}")
        raise


def validate_job_setup(job: Any) -> dict[str, Any]:
    """Validate a Path job setup and return validation results."""
    try:
        validation = {"valid": True, "warnings": [], "errors": [], "info": {}}

        # Check base geometry
        if not job.Base:
            validation["errors"].append("No base geometry defined")
            validation["valid"] = False
        else:
            validation["info"]["base_objects"] = len(job.Base)

        # Check stock
        if not hasattr(job, "Stock") or not job.Stock:
            validation["warnings"].append("No stock defined")
        else:
            validation["info"]["stock_type"] = job.Stock.TypeId

        # Check tool controllers
        if not hasattr(job, "ToolController") or not job.ToolController:
            validation["errors"].append("No tool controllers defined")
            validation["valid"] = False
        else:
            validation["info"]["tool_controllers"] = len(job.ToolController)

        # Check operations
        if not hasattr(job, "Operations") or not job.Operations:
            validation["warnings"].append("No operations defined")
        else:
            validation["info"]["operations"] = len(job.Operations)

            # Check if operations have toolpaths
            operations_with_paths = 0
            for op in job.Operations:
                if hasattr(op, "Path") and op.Path:
                    operations_with_paths += 1

            validation["info"]["operations_with_toolpaths"] = operations_with_paths

            if operations_with_paths == 0:
                validation["warnings"].append("No operations have calculated toolpaths")

        # Check post processor
        if not job.PostProcessor:
            validation["warnings"].append("No post processor specified")

        logger.info(f"Job validation: {'VALID' if validation['valid'] else 'INVALID'}")
        return validation

    except Exception as e:
        logger.error(f"Failed to validate job setup: {e}")
        return {
            "valid": False,
            "warnings": [],
            "errors": [f"Validation failed: {e}"],
            "info": {},
        }


def get_job_statistics(job: Any) -> dict[str, Any]:
    """Get comprehensive statistics about a Path job."""
    try:
        stats = {
            "job_name": job.Label,
            "base_objects": len(job.Base) if job.Base else 0,
            "operations": len(job.Operations) if hasattr(job, "Operations") else 0,
            "tool_controllers": (
                len(job.ToolController) if hasattr(job, "ToolController") else 0
            ),
            "total_toolpath_length": 0.0,
            "estimated_machining_time": 0.0,
            "bounding_box": None,
        }

        # Calculate toolpath statistics
        if hasattr(job, "Operations"):
            for operation in job.Operations:
                if hasattr(operation, "Path") and operation.Path:
                    # Calculate path length (simplified)
                    path_length = 0.0
                    prev_point = None

                    for command in operation.Path.Commands:
                        if hasattr(command, "Parameters"):
                            params = command.Parameters
                            current_point = (
                                params.get("X", 0.0),
                                params.get("Y", 0.0),
                                params.get("Z", 0.0),
                            )

                            if prev_point:
                                # Calculate distance
                                dx = current_point[0] - prev_point[0]
                                dy = current_point[1] - prev_point[1]
                                dz = current_point[2] - prev_point[2]
                                distance = (dx * dx + dy * dy + dz * dz) ** 0.5
                                path_length += distance

                            prev_point = current_point

                    stats["total_toolpath_length"] += path_length

        # Get bounding box from stock or base geometry
        if hasattr(job, "Stock") and job.Stock:
            bbox = job.Stock.Shape.BoundBox
            stats["bounding_box"] = {
                "x_min": bbox.XMin,
                "x_max": bbox.XMax,
                "y_min": bbox.YMin,
                "y_max": bbox.YMax,
                "z_min": bbox.ZMin,
                "z_max": bbox.ZMax,
                "length": bbox.XLength,
                "width": bbox.YLength,
                "height": bbox.ZLength,
            }

        logger.info(f"Generated job statistics for: {stats['job_name']}")
        return stats

    except Exception as e:
        logger.error(f"Failed to get job statistics: {e}")
        return {"error": str(e)}
