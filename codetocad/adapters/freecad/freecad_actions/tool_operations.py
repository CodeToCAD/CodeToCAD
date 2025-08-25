"""
FreeCAD tool operations for CAM functionality.

This module provides low-level operations for creating and managing
FreeCAD Path tools and tool controllers.
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


def create_tool(name: str, tool_type: str, diameter: float, **kwargs) -> Any:
    """Create a FreeCAD Path Tool."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        # Create tool using Path.Tool
        tool = Path.Tool()

        # Set basic properties
        tool.Name = name
        tool.ToolType = tool_type
        tool.Diameter = diameter

        # Set optional properties from kwargs
        if "length" in kwargs:
            tool.Length = kwargs["length"]
        if "cutting_edge_height" in kwargs:
            tool.CuttingEdgeHeight = kwargs["cutting_edge_height"]
        if "material" in kwargs:
            tool.Material = kwargs["material"]
        if "flute_count" in kwargs:
            tool.FluteCount = kwargs["flute_count"]
        if "tip_angle" in kwargs:
            tool.TipAngle = kwargs["tip_angle"]
        if "helix_angle" in kwargs:
            tool.HelixAngle = kwargs["helix_angle"]

        logger.info(f"Created tool: {name} ({tool_type}, ⌀{diameter}mm)")
        return tool

    except Exception as e:
        logger.error(f"Failed to create tool {name}: {e}")
        raise


def create_tool_controller(job: Any, tool: Any, name: str, **kwargs) -> Any:
    """Create a FreeCAD Path Tool Controller."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        doc = job.Document

        # Create tool controller
        tc = doc.addObject("Path::FeaturePython", name)

        # Initialize with PathScripts
        from PathScripts import PathToolController

        PathToolController.ObjectToolController(tc)

        # Set tool
        tc.Tool = tool

        # Set cutting parameters from kwargs
        if "horizontal_feed" in kwargs:
            tc.HorizFeed = kwargs["horizontal_feed"]
        if "vertical_feed" in kwargs:
            tc.VertFeed = kwargs["vertical_feed"]
        if "horizontal_rapid" in kwargs:
            tc.HorizRapid = kwargs["horizontal_rapid"]
        if "vertical_rapid" in kwargs:
            tc.VertRapid = kwargs["vertical_rapid"]
        if "spindle_speed" in kwargs:
            tc.SpindleSpeed = kwargs["spindle_speed"]
        if "spindle_direction" in kwargs:
            tc.SpindleDir = kwargs["spindle_direction"]

        # Add to job's tool controllers
        if hasattr(job, "ToolController"):
            job.ToolController = job.ToolController + [tc]
        else:
            job.ToolController = [tc]

        doc.recompute()
        logger.info(f"Created tool controller: {name}")

        return tc

    except Exception as e:
        logger.error(f"Failed to create tool controller {name}: {e}")
        raise


def import_tool_library(file_path: str) -> dict[str, Any]:
    """Import tools from a FreeCAD tool library file."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        # Use FreeCAD's tool library functionality
        from PathScripts import PathToolLibraryManager

        library_manager = PathToolLibraryManager.ToolLibraryManager()
        tools = library_manager.getTools(file_path)

        logger.info(f"Imported {len(tools)} tools from {file_path}")
        return tools

    except Exception as e:
        logger.error(f"Failed to import tool library from {file_path}: {e}")
        raise


def export_tool_library(tools: dict[str, Any], file_path: str) -> bool:
    """Export tools to a FreeCAD tool library file."""
    FreeCAD, Path, PathScripts = _ensure_freecad_available()

    try:
        # Use FreeCAD's tool library functionality
        from PathScripts import PathToolLibraryManager

        library_manager = PathToolLibraryManager.ToolLibraryManager()
        library_manager.setTools(tools, file_path)

        logger.info(f"Exported {len(tools)} tools to {file_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to export tool library to {file_path}: {e}")
        return False


def get_tool_shape_file(tool_type: str) -> str | None:
    """Get the tool shape file path for a given tool type."""
    try:
        # Map tool types to FreeCAD tool shape files
        shape_map = {
            "flat_end_mill": "endmill.fcstd",
            "ball_end_mill": "ballend.fcstd",
            "drill": "drill.fcstd",
            "v_bit": "v-bit.fcstd",
            "chamfer_mill": "chamfer.fcstd",
        }

        return shape_map.get(tool_type)

    except Exception as e:
        logger.error(f"Failed to get tool shape file for {tool_type}: {e}")
        return None


def calculate_feeds_speeds(tool: Any, material: str = "aluminum") -> dict[str, float]:
    """Calculate recommended feeds and speeds for a tool and material."""
    try:
        # Basic calculation based on tool diameter and material
        diameter = tool.Diameter

        # Material-specific parameters
        material_params = {
            "aluminum": {"surface_speed": 200, "chip_load": 0.1},
            "steel": {"surface_speed": 100, "chip_load": 0.08},
            "plastic": {"surface_speed": 300, "chip_load": 0.15},
            "wood": {"surface_speed": 400, "chip_load": 0.2},
        }

        params = material_params.get(material.lower(), material_params["aluminum"])

        # Calculate spindle speed: RPM = (Surface Speed * 1000) / (π * Diameter)
        import math

        spindle_speed = (params["surface_speed"] * 1000) / (math.pi * diameter)

        # Calculate feed rate: Feed = RPM * Flutes * Chip Load
        flute_count = getattr(tool, "FluteCount", 2)
        feed_rate = spindle_speed * flute_count * params["chip_load"]

        # Plunge rate is typically 25% of feed rate
        plunge_rate = feed_rate * 0.25

        result = {
            "spindle_speed": round(spindle_speed),
            "feed_rate": round(feed_rate),
            "plunge_rate": round(plunge_rate),
        }

        logger.info(f"Calculated feeds/speeds for {tool.Name}: {result}")
        return result

    except Exception as e:
        logger.error(f"Failed to calculate feeds/speeds for tool: {e}")
        return {"spindle_speed": 12000, "feed_rate": 1000, "plunge_rate": 250}


def validate_tool_for_operation(tool: Any, operation_type: str) -> bool:
    """Validate if a tool is suitable for a specific operation type."""
    try:
        tool_type = tool.ToolType.lower()
        operation_type = operation_type.lower()

        # Define valid tool-operation combinations
        valid_combinations = {
            "profile": ["flat_end_mill", "ball_end_mill", "bull_nose_mill"],
            "pocket": ["flat_end_mill", "roughing_mill"],
            "drilling": ["drill", "center_drill"],
            "adaptive": ["flat_end_mill", "roughing_mill"],
            "surface": ["ball_end_mill", "bull_nose_mill"],
            "engraving": ["v_bit", "ball_end_mill"],
        }

        valid_tools = valid_combinations.get(operation_type, [])
        is_valid = tool_type in valid_tools

        if not is_valid:
            logger.warning(
                f"Tool {tool.Name} ({tool_type}) may not be suitable for {operation_type}"
            )

        return is_valid

    except Exception as e:
        logger.error(f"Failed to validate tool for operation: {e}")
        return True  # Default to valid if validation fails


def get_tool_reach(tool: Any) -> float:
    """Calculate the effective reach of a tool."""
    try:
        # Effective reach is the cutting edge height
        if hasattr(tool, "CuttingEdgeHeight"):
            return tool.CuttingEdgeHeight
        elif hasattr(tool, "Length"):
            # Estimate cutting edge height as 80% of total length
            return tool.Length * 0.8
        else:
            # Default estimate based on diameter
            return tool.Diameter * 3

    except Exception as e:
        logger.error(f"Failed to calculate tool reach: {e}")
        return 10.0  # Default 10mm reach


def optimize_tool_selection(operations: list, available_tools: list) -> dict[str, Any]:
    """Optimize tool selection for a list of operations."""
    try:
        tool_assignments = {}
        tool_changes = 0

        for operation in operations:
            operation_type = operation.get("type", "profile")
            required_diameter = operation.get("min_diameter", 3.0)
            max_diameter = operation.get("max_diameter", 20.0)

            # Find suitable tools
            suitable_tools = []
            for tool in available_tools:
                if (
                    validate_tool_for_operation(tool, operation_type)
                    and required_diameter <= tool.Diameter <= max_diameter
                ):
                    suitable_tools.append(tool)

            if suitable_tools:
                # Select the most appropriate tool (e.g., smallest suitable diameter)
                selected_tool = min(suitable_tools, key=lambda t: t.Diameter)
                tool_assignments[operation["name"]] = selected_tool

                # Count tool changes
                if len(tool_assignments) > 1:
                    previous_tools = list(tool_assignments.values())[:-1]
                    if selected_tool not in previous_tools:
                        tool_changes += 1

        result = {
            "assignments": tool_assignments,
            "tool_changes": tool_changes,
            "unique_tools": len(set(tool_assignments.values())),
        }

        logger.info(
            f"Optimized tool selection: {result['unique_tools']} tools, {tool_changes} changes"
        )
        return result

    except Exception as e:
        logger.error(f"Failed to optimize tool selection: {e}")
        return {"assignments": {}, "tool_changes": 0, "unique_tools": 0}
